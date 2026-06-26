---
name: Backtest Expert
version: 1.0.2
description: "Design, execute, and evaluate quantitative trading strategies using historical price data and Fama-French factor attribution via the Finskills API."
author: finskills
metadata:
  openclaw:
    requires:
      env:
        - FINSKILLS_API_KEY
    primaryEnv: FINSKILLS_API_KEY
  homepage: https://github.com/finskills/backtest-expert
---

# Backtest Expert

Design, execute, and evaluate quantitative trading strategies using historical
price data from the Finskills API. Transforms a natural-language strategy hypothesis
into a rigorous backtest with performance metrics, drawdown analysis, Fama-French
factor attribution, and walk-forward validation.

---

## Setup

**API Key required** — [Register at https://finskills.net](https://finskills.net) to get your free key.  
Header: `X-API-Key: <your_api_key>`
> **Get your API key**: Register at **https://finskills.net** — free tier available, Pro plan unlocks real-time quotes, history, and financials.

---

## When to Activate This Skill

Activate when the user:
- Describes a trading rule they want to test historically
- Asks "how would X strategy have performed?"
- Wants to validate a momentum, mean-reversion, or factor-based strategy
- Asks about Sharpe ratio, maximum drawdown, or strategy performance metrics
- Wants to see walk-forward or out-of-sample testing
- Asks to compare two or more strategies head-to-head

---

## Strategy Hypothesis Formulation

Before fetching data, clarify the strategy with the user:

1. **Universe**: Which stocks? (Single stock, S&P 500, sector, custom list)
2. **Signal**: What is the entry trigger? (Moving average crossover, RSI level, fundamental metric, etc.)
3. **Entry**: Long, Short, or Long/Short?
4. **Exit**: Trailing stop, fixed target, time-based, signal reversal?
5. **Holding Period**: Daily, weekly, monthly?
6. **Position Sizing**: Equal weight, volatility-adjusted, Kelly?
7. **Benchmark**: SPY (default) or sector ETF?

State the strategy in a formal grammar:
```
ENTRY:  Buy {SYMBOL} when {condition}
EXIT:   Sell when {condition} OR stop at {-X%}
HOLD:   Max {N} days / bars
SIZING: {$N fixed / X% of portfolio / equal weight}
BENCH:  {SPY / QQQ / custom}
PERIOD: From {YYYY-MM-DD} to {YYYY-MM-DD}
```

---

## Data Retrieval — Finskills API Calls

### 1. Historical OHLCV for Strategy Symbols
```
GET https://finskills.net/v1/stocks/history/{SYMBOL}?period=5y&interval=1d
```
Parameters:
- `period`: `1y`, `2y`, `5y`, `10y`, `max`
- `interval`: `1d` (daily), `1wk` (weekly), `1mo` (monthly)

Extract: date, open, high, low, close, volume, adjustedClose

Repeat for each symbol in the strategy universe AND the benchmark (SPY or QQQ).

### 2. Fama-French 3-Factor Data
```
GET https://finskills.net/v1/free/market/fama-french
```
Extract: Mkt-RF (market excess return), SMB (small-minus-big), HML (high-minus-low), RF (risk-free rate)  
Use for: Attribution analysis — what % of strategy return is explained by market, size, value factors

---

## Analysis Workflow

### Step 1 — Data Preparation

1. Align all price series to the same trading calendar (drop non-overlapping dates).
2. Use `adjustedClose` for all calculations (accounts for splits and dividends).
3. Compute daily returns: `r_t = (adjustedClose_t / adjustedClose_{t-1}) - 1`
4. Handle missing data: forward-fill up to 2 days; drop if missing > 2 consecutive days.

### Step 2 — Signal Generation

Based on the strategy rules, generate entry/exit signals for each day in the backtest.

**Example Signal Implementations:**

**Simple Moving Average Crossover:**
```
SMA_fast = rolling_mean(adjustedClose, window=fast_n)
SMA_slow = rolling_mean(adjustedClose, window=slow_n)
Signal = 1 (Long)  when SMA_fast crosses above SMA_slow
Signal = 0 (Flat)  when SMA_fast crosses below SMA_slow
```

**RSI Reversion:**
```
RSI = 100 - 100 / (1 + avg_gain_14 / avg_loss_14)
Signal = 1 (Long)  when RSI < 30 (oversold)
Signal = 0 (Flat)  when RSI > 70 (overbought)
```

**Momentum:**
```
Momentum_N = current_price / price_N_days_ago - 1
Signal = 1 when Momentum_N > threshold
Signal = 0 otherwise
```

### Step 3 — Portfolio Returns Calculation

```
strategy_return_t = Signal_{t-1} × return_t   (signal from prior day, no lookahead)
benchmark_return_t = SPY daily return
```

Compute cumulative returns:
```
cumulative_return = PRODUCT(1 + strategy_return_t) - 1
```

Apply transaction costs (default: 0.10% per round-trip trade, adjustable):
```
cost_t = 0.001 × |Signal_t - Signal_{t-1}|  (cost only on signal changes)
net_return_t = strategy_return_t - cost_t
```

### Step 4 — Performance Metrics

Compute the full performance scorecard:

| Metric | Formula |
|--------|---------|
| **Total Return** | PRODUCT(1 + r_t) - 1 |
| **Annualized Return (CAGR)** | (1 + total_return)^(252/n_days) - 1 |
| **Annualized Volatility** | STD(r_t) × √252 |
| **Sharpe Ratio** | (CAGR - rf_rate) / annualized_vol |
| **Sortino Ratio** | (CAGR - rf_rate) / downside_vol |
| **Max Drawdown** | max(1 - V_t / max(V_s for s ≤ t)) |
| **Calmar Ratio** | CAGR / Max Drawdown |
| **Win Rate** | % of trading days with positive return |
| **Avg Win / Avg Loss** | mean positive return / mean negative return |
| **Profit Factor** | sum wins / sum losses |
| **Alpha (vs benchmark)** | CAGR_strategy - CAGR_benchmark |
| **Beta** | COV(r_strategy, r_benchmark) / VAR(r_benchmark) |
| **Information Ratio** | Alpha / tracking error |
| **Number of Trades** | Count of signal transitions |
| **Avg Holding Period** | Avg days per trade |

### Step 5 — Fama-French Factor Attribution

Regress strategy excess returns against F-F factors:
```
r_strategy - RF = α + β₁(Mkt-RF) + β₂(SMB) + β₃(HML) + ε
```

Interpret:
- **α (Alpha)**: Risk-adjusted return not explained by factors — the "skill" component
- **β₁ (Market Beta)**: Sensitivity to market direction
- **β₂ (SMB loading)**: Small-cap vs. large-cap tilt
- **β₃ (HML loading)**: Value (high) vs. growth (low) tilt
- **R²**: How much of returns are explained by common factors (R² < 0.3 = distinctive strategy)

### Step 6 — Walk-Forward Validation

To detect overfitting, split the full history:
- **In-Sample (IS)**: First 60% of data — used to identify strategy parameters
- **Out-of-Sample (OOS)**: Last 40% — held out, tested after IS optimization

**Walk-Forward Efficiency Ratio:**
```
WFE = OOS_Sharpe / IS_Sharpe
```
- WFE > 0.7: Strategy generalizes well — low overfitting concern
- WFE 0.4–0.7: Some degradation — monitor live, reduce leverage
- WFE < 0.4: Likely overfit to historical data — do not trade with confidence

### Step 7 — Risk Scenarios

Stress-test the strategy in 3 regimes:
1. **2020 COVID Crash**: Feb 19 – Mar 23, 2020 (S&P -34% in 33 days)
2. **2022 Bear Market**: Jan 1 – Dec 31, 2022 (S&P -19.4%)
3. **2008 Financial Crisis**: Oct 1 – Dec 31, 2008 (S&P -38% in quarter)

For each stress scenario, report the strategy's return vs. SPY return.

---

## Output Format

```
╔══════════════════════════════════════════════════════════════════╗
║    BACKTEST REPORT  —  {STRATEGY NAME}                          ║
║    Period: {start_date}  to  {end_date}   ({N} trading days)   ║
╚══════════════════════════════════════════════════════════════════╝

📋 STRATEGY SUMMARY
  Universe:       {SYMBOL(s) or index}
  Entry Signal:   {description}
  Exit Signal:    {description}
  Position Type:  {Long / Long-Short}
  Benchmark:      {SPY / QQQ}
  Tx Cost:        0.10% per round-trip

📈 CUMULATIVE RETURNS
  Strategy:   +{X.X}%  ($100K → ${value}K)
  Benchmark:  +{X.X}%  ($100K → ${value}K)
  Alpha:      +{X.X}% annualized

📊 PERFORMANCE SCORECARD
               Strategy     Benchmark    Δ vs. Bench
  CAGR:         {X.X}%       {X.X}%      +{X.X}%
  Volatility:   {X.X}%       {X.X}%      
  Sharpe:        {X.XX}       {X.XX}      +{X.XX}
  Sortino:       {X.XX}       {X.XX}
  Max Drawdown: -{X.X}%      -{X.X}%
  Calmar:        {X.XX}       {X.XX}
  Win Rate:      {X.X}%       —
  Profit Factor: {X.XX}       —
  Avg Hold:      {N} days     —
  N Trades:      {count}      —

📉 DRAWDOWN ANALYSIS
  Worst Drawdown:       -{X}%  (from {date} to {date}, {N} days to recover)
  2nd Worst Drawdown:   -{X}%
  Average Drawdown:     -{X}%

🧬 FACTOR ATTRIBUTION (Fama-French)
  α (Annualized):   {X.XX}%  [{statistically significant yes/no}]
  β Market:         {X.XX}
  β SMB (size):     {X.XX}  [{small-cap / large-cap} tilt]
  β HML (value):    {X.XX}  [{value / growth} tilt]
  R² (explained):   {X}%

🔁 WALK-FORWARD VALIDATION
  In-Sample  ({dates}):  Sharpe {X.XX},  CAGR {X.X}%
  Out-of-Sample ({dates}): Sharpe {X.XX},  CAGR {X.X}%
  WF Efficiency Ratio:   {X.XX}  → {Generalizes well / Some degradation / Likely overfit}

💥 STRESS TEST
  2020 COVID Crash:    Strategy {+/-X}%  vs SPY -{X}%
  2022 Bear Market:    Strategy {+/-X}%  vs SPY -{X}%
  2008 Q4 Crash:       Strategy {+/-X}%  vs SPY -{X}%

🎯 VERDICT
  Signal Quality:   {Strong / Moderate / Weak / Overfit}
  Trade Live?       {Yes / Caution / No — further development needed}
  Suggested Refinement: {1–2 concrete suggestions to improve the strategy}
```

---

## Limitations

- Backtests suffer from survivorship bias (S&P 500 historical data excludes delisted companies).
- Look-ahead bias is explicitly prevented by using prior-day signals; verify signal construction.
- Slippage is not modeled (real-world execution will have impact beyond transaction cost assumption).
- Fama-French data may have a 1–2 month lag; factors are smoothed — not for very recent periods.
- Past performance in backtests does not guarantee future results.
