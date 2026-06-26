# Market Context Checklist

Use this checklist before naming a setup. Context decides whether a pattern matters.

## 1. Start With The Higher Timeframe

- Is price near a prior swing high or low?
- Is price testing a breakout point, channel line, EMA, gap, or measured move?
- Is there room to move, or is price trapped in the middle of a larger range?

## 2. Classify The Recent Environment

### `trending`

- Several closes in one direction
- Limited overlap
- Pullbacks are shallow or brief
- Breakouts get follow-through

### `trading_range`

- Repeated overlap
- Big tails
- Breakouts fail quickly
- Reversals occur every few bars

### `broad_channel`

- There is directional drift
- But swings are deep enough to punish weak entries
- Strong continuation is less reliable than in a tight trend

If you cannot clearly distinguish the environment, use `unknown` or downgrade to `trading_range`.

## 3. Decide `Always In`

Use the recent sequence, not a single bar.

### `always_in = long`

- Bull bars are stronger than bear bars
- Pullbacks are weak, overlapping, or quickly bought
- Price spends most of its time above EMA or above a recent breakout point

### `always_in = short`

- Bear bars are stronger than bull bars
- Rallies are weak, overlapping, or quickly sold
- Price spends most of its time below EMA or below a recent breakout point

### `always_in = unknown`

- Reversals keep failing both ways
- Opposing bars are symmetrical
- The chart is balanced or trapped around magnets

## 4. Mark The Magnets

Useful magnets include:

- prior day/session high or low
- prior swing high or low
- range top or range bottom
- breakout point
- EMA or moving average cluster
- measured move target
- opening price or gap close on intraday charts

If the market is very close to a magnet, expect hesitation, profit-taking, or failed follow-through.

## 5. Ask Who Is Trapped

- Are breakout traders stuck from the latest failed move?
- Are counter-trend traders trapped by a strong surprise bar?
- Is the market likely to move just far enough to punish the weaker side before choosing direction?

Trap logic often explains why follow-through appears or disappears.

## 6. Filter For Tradeability

Downgrade or reject the setup when:

- it is in the middle of a clear range
- it runs directly into a nearby magnet
- the signal bar is weak
- the setup is counter-trend without strong reversal evidence
- the market has repeatedly disappointed in both directions

## Bottom-Line Rule

First decide whether the chart is tradable. Only then decide which setup name fits. If tradeability is low, output `watch` or `none` even when you can describe a recognizable pattern.
