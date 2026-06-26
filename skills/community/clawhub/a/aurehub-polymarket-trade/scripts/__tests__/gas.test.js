import { describe, it, expect, vi } from 'vitest';
import { ethers } from 'ethers';

// polyGasOverrides is not exported, so test via a mock provider
vi.mock('ethers', async () => {
  const actual = await vi.importActual('ethers');
  return { ...actual };
});

import { polyGasOverrides } from '../lib/gas.js';

const gwei = n => ethers.utils.parseUnits(String(n), 'gwei');
const MIN_TIP = gwei(30);

function mockProvider(maxPriorityFeePerGas, maxFeePerGas) {
  return { getFeeData: async () => ({ maxPriorityFeePerGas, maxFeePerGas }) };
}

describe('polyGasOverrides', () => {
  it('passes through values above the 30 Gwei floor', async () => {
    const overrides = await polyGasOverrides(mockProvider(gwei(50), gwei(100)));
    expect(overrides.maxPriorityFeePerGas.eq(gwei(50))).toBe(true);
    expect(overrides.maxFeePerGas.eq(gwei(100))).toBe(true);
  });

  it('clamps values below the 30 Gwei floor up to MIN_GAS_TIP', async () => {
    const overrides = await polyGasOverrides(mockProvider(gwei(10), gwei(15)));
    expect(overrides.maxPriorityFeePerGas.eq(MIN_TIP)).toBe(true);
    expect(overrides.maxFeePerGas.eq(MIN_TIP)).toBe(true);
  });

  it('returns MIN_GAS_TIP when fee data fields are null (degraded RPC)', async () => {
    const overrides = await polyGasOverrides(mockProvider(null, null));
    expect(overrides.maxPriorityFeePerGas.eq(MIN_TIP)).toBe(true);
    expect(overrides.maxFeePerGas.eq(MIN_TIP)).toBe(true);
  });

  it('returns MIN_GAS_TIP when fee data fields are undefined', async () => {
    const overrides = await polyGasOverrides(mockProvider(undefined, undefined));
    expect(overrides.maxPriorityFeePerGas.eq(MIN_TIP)).toBe(true);
    expect(overrides.maxFeePerGas.eq(MIN_TIP)).toBe(true);
  });

  it('clamps exactly at the 30 Gwei boundary', async () => {
    const overrides = await polyGasOverrides(mockProvider(gwei(30), gwei(30)));
    expect(overrides.maxPriorityFeePerGas.eq(MIN_TIP)).toBe(true);
    expect(overrides.maxFeePerGas.eq(MIN_TIP)).toBe(true);
  });
});
