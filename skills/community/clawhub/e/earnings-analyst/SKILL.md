---
name: Earnings Analyst
version: 1.0.2
description: "Research upcoming earnings events, analyze historical beat/miss patterns, and estimate post-earnings price reactions using the Finskills API."
author: finskills
metadata:
  openclaw:
    requires:
      env:
        - FINSKILLS_API_KEY
    primaryEnv: FINSKILLS_API_KEY
  homepage: https://github.com/finskills/earnings-analyst
---

# Earnings Analyst

Track upcoming earnings events, analyze EPS beat/miss history, assess options-
implied earnings move expectations, and monitor analyst estimate revisions — all
powered by the Finskills API earnings calendar and company earnings endpoints.

---

## Setup

**API Key required** — [Register at https://finskills.net](https://finskills.net) to get your free key.  
Header: `X-API-Key: <your_api_key>`
> **Get your API key**: Register at **https://finskills.net** — free tier available, Pro plan unlocks real-time quotes, history, and financials.

---

## When to Activate This Skill

Activate when the user:
- Asks when a specific company reports earnings
- Wants to know historical earnings beat/miss rate for a stock
- Asks about analyst EPS/revenue estimates for an upcoming quarter
- Wants to understand the "earnings move" priced into options
- Asks which major companies are reporting this week
- Wants pre-earnings research before a binary event

---

## Use Cases

### Mode A — Market Earnings Calendar
"What major companies are reporting earnings this week?"

### Mode B — Per-Stock Earnings Deep Dive
"Analyze NVDA's upcoming earnings — what should I expect?"

### Mode C — Pre-Earnings Trade Setup
"Set up a pre-earnings analysis for AAPL with options context"

---

## Data Retrieval — Finskills API Calls

### Mode A — Earnings Calendar

```
GET https://finskills.net/v1/free/market/earnings-calendar
```
(Optional query params: `from=YYYY-MM-DD&to=YYYY-MM-DD`)  
Extract: company name, ticker, report date, timing (before market / after market), EPS estimate

Filter and group by day. Sort by market cap or analyst attention.

### Mode B — Per-Stock Earnings Analysis

**Earnings History & Next Quarter Estimate:**
```
GET https://finskills.net/v1/stocks/earnings/{SYMBOL}
```
Extract:
- Last 4–8 quarters: `date`, `epsActual`, `epsEstimate`, `epsSurprise`, `epsSurprisePercent`
- Last 4–8 quarters: `revenueActual`, `revenueEstimate`, `revenueSurprise`
- Next quarter: `epsEstimate`, `revenueEstimate`
- Next report date, timing (AMC/BMO)

**Analyst Estimates (revision trend):**
```
GET https://finskills.net/v1/free/stocks/estimates/{SYMBOL}
```
Extract: current quarter EPS estimate, next quarter, current year, next year consensus  
Note upward vs. downward revision trend (compare to 30-day-ago estimates if available)

**Latest News (pre-earnings catalyst check):**
```
GET https://finskills.net/v1/news/by-symbol/{SYMBOL}
```
Extract: recent headlines, sentiment signals, any pre-announcements or guidance updates

**Options Chain (for implied move):**
```
GET https://finskills.net/v1/stocks/options/{SYMBOL}
```
Extract near-term ATM straddle price to calculate implied earnings move.

---

## Analysis Workflow

### Step 1 — Earnings Calendar View (Mode A)

Group events by day (Mon–Fri this week):
- Show pre-market (BMO) and after-close (AMC) separately
- Flag mega-caps (market cap > $100B) with ★
- Include consensus EPS estimate for context
- Highlight sector clusters (earnings tend to move entire sectors)

### Step 2 — Earnings History Analysis (Mode B)

Build a beat/miss scorecard:

| Quarter | EPS Est | EPS Actual | Surprise | Rev Est | Rev Actual | Rev Surprise |
|---------|---------|-----------|----------|---------|-----------|--------------|
| Q1 2025 | $X.XX | $X.XX | +X% | $XB | $XB | +X% |
| ... | | | | | | |

Compute:
- **EPS Beat Rate**: % of quarters beating EPS estimate
- **Avg EPS Surprise**: Mean % beat magnitude (positive = bullish quality)
- **Revenue Beat Rate**: % of quarters beating revenue estimate
- **Consistency Score**: 5/5 beats vs 3/5 vs 2/5 — flag inconsistency
- **Trend**: Is beat magnitude growing or shrinking? (quality signal)

### Step 3 — Estimate Revision Momentum

Classify revision trend:
- **Positive momentum**: Estimates revised UP in last 30–90 days → analyst conviction rising
- **Negative momentum**: Estimates revised DOWN → potential guidance cut risk
- **Stable**: No significant revisions

This is a leading indicator — stocks with positive estimate revisions tend to outperform.

### Step 4 — Implied Earnings Move (if options data available)

Calculate using ATM straddle at nearest expiration AFTER earnings date:
```
ATM Straddle Price = ATM Call Mid + ATM Put Mid
Implied Move %     = Straddle Price / Current Stock Price × 100
Expected Range     = [Current Price × (1 − implied_move%), Current Price × (1 + implied_move%)]
```

Compare to **historical earnings moves** (from earnings history — abs value of price change on earnings day):
- If implied move > average historical move: options are pricing in extra uncertainty → consider neutral strategies
- If implied move < average historical move: options may be cheap for directional play

### Step 5 — Pre-Earnings Assessment

Summarize the opportunity:

**Bull Case** (if expecting beat):
- Revenue acceleration + margin expansion signals?
- Positive estimate revisions?
- Strong sector tailwinds?

**Bear Case** (if expecting miss or disappointment):
- Slowing beat magnitude trend?
- Recent negative estimate revisions?
- Macro headwinds for the sector?

**Key Watch Items**:
- Management guidance language (forward-looking statements)
- Segment breakdowns to watch (e.g., Cloud for MSFT, iPhone for AAPL)
- Margin trajectory (gross margin, operating margin vs estimates)

---

## Output Format — Mode A (Calendar)

```
📅 EARNINGS CALENDAR  —  Week of {DATE}

MONDAY {Date}
  ⭐ {CompanyName} ({TICKER}) — AMC  |  EPS Est: ${est}
  {CompanyName} ({TICKER}) — BMO    |  EPS Est: ${est}

TUESDAY {Date}
  ⭐ {CompanyName} ({TICKER}) — BMO  |  EPS Est: ${est}
  ...

[⚠️ Sector note: {sector} reports in concentration — expect spillover moves]
```

---

## Output Format — Mode B (Per-Stock Deep Dive)

```
╔══════════════════════════════════════════════════════╗
║    EARNINGS ANALYSIS — {TICKER}  ({DATE})           ║
╚══════════════════════════════════════════════════════╝

📅 NEXT EARNINGS
  Expected Date: {date}  |  Timing: {BMO/AMC}
  EPS Estimate:  ${eps}  |  Revenue Estimate: ${rev}B

📊 EARNINGS TRACK RECORD (Last {N} Quarters)
  EPS Beat Rate:     {%} ({n}/{total})
  Avg EPS Surprise:  +{%}
  Rev Beat Rate:     {%} ({n}/{total})
  Consistency:       {All beats / Mostly beats / Mixed}

  Quarter   EPS Est  Actual  EPS Surp  Rev Est   Actual   Rev Surp
  Q4 2024   $X.XX    $X.XX   +X.X%     $XB       $XB      +X.X%
  Q3 2024   ...

📈 ESTIMATE REVISION TREND
  Current FY EPS Estimate:  ${est}  ({+/-}% from 90 days ago)
  Revision Trend:           {Positive / Stable / Negative Momentum}
  Implications:             {one-line interpretation}

📐 IMPLIED EARNINGS MOVE (Options)
  ATM Straddle Price: ${price}  →  Implied Move: ±{%}
  Expected Range:     ${low} — ${high}
  Historical Avg Move: ±{%}
  Options Assessment: {Cheap/Rich/Fair relative to history}

📰 PRE-EARNINGS SIGNALS
  Recent News Sentiment: {Positive/Neutral/Negative}
  Key Headlines:
    • {headline 1}
    • {headline 2}

⚠️ KEY WATCH ITEMS FOR THIS EARNINGS
  1. {metric/segment to watch}
  2. {metric/segment to watch}
  3. {guidance language to watch}

🎯 EARNINGS SETUP SUMMARY
  Bull Case:  {2 sentences}
  Bear Case:  {2 sentences}
  Strategy:   {Directional bet / Neutral straddle / Avoid — with reasoning}
```

---

## Limitations

- Earnings dates can shift by 1–2 weeks; always verify directly with the company's IR page.
- Implied move is based on options chain snapshot; liquidity affects pricing accuracy.
- EPS surprise history may not account for non-GAAP vs. GAAP differences.
