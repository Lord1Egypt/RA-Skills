# Binance Event Contract Risk Manager

## 1. Scenario Definition
- **Trigger Timing**: Active continuously; validates every signal before execution; also supports manual trigger via `/binance-risk-check`; 24/7
- **Core Intent**: Provide comprehensive risk control for all signal executions; calculate position size, exposure, daily loss limit, and emergency circuit breaker; ensure no single trade risks more than 2% of capital
- **Context**: Applies to BTCUSDT & ETHUSDT Event Contracts; enforces Binance Event Contract rules (5-250 USDT per trade, daily loss limits); monitors account exposure across all open positions

## 2. Goal Setting
- Max position size: 5% of total capital per signal
- Max risk per trade: 2% of total capital (stop loss distance × position)
- Max daily loss: 10% of total capital (circuit breaker trigger)
- Max total exposure: 20% of capital across all concurrent positions
- Leverage check: Binance Event Contract leverage display only (no actual leverage used)

## 3. Execution Rules

### 3.1 Position Size Calculation
```
Risk Amount = Capital × 2%
Position Size = Risk Amount ÷ (Entry Price - Stop Loss)
Max Position (USD) = Min(Capital × 5%, 250 USDT) ← Binance per-trade limit
Final Position = Min(Risk-based Size, Max Position)
```

### 3.2 Daily Loss Limit Rules
- Track cumulative P&L each UTC day
- Daily Loss ≥ 5% → Warning alert (reduce position by 50%)
- Daily Loss ≥ 10% → Circuit breaker (stop new signals until next UTC day)
- Recovery: Only reset after new UTC day starts

### 3.3 Exposure Management
- Max concurrent open positions: 4 (2 per pair)
- If 4 active → reject new signals until one closes
- Exposure = Σ(all open position notional values) ≤ 20% of capital

### 3.4 Binance Contract Rule Enforcement
- Verify trade size: Min 5 USDT, Max 250 USDT per trade
- Reject any signal with position size outside 5-250 USDT
- Monitor contract cycle: warn if signal within 5min of expiry

### 3.5 Emergency Circuit Breaker
Trigger circuit breaker if ANY of:
- Daily loss ≥ 10%
- 3 consecutive losses in same cycle
- API data failure > 3 times
- Price slippage > 1% from entry (reject execution)

## 4. Example Output

### ✅ Positive Example (Risk Approved)
```
【 Risk Check PASSED | BTCUSDT Long | 12:10 UTC 】
Capital: 1,000 USDT
Risk Amount (2%): 20 USDT
Position Size: 0.023 BTC (≈157 USDT) ← within 5-250 USDT ✓
Max Exposure: 200 USDT (20% of capital) ← OK ✓
Stop Loss Distance: 0.5%
Risk/Reward: 1:2.4
Daily P&L: -2.3% ← No warning ✓
Concurrent Positions: 2/4 ← OK ✓
✅ Execution approved
```

### ❌ Negative Example (Risk Rejected)
```
【 Risk Check FAILED | ETHUSDT Short | 12:10 UTC 】
Reason: Daily loss 11.2% exceeded circuit breaker threshold
Action: ALL new signals suspended until 00:00 UTC
Recovery: Reduce position immediately or wait for reset
⚠️ CIRCUIT BREAKER TRIGGERED
```

## 5. Boundary Definition
- **FORBIDDEN**: Approve position size > 250 USDT (Binance hard limit)
- **FORBIDDEN**: Approve trade if daily loss ≥ 10%
- **FORBIDDEN**: Allow more than 4 concurrent positions
- **FORBIDDEN**: Approve trades 5 minutes before contract expiry
- **Exception**: If circuit breaker triggered → suspend all execution, alert immediately

## Installation
```bash
npx clawhub@latest install binance-event-contract-risk-manager --dir /workspace/skills
```

## Trigger Command
`/binance-risk-check`
