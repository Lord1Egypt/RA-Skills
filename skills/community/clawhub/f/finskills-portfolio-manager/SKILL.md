---
name: Portfolio Manager
version: 1.0.3
description: "Monitor and rebalance a multi-asset portfolio using real-time quotes, sector allocation, and risk metrics from the Finskills API."
author: finskills
metadata:
  openclaw:
    requires:
      env:
        - FINSKILLS_API_KEY
    primaryEnv: FINSKILLS_API_KEY
  homepage: https://github.com/finskills/portfolio-manager
---

# Portfolio Manager

Monitor, analyze, and optimize a multi-asset US equity portfolio using live batch
quotes, market summary data, and sector performance from the Finskills API.
Computes real-time P&L, risk metrics, sector concentration, and generates
rebalancing recommendations aligned with your target allocation.

---

## Setup

**API Key required** — [Register at https://finskills.net](https://finskills.net) to get your free key.  
Header: `X-API-Key: <your_api_key>`
> **Get your API key**: Register at **https://finskills.net** — free tier available, Pro plan unlocks real-time quotes, history, and financials.

---

## When to Activate This Skill

Activate when the user:
- Provides a list of holdings (ticker + shares or $ value) and asks for portfolio analysis
- Asks about their portfolio's performance, sector concentration, or risk metrics
- Wants a rebalancing recommendation
- Asks how their portfolio compares to the S&P 500 or benchmarks
- Asks which positions are dragging or leading performance

---

## Required Information

Before starting, collect:
1. **Holdings list**: Each entry needs `ticker`, `shares` (or `current_value`), and optionally `cost_basis`
2. **Total portfolio value** (or derive from positions)
3. **Target allocation** (if rebalancing is requested) — e.g., "60% equities, 30% bonds, 10% cash"
4. **Benchmark** — Default is S&P 500 (SPY)

Example holdings input format:
```
AAPL: 50 shares @ $150 cost basis
MSFT: 30 shares @ $280 cost basis
NVDA: 20 shares @ $400 cost basis
SPY:  100 shares @ $420 cost basis
```

---

## Data Retrieval — Finskills API Calls

### 1. Batch Quotes for All Holdings
```
GET https://finskills.net/v1/stocks/quotes?symbols={TICKER1,TICKER2,...}
```
Extract for each: `price`, `changePercent`, `marketCap`, `volume`

### 2. Market Summary (Benchmark)
```
GET https://finskills.net/v1/market/summary
```
Extract: S&P 500, Nasdaq, Dow Jones — current level, daily change, YTD performance

### 3. Sector Performance
```
GET https://finskills.net/v1/market/sectors
```
Extract: All 11 GICS sector ETF performances (1D, 1W, 1M, YTD) for context

### 4. Company Profile (for sector classification)
For each unique ticker not already classified:
```
GET https://finskills.net/v1/stocks/profile/{SYMBOL}
```
Extract: `sector`, `industry` (to assign sector weight in portfolio)

---

## Analysis Workflow

### Step 1 — Position Valuation

For each holding:
```
Current Value   = shares × current_price
Daily P&L       = shares × (current_price − prev_close_price)
Daily P&L %     = current_price / prev_close_price − 1
Total P&L       = current_value − (shares × cost_basis)    [if cost basis provided]
Total P&L %     = (current_value / (shares × cost_basis)) − 1
Portfolio Weight = current_value / total_portfolio_value
```

### Step 2 — Portfolio-Level Metrics

**Performance:**
```
Portfolio Daily Return  = Σ (weight_i × daily_return_i)
Portfolio Total Return  = (total_current_value / total_cost_basis) − 1  [if basis known]
Best Performer (1D)     = max daily_return_i
Worst Performer (1D)    = min daily_return_i
```

**Risk Metrics (estimate from weights and sector exposure):**
- **Concentration Risk**: Largest single position as % of portfolio
  - > 20%: High concentration ⚠️
  - > 35%: Very high concentration 🚨
- **Sector Concentration**: Top sector weight
  - > 40%: Sector-concentrated ⚠️
- **Beta Approximation**: Weight-average of individual stock betas (if available from profile data)
  - Use sector beta proxies: Tech ≈ 1.3, Utilities ≈ 0.5, Financials ≈ 1.1, Healthcare ≈ 0.7

**Benchmark Comparison:**
```
Relative Return (1D) = Portfolio Daily Return − S&P 500 Daily Return
```

### Step 3 — Sector Allocation Analysis

Group holdings by sector (using profile data):
- Compute actual sector weights
- Compare to S&P 500 sector weights (approximate benchmarks):
  - Technology: 29%, Healthcare: 13%, Financials: 13%, Consumer Disc: 11%,
    Industrials: 9%, Communication: 8%, Energy: 4%, Consumer Staples: 6%,
    Real Estate: 3%, Materials: 2%, Utilities: 2%

Flag **overweight** (> +10pp vs benchmark) and **underweight** (< -10pp vs benchmark) sectors.

### Step 4 — Rebalancing Analysis (if requested)

**Target deviation detection:**
```
For each position:
  Target Weight = stated_target_%
  Current Weight = current_value / total_value
  Drift = Current Weight − Target Weight
  Rebalance Action = BUY/SELL if abs(Drift) > 5%
  Rebalance Quantity = abs(Drift × total_value) / current_price  [shares to trade]
```

**Tax-aware note**: Flag positions with > 1 year holding for LTCG treatment before suggesting sells.

### Step 5 — Actionable Recommendations

Generate 3–5 specific recommendations:
- Positions to trim (concentration/overweight sector)
- Positions to add (underweight sectors relative to conviction)
- Hedging suggestions (if portfolio Beta > 1.2 and market at all-time highs)
- Cash deployment suggestions (if cash > 10% of target)

---

## Output Format

```
╔══════════════════════════════════════════════════════╗
║      PORTFOLIO REPORT  —  {DATE}                    ║
╚══════════════════════════════════════════════════════╝

💼 PORTFOLIO SUMMARY
  Total Value:     ${total_value}
  Daily P&L:       ${daily_pnl}  ({daily_pnl_pct}%)
  Total Return:    ${total_pnl}  ({total_pnl_pct}%)  [vs. cost basis]
  vs. S&P 500 (1D): {+/- bps} bps

📋 HOLDINGS BREAKDOWN
  {Ticker}  {Shares}sh  ${price}  {weight}%  Day: {+/-}%  Total: {+/-}%
  ─────────────────────────────────────────────────────
  AAPL      50 sh       $189.40   18.4%      +1.2%       +26.3%
  MSFT      30 sh       $415.20   24.2%      -0.3%       +48.2%
  ...
  ─────────────────────────────────────────────────────
  TOTAL     —           —         100%       {port_day}% {port_total}%

  🏆 Best Today:  {ticker} +{%}
  📉 Worst Today: {ticker} -{%}

🏛️ SECTOR ALLOCATION
  Sector           Portfolio  S&P 500  Over/Under
  Technology         {%}       29%      {+/-pp}
  Healthcare         {%}       13%      {+/-pp}
  ...
  [⚠️ Any sectors > 40% or > +15pp vs benchmark]

⚠️ RISK FLAGS
  • Largest position: {ticker} at {%} [{normal/concentrated}]
  • Est. Portfolio Beta: {beta} [vs SPY]
  • {Any other flags}

📊 MARKET CONTEXT
  S&P 500:  {level}  {day_change}%  YTD: {ytd}%
  Nasdaq:   {level}  {day_change}%  YTD: {ytd}%
  {Leading sector today}: +{%}
  {Lagging sector today}: -{%}

🔄 REBALANCING RECOMMENDATIONS
  1. {Action}: {Ticker} — {rationale}
  2. {Action}: {Ticker} — {rationale}
  3. {Action}: Consider adding {sector} exposure (currently underweight {pp})
```

---

## Limitations

- Batch quote latency may be 1–15 minutes delayed depending on data source.
- Beta estimates are approximated from sector proxies unless individual beta data is available.
- Bond, international equity, and alternative assets are not currently covered.
- This skill does not connect to brokerage accounts or execute trades.
