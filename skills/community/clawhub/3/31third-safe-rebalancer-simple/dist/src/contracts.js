import ExecutorModuleArtifact from '../abi/ExecutorModule.json' with { type: 'json' };
import AssetUniversePolicyArtifact from '../abi/AssetUniversePolicy.json' with { type: 'json' };
import StaticAllocationPolicyArtifact from '../abi/StaticAllocationPolicy.json' with { type: 'json' };
import SlippagePolicyArtifact from '../abi/SlippagePolicy.json' with { type: 'json' };
import PriceOracleArtifact from '../abi/PriceOracle.json' with { type: 'json' };
export const executorModuleAbi = ExecutorModuleArtifact.abi;
export const assetUniversePolicyAbi = AssetUniversePolicyArtifact.abi;
export const staticAllocationPolicyAbi = StaticAllocationPolicyArtifact.abi;
export const slippagePolicyAbi = SlippagePolicyArtifact.abi;
export const priceOracleAbi = PriceOracleArtifact.abi;
export const erc20Abi = [
    {
        type: 'function',
        name: 'balanceOf',
        stateMutability: 'view',
        inputs: [{ name: 'account', type: 'address' }],
        outputs: [{ name: '', type: 'uint256' }]
    },
    {
        type: 'function',
        name: 'decimals',
        stateMutability: 'view',
        inputs: [],
        outputs: [{ name: '', type: 'uint8' }]
    }
];
