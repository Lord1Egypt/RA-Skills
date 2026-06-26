---
name: US Stock Analyzer
version: 1.0.0
description: "Perform institutional-grade analysis of any US-listed stock using real-time and fundamental data from the Finskills API."
author: finskills
homepage: https://github.com/finskills/us-stock-analyzer
credentials:
  - name: FINSKILLS_API_KEY
    description: "Finskills API key — register for free at https://finskills.net (Pro plan unlocks historical data, financials, and batch quotes)"
    required: true
    link: https://finskills.net
---

# US Stock Analyzer

Perform institutional-grade analysis of any US-listed stock using real-time and
fundamental data from the Finskills API. Delivers a structured investment report
covering business quality, financial health, valuation, analyst consensus, and
key risks — all in a single conversation turn.

---

## Setup

**API Key required** — [Register at https://finskills.net](https://finskills.net) to get your free key (Pro plan for full functionality).  
Set your key as: `FINSKILLS_API_KEY=your_key_here`  
All requests use header: `X-API-Key: <your_api_key>`

---

## When to Activate This Skill

Activate when the user:
- Asks to "analyze", "research", "evaluate", or "deep dive" into a specific stock
- Provides a ticker symbol and asks for an investment opinion
- Requests a buy/sell/hold assessment on a US equity
- Asks for fundamental analysis, valuation, or earnings quality review

---

## Required Information

Before starting, resolve:
1. **Ticker symbol** — e.g., `AAPL`, `NVDA`, `MSFT`. Ask if not provided.
2. **Analysis depth** — Quick (Level 1), Standard (Level 2, default), or Deep (Level 3).
3. **Investment horizon** — Short-term (< 3 months), medium (3–12 months), long-term (> 12 months). Default: long-term.

---

## Data Retrieval — Finskills API Calls

Make the following API calls in parallel (all require `X-API-Key` header):

### 1. Real-Time Quote
```
GET https://finskills.net/v1/stocks/quote/{SYMBOL}
```
Extract: `price`, `change`, `changePercent`, `volume`, `marketCap`, `week52High`, `week52Low`, `avgVolume`

### 2. Company Profile
```
GET https://finskills.net/v1/stocks/profile/{SYMBOL}
```
Extract: `name`, `sector`, `industry`, `description`, `employees`, `website`, `country`, `exchange`

### 3. Financial Statements (3–5 years)
```
GET https://finskills.net/v1/stocks/financials/{SYMBOL}
```
Extract from income statement: `revenue`, `grossProfit`, `operatingIncome`, `netIncome`, `eps`  
Extract from balance sheet: `totalDebt`, `cashAndEquivalents`, `totalAssets`, `totalEquity`  
Extract from cash flow: `operatingCashFlow`, `freeCashFlow`, `capitalExpenditures`

### 4. Analyst Recommendations
```
GET https://finskills.net/v1/stocks/recommendations/{SYMBOL}
```
Extract: `strongBuy`, `buy`, `hold`, `sell`, `strongSell` counts; consensus rating; mean target price; price target range

### 5. Earnings History & Estimates
```
GET https://finskills.net/v1/stocks/earnings/{SYMBOL}
```
Extract: last 4 quarters of EPS (actual vs estimate, beat/miss); next quarter EPS estimate; revenue estimates

### 6. Institutional Holders (optional, Level 2+)
```
GET https://finskills.net/v1/stocks/holders/{SYMBOL}
```
Extract: top 5 holders, total institutional ownership %, recent changes (bought/sold)

---

## Analysis Workflow

### Step 1 — Data Validation
Confirm all API calls returned `success: true`. Note which data provider served
each call (`source` field). Flag any stale data (cached > 24h for quotes).

### Step 2 — Business Quality Assessment

Score each dimension 1–5:

| Dimension | Signals to Look For |
|-----------|-------------------|
| **Competitive Moat** | Market leadership, pricing power, switching costs, network effects |
| **Management Quality** | Capital allocation history, FCF conversion, debt management |
| **Revenue Quality** | Recurring/subscription vs one-time, customer concentration |
| **Growth Trajectory** | YoY revenue growth trend (accelerating/decelerating/stable) |

Calculate a composite Business Quality Score (BQS) = average of the four dimensions.

### Step 3 — Financial Health Scorecard

Compute and interpret:

| Metric | Formula | Benchmark |
|--------|---------|-----------|
| Gross Margin | grossProfit / revenue | Industry-specific |
| Operating Margin | operatingIncome / revenue | > 15% healthy |
| FCF Margin | freeCashFlow / revenue | > 10% excellent |
| Net Debt / EBITDA | (totalDebt − cash) / EBITDA | < 2x conservative |
| ROE | netIncome / totalEquity | > 15% strong |
| FCF Yield | freeCashFlow / marketCap | > 4% attractive |
| Current Ratio | currentAssets / currentLiabilities | > 1.5 healthy |

Flag any metric outside healthy range with a ⚠️ symbol.

### Step 4 — Valuation Analysis

Calculate:

| Ratio | Formula | Context |
|-------|---------|---------|
| P/E (TTM) | price / EPS_TTM | vs sector average |
| Forward P/E | price / EPS_NextYear_estimate | vs 5-yr historical avg |
| EV/EBITDA | (marketCap + netDebt) / EBITDA | < 15x value zone |
| P/FCF | marketCap / freeCashFlow | vs growth peers |
| PEG Ratio | P/E / EPS_3yr_growth | < 1.0 undervalued |

Classify valuation as: **Deep Value** / **Fair Value** / **Premium** / **Stretched**

Provide a range-based fair value estimate using at least two methods (DCF implied
from FCF yield, and P/E reversion to sector mean).

### Step 5 — Earnings Quality & Analyst Coverage

Analyze earnings history (last 4 quarters):
- Beat rate: percentage of quarters beating EPS estimates
- Average surprise magnitude (positive/negative)
- Revenue trend vs EPS trend (divergence signals accounting risk)

Analyst consensus summary:
- Consensus rating label (Strong Buy / Buy / Hold / Underperform / Sell)
- Mean price target vs current price (implied upside/downside %)
- Breadth: number of analysts covering the stock
- Target price range (bull case vs bear case)

### Step 6 — Risk Identification

Systematically identify:
- **Balance sheet risk**: leverage, debt maturity, liquidity
- **Earnings risk**: customer concentration, cyclicality, margin pressure trends  
- **Macro risk**: interest rate sensitivity, FX exposure, commodity input costs
- **Regulatory/ESG risk**: industry-specific regulatory environment
- **Valuation risk**: how much multiple compression would hurt total return

### Step 7 — Investment Verdict

Based on all data, output:
- **Rating**: STRONG BUY / BUY / HOLD / AVOID / SELL
- **12-Month Price Target**: derived from valuation analysis (base case)
- **Bull Case / Bear Case**: target under favorable / adverse scenario
- **Confidence Level**: HIGH / MEDIUM / LOW (based on data completeness and
  earnings predictability)

---

## Output Format

```
═══════════════════════════════════════════════════
  US STOCK ANALYSIS REPORT — {TICKER} ({DATE})
═══════════════════════════════════════════════════

📌 COMPANY SNAPSHOT
  {Company Name} | {Sector} | {Industry}
  Price: ${price}  Change: {change}%  Market Cap: ${marketCap}
  52-Week Range: ${week52Low} — ${week52High}

📊 BUSINESS QUALITY SCORE: {BQS}/5
  ◦ Competitive Moat:   {score}/5 — {brief rationale}
  ◦ Management Quality: {score}/5 — {brief rationale}
  ◦ Revenue Quality:    {score}/5 — {brief rationale}
  ◦ Growth Trajectory:  {score}/5 — {brief rationale}

💰 FINANCIAL HEALTH
  Revenue Growth (YoY): {%}  |  Gross Margin: {%}  |  Operating Margin: {%}
  FCF Margin: {%}  |  Net Debt/EBITDA: {x}  |  ROE: {%}
  [⚠️ Flag any concerns]

📐 VALUATION
  TTM P/E: {x}  |  Forward P/E: {x}  |  EV/EBITDA: {x}
  P/FCF: {x}    |  PEG: {x}
  Assessment: {Deep Value / Fair Value / Premium / Stretched}
  Fair Value Range: ${low} — ${high}

📈 ANALYST CONSENSUS
  Rating: {consensus}  |  Mean Target: ${target}  ({upside}% upside)
  Distribution: {strongBuy}SB / {buy}B / {hold}H / {sell}S / {strongSell}SS
  Analysts: {count}  |  Target Range: ${low} — ${high}

📋 EARNINGS QUALITY
  Beat Rate: {%} ({n}/{total} quarters)  |  Avg Surprise: {+/-}%
  Next Quarter EPS Estimate: ${estimate}

⚠️ KEY RISKS
  1. {Risk 1}
  2. {Risk 2}
  3. {Risk 3}

🎯 INVESTMENT VERDICT
  Rating:         {STRONG BUY / BUY / HOLD / AVOID / SELL}
  12M Target:     ${target}  (Base: ${base} | Bull: ${bull} | Bear: ${bear})
  Confidence:     {HIGH / MEDIUM / LOW}
  Horizon:        {investment horizon}

  Thesis Summary: {2–3 sentence bull case}
  Key Risks:      {1–2 sentence risk summary}
═══════════════════════════════════════════════════
```

---

## Formatting Rules

- Always show data source (`source` field from API response) in a footnote.
- If an API call fails, note "Data unavailable" for that section — do not omit
  the section header.
- Round monetary values to 2 decimal places; percentages to 1 decimal place.
- Do not provide financial advice. Frame all outputs as analytical research.

---

## Limitations

- Financial statements may lag by 1 quarter (SEC filing cadence).
- Analyst targets represent consensus forecasts, not guarantees.
- This skill does not execute trades or interact with brokerage accounts.
