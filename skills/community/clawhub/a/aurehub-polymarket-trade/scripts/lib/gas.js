// scripts/lib/gas.js
import { ethers } from 'ethers';

// Polygon requires a minimum 30 Gwei tip; some public RPCs return stale low estimates.
// NOTE: if this constant changes, update it here only — all callers import from this file.
const MIN_GAS_TIP = ethers.utils.parseUnits('30', 'gwei');

export async function polyGasOverrides(provider) {
  const feeData = await provider.getFeeData();
  // Use MIN_GAS_TIP as a floor. Optional chaining alone is insufficient: when fee data is null,
  // `?.lt()` returns undefined and the ternary would return undefined rather than MIN_GAS_TIP.
  const tip = (!feeData.maxPriorityFeePerGas || feeData.maxPriorityFeePerGas.lt(MIN_GAS_TIP))
    ? MIN_GAS_TIP : feeData.maxPriorityFeePerGas;
  const fee = (!feeData.maxFeePerGas || feeData.maxFeePerGas.lt(MIN_GAS_TIP))
    ? MIN_GAS_TIP : feeData.maxFeePerGas;
  return { maxPriorityFeePerGas: tip, maxFeePerGas: fee };
}
