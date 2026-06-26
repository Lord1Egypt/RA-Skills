---
map_index: "1"
exploration_mode: "breadth"
strategy_family: "moving_average_crossover"
notes: "Baseline daily SMA crossover for the open-source backtesting.py workspace."
---

# AutoTradeResearch Program

This file is the strategy notebook for the coding agent.

Read it before every experiment and update the notes when you learn something reusable.

## Frozen guidance

- This is the open-source AutoTradeResearch repository.
- Keep the workspace lightweight and avoid adding new framework layers.
- The evaluator is fixed outside `agent/`. Improve the strategy, not the scoring path.
- Read generated results before choosing the next move.

## Current setup

Market: US stocks / ETFs by default unless the user chooses otherwise
Assets: SPY by default for the sample evaluator data
Data source: local `../data/prices.csv` when present, otherwise evaluator default
Timeframe: daily by default unless the user chooses otherwise
Mode: historical backtesting only

## Map index rules

- A new direction is `1`, `2`, `3`.
- A child of strategy `1` is `1-1`.
- A parallel child of `1-1` is `1-2`.
- A deeper child of `1-1` is `1-1-1`.
- Parameter-only tweaks may reuse the same `map_index` and explain the difference in notes.

## Experiment loop reminder

1. Choose breadth or depth.
2. Choose one strategy idea.
3. State the hypothesis: signal, why it might work, when it might fail.
4. Modify files under this `agent/` directory.
5. Let the outer loop run the fixed evaluator.
6. Update this file only when there is a reusable lesson.

## Strategy families

Explore both breadth and depth.

Potential families:

- trend following
- moving-average crossover
- breakout
- mean reversion
- RSI / Bollinger reversal
- cross-sectional momentum
- volatility filter
- carry / funding
- price-volume divergence
- multi-signal combination

Rules:

- If three consecutive experiments are from one family, switch families.
- If a family has around ten variants without improvement, park it.
- Prefer strategy-family changes over tiny parameter nudges.
- Keep strategies simple and explainable.

## Strategy source levels

L0 — built-in seeds
L1 — user-described ideas
L2 — public strategies from GitHub, TradingView, QuantConnect, Freqtrade examples, blogs, notebooks
L3 — collisions between components from different strategies
L4 — survivors from previous backtests

## Notes maintained by the agent

### Active direction

Baseline family: moving-average crossover.

### Active hypothesis

Use a simple trend-following baseline first, then branch into either faster trend filters or a different family.

### Promising ideas

- Add a regime filter only if the plain crossover shows a stable edge.

### Parked ideas

- not set yet

### Failed patterns

- not set yet

### Reusable lessons

- not set yet
