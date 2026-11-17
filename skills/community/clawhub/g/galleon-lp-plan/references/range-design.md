# Range design

A range is a risk decision, not a formatting choice.

## Choose inputs

- user objective: fee capture, passive inventory conversion, market making, or incentive farming
- expected holding period and maximum maintenance cadence
- price distribution and realized volatility over stated windows
- known catalysts, gaps, depeg boundaries, or correlated breaks
- active liquidity, depth, fee density, and reward density by tick
- gas and execution cost relative to position size
- maximum acceptable one-sided inventory

Narrow ranges concentrate fee exposure and short more gamma. Wide ranges reduce maintenance and fee density. A symmetric percentage range is only a baseline. Do not center blindly into a trend, a thin launch, an oracle discontinuity, or a known event.

## Tick conversion

For a human price stated as token1 per token0:

```text
raw ratio = human price * 10^(decimals1 - decimals0)
tick = ln(raw ratio) / ln(1.0001)
```

Read token0, token1, decimals, and tick spacing from the pool. Snap the lower tick down and the upper tick up to usable spacing when the goal is to contain the requested price interval. Check protocol tick bounds. The upper tick is exclusive.

Use the bundled helper:

```bash
node scripts/range.mjs --price 1.25 --width 10 --tick-spacing 60 --decimals0 18 --decimals1 18
```

Verify its output against the current official SDK or pool library before execution.

## Concentrated amount shape

Using square-root prices `sqrtPa`, `sqrtP`, and `sqrtPb` and liquidity `L`:

```text
P <= Pa: amount0 = L * (1/sqrtPa - 1/sqrtPb), amount1 = 0
Pa < P < Pb: amount0 = L * (1/sqrtP - 1/sqrtPb), amount1 = L * (sqrtP - sqrtPa)
P >= Pb: amount0 = 0, amount1 = L * (sqrtPb - sqrtPa)
```

Use protocol integer formulas for production values. Preserve token ordering and rounding direction. Calculate desired amounts from the execution quote, then set explicit maximum spend and minimum minted liquidity.

## Range evidence

Record why each boundary exists, what price or event invalidates it, expected time in range, estimated action frequency, and the net fee hurdle for a rebalance. If the evidence does not support a boundary, label the range a user-selected heuristic.
