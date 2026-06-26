---
name: Macro Regime Detector
version: 1.0.2
description: "Classify the current macroeconomic regime across six states using GDP, CPI, Fed Funds rate, yield curve, and credit spread data from the Finskills API."
author: finskills
metadata:
  openclaw:
    requires:
      env:
        - FINSKILLS_API_KEY
    primaryEnv: FINSKILLS_API_KEY
  homepage: https://github.com/finskills/macro-regime-detector
---

# Macro Regime Detector

Identify the current US macroeconomic regime by synthesizing real-time treasury
yields, GDP growth, inflation, interest rates, and commodity price signals from
the Finskills API. Output a regime classification with an evidence-based rationale
and asset allocation implications.

---

## Setup

**API Key required** — [Register at https://finskills.net](https://finskills.net) to get your free key.  
Header: `X-API-Key: <your_api_key>`
> **Get your API key**: Register at **https://finskills.net** — free tier available, Pro plan unlocks real-time quotes, history, and financials.

---

## When to Activate This Skill

Activate when the user:
- Asks "what macro regime are we in?"
- Asks how the current macro environment affects their portfolio or sector
- Wants to understand Fed policy implications, yield curve shape, or inflation trend
- Asks for an asset allocation view based on macro conditions
- Mentions recession risk, stagflation, reflation, or rate cycle questions

---

## Macro Regime Framework

This skill classifies the US economy into one of six regimes:

| Regime | GDP Growth | Inflation | Rate Direction | Risk Assets |
|--------|-----------|-----------|---------------|-------------|
| **Goldilocks** | Expanding | Moderate (2–3%) | Stable/Falling | Risk-On ✅ |
| **Reflation** | Expanding | Rising (3–5%) | Rising | Cyclicals ✅ |
| **Overheating** | Strong | High (>5%) | Rising fast | Commodities ✅ |
| **Stagflation** | Slowing | High (>4%) | Elevated | Hard Assets ✅ |
| **Slowdown** | Decelerating | Falling | Stable | Defensives ✅ |
| **Recession** | Contracting | Low/Deflating | Falling | Cash/Bonds ✅ |

---

## Data Retrieval — Finskills API Calls

Make the following calls (all free-tier endpoints):

### 1. US Treasury Rates (Yield Curve)
```
GET https://finskills.net/v1/free/macro/treasury-rates
```
Extract: `3m`, `6m`, `1y`, `2y`, `5y`, `10y`, `30y` yields  
Compute: 2y10y spread (primary inversion signal), 3m10y spread (recession predictor)

### 2. GDP Growth
```
GET https://finskills.net/v1/free/macro/gdp/US
```
Extract: latest GDP growth rate (QoQ annualized), trend direction (3-quarter comparison)

### 3. Inflation
```
GET https://finskills.net/v1/macro/inflation
```
Extract: CPI YoY, core CPI YoY, PCE YoY, trend (accelerating/stable/decelerating)

### 4. Interest Rates (Fed Policy)
```
GET https://finskills.net/v1/macro/interest-rates
```
Extract: Federal Funds Rate (current), last 6 rate decisions, trend (hiking/cutting/pausing)

### 5. Key Economic Indicators (FRED via free endpoint)
```
GET https://finskills.net/v1/free/macro/indicator/UNRATE
```
Extract: US unemployment rate (latest, 3-month trend)

```
GET https://finskills.net/v1/free/macro/indicator/INDPRO
```
Extract: Industrial Production Index (latest YoY%)

### 6. Commodity Price Signals
```
GET https://finskills.net/v1/free/commodity/prices
```
Extract: Gold (safe haven demand), WTI Crude (inflation/demand signal), Copper (growth proxy)

---

## Analysis Workflow

### Step 1 — Yield Curve Classification

Using treasury rates data:

| Signal | Threshold | Interpretation |
|--------|-----------|----------------|
| 2y10y spread | > +50 bps | Normal — growth expected |
| 2y10y spread | -25 to +50 bps | Flat — transition phase |
| 2y10y spread | < -25 bps | Inverted ⚠️ — recession risk elevated |
| 3m10y spread | < 0 bps | Classic recession predictor (12–18 month lead) |

Note the steepening/flattening trend direction (compare to 3 months ago if data allows).

### Step 2 — Growth Assessment

| GDP Signal | Label |
|-----------|-------|
| > 3% annualized | Strong expansion |
| 1–3% annualized | Moderate expansion |
| 0–1% annualized | Stagnation |
| < 0% (1 quarter) | Contraction risk |
| < 0% (2 quarters) | Technical recession |

Cross-check with: Industrial Production YoY, Unemployment trend.

### Step 3 — Inflation Regime

| CPI YoY | PCE YoY | Label |
|---------|---------|-------|
| < 2% | < 2% | Deflationary/below-target |
| 2–3% | 2–2.5% | Target range (Goldilocks) |
| 3–5% | 2.5–4% | Above-target, manageable |
| > 5% | > 4% | High inflation |

Classify trend: **Rising** / **Stable** / **Falling** (compare last 3 readings).

### Step 4 — Fed Policy Stance

| Rate Trend | Description |
|-----------|-------------|
| 3+ consecutive hikes | Tightening cycle |
| Hold after hikes | Pause (peak rates) |
| First cut after hikes | Pivot (easing begins) |
| 3+ consecutive cuts | Easing cycle |
| Hold at low rates | Accommodative |

### Step 5 — Commodity Cross-Check

- **Gold rising + stocks flat or falling**: Flight to safety, risk-off signal
- **Oil rising + copper rising**: Demand-driven inflation, growth-positive
- **Oil rising + copper falling**: Supply shock, stagflation signal
- **Gold + bonds both rising**: Deflation/recession fear

### Step 6 — Regime Classification

Score each indicator and use this decision matrix:

```
IF GDP_expanding AND inflation_2-4% AND rates_stable: → GOLDILOCKS
IF GDP_expanding AND inflation_rising AND rates_rising: → REFLATION/OVERHEATING
IF GDP_slowing AND inflation_high AND rates_elevated: → STAGFLATION
IF GDP_slowing AND inflation_falling AND rates_cutting: → SLOWDOWN
IF GDP_contracting AND yield_curve_inverted: → RECESSION
```

Assign confidence: HIGH (3+ signals aligned), MEDIUM (2 signals), LOW (mixed signals).

### Step 7 — Asset Allocation Implications

For each regime, output the relative preference for major asset classes:

| Asset Class | Goldilocks | Reflation | Stagflation | Slowdown | Recession |
|-------------|-----------|-----------|-------------|----------|-----------|
| US Equities | ✅ OW | ✅ OW | ❌ UW | ⚖️ N | ❌ UW |
| Growth Tech | ✅ OW | ⚖️ N | ❌ UW | ⚖️ N | ❌ UW |
| Energy/Materials | ⚖️ N | ✅ OW | ✅ OW | ❌ UW | ❌ UW |
| Defensives | ❌ UW | ❌ UW | ✅ OW | ✅ OW | ✅ OW |
| REITs | ✅ OW | ❌ UW | ❌ UW | ⚖️ N | ❌ UW |
| Long Bonds | ❌ UW | ❌ UW | ❌ UW | ✅ OW | ✅ OW |
| TIPS/I-Bonds | ⚖️ N | ✅ OW | ✅ OW | ❌ UW | ❌ UW |
| Gold | ❌ UW | ⚖️ N | ✅ OW | ✅ OW | ✅ OW |
| Cash | ❌ UW | ⚖️ N | ✅ OW | ✅ OW | ✅ OW |

OW = Overweight | N = Neutral | UW = Underweight

---

## Output Format

```
╔══════════════════════════════════════════════════╗
║       US MACRO REGIME REPORT  —  {DATE}         ║
╚══════════════════════════════════════════════════╝

🏛️ REGIME CLASSIFICATION: {REGIME NAME}
   Confidence: {HIGH / MEDIUM / LOW}
   Trend: {Deepening / Stable / Transitioning}

📊 MACRO DASHBOARD
  Treasury Yields:
    3M: {%}  |  2Y: {%}  |  5Y: {%}  |  10Y: {%}  |  30Y: {%}
    2Y–10Y Spread: {bps} ({normal/flat/inverted})
    3M–10Y Spread: {bps}

  Growth:
    GDP Growth:         {%} annualized ({direction})
    Industrial Prod:    {%} YoY
    Unemployment:       {%} ({trend})

  Inflation:
    CPI YoY:            {%}
    Core CPI YoY:       {%}
    PCE YoY:            {%}
    Trend:              {Rising / Stable / Falling}

  Fed Policy:
    Fed Funds Rate:     {%}
    Policy Stance:      {Tightening / Pause / Pivoting / Easing}
    Last Decision:      {hike/cut/hold} ({date})

  Commodity Signals:
    WTI Crude:  ${price} ({weekly change}%)
    Gold:       ${price} ({weekly change}%)
    Copper:     ${price} ({weekly change}%)
    Interpretation: {one-line signal}

🎯 ASSET ALLOCATION IMPLICATIONS
   Overweight:  {asset classes}
   Neutral:     {asset classes}
   Underweight: {asset classes}

📝 REGIME NARRATIVE
   {3–4 sentences describing the current macro environment, key risks,
    and what conditions would trigger a regime shift}

⚠️ WATCH — REGIME SHIFT TRIGGERS
   Bull shift if: {conditions}
   Bear shift if: {conditions}
```

---

## Limitations

- GDP data has a 30–60 day reporting lag (advance estimate vs. final).
- This is a macro framework for portfolio positioning, not a market timing tool.
- Commodity prices can be noisy on short timeframes; use weekly/monthly trends.
