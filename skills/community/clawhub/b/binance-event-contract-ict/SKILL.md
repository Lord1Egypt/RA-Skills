# Binance ICT Structure Recognizer

## 1. Scenario Definition
- **Trigger Timing**: Auto-trigger when SSS tier signal is calculated; also supports manual trigger via `/binance-ict-recognize`; runs after each 10min/30min/1h K-line closed; 24/7
- **Core Intent**: Provide ICT structure verification for SSS tier highest win rate signal; identify Order Blocks, FVG (Fair Value Gap), liquidity sweep zones of Binance BTC/ETH corresponding cycles; improve SSS tier signal win rate
- **Context**: Only for SSS tier signal of Binance Event Contract 1h cycle; only uses Binance official K-line data; adapts to price fluctuation characteristics of short-term event contracts

## 2. Goal Setting
Accurately identify ICT core structure of corresponding cycle; provide 100% accurate structure verification for SSS tier signal; filter false signals without ICT structure support; ensure SSS tier signal win rate stable above 95%.

## 3. Execution Rules

### 3.1 Data Dependency
- **MUST** only use Binance official BTC/ETH K-line data from `binance-event-contract-data-fetcher` Skill
- **PROHIBITED**: Use any third-party indicator or data source

### 3.2 Core Recognition Dimensions

**Order Block Recognition:**
- Identify bullish/bearish valid Order Blocks of corresponding cycle
- Confirm signal trigger after price backtest Order Block
- Tag: Bullish OB (last candle red before bullish candle) | Bearish OB (last candle green before bearish candle)

**FVG Recognition:**
- Identify Fair Value Gaps (3-candle pattern)
- Bullish FVG: gap between high of candle 1 and low of candle 3
- Bearish FVG: gap between low of candle 1 and high of candle 3
- Calculate FVG fill probability

**Liquidity Sweep Zone:**
- Identify stop hunt zones above/below key structure
- Detect liquidity sweeps at highs/lows of previous cycle
- Calculate sweep-to-reversal zones

**Inducement Identification:**
- Identify fake breakouts at key levels
- Detect liquidity grabs at chart patterns

### 3.3 ICT Signal Scoring
- Score each ICT element: OB (0-40pts), FVG (0-30pts), Liquidity Sweep (0-20pts), Inducement (0-10pts)
- Total Score ≥ 80 = SSS Strong Confirm | 60-79 = SS Confirm | < 60 = No Trade

### 3.4 Running Rule
- Trigger automatically when SSS signal detected from signal calculator
- Run after each 10min/30min/1h K-line close
- Output structured ICT report to risk manager

## 4. Example Output

### ✅ Positive Example
```
【 ICT Structure Recognition | BTCUSDT 1H | 2026-03-18 12:10 】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Order Blocks:
  → Bullish OB: Zone 67850-67920 (Price returned, VALID)
  → Bearish OB: Zone 68500-68580 (Not touched, PENDING)

FVG Detection:
  → Bullish FVG: 67980-68100 (Unfilled, HIGH PROBABILITY)
  → Bearish FVG: 68320-68400 (Partially filled, CAUTION)

Liquidity Sweep:
  → Low liquidity sweep at 68150 (逆向吃到流动性)
  → High sweep at 68600 (Inducement detected)

ICT Score: 88/100 → SSS STRONG CONFIRM ✓
Recommendation: Long Entry at OB retest 67850 | Target 68500 | SL 67500
```

### ❌ Negative Example
- Recognize ICT patterns using non-Binance data
- Issue trade signal without full ICT scan
- Ignore timeframe confluence (multi-timeframe analysis)

## 5. Boundary Definition
- **FORBIDDEN**: Issue trading signals directly — only output ICT structure analysis
- **FORBIDDEN**: Use timeframe below 10min for SSS tier signals
- **Exception**: If K-line data missing → output "Data Unavailable" and wait for next close

## Installation
```bash
npx clawhub@latest install binance-event-contract-ict-recognizer --dir /workspace/skills
```

## Trigger Command
`/binance-ict-recognize`
