---
name: Trading Plan Generator
version: 1.0.2
description: "Generate structured trade plans with entry, stop-loss, and take-profit levels based on technical and fundamental data from the Finskills API."
author: finskills
metadata:
  openclaw:
    requires:
      env:
        - FINSKILLS_API_KEY
    primaryEnv: FINSKILLS_API_KEY
  homepage: https://github.com/finskills/trading-plan-generator
---

# Trading Plan Generator

Transform a stock idea into a complete, structured trading plan with specific
entry triggers, position sizing, stop-loss levels, profit targets, timeline,
and thesis statement — powered by live data from the Finskills API.
Implements professional trading desk methodology for both swing trades (days to weeks)
and position trades (weeks to months).

---

## Setup

**API Key required** — [Register at https://finskills.net](https://finskills.net) to get your free key.  
Header: `X-API-Key: <your_api_key>`
> **Get your API key**: Register at **https://finskills.net** — free tier available, Pro plan unlocks real-time quotes, history, and financials.

---

## When to Activate This Skill

Activate when the user:
- Has a stock pick and wants a complete trade plan around it
- Asks "how should I size this position?"
- Says "I think AAPL is going to $200, help me plan this trade"
- Asks for entry, stop-loss, and target for a specific trade
- Wants to calculate position size based on account risk tolerance
- Uses terms like "trade plan", "entry point", "risk/reward", "stop loss", "price target"

---

## Information to Collect from the User

Before fetching data, confirm:

1. **Symbol**: Which stock/ETF?
2. **Thesis**: Why do they want this trade? (Earnings catalyst, technical breakout, macro tailwind, etc.)
3. **Direction**: Long or Short?
4. **Account Size**: Portfolio total value (for position sizing)
5. **Max Risk per Trade**: % of portfolio willing to lose on this trade (default: 1–2%)
6. **Time Horizon**: Swing trade (1–10 days), Position trade (1–3 months), or Investment (6+ months)?

---

## Data Retrieval — Finskills API Calls

### 1. Current Quote + Market Context
```
GET https://finskills.net/v1/stocks/quote/{SYMBOL}
```
Extract: `price`, `dayHigh`, `dayLow`, `open`, `previousClose`, `volume`, `avgVolume`, `marketCap`, `52WeekHigh`, `52WeekLow`, `peRatio`, `beta`

### 2. Historical Price Data (for ATR, support/resistance, trend)
```
GET https://finskills.net/v1/stocks/history/{SYMBOL}?period=6mo&interval=1d
```
Extract: last 6 months of daily OHLCV  
Compute: ATR (14), key swing highs/lows, 50-day SMA, 20-day SMA, 200-day SMA, RSI

### 3. Analyst Recommendations + Price Targets
```
GET https://finskills.net/v1/stocks/recommendations/{SYMBOL}
```
Extract:
- Consensus recommendation (Strong Buy / Buy / Hold / Underperform / Sell)
- Mean price target
- Highest/lowest price target
- Number of analysts

---

## Analysis Workflow

### Step 1 — Live Market Context Assessment

From the quote data, determine:
- Where is price relative to 52-week range? (Near high/low/mid-range)
- Is today's volume above or below average? (Volume confirmation check)
- Beta: How volatile is this stock relative to market?
- P/E: Is valuation extreme (which might cap upside for long trades)?

### Step 2 — Key Level Identification (from historical data)

Compute critical levels:

**ATR-based volatility:**
```
ATR_14 = EWM(True_Range, span=14)
Daily_Range_Estimate = 1.2 × ATR_14
```

**Support Levels** (from 6-month history):
- S1: Most recent swing low (last 20 sessions)
- S2: Prior swing low (last 60 sessions)
- S3: Major structure low (52-week low if within 20% of current price)

**Resistance Levels** (from 6-month history):
- R1: Most recent swing high or overhead consolidation zone
- R2: Prior swing high
- R3: 52-week high or prior major resistance

**Moving Averages** (dynamic support/resistance):
- SMA_20, SMA_50, SMA_200 — note if price is above or below each

### Step 3 — Entry Strategy

**For Long Trades:**
- **Breakout Entry**: Enter above R1 on above-avg volume (aggressive)
- **Pullback Entry**: Enter at S1 or SMA_20 with bounce confirmation (conservative)
- **Range Entry**: Enter at lower third of recent range when RSI < 40 (mean reversion)

**For Short Trades:**
- **Breakdown Entry**: Enter below S1 on above-avg volume
- **Bounce Entry**: Enter on rally to resistance (R1/SMA_20) with bearish conditions

Recommend an entry type and exact trigger price based on the user's thesis and time horizon.

**Entry Trigger:**
```
Entry = Buy {SYMBOL} at $X only if {volume confirmation condition AND price condition}
       or
Entry = Limit order at ${level} (pullback entry)
```

### Step 4 — Position Sizing (Risk-Based)

**Fixed Risk Position Sizing (Industry Standard):**

```
Dollar Risk Per Trade = Account_Size × Max_Risk_Pct
                      e.g., $100,000 × 2% = $2,000 max risk

Distance to Stop = Entry_Price - Stop_Loss_Price  (for longs)

Shares to Buy = Dollar_Risk_Per_Trade / Distance_to_Stop

Position Value = Shares × Entry_Price
Position % of Portfolio = Position_Value / Account_Size
```

Flag if position exceeds 20% of portfolio (concentration risk warning).

**Volatility-Adjusted Check:**
- If beta > 2.0: Reduce max risk % by 50% (high-beta stocks need smaller positions)
- If beta < 0.5: Position can be slightly larger if fundamentals are strong

### Step 5 — Stop-Loss Placement

**ATR-Based Stop (preferred):**
```
For Long: Stop_Loss = Entry_Price - (1.5 × ATR_14)
For Short: Stop_Loss = Entry_Price + (1.5 × ATR_14)
```

**Structure-Based Stop (alternative):**
- Long: Stop just below S1 (last swing low) with small buffer (~0.5%)
- Short: Stop just above R1 (last swing high) with small buffer

**Hard Rule**: Never place stop inside a natural support/resistance zone — price will "shake you out" before continuing.

Choose the wider of the two methods for stops (more conservative).

### Step 6 — Profit Targets

**Target 1 (partial exit — 50% of position):**
- Risk/Reward ratio ≥ 2:1 for swing trades
- Target_1 = Entry + (2 × Distance_to_Stop)  [for longs]

**Target 2 (remaining position — trail or hold):**
- Next major resistance level (R2) or analyst mean price target
- Minimum R:R 3:1

**Target 3 (maximum case):**
- Analyst high price target or key technical level

**Time Stop (important):**
- If trade has not reached T1 within the defined time horizon, exit regardless of P&L
- Swing trade time stop: 10 trading days
- Position trade time stop: 45 trading days

### Step 7 — Trade Thesis Validation

Write a formal 3-part thesis:
1. **Catalyst**: What is the specific reason this trade will work?
2. **Invalidation**: What would tell you the thesis is wrong? (beyond the price stop)
3. **Monitoring Points**: What news, data, or price action to watch during the trade?

---

## Output Format

```
╔══════════════════════════════════════════════════════════════════╗
║    TRADE PLAN  —  {DIRECTION} {TICKER}                          ║
║    Generated: {DATE}   |   Type: {Swing/Position/Investment}    ║
╚══════════════════════════════════════════════════════════════════╝

📌 TRADE THESIS
  "I believe {TICKER} will {rise/fall} because {1-sentence catalyst}.
   The trade is invalidated if {invalidation condition}."

  Tag: {Breakout / Reversal / Catalyst / Macro-Driven / Technical}

📊 MARKET SNAPSHOT  —  {TICKER}
  Price:         ${price}   Day Range: ${low} – ${high}
  52-Week:       ${52wkLow} – ${52wkHigh}   Position: {Top/Mid/Bottom} third of range
  Beta:          {X.X}   P/E: {X.X}x   Avg Volume: {Xm} shares/day
  Today's Vol:   {Xm} shares ({+/-}% vs. average)

  Analyst Consensus: {Strong Buy / Buy / Hold}   Target: ${mean}  Range: ${low}–${high}

🎯 KEY LEVELS
  Resistance 3:  ${R3}  [{structure / 52wk-high}]
  Resistance 2:  ${R2}  [{structure}]
  ► Resistance 1:${R1}  [{recent swing high}]     ← Nearest overhead
  ─── CURRENT:   ${price} ───
  ► Support 1:   ${S1}  [{recent swing low}]      ← Stop zone
  Support 2:     ${S2}  [{prior swing low}]
  Support 3:     ${S3}  [{major level}]

  20-Day SMA:    ${SMA20}   50-Day SMA: ${SMA50}   200-Day SMA: ${SMA200}
  ATR (14):      ${ATR}  ({X.X}% of price)

📋 TRADE PARAMETERS

  ┌─────────────────────────────────────────────────────┐
  │  ENTRY TYPE:   {Breakout above} / {Pullback to} ${entry_price}
  │  Entry Trigger: Price ${entry_trigger} on volume > {X}M shares
  │                  OR limit order at ${limit_price}      │
  │                                                         │
  │  STOP-LOSS:    ${stop_price}  ({ATR-based / Structure})  │
  │  Distance:     ${entry - stop}  ({X.X}% below entry)   │
  │                                                         │
  │  TARGET 1:     ${t1}  ({2.1:1} R:R)  ← Exit 50%      │
  │  TARGET 2:     ${t2}  ({3.2:1} R:R)  ← Exit 35%      │
  │  TARGET 3:     ${t3}  ({4.5:1} R:R)  ← Trail 15%     │
  │                                                         │
  │  TIME STOP:    Exit by {date} if no progress           │
  └─────────────────────────────────────────────────────┘

💰 POSITION SIZING  (Account: ${account_size})
  Max Risk:             ${risk_amount}  ({risk_pct}% of portfolio)
  Stop Distance:        ${stop_distance}/share  ({stop_pct}%)
  Shares to Buy:        {shares_count} shares
  Position Value:       ${position_value}  ({position_pct}% of portfolio)
  Beta-Adjusted Risk:   ${adjusted_risk}

  ⚠️ {Any concentration or volatility warnings}

📅 TRADE MANAGEMENT RULES
  On entry day:     Confirm volume and price action before committing
  At -50% to stop:  Evaluate — add context, consider waiting for new catalyst
  At Target 1:      Sell 50%, move stop to break-even
  At Target 2:      Sell 35%, trail stop at 2× ATR
  At Target 3:      Sell remaining 15%
  Time Stop:        Exit FULL position on {date}, regardless of P&L

📌 MONITORING CHECKLIST
  □ {Key upcoming earnings date if applicable}
  □ {Key macro data that could impact trade}
  □ {Sector ETF behavior as leading indicator}
  □ {Price/Volume action to watch for confirmation or invalidation}
```

---

## Limitations

- Price targets are based on technical structure and analyst consensus — not guaranteed.
- Stop-loss placement does not eliminate the risk of gap-down opens in fast markets.
- ATR-based position sizing assuming normal market conditions; extreme volatility events can bypass stops.
- This plan is for educational purposes; complete research and use your own judgment before trading.
