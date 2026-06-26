import { vi, describe, it, expect, afterEach } from 'vitest';
import { getSafetyLevel, validateHardStops, checkRecentFill } from '../trade.js';

vi.mock('../lib/swap.js', () => ({
  getSwapQuote: vi.fn(),
  swapPolToUsdc: vi.fn(),
}));

import { getSwapQuote, swapPolToUsdc } from '../lib/swap.js';
import { checkAndSwapIfNeeded } from '../trade.js';

describe('getSafetyLevel', () => {
  it('under warn threshold → proceed', () => {
    expect(getSafetyLevel(10, { warn_threshold_usd: 50, confirm_threshold_usd: 500 })).toBe('proceed');
  });
  it('at warn threshold → warn', () => {
    expect(getSafetyLevel(50, { warn_threshold_usd: 50, confirm_threshold_usd: 500 })).toBe('warn');
  });
  it('between thresholds → warn', () => {
    expect(getSafetyLevel(200, { warn_threshold_usd: 50, confirm_threshold_usd: 500 })).toBe('warn');
  });
  it('at confirm threshold → confirm', () => {
    expect(getSafetyLevel(500, { warn_threshold_usd: 50, confirm_threshold_usd: 500 })).toBe('confirm');
  });
  it('over confirm threshold → confirm', () => {
    expect(getSafetyLevel(1000, { warn_threshold_usd: 50, confirm_threshold_usd: 500 })).toBe('confirm');
  });
});

describe('validateHardStops', () => {
  const ok = { usdceBalance: 200, polBalance: 0.05, marketActive: true, minOrderSize: 5 };

  it('passes when all conditions ok', () => {
    expect(() => validateHardStops(100, ok)).not.toThrow();
  });
  it('throws when USDC.e insufficient', () => {
    expect(() => validateHardStops(100, { ...ok, usdceBalance: 50 })).toThrow('USDC.e');
  });
  it('throws when gas too low', () => {
    expect(() => validateHardStops(100, { ...ok, polBalance: 0.005 })).toThrow('POL');
  });
  it('throws when market is closed', () => {
    expect(() => validateHardStops(100, { ...ok, marketActive: false })).toThrow('CLOSED');
  });
  it('throws when below min order size', () => {
    expect(() => validateHardStops(3, { ...ok, minOrderSize: 5 })).toThrow('min');
  });
});

describe('checkAndSwapIfNeeded', () => {
  afterEach(() => vi.clearAllMocks());

  const baseParams = {
    amount: 25,
    usdceBalance: 100,
    polBalance: 5,
    cfg: { yaml: {} },
    wallet: { address: '0xUser' },
    provider: {},
    confirmFn: vi.fn().mockResolvedValue(true),
  };

  it('returns false (no swap) when USDC.e is sufficient', async () => {
    const result = await checkAndSwapIfNeeded({ ...baseParams, usdceBalance: 100 });
    expect(result).toBe(false);
    expect(getSwapQuote).not.toHaveBeenCalled();
  });

  it('offers swap when USDC.e insufficient + POL sufficient, executes on confirm', async () => {
    const { ethers } = await import('ethers');
    getSwapQuote.mockResolvedValue({
      polNeeded: ethers.utils.parseEther('1'),
      rate: 2.5,
    });
    swapPolToUsdc.mockResolvedValue('27.50');

    const result = await checkAndSwapIfNeeded({ ...baseParams, usdceBalance: 3 });
    expect(result).toBe(true);
    expect(swapPolToUsdc).toHaveBeenCalled();
    expect(baseParams.confirmFn).toHaveBeenCalledOnce();
  });

  it('hard-stops when POL insufficient for swap + gas reserve', async () => {
    const { ethers } = await import('ethers');
    getSwapQuote.mockResolvedValue({
      polNeeded: ethers.utils.parseEther('10'),
      rate: 2.5,
    });

    // polAmountMax = 10 × 1.02 = 10.2; + 0.05 reserve = 10.25; polBalance = 5 → insufficient
    await expect(checkAndSwapIfNeeded({ ...baseParams, usdceBalance: 3, polBalance: 5 }))
      .rejects.toThrow('Insufficient POL');
  });

  it('returns "cancelled" when user declines swap', async () => {
    const { ethers } = await import('ethers');
    getSwapQuote.mockResolvedValue({
      polNeeded: ethers.utils.parseEther('1'),
      rate: 2.5,
    });

    const result = await checkAndSwapIfNeeded({
      ...baseParams,
      usdceBalance: 3,
      polBalance: 5,
      confirmFn: vi.fn().mockResolvedValue(false),
    });
    expect(result).toBe('cancelled');
    expect(swapPolToUsdc).not.toHaveBeenCalled();
  });

  it('returns "dry-run-swap" without executing swap when dryRun=true and USDC.e insufficient', async () => {
    const { ethers } = await import('ethers');
    getSwapQuote.mockResolvedValue({
      polNeeded: ethers.utils.parseEther('1'),
      rate: 2.5,
    });

    const result = await checkAndSwapIfNeeded({ ...baseParams, usdceBalance: 3, dryRun: true });
    expect(result).toBe('dry-run-swap');
    expect(swapPolToUsdc).not.toHaveBeenCalled();
    expect(baseParams.confirmFn).not.toHaveBeenCalled();
  });
});

// ── checkRecentFill ───────────────────────────────────────────────────────────

describe('checkRecentFill', () => {
  afterEach(() => vi.clearAllMocks());

  const tokenID = '0xabc123';
  const makerAddress = '0xUser';
  const nowSec = Math.floor(Date.now() / 1000);

  it('returns matching trade when found within window', async () => {
    const recentTrade = { id: 'trade-1', asset_id: tokenID, timestamp: String(nowSec - 10) };
    const client = { getTrades: vi.fn().mockResolvedValue([recentTrade]) };
    const result = await checkRecentFill(client, tokenID, makerAddress);
    expect(result).toEqual(recentTrade);
    expect(client.getTrades).toHaveBeenCalledWith(
      { maker_address: makerAddress, asset_id: tokenID },
      true,
    );
  });

  it('returns null when trade is outside the time window', async () => {
    const oldTrade = { id: 'trade-old', asset_id: tokenID, timestamp: String(nowSec - 300) };
    const client = { getTrades: vi.fn().mockResolvedValue([oldTrade]) };
    const result = await checkRecentFill(client, tokenID, makerAddress);
    expect(result).toBeNull();
  });

  it('returns null when no trades found', async () => {
    const client = { getTrades: vi.fn().mockResolvedValue([]) };
    const result = await checkRecentFill(client, tokenID, makerAddress);
    expect(result).toBeNull();
  });

  it('returns null (safe fallback) when getTrades throws', async () => {
    const client = { getTrades: vi.fn().mockRejectedValue(new Error('Network error')) };
    const result = await checkRecentFill(client, tokenID, makerAddress);
    expect(result).toBeNull();
  });
});
