import { describe, expect, it, vi } from 'vitest';
import { encodeFunctionData } from 'viem';
import { batchTradeAbi, executorModuleAbi } from '../src/contracts.js';
import { checkPoliciesVerbose, decodeRebalancingTxData, encodeExecuteTradeNowCall, executeTradeNow, normalizeRebalancingAllowances, simulateExecuteTradeNow } from '../src/executor.js';
const EXECUTOR = '0x1000000000000000000000000000000000000001';
const TOKEN_A = '0x2000000000000000000000000000000000000002';
const TOKEN_B = '0x3000000000000000000000000000000000000003';
const TRADES = [{
        exchangeName: 'mockdex',
        from: TOKEN_A,
        fromAmount: 1000n,
        to: TOKEN_B,
        minToReceiveBeforeFees: 900n,
        data: '0x1234',
        signature: '0xabcd'
    }];
const APPROVALS = [{ token: TOKEN_A, amount: 1000n }];
const CONFIG = { checkFeelessWallets: true, revertOnError: true };
describe('executor', () => {
    it('encodes execute exactly as executor ABI expects', () => {
        const encoded = encodeExecuteTradeNowCall({
            approvals: APPROVALS,
            trades: TRADES,
            config: CONFIG
        });
        const expected = encodeFunctionData({
            abi: executorModuleAbi,
            functionName: 'execute',
            args: [TRADES, CONFIG]
        });
        expect(encoded).toBe(expected);
    });
    it('simulateExecuteTradeNow calls publicClient.simulateContract', async () => {
        const simulateContract = vi.fn(async () => ({}));
        await simulateExecuteTradeNow({
            publicClient: { simulateContract },
            executorModule: EXECUTOR,
            approvals: APPROVALS,
            trades: TRADES,
            config: CONFIG
        });
        expect(simulateContract).toHaveBeenCalledTimes(1);
        const simulateArgs = simulateContract.mock.calls[0][0];
        expect(simulateArgs.functionName).toBe('execute');
        expect(simulateArgs.account).toBeUndefined();
    });
    it('executeTradeNow calls walletClient.writeContract and returns tx hash', async () => {
        const writeContract = vi.fn(async () => '0xdeadbeef');
        const txHash = await executeTradeNow({
            walletClient: { writeContract },
            executorModule: EXECUTOR,
            approvals: APPROVALS,
            trades: TRADES,
            config: CONFIG
        });
        expect(writeContract).toHaveBeenCalledTimes(1);
        const writeArgs = writeContract.mock.calls[0][0];
        expect(writeArgs.functionName).toBe('execute');
        expect(txHash).toBe('0xdeadbeef');
    });
    it('checkPoliciesVerbose reads policy validation result', async () => {
        const publicClient = {
            readContract: vi.fn(async () => [true, EXECUTOR, 'ok'])
        };
        const result = await checkPoliciesVerbose({
            publicClient,
            executorModule: EXECUTOR,
            trades: TRADES,
            config: CONFIG
        });
        expect(result).toEqual({ ok: true, failedPolicy: EXECUTOR, reason: 'ok' });
    });
    it('decodes rebalancing txData and normalizes allowances', () => {
        const txData = encodeFunctionData({
            abi: batchTradeAbi,
            functionName: 'batchTrade',
            args: [TRADES, CONFIG]
        });
        const decoded = decodeRebalancingTxData(txData);
        const approvals = normalizeRebalancingAllowances([
            { token: { address: TOKEN_A }, neededAllowance: '1000' }
        ]);
        expect(decoded.trades).toEqual(TRADES);
        expect(decoded.config).toEqual(CONFIG);
        expect(approvals).toEqual([{ token: TOKEN_A, amount: 1000n }]);
    });
});
