/**
 * PancakeSwap V3 / Uniswap V3: derive token amounts from liquidity L at current sqrt price.
 * Matches Uniswap V3 Periphery LiquidityAmounts.getAmountsForLiquidity (same math as frontend v3math.ts).
 */

const Q96 = 2n ** 96n;

export function tickToSqrtPriceX96(tick) {
  const sqrtPrice = Math.sqrt(1.0001 ** tick);
  return BigInt(Math.round(sqrtPrice * Number(Q96)));
}

function getAmount0ForLiquidity(sqrtRatioAX96, sqrtRatioBX96, liquidity) {
  let a = sqrtRatioAX96;
  let b = sqrtRatioBX96;
  if (a > b) [a, b] = [b, a];
  if (a === b || liquidity === 0n) return 0n;
  const diff = b - a;
  return (liquidity * Q96 * diff) / b / a;
}

function getAmount1ForLiquidity(sqrtRatioAX96, sqrtRatioBX96, liquidity) {
  let a = sqrtRatioAX96;
  let b = sqrtRatioBX96;
  if (a > b) [a, b] = [b, a];
  if (a === b || liquidity === 0n) return 0n;
  return (liquidity * (b - a)) / Q96;
}

/**
 * @param {bigint} sqrtRatioX96 - current pool price from slot0
 * @param {number} tickLower
 * @param {number} tickUpper
 * @param {bigint} liquidity - position L (uint128)
 * @returns {{ amount0: bigint, amount1: bigint }}
 */
export function getAmountsForLiquidity(sqrtRatioX96, tickLower, tickUpper, liquidity) {
  if (liquidity === 0n || sqrtRatioX96 === 0n) return { amount0: 0n, amount1: 0n };

  let sqrtA = tickToSqrtPriceX96(tickLower);
  let sqrtB = tickToSqrtPriceX96(tickUpper);
  if (sqrtA > sqrtB) [sqrtA, sqrtB] = [sqrtB, sqrtA];

  if (sqrtRatioX96 <= sqrtA) {
    return { amount0: getAmount0ForLiquidity(sqrtA, sqrtB, liquidity), amount1: 0n };
  }
  if (sqrtRatioX96 >= sqrtB) {
    return { amount0: 0n, amount1: getAmount1ForLiquidity(sqrtA, sqrtB, liquidity) };
  }
  return {
    amount0: getAmount0ForLiquidity(sqrtRatioX96, sqrtB, liquidity),
    amount1: getAmount1ForLiquidity(sqrtA, sqrtRatioX96, liquidity),
  };
}
