import { describe, expect, it, vi } from 'vitest';
import { runSmoke } from '../scripts/smoke.js';
function makeIo() {
    const log = vi.fn();
    const error = vi.fn();
    const io = { log, error };
    return { io, log, error };
}
function makeConfig() {
    return {
        safeAddress: '0x1000000000000000000000000000000000000001',
        chainId: 8453,
        rpcUrl: 'https://mainnet.base.org',
        executorModuleAddress: '0x2000000000000000000000000000000000000002'
    };
}
describe('smoke', () => {
    it('returns non-zero when config load fails', async () => {
        const { io, log } = makeIo();
        const code = await runSmoke([], io, {
            readConfigFromEnv: () => {
                throw new Error('bad env');
            },
            createViemClients: vi.fn(),
            readPolicySnapshot: vi.fn(),
            check_drift: vi.fn(),
            plan_rebalance: vi.fn(),
            simulateExecuteTradeNow: vi.fn()
        });
        expect(code).toBe(1);
        expect(String(log.mock.calls[0][0])).toContain('"ok": false');
    });
    it('passes happy-path checks and warns for skipped optional preflights', async () => {
        const { io, log } = makeIo();
        const publicClient = { getChainId: vi.fn(async () => 8453) };
        const code = await runSmoke([], io, {
            readConfigFromEnv: () => makeConfig(),
            createViemClients: () => ({ publicClient }),
            readPolicySnapshot: vi.fn(async () => ({
                assetUniverseTokens: [],
                targetAllocations: []
            })),
            check_drift: vi.fn(async () => ({
                shouldRebalance: false,
                thresholdBps: 0,
                maxDriftBps: 0,
                explanation: 'ok',
                why: 'ok',
                tokens: []
            })),
            plan_rebalance: vi.fn(),
            simulateExecuteTradeNow: vi.fn()
        });
        expect(code).toBe(0);
        const output = String(log.mock.calls[0][0]);
        expect(output).toContain('"ok": true');
        expect(output).toContain('"status": "warn"');
    });
});
