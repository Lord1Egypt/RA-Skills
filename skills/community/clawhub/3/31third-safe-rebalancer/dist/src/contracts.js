import executorArtifact from '../abi/ExecutorModule.json' with { type: 'json' };
import assetUniverseArtifact from '../abi/AssetUniversePolicy.json' with { type: 'json' };
import staticAllocationArtifact from '../abi/StaticAllocationPolicy.json' with { type: 'json' };
import slippageArtifact from '../abi/SlippagePolicy.json' with { type: 'json' };
import priceOracleArtifact from '../abi/PriceOracle.json' with { type: 'json' };
import tokenFeedRegistryArtifact from '../abi/TokenFeedRegistry.json' with { type: 'json' };
import batchTradeArtifact from '../abi/IBatchTrade.json' with { type: 'json' };
export const executorModuleAbi = executorArtifact.abi;
export const assetUniversePolicyAbi = assetUniverseArtifact.abi;
export const staticAllocationPolicyAbi = staticAllocationArtifact.abi;
export const slippagePolicyAbi = slippageArtifact.abi;
export const priceOracleAbi = priceOracleArtifact.abi;
export const tokenFeedRegistryAbi = tokenFeedRegistryArtifact.abi;
export const batchTradeAbi = batchTradeArtifact.abi;
export const HARDCODED_BATCH_TRADE_ADDRESS = '0xD20c024560ccA40288C05BAB650ac087ae9b0f6e';
export const HARDCODED_TOKEN_FEED_REGISTRY_ADDRESS = '0x1d4999242A24C8588c4f5dB7dFF1D74Df6bC746A';
export function createContractRefs(addresses) {
    return {
        executorModule: {
            address: addresses.executorModule,
            abi: executorModuleAbi
        },
        batchTrade: {
            address: HARDCODED_BATCH_TRADE_ADDRESS,
            abi: batchTradeAbi
        },
        tokenFeedRegistry: {
            address: HARDCODED_TOKEN_FEED_REGISTRY_ADDRESS,
            abi: tokenFeedRegistryAbi
        }
    };
}
