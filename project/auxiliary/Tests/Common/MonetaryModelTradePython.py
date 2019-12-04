from ContractAddressLocator import ContractAddressLocator
from ModelDataSource             import ModelDataSource
from MintingPointTimersManager            import MintingPointTimersManager
from MintManager            import MintManager           
from IntervalIterator       import IntervalIterator      
from MonetaryModelState         import MonetaryModelState
from MonetaryModel              import MonetaryModel


from Common.ModelDataSource import initialize
from Common.Utils.CommandReader import load
from Common.Utils.UnitConverter import dec2wei
from Common.Utils.UnitConverter import wei2dec


def run(fileName,logger,modelCalculator,priceBandCalculator):
    logger.info('Executing sequence...')
    for command in load(fileName):
        if command['operation'] == 'init':
            mintingPointTimersManager,monetaryModelState,monetaryModel = init(logger,modelCalculator,priceBandCalculator,command['timeout'])
        elif command['operation'] == 'buy':
            mintingPointTimersManager.now += command['elapsed']
            sdrAmount = dec2wei(command['amount'])
            sgaAmount = monetaryModel.buy(sdrAmount)
            logger.debug('buy: {:.2f} SDR ==> {:.2f} SGA'.format(wei2dec(sdrAmount),wei2dec(sgaAmount)))
        elif command['operation'] == 'sell':
            mintingPointTimersManager.now += command['elapsed']
            sgaAmount = dec2wei(command['amount'])
            sdrAmount = monetaryModel.sell(sgaAmount)
            logger.debug('sell: {:.2f} SGA ==> {:.2f} SDR'.format(wei2dec(sgaAmount),wei2dec(sdrAmount)))
        elif command['operation'] == 'info':
            logger.debug('SDR = {:.2f}'.format(wei2dec(monetaryModelState.getSdrTotal())))
            logger.debug('SGA = {:.2f}'.format(wei2dec(monetaryModelState.getSgaTotal())))
        else:
            logger.debug('Undefined operation')
    logger.info('Done')


def init(logger,modelCalculator,priceBandCalculator,timeout):
    contractAddressLocator = ContractAddressLocator()
    modelDataSource             = ModelDataSource            ()
    mintingPointTimersManager            = MintingPointTimersManager           (contractAddressLocator,timeout)
    mintManager            = MintManager           (contractAddressLocator)
    intervalIterator       = IntervalIterator      (contractAddressLocator)
    monetaryModelState         = MonetaryModelState        (contractAddressLocator)
    monetaryModel              = MonetaryModel             (contractAddressLocator)

    contractAddressLocator.set('ModelCalculator' ,modelCalculator )
    contractAddressLocator.set('PriceBandCalculator',priceBandCalculator)
    contractAddressLocator.set('ModelDataSource'      ,modelDataSource      )
    contractAddressLocator.set('MintingPointTimersManager'     ,mintingPointTimersManager     )
    contractAddressLocator.set('MintManager'     ,mintManager     )
    contractAddressLocator.set('IntervalIterator',intervalIterator)
    contractAddressLocator.set('MonetaryModelState'  ,monetaryModelState  )
    contractAddressLocator.set('MonetaryModel'       ,monetaryModel       )

    initialize(modelDataSource,logger)

    return mintingPointTimersManager,monetaryModelState,monetaryModel