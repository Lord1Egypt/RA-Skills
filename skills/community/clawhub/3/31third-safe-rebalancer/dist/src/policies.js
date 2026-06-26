import { HARDCODED_TOKEN_FEED_REGISTRY_ADDRESS } from './contracts.js';
import { assetUniversePolicyAbi, executorModuleAbi, priceOracleAbi, slippagePolicyAbi, staticAllocationPolicyAbi } from './contracts.js';
export async function getExecutorPolicies(publicClient, executorModule) {
    const withTypes = (await publicClient.readContract({
        address: executorModule,
        abi: executorModuleAbi,
        functionName: 'getPoliciesWithTypes'
    }));
    if (withTypes.length > 0) {
        return withTypes;
    }
    const policies = (await publicClient.readContract({
        address: executorModule,
        abi: executorModuleAbi,
        functionName: 'getPolicies'
    }));
    const resolved = await Promise.all(policies.map(async (policy) => {
        const policyType = (await publicClient.readContract({
            address: policy,
            abi: assetUniversePolicyAbi,
            functionName: 'policyType'
        }));
        return { policy, policyType };
    }));
    return resolved;
}
export async function readPolicySnapshot(publicClient, executorModule) {
    const policyStates = await getExecutorPolicies(publicClient, executorModule);
    const snapshot = {
        assetUniverseTokens: [],
        targetAllocations: []
    };
    for (const policyState of policyStates) {
        const kind = policyState.policyType.toLowerCase();
        if (kind === 'assetuniverse') {
            snapshot.assetUniverseTokens = (await publicClient.readContract({
                address: policyState.policy,
                abi: assetUniversePolicyAbi,
                functionName: 'getTokens'
            }));
            continue;
        }
        if (kind === 'staticallocation') {
            const priceOracle = (await publicClient.readContract({
                address: policyState.policy,
                abi: staticAllocationPolicyAbi,
                functionName: 'priceOracle'
            }));
            const driftThresholdBps = (await publicClient.readContract({
                address: policyState.policy,
                abi: staticAllocationPolicyAbi,
                functionName: 'driftThresholdBps'
            }));
            const toleranceThresholdBps = (await publicClient.readContract({
                address: policyState.policy,
                abi: staticAllocationPolicyAbi,
                functionName: 'toleranceThresholdBps'
            }));
            const targets = (await publicClient.readContract({
                address: policyState.policy,
                abi: staticAllocationPolicyAbi,
                functionName: 'getAllTargets'
            }));
            snapshot.driftThresholdBps = Number(driftThresholdBps);
            snapshot.toleranceThresholdBps = Number(toleranceThresholdBps);
            snapshot.priceOracle = priceOracle;
            snapshot.tokenFeedRegistry = (await publicClient.readContract({
                address: priceOracle,
                abi: priceOracleAbi,
                functionName: 'feedRegistry'
            }));
            snapshot.targetAllocations = targets.map((item) => ({
                token: item.token,
                bps: Number(item.bps)
            }));
            continue;
        }
        if (kind === 'slippage') {
            const priceOracle = (await publicClient.readContract({
                address: policyState.policy,
                abi: slippagePolicyAbi,
                functionName: 'priceOracle'
            }));
            const maxSlippageBps = (await publicClient.readContract({
                address: policyState.policy,
                abi: slippagePolicyAbi,
                functionName: 'maxSlippageBps'
            }));
            snapshot.priceOracle = snapshot.priceOracle ?? priceOracle;
            snapshot.tokenFeedRegistry = snapshot.tokenFeedRegistry ?? (await publicClient.readContract({
                address: priceOracle,
                abi: priceOracleAbi,
                functionName: 'feedRegistry'
            }));
            snapshot.maxSlippageBps = Number(maxSlippageBps);
        }
    }
    snapshot.tokenFeedRegistry = snapshot.tokenFeedRegistry ?? HARDCODED_TOKEN_FEED_REGISTRY_ADDRESS;
    return snapshot;
}
