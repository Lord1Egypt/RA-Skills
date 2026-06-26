---
name: Technical Analyst
version: 1.0.2
description: "Perform comprehensive technical analysis using 12+ indicators including RSI, MACD, Bollinger Bands, support/resistance, and chart patterns via the Finskills API."
author: finskills
metadata:
  openclaw:
    requires:
      env:
        - FINSKILLS_API_KEY
    primaryEnv: FINSKILLS_API_KEY
  homepage: https://github.com/finskills/technical-analyst
---

# Technical Analyst

Perform comprehensive technical analysis on any US-listed stock using historical
OHLCV data from the Finskills API. Computes trend indicators (SMA/EMA, MACD),
momentum oscillators (RSI, Stochastic), volatility bands (Bollinger Bands, ATR),
volume analysis, and pattern recognition — then synthesizes a structured trading
bias with support/resistance levels.

---

## Setup

**API Key required** — [Register at https://finskills.net](https://finskills.net) to get your free key.  
Header: `X-API-Key: <your_api_key>`
> **Get your API key**: Register at **https://finskills.net** — free tier available, Pro plan unlocks real-time quotes, history, and financials.

---

## When to Activate This Skill

Activate when the user:
- Asks for a technical analysis of a stock, index, or ETF
- Mentions RSI, MACD, moving averages, Bollinger Bands, or support/resistance
- Asks "where is the stock heading?" or "should I buy the dip?"
- Requests an entry point, stop-loss level, or price target based on technicals
- Asks about chart patterns (head & shoulders, cup & handle, breakout, etc.)
- Uses terms like "overbought", "oversold", "trend", "momentum reversal"

---

## Data Retrieval — Finskills API Calls

### 1. Historical OHLCV Data
```
GET https://finskills.net/v1/stocks/history/{SYMBOL}?period=1y&interval=1d
```
For weekly context (longer-term trend):
```
GET https://finskills.net/v1/stocks/history/{SYMBOL}?period=2y&interval=1wk
```
Extract: date, open, high, low, close, volume, adjustedClose

### 2. Market Breadth Context
```
GET https://finskills.net/v1/free/market/breadth
```
Extract: % stocks above 200MA, % stocks above 50MA (macro tailwind/headwind context)

---

## Indicator Calculations

Use the `adjustedClose` price series for all calculations.

### Trend Indicators

**Simple Moving Averages (SMA):**
```
SMA_20 = rolling_mean(close, 20)
SMA_50 = rolling_mean(close, 50)
SMA_200 = rolling_mean(close, 200)
```

**Exponential Moving Averages (EMA):**
```
EMA_12 = EW_mean(close, span=12)
EMA_26 = EW_mean(close, span=26)
```

**Trend Alignment (Bull): Price > SMA_20 > SMA_50 > SMA_200**
**Trend Alignment (Bear): Price < SMA_20 < SMA_50 < SMA_200**

**MACD:**
```
MACD_line = EMA_12 - EMA_26
Signal_line = EMA(MACD_line, span=9)
MACD_histogram = MACD_line - Signal_line
```
- MACD crossing above signal + histogram flipping to positive: Bullish momentum building
- MACD crossing below signal + histogram going negative: Bearish momentum

### Momentum Oscillators

**RSI (14-period):**
```
gain_t = max(close_t - close_{t-1}, 0)
loss_t = max(close_{t-1} - close_t, 0)
avg_gain_14 = rolling_mean(gain_t, 14)
avg_loss_14 = rolling_mean(loss_t, 14)
RS = avg_gain_14 / avg_loss_14
RSI = 100 - 100 / (1 + RS)
```
- RSI > 70: Overbought — watch for reversal or consolidation
- RSI < 30: Oversold — potential bounce setup
- RSI divergence vs. price: Strong reversal signal

**Stochastic Oscillator (slow %K/%D):**
```
%K = (close - lowest_low_14) / (highest_high_14 - lowest_low_14) × 100
%D = SMA(%K, 3)
```
- %K crosses above %D from below 20: Bullish
- %K crosses below %D from above 80: Bearish

### Volatility Indicators

**Bollinger Bands (20-period, 2 standard deviations):**
```
BB_middle = SMA_20
BB_upper = SMA_20 + 2 × STD(close, 20)
BB_lower = SMA_20 - 2 × STD(close, 20)
BB_width = (BB_upper - BB_lower) / BB_middle
```
- Price at/above upper band: Overextended
- Price at/below lower band: Oversold / potential bounce
- Bandwidth squeezing (< 0.10): Coiling for breakout

**Average True Range (ATR, 14-period):**
```
TR = max(high - low, |high - prev_close|, |low - prev_close|)
ATR_14 = rolling_mean(TR, 14)
```
Use ATR for stop-loss placement: Stop = entry - (1.5 × ATR) for longs

### Volume Analysis

**Volume Moving Average:**
```
Vol_SMA_20 = rolling_mean(volume, 20)
```

**Volume Confirmation:**
- Price up + volume > Vol_SMA_20: Strong bullish conviction
- Price up + volume < Vol_SMA_20: Weak rally, distribution risk
- Price down + volume > Vol_SMA_20: Distribution/capitulation

**On-Balance Volume (OBV):**
```
OBV_t = OBV_{t-1} + volume_t  if close_t > close_{t-1}
OBV_t = OBV_{t-1} - volume_t  if close_t < close_{t-1}
```
OBV rising while price flat/declining: Accumulation signal (bullish)
OBV falling while price flat/rising: Distribution signal (bearish)

---

## Support & Resistance Identification

Find key levels from recent price history:

1. **Swing Highs/Lows**: Price levels that acted as pivots (local max/min within 20-bar window)
2. **Round Number Levels**: Major psychological levels ($50, $100, $150 etc.)
3. **Prior Consolidation Zones**: Ranges where price traded sideways for > 5 sessions
4. **200-Day SMA**: Acts as major dynamic support/resistance for institutional investors
5. **52-Week High/Low**: Key psychological and technical levels

**Define 3 support levels (S1 < S2 < current price) and 3 resistance levels (current price < R1 < R2 < R3).**

---

## Pattern Recognition

Check for the following patterns in the most recent 60 bars:

**Bullish Patterns:**
- **Cup & Handle**: Smooth U-shaped base + small consolidation + breakout above handle high
- **Ascending Triangle**: Flat resistance + rising support → breakout target = base height
- **Double Bottom (W)**: Two equal lows + breakout above neckline
- **Bull Flag**: Sharp rally + tight consolidation → continuation target = flag pole height

**Bearish Patterns:**
- **Head & Shoulders**: Three peaks (higher center) + neckline break → target = head height below neckline
- **Descending Triangle**: Flat support + lower highs → breakdown target = base height
- **Double Top (M)**: Two equal highs + breakdown below neckline
- **Bear Flag**: Sharp decline + tight bounce → continuation target = flag pole height down

---

## Analysis Workflow

### Step 1 — Multi-Timeframe Trend Assessment
1. Fetch daily (1Y) and weekly (2Y) data
2. Determine primary trend from weekly chart (SMA_20, SMA_50 slope)
3. Determine intermediate trend from daily chart (SMA_20, SMA_50)
4. Flag agreement or conflict between timeframes

### Step 2 — Indicator Synthesis
Compute all 12 indicators; create a signal table:

| Indicator | Value | Signal | Weight |
|-----------|-------|--------|--------|
| SMA_20 vs. Price | Above/Below | Bull/Bear | 3 |
| SMA_50 vs. Price | Above/Below | Bull/Bear | 3 |
| SMA_200 vs. Price | Above/Below | Bull/Bear | 4 |
| Golden/Death Cross | State | Bull/Bear/Neutral | 4 |
| RSI (14) | X.X | OB/OS/Neutral | 3 |
| MACD vs. Signal | Cross state | Bull/Bear/Neutral | 3 |
| Bollinger Position | Upper/Mid/Lower | OB/OS/Neutral | 2 |
| Volume Trend | Above/Below avg | Strong/Weak | 2 |
| OBV trend | Rising/Falling | Accum/Distrib | 2 |

Compute bullish signal count vs. bearish signal count (weighted).

### Step 3 — Support/Resistance Map
Identify and rank 3 support and 3 resistance levels.

### Step 4 — Pattern Identification
Check for active patterns in the 60-bar lookback window.

### Step 5 — Trade Setup Parameters
- **Bias**: Bullish / Neutral / Bearish
- **Entry Zone**: Price range for optimal entry
- **Stop-Loss**: 1.5× ATR below entry (for longs) or above resistance (for shorts)
- **Target 1**: First resistance level
- **Target 2**: Second resistance level (extended target)
- **Risk/Reward**: (Target1 - Entry) / (Entry - Stop)

---

## Output Format

```
╔══════════════════════════════════════════════════════════════╗
║    TECHNICAL ANALYSIS  —  {TICKER}   ({DATE})               ║
║    Current Price: ${price}  |  52-week: ${low} – ${high}    ║
╚══════════════════════════════════════════════════════════════╝

📈 TREND STRUCTURE
  Weekly Trend:    {Uptrend / Downtrend / Sideways}  (SMA alignment: {Bull/Bear/Mixed})
  Daily Trend:     {Uptrend / Downtrend / Sideways}
  Trend Alignment: {Aligned / Conflicted}
  
  Key MAs:
    SMA 20:   ${val}    Price is {above/below}  +{%} from SMA20
    SMA 50:   ${val}    Price is {above/below}  +{%} from SMA50
    SMA 200:  ${val}    Price is {above/below}  +{%} from SMA200
  
  Golden/Death Cross Status: {Golden cross on {date} / Death cross on {date} / Neither}

📊 MOMENTUM & OSCILLATORS
  RSI (14):         {val}  →  {Overbought / Neutral / Oversold}
  MACD:             {val}  Signal: {val}  Hist: {val}  →  {Bullish/Bearish}
  Stochastic %K/%D: {val}/{val}  →  {Cross direction / level}

📉 VOLATILITY & VOLUME
  Bollinger位置:    {Upper / Middle / Lower} band region  (Width: {val})
  ATR (14):         ${val}  ({X}% of price — {Low/Medium/High} volatility)
  Volume vs. 20MA:  {+/-X}%  →  {Above-average / Below-average}
  OBV Trend:        {Rising / Falling / Flat}  →  {Accumulation / Distribution}

🎯 SUPPORT & RESISTANCE MAP
  Resistance 3:  ${R3}  [{Level type}]
  Resistance 2:  ${R2}  [{Level type}]
  Resistance 1:  ${R1}  [{Level type}]   ← Nearest overhead
  ► CURRENT PRICE:  ${price}  ◄
  Support 1:     ${S1}  [{Level type}]   ← Nearest floor
  Support 2:     ${S2}  [{Level type}]
  Support 3:     ${S3}  [{Level type}]

🔍 PATTERN DETECTED: {Pattern name or "No clear pattern"}
  {Pattern description and implication, 1-2 sentences}
  Breakout/Breakdown trigger: ${level}
  Pattern target:             ${target}

📊 SIGNAL SCORECARD
  Bullish signals: {N}/9  |  Bearish signals: {N}/9  |  Neutral: {N}/9
  Weighted tally: Bullish {X}/26  vs.  Bearish {X}/26

🎯 TRADE SETUP
  Bias:         {BULLISH / NEUTRAL / BEARISH}
  Entry Zone:   ${low} – ${high}
  Stop-Loss:    ${level}  ({ATR}-based, {%} below entry)
  Target 1:     ${t1}    ({R:R ratio} risk/reward)
  Target 2:     ${t2}    ({R:R ratio} risk/reward)
  Time Horizon: {Days/weeks based on setup type}

  Recommended Action: {Buy above ${X} with stop at ${Y} / Wait for pullback to ${S1} / Avoid until trend clarifies}

📊 MARKET BREADTH CONTEXT
  % of S&P 500 stocks above 200MA: {%}
  Macro tailwind/headwind: {Tailwind — broad market healthy / Headwind — take smaller position}
```

---

## Limitations

- Technical analysis describes probability, not certainty; no setup has > 65% win rate historically.
- All indicators are lagging by construction — they confirm existing moves, not predict new ones.
- Patterns are identified algorithmically — manual chart reading by an expert may interpret differently.
- Volume signals may be distorted by options expiration or index rebalancing days.
