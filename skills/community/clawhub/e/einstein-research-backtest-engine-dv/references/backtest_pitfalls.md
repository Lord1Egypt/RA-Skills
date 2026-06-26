# Backtest Pitfalls & How the Engine Avoids Them

_Reference guide for the `einstein-research-backtest-engine` skill._
_Companion to `einstein-research-backtest` (methodology guidance) and the engine code itself._

---

## Overview

A backtest is an experiment. Like any experiment, it can be rigged—intentionally or not—to show the result you want. The biases below are the most common ways backtests deceive, along with how the engine is designed to guard against each.

The golden rule: **if your backtest looks too good, it probably is.**

---

## 1. Look-Ahead Bias

### What it is
Using information that was not available at the time of the simulated trade decision.

### How it manifests
- Using today's closing price to decide today's trade (instead of tomorrow's open)
- Calculating a rolling average that includes future data points
- Referencing an index constituent list that was updated later (survivorship bias cousin)
- Using earnings data before the earnings release date

### How the engine guards against it
- All signals are **lagged by 1 trading day** before being applied to returns:
  ```python
  position = signals.shift(1).fillna(0)
  gross_returns = position * asset_returns
  ```
- The engine computes `pct_change()` on Close prices; to simulate proper entry you should use the **next day's open** in your strategy — an optional `--use-open` flag for this is the recommended enhancement
- Rolling windows in strategy templates use `min_periods` to avoid partial early windows generating unrealistic signals

### Red flags to watch for
- Sharpe ratio > 3.0 on daily data
- Win rate > 80%
- Zero or near-zero max drawdown over a long test period

---

## 2. Survivorship Bias

### What it is
Testing only on assets that survived to the present, ignoring companies that went bankrupt, delisted, or were acquired.

### How it manifests
- Downloading S&P 500 constituents today and testing from 2000 — you're excluding Enron, Lehman, Kodak, and hundreds of others
- A "sector rotation into strong stocks" study that only looks at stocks still trading

### How the engine guards against it
- The engine works on **user-specified tickers** — it makes no assumptions about index constituents
- When testing on indices like SPY, QQQ (as ETFs), survivorship bias is largely absent because the ETF itself held the survivors-at-the-time
- **Recommended practice**: Use ETFs for broad market backtests rather than individual stock universes

### Mitigation in user strategies
- Obtain point-in-time constituent data (Compustat, CRSP, Quandl) for equity universe tests
- Include delisted ticker data if available
- Test on ETFs when the question is about asset allocation, not stock selection

---

## 3. Overfitting / Curve-Fitting

### What it is
Optimizing strategy parameters so extensively on historical data that the strategy "memorizes" noise rather than capturing a genuine edge.

### How it manifests
- Testing 200 parameter combinations and selecting the best one
- Having many parameters (>5) for a simple strategy
- "Working" only in a narrow parameter range (spike, not plateau)

### How the engine guards against it
- **Walk-forward optimization** (`--walk-forward`) evaluates performance on out-of-sample periods the strategy has never seen
- The **degradation ratio** (OOS Sharpe / IS Sharpe) quantifies overfitting:
  - > 0.7 = good generalization
  - 0.5–0.7 = acceptable
  - < 0.5 = likely overfitting
- Built-in strategies use minimal parameters (2-4) with intuitive economic interpretations
- The verdict heuristic in the report explicitly penalizes strategies with poor WF degradation

### Red flags to watch for
- Performance spike at specific parameter values; poor performance ±10% away
- Walk-forward degradation ratio < 0.5
- Strategy requires frequent parameter re-optimization to maintain edge

---

## 4. Selection Bias / Data Snooping

### What it is
The act of choosing which data period, assets, or market conditions to report based on what makes the strategy look good.

### How it manifests
- "It works great on FAANG stocks 2010-2020" (cherry-picked assets + cherry-picked period)
- Testing 50 strategies, reporting only the 5 that worked
- Excluding "outlier" crash periods from the test

### How the engine guards against it
- **Full period testing**: The engine tests the entire `--start` to `--end` range with no gaps
- **Regime analysis** (`regime_metrics` in the report) forces you to see performance separately in bull, bear, and sideways markets — you can't hide bad bear-market performance
- All regime splits are computed automatically; no user intervention in regime labeling

### Mitigation in practice
- Test the same strategy logic on multiple asset classes / geographies
- If the strategy "doesn't work" in certain periods, that's data — not noise to remove

---

## 5. Transaction Cost Underestimation

### What it is
Assuming unrealistically low or zero trading costs, which inflates performance for high-turnover strategies.

### How it manifests
- Running a daily-rebalanced strategy with zero commission
- Ignoring market impact when the simulated position size is large
- Assuming limit order fills at mid rather than bid/ask crossing

### How the engine guards against it
- **Three-layer cost model**: commission + slippage + market impact (linear or square-root)
  ```
  cost = turnover × (commission + slippage)
  ```
- **`--pessimistic-costs` flag**: automatically doubles slippage and adds 50% to commissions — use this for stress testing
- **Square-root market impact model** (`--impact-model sqrt`): scales slippage by `sqrt(turnover)` to model the nonlinear impact of larger orders

### Recommended defaults
| Strategy type | Commission | Slippage | Mode |
|---|---|---|---|
| Daily ETF rotation | 0.001 | 0.001 | linear |
| Monthly asset allocation | 0.001 | 0.0005 | linear |
| High-turnover intraday | 0.002 | 0.002 | sqrt |
| Large position sizing | 0.001 | 0.001 | sqrt |

---

## 6. Time-Period Bias

### What it is
A strategy that only works in a specific market regime or time window, not in general.

### How it manifests
- Momentum strategy tested only in the 2010–2021 bull market
- Mean reversion strategy that fails during trending regimes
- A strategy that benefited from falling interest rates (1982–2022) but may not work going forward

### How the engine guards against it
- **Regime-aware metrics**: bull/bear/sideways splits are computed automatically using SPY's 200-day SMA
- **Minimum test period**: We recommend ≥ 10 years covering at least one full bear market
- Reports surface `years_tested` and per-regime metrics to make this visible

### Red flags to watch for
- Strategy shows Sharpe > 1.5 in bull regime but Sharpe < 0 in bear regime
- All profitable years are in one contiguous stretch
- Out-of-sample period happens to land in the same regime as in-sample

---

## 7. Rebalancing Frequency Mismatch

### What it is
Assuming trades can be executed at a frequency that isn't realistic for the strategy's edge.

### How it manifests
- A "weekly" momentum strategy actually rebalancing daily
- Assuming intraday signals can be executed at daily close prices

### How the engine guards against it
- Strategy templates explicitly define `holding_period` and `rebalance_dates`
- The dual momentum template rebalances only monthly, matching Antonacci's original methodology
- Turnover is computed daily and transaction costs are proportional to actual position changes

---

## 8. Leverage and Risk Scaling Blindness

### What it is
Not accounting for the leverage implicit in a strategy, or comparing a leveraged strategy to an unleveraged benchmark.

### How it manifests
- Reporting a portfolio with 2× leverage as outperforming SPY without noting the leverage
- Risk parity strategies that use leverage to equalize volatility contributions

### How the engine guards against it
- Default position sizes are clipped to [-1, 1] (no leverage)
- Benchmark is always buy-and-hold (unleveraged) for fair comparison
- The `information_ratio` (planned enhancement) normalizes by tracking error

---

## 9. Benchmark Mismatch

### What it is
Comparing a strategy's performance to an inappropriate benchmark, making the alpha appear larger.

### How it manifests
- Comparing a high-yield bond rotation strategy to the S&P 500 (different asset class)
- Comparing a low-beta defensive strategy to SPY during a raging bull market

### How the engine guards against it
- `--benchmark-ticker` is configurable; always specify a relevant benchmark
- The report shows both absolute metrics and alpha vs the benchmark
- For multi-asset strategies, consider using a blended benchmark

---

## 10. Liquidity Blindness

### What it is
Assuming the strategy can trade at observed prices without moving the market, which is unrealistic for large positions in illiquid stocks.

### How it manifests
- A micro-cap momentum strategy that assumes executing at the next-day VWAP in thin markets
- Options strategies ignoring bid-ask spread

### How the engine guards against it
- The square-root market impact model (`--impact-model sqrt`) scales costs with position size
- For equity strategies on liquid ETFs and large-caps, standard slippage assumptions are adequate
- **User responsibility**: Always verify that your universe is sufficiently liquid for the simulated trade sizes

---

## Summary Checklist

Before accepting any backtest result, verify:

- [ ] No look-ahead: signals lagged, price data point-in-time
- [ ] No survivorship: using ETFs or point-in-time universe data  
- [ ] Not overfitted: walk-forward degradation ratio ≥ 0.5
- [ ] Not data-snooped: strategy tested on the full period, all regimes shown
- [ ] Realistic costs: commission + slippage, consider `--pessimistic-costs`
- [ ] Sufficient time: ≥ 5 years, preferably ≥ 10 including a bear market
- [ ] Appropriate benchmark: comparable risk and asset class
- [ ] Adequate sample size: ≥ 100 non-trivial trade decisions
- [ ] Performance is stable across parameter ranges (plateau, not spike)
- [ ] Bear-market regime performance is acceptable

---

## Further Reading

- Jegadeesh & Titman (1993) — "Returns to Buying Winners and Selling Losers"
- Faber (2007) — "A Quantitative Approach to Tactical Asset Allocation" 
- Antonacci (2012) — "Risk Premia Harvesting Through Dual Momentum"
- Bailey et al. (2014) — "The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting, and Non-Normality"
- Lopez de Prado (2018) — "Advances in Financial Machine Learning" (esp. Chapter 11: Backtesting)
- Harvey & Liu (2015) — "Backtesting" (multiple testing problem in financial research)
