# Binance Event Contract Signal Calculator

## 1. Scenario Definition
- **Trigger Timing**: Auto-trigger every minute when new K-line data is available; also supports manual trigger via `/binance-signal-calculate`; 24/7 minute-level
- **Core Intent**: Calculate 3-tier resonance signals (SSS/SS/S) for Binance Event Contract cycles using full data from fetcher and ICT recognizer; output precise Long Entry / Short Entry zones with entry price, target, and stop loss
- **Context**: Works on BTCUSDT & ETHUSDT only; 10min/30min/1h Event Contract cycles; combines market data + liquidity + ICT structure for multi-factor resonance

## 2. Goal Setting
Generate 3-tier resonance signals with ≥90% win rate for SSS tier, ≥75% for SS tier; each signal includes: direction, entry zone, exact entry price, target price, stop loss, confidence score, cycle type, and position size recommendation.

## 3. Execution Rules

### 3.1 Signal Tier Classification

**SSS Tier (Win Rate ≥ 95%):**
- All 3 timeframes aligned (10min + 30min + 1hICT structure confirmed)
- Liquidity qualified (bid/ask ≥ 500,000 USDT both sides)
- ICT Score ≥ 80/100
- Volume confirmation (volume > 1.5x 20-period average)
- 3+ confluence factors present

**SS Tier (Win Rate ≥ 80%):**
- 2 timeframes aligned
- Liquidity qualified on at least one side
- ICT Score 60-79/100
- 2 confluence factors present

**S Tier (Win Rate ≥ 65%):**
- 1 timeframe confirmed
- Basic ICT structure present
- 1+ confluence factor

### 3.2 Resonance Strategy Rules

**Multi-Timeframe Alignment:**
- 10min confirms direction + entry timing
- 30min confirms structure + target
- 1h confirms trend + stop loss placement

**Confluence Factors:**
1. ICT Order Block at key level
2. FVG not yet filled
3. Liquidity sweep + reversal
4. Index price at EMA 20/50/200 confluence
5. Volume spike at structure break
6. Contract cycle expiry timing (avoid expiry 5min before close)

### 3.3 Signal Output Format
```
【 SSS SIGNAL | BTCUSDT | 10min Event Contract | 12:10 UTC 】
Direction: Long Entry
Entry Zone: 67850-67920 USDT
Exact Entry: Wait for retest of 67880
Target 1: 68300 (+0.6%)
Target 2: 68500 (+0.9%)
Target 3: 68700 (+1.2%)
Stop Loss: 67500 (-0.5%)
Confidence: 96%
Confluence Factors: OB✓ FVG✓ Liquidity✓ Volume✓ ICT:88pts
Position Size: Max 5% of capital per signal
Risk/Reward: 1:2.4
Next Check: 12:15 UTC (5min close)
```

### 3.4 Data Input Dependency
- K-line data: from `binance-event-contract-data-fetcher`
- ICT structure: from `binance-ict-recognizer`
- Risk parameters: from `binance-event-contract-risk-manager`

## 4. Example Output

### ✅ Positive Example
```
【 SSS SIGNAL | ETHUSDT | 30min Event Contract | 12:00 UTC 】
Direction: Short Entry
Entry Zone: 3845-3850 USDT
Exact Entry: 3847 (breakdown confirmation)
Targets: 3820 / 3800 / 3780
Stop Loss: 3870
Confidence: 94%
Confluence: OB✓ FVG✓ Liquidity✓ ICT:82pts
Cycle: 30min expiry at 12:30 UTC
Risk/Reward: 1:2.8
```

### ❌ Negative Example
- Output signal with only 1 timeframe, no ICT confirm
- Ignore liquidity data
- Issue signal without stop loss

## 5. Boundary Definition
- **FORBIDDEN**: Issue signal if liquidity < 500,000 USDT on both sides
- **FORBIDDEN**: Issue signal if ICT score < 60 for SSS/SS tier
- **FORBIDDEN**: Issue signals 5 minutes before contract expiry
- **Fallback**: If data missing → output "Signal Pending" and wait

## Installation
```bash
npx clawhub@latest install binance-event-contract-signal-calculator --dir /workspace/skills
```

## Trigger Command
`/binance-signal-calculate`
