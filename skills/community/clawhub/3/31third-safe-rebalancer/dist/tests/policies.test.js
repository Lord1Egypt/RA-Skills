import { describe, expect, it } from 'vitest';
import { HARDCODED_TOKEN_FEED_REGISTRY_ADDRESS } from '../src/contracts.js';
import { getExecutorPolicies, readPolicySnapshot } from '../src/policies.js';
const EXECUTOR = '0x1000000000000000000000000000000000000001';
const POLICY_A = '0x2000000000000000000000000000000000000002';
const POLICY_B = '0x3000000000000000000000000000000000000003';
const POLICY_C = '0x4000000000000000000000000000000000000004';
const TOKEN_A = '0x5000000000000000000000000000000000000005';
const TOKEN_B = '0x6000000000000000000000000000000000000006';
const PRICE_ORACLE = '0x7000000000000000000000000000000000000007';
const FEED_REGISTRY = '0x8000000000000000000000000000000000000008';
function mockPublicClient(readContractImpl) {
    return {
        readContract: async (args) => readContractImpl(args)
    };
}
describe('policies', () => {
    it('getExecutorPolicies uses getPoliciesWithTypes when available', async () => {
        const publicClient = mockPublicClient(({ address, functionName }) => {
            if (address === EXECUTOR && functionName === 'getPoliciesWithTypes') {
                return [{ policy: POLICY_A, policyType: 'assetuniverse' }];
            }
            throw new Error(`Unexpected call: ${address}:${functionName}`);
        });
        const result = await getExecutorPolicies(publicClient, EXECUTOR);
        expect(result).toEqual([{ policy: POLICY_A, policyType: 'assetuniverse' }]);
    });
    it('getExecutorPolicies falls back to getPolicies and resolves policyType', async () => {
        const publicClient = mockPublicClient(({ address, functionName }) => {
            if (address === EXECUTOR && functionName === 'getPoliciesWithTypes')
                return [];
            if (address === EXECUTOR && functionName === 'getPolicies')
                return [POLICY_A, POLICY_B];
            if (address === POLICY_A && functionName === 'policyType')
                return 'assetuniverse';
            if (address === POLICY_B && functionName === 'policyType')
                return 'slippage';
            throw new Error(`Unexpected call: ${address}:${functionName}`);
        });
        const result = await getExecutorPolicies(publicClient, EXECUTOR);
        expect(result).toEqual([
            { policy: POLICY_A, policyType: 'assetuniverse' },
            { policy: POLICY_B, policyType: 'slippage' }
        ]);
    });
    it('readPolicySnapshot merges asset, static allocation, and slippage policies', async () => {
        const publicClient = mockPublicClient(({ address, functionName }) => {
            if (address === EXECUTOR && functionName === 'getPoliciesWithTypes') {
                return [
                    { policy: POLICY_A, policyType: 'assetuniverse' },
                    { policy: POLICY_B, policyType: 'staticallocation' },
                    { policy: POLICY_C, policyType: 'slippage' }
                ];
            }
            if (address === POLICY_A && functionName === 'getTokens')
                return [TOKEN_A, TOKEN_B];
            if (address === POLICY_B && functionName === 'priceOracle')
                return PRICE_ORACLE;
            if (address === POLICY_B && functionName === 'driftThresholdBps')
                return 250n;
            if (address === POLICY_B && functionName === 'toleranceThresholdBps')
                return 100n;
            if (address === POLICY_B && functionName === 'getAllTargets')
                return [
                    { token: TOKEN_A, bps: 6_000 },
                    { token: TOKEN_B, bps: 4_000 }
                ];
            if (address === POLICY_C && functionName === 'priceOracle')
                return PRICE_ORACLE;
            if (address === PRICE_ORACLE && functionName === 'feedRegistry')
                return FEED_REGISTRY;
            if (address === POLICY_C && functionName === 'maxSlippageBps')
                return 80n;
            throw new Error(`Unexpected call: ${address}:${functionName}`);
        });
        const snapshot = await readPolicySnapshot(publicClient, EXECUTOR);
        expect(snapshot.assetUniverseTokens).toEqual([TOKEN_A, TOKEN_B]);
        expect(snapshot.targetAllocations).toEqual([
            { token: TOKEN_A, bps: 6_000 },
            { token: TOKEN_B, bps: 4_000 }
        ]);
        expect(snapshot.driftThresholdBps).toBe(250);
        expect(snapshot.toleranceThresholdBps).toBe(100);
        expect(snapshot.maxSlippageBps).toBe(80);
        expect(snapshot.priceOracle).toBe(PRICE_ORACLE);
        expect(snapshot.tokenFeedRegistry).toBe(FEED_REGISTRY);
    });
    it('readPolicySnapshot falls back to hardcoded feed registry when none configured', async () => {
        const publicClient = mockPublicClient(({ address, functionName }) => {
            if (address === EXECUTOR && functionName === 'getPoliciesWithTypes')
                return [];
            if (address === EXECUTOR && functionName === 'getPolicies')
                return [];
            throw new Error(`Unexpected call: ${address}:${functionName}`);
        });
        const snapshot = await readPolicySnapshot(publicClient, EXECUTOR);
        expect(snapshot.tokenFeedRegistry).toBe(HARDCODED_TOKEN_FEED_REGISTRY_ADDRESS);
        expect(snapshot.assetUniverseTokens).toEqual([]);
        expect(snapshot.targetAllocations).toEqual([]);
    });
});
