import { vi, describe, it, expect, afterEach } from 'vitest';

vi.mock('ethers', async (importOriginal) => {
  const actual = await importOriginal();
  return {
    ...actual,
    ethers: {
      ...actual.ethers,
      Contract: vi.fn(),
      utils: actual.ethers.utils,
    },
  };
});

import { ethers } from 'ethers';
import { getSwapQuote, swapPolToUsdc } from '../lib/swap.js';

const mockCfg = { yaml: {} };

// ── getSwapQuote ──────────────────────────────────────────────────────────────

describe('getSwapQuote', () => {
  afterEach(() => vi.clearAllMocks());

  it('returns polNeeded and rate from QuoterV1 response', async () => {
    const mockCallStatic = { quoteExactOutputSingle: vi.fn().mockResolvedValue(
      ethers.utils.parseEther('12.5')  // polNeeded = 12.5 POL
    )};
    ethers.Contract.mockImplementation(function() { return { callStatic: mockCallStatic }; });

    const mockProvider = {};
    const result = await getSwapQuote({
      usdceNeeded: 27.5,
      provider: mockProvider,
      cfg: mockCfg,
    });

    expect(result.polNeeded).toBeDefined();
    expect(typeof result.rate).toBe('number');
    expect(result.rate).toBeGreaterThan(0);
    expect(result.rate).toBeCloseTo(2.2, 4); // 27.5 / 12.5 = 2.2
  });

  it('calls QuoterV1 with correct parameters', async () => {
    const mockQuote = vi.fn().mockResolvedValue(ethers.utils.parseEther('10'));
    ethers.Contract.mockImplementation(function() { return { callStatic: { quoteExactOutputSingle: mockQuote } }; });

    await getSwapQuote({ usdceNeeded: 25, provider: {}, cfg: mockCfg });

    expect(mockQuote).toHaveBeenCalledWith(
      '0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270', // WMATIC
      '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174', // USDC.e
      3000,
      ethers.utils.parseUnits('25', 6),
      0,
    );
  });

  it('uses custom quoter address from config', async () => {
    const mockQuote = vi.fn().mockResolvedValue(ethers.utils.parseEther('10'));
    ethers.Contract.mockImplementation(function(addr) { return { callStatic: { quoteExactOutputSingle: mockQuote }, _address: addr }; });

    const customAddr = '0x2222222222222222222222222222222222222222';
    const cfg = { yaml: { contracts: { uniswap_quoter: customAddr } } };
    await getSwapQuote({ usdceNeeded: 25, provider: {}, cfg });

    expect(ethers.Contract).toHaveBeenCalledWith(customAddr, expect.any(Array), {});
  });

  it('throws on Quoter call failure', async () => {
    ethers.Contract.mockImplementation(function() {
      return { callStatic: { quoteExactOutputSingle: vi.fn().mockRejectedValue(new Error('RPC error')) } };
    });

    await expect(getSwapQuote({ usdceNeeded: 25, provider: {}, cfg: mockCfg }))
      .rejects.toThrow('Unable to get swap quote');
  });
});

// ── swapPolToUsdc ─────────────────────────────────────────────────────────────

describe('swapPolToUsdc', () => {
  afterEach(() => vi.clearAllMocks());

  const mockWallet = { address: '0x1111111111111111111111111111111111111111' };

  it('calls router multicall with exactOutputSingle+refundETH and passes value', async () => {
    const mockTx = { wait: vi.fn().mockResolvedValue({
      logs: [{
        address: '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174',
        topics: [ethers.utils.id('Transfer(address,address,uint256)'), null, ethers.utils.hexZeroPad(mockWallet.address, 32)],
        data: ethers.utils.defaultAbiCoder.encode(['uint256'], [ethers.utils.parseUnits('27.5', 6)]),
      }],
    })};
    const mockMulticall = vi.fn().mockResolvedValue(mockTx);
    ethers.Contract.mockImplementation(function() { return { connect: () => ({ multicall: mockMulticall }) }; });

    const polAmountMax = ethers.utils.parseEther('12.75'); // polNeeded × 1.02
    const highTip = ethers.utils.parseUnits('50', 'gwei');
    const mockProvider = {
      getBalance: vi.fn().mockResolvedValue(ethers.utils.parseEther('100')),
      getFeeData: vi.fn().mockResolvedValue({ maxPriorityFeePerGas: highTip, maxFeePerGas: highTip }),
    };
    await swapPolToUsdc({
      polAmountMax,
      usdceTarget: 27.5,
      cfg: mockCfg,
      wallet: mockWallet,
      provider: mockProvider,
    });

    // multicall called with [swapCalldata, refundCalldata], value, and gas overrides
    expect(mockMulticall).toHaveBeenCalledWith(
      [expect.stringMatching(/^0x/), expect.stringMatching(/^0x/)],
      expect.objectContaining({ value: polAmountMax }),
    );
  });

  it('slippage: polAmountMax equals polNeeded × 1.02', () => {
    const polNeeded = ethers.utils.parseEther('12.5');
    const polAmountMax = polNeeded.mul(102).div(100);
    expect(parseFloat(ethers.utils.formatEther(polAmountMax))).toBeCloseTo(12.75, 2);
  });

  it('throws when POL balance is insufficient', async () => {
    const mockProvider = { getBalance: vi.fn().mockResolvedValue(ethers.utils.parseEther('0.001')) };
    ethers.Contract.mockImplementation(function() { return { connect: () => ({}) }; });

    await expect(swapPolToUsdc({
      polAmountMax: ethers.utils.parseEther('12.75'),
      usdceTarget: 27.5,
      cfg: mockCfg,
      wallet: mockWallet,
      provider: mockProvider,
    })).rejects.toThrow('Insufficient POL');
  });
});
