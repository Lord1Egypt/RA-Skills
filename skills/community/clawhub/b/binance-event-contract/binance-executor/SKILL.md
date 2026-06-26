# Binance Event Contract Executor

## 1. Scenario Definition
- **Trigger Timing**: Executes ONLY when valid SSS/SS tier signal is confirmed AND risk check is passed; also supports manual trigger via `/binance-execute` with signal ID; 24/7 minute-level
- **Core Intent**: Logically record and track signal execution status; confirm exchange data alignment; output execution confirmation report with entry price, targets, and SL; do NOT execute actual orders (agent advisory mode)
- **Context**: Operates in advisory-only mode — outputs structured execution plan for human review; logs all signals for backtesting and performance tracking; tracks entry prices, targets, and P&L in real-time

## 2. Goal Setting
- 100% signal execution logging (zero missed signals)
- Execution confirmation within 10 seconds of signal generation
- Accurate tracking of entry price, targets, stop loss, and P&L
- Real-time signal status: PENDING → CONFIRMED → TARGET HIT / SL HIT → CLOSED
- Zero data inconsistency between signal output and execution log

## 3. Execution Rules

### 3.1 Pre-Execution Verification
Before confirming execution:
1. Verify signal is SSS or SS tier (reject S tier signals)
2. Verify risk check passed (check from risk manager output)
3. Verify liquidity still qualified (bid/ask ≥ 500,000 USDT)
4. Verify price not moved > 0.5% from signal entry zone
5. Verify not within 5 minutes of contract expiry

### 3.2 Execution Status Tracking
```
PENDING → (confirmation check) → CONFIRMED / REJECTED
CONFIRMED → (price hits target/sl) → TARGET HIT / SL HIT
TARGET HIT / SL HIT → (manual close) → CLOSED
```

### 3.3 Logged Data Per Execution
- Signal ID (timestamp-based, unique)
- Pair + Contract Cycle
- Signal Tier (SSS/SS)
- Entry Price (exact)
- Entry Time
- Stop Loss Price
- Target 1/2/3 Prices
- Position Size (USDT)
- Risk/Reward Ratio
- ICT Confluence Score
- Actual Exit Price (when closed)
- Actual P&L (USDT + %)
- Status: PENDING | CONFIRMED | TARGET HIT | SL HIT | CLOSED

### 3.4 Real-Time P&L Tracking
- Update P&L every minute based on current index price
- Alert if price enters within 0.3% of stop loss (warning)
- Alert if price hits target 1/2/3
- Log time spent in trade

### 3.5 Exchange Data Verification
- Compare executed entry with Binance Event Contract settlement price
- Flag if deviation > 0.1% (data inconsistency alert)
- Record actual trade execution price vs signal entry price

## 4. Example Output

### ✅ Positive Example (Execution Confirmed)
```
【 Execution Confirmed | ID: 202603181210_BTC_Long_SSS 】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Signal Tier: SSS ✓
Entry Price: 67880 USDT (BTCUSDT 10min)
Entry Time: 2026-03-18 12:10:00 UTC
Stop Loss: 67500 USDT (-0.56%)
Target 1: 68300 (+0.62%)
Target 2: 68500 (+0.91%)
Target 3: 68700 (+1.21%)
Position: 50 USDT
Risk/Reward: 1:2.4
ICT Score: 88/100
Status: CONFIRMED → MONITORING
Current P&L: +0.00% (at entry)
Next Update: 12:15 UTC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### ❌ Negative Example (Execution Rejected)
```
【 Execution Rejected | ID: 202603181210_ETH_Short_S 】
Reason: Signal tier S (below minimum SSS/SS threshold)
Action: Signal archived, no execution
Alternative: Wait for next SSS/SS signal
⚠️ NO TRADE LOGGED
```

## 5. Boundary Definition
- **FORBIDDEN**: Execute S tier signals (minimum requirement: SSS or SS)
- **FORBIDDEN**: Execute if risk manager returned FAILED
- **FORBIDDEN**: Execute if within 5 minutes of contract expiry
- **FORBIDDEN**: Execute if position size < 5 USDT or > 250 USDT
- **Exception**: If price moved > 0.5% from signal zone → reject, wait for next signal

## Installation
```bash
npx clawhub@latest install binance-event-contract-executor --dir /workspace/skills
```

## Trigger Command
`/binance-execute`
