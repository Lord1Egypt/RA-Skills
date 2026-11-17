# Protocol state

## Uniswap v2 and Aerodrome classic

Read pair reserves, total LP supply, wallet LP balance, decimals, fee parameters, and any gauge balance. The position's reserve share is:

```text
amount0 = reserve0 * lpBalance / totalSupply
amount1 = reserve1 * lpBalance / totalSupply
```

Use integer arithmetic with protocol rounding. Fees normally appear through reserve growth and LP value. If LP tokens are staked, include the gauge-held balance and verify who owns fees and rewards.

## Uniswap v3

Read NFT owner, pool, fee tier, tick spacing, lower and upper ticks, liquidity, tokens owed, current tick, fee growth inside, and collection history. Ownership approval is not ownership. Include both principal inventory and uncollected fees.

## Uniswap v4

Read pool state through the deployed StateView or the current official read path, not a v3-shaped pool contract. Bind the complete PoolKey and PoolId. Read position ownership, liquidity, current tick, fee state, subscriber or manager state, and hook state. Position discovery may require indexed PositionManager events, but the index is only discovery evidence; recheck ownership and state onchain. Decode hook permissions. Hook logic can change fee, liquidity, donation, or settlement behavior.

For a hook-issued share model, read the full currency set, internal reserves, actual balances, share supply, wallet or custodied shares, rate sources, amplification or other invariant state, and fee accumulators. Do not interpret the position as an NFT or sum shared reserves once per pairwise PoolKey.

## Slipstream

Read NFT owner, gauge custody or deposit state, liquidity, ticks, current tick, fee rights, reward accrual, epoch state, and reward dilution. Confirm whether unstaking is required to collect or modify. Never add unstaked fees and staked emissions unless current contracts prove both accrue.

## Current liquidity

For concentrated pools, headline TVL is insufficient. Read active liquidity and initialized ticks around the current price when action quality depends on depth. Use correct signed floor division for negative tick compression. Bound bitmap reads and mark incomplete profiles instead of returning false precision.
