import { describe, expect, it, vi } from 'vitest';
import { encodeFunctionData, type Address } from 'viem';

import { batchTradeAbi, executorModuleAbi } from '../src/contracts.js';
import {
  checkPoliciesVerbose,
  decodeRebalancingTxData,
  encodeExecuteTradeNowCall,
  encodeTradeData,
  executeTradeNow,
  normalizeRebalancingAllowances,
  simulateExecuteTradeNow,
  type BatchTrade,
  type BatchTradeConfig,
  type TokenApproval
} from '../src/executor.js';

const EXECUTOR = '0x1000000000000000000000000000000000000001' as Address;
const TOKEN_A = '0x2000000000000000000000000000000000000002' as Address;
const TOKEN_B = '0x3000000000000000000000000000000000000003' as Address;

const TRADES: BatchTrade[] = [{
  exchangeName: 'mockdex',
  from: TOKEN_A,
  fromAmount: 1_000n,
  to: TOKEN_B,
  minToReceiveBeforeFees: 900n,
  data: '0x1234',
  signature: '0xabcd'
}];

const APPROVALS: TokenApproval[] = [{ token: TOKEN_A, amount: 1_000n }];
const CONFIG: BatchTradeConfig = { checkFeelessWallets: true, revertOnError: true };

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
      publicClient: { simulateContract } as any,
      executorModule: EXECUTOR,
      approvals: APPROVALS,
      trades: TRADES,
      config: CONFIG
    });

    expect(simulateContract).toHaveBeenCalledTimes(1);
    const simulateArgs = (simulateContract as any).mock.calls[0][0];
    expect(simulateArgs.functionName).toBe('execute');
    expect(simulateArgs.account).toBeUndefined();
  });

  it('executeTradeNow calls walletClient.writeContract and returns tx hash', async () => {
    const writeContract = vi.fn(async () => '0xdeadbeef');

    const txHash = await executeTradeNow({
      walletClient: { writeContract } as any,
      executorModule: EXECUTOR,
      approvals: APPROVALS,
      trades: TRADES,
      config: CONFIG
    });

    expect(writeContract).toHaveBeenCalledTimes(1);
    const writeArgs = (writeContract as any).mock.calls[0][0];
    expect(writeArgs.functionName).toBe('execute');
    expect(txHash).toBe('0xdeadbeef');
  });

  it('checkPoliciesVerbose reads policy validation result', async () => {
    const publicClient = {
      readContract: vi.fn(async () => [true, EXECUTOR, 'ok'])
    } as any;

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
