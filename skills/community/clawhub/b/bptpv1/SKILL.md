---
name: paper-trading-plan
description: Generates structured paper trading plans with entry, stop loss, take profit, position size, and failure conditions for SPX, indices, and US equity options.
metadata:
  openclaw:
    emoji: "📊"
    requires:
      bins:
        - python3
    always: false
---

# Paper Trading Plan Generator

Generates comprehensive, structured paper trading plans for SPX, index options, and US equities. Perfect for pre-market planning and session prep.

## Usage

```bash
python3 plan.py --ticker SPX --direction long --entry 5200 --stop 5150 --target 5300
```

## Input Parameters

| Flag | Description | Example |
|------|-------------|---------|
| `--ticker` | Underlying symbol | SPX, AAPL, QQQ |
| `--direction` | long or short | long |
| `--entry` | Entry price | 5200 |
| `--stop` | Stop loss price | 5150 |
| `--target` | Take profit price | 5300 |
| `--price` | Current price (optional) | 5225 |
| `--option-type` | call or put (optional) | call |
| `--expiry` | Option expiry (optional) | 2026-04-18 |

## Output Structure

```
=== PAPER TRADING PLAN ===
Symbol:     SPX
Direction:  LONG
Entry:      5200
Stop Loss:   5150 (-1.0%)
Take Profit: 5300 (+1.9%)
Risk/Reward: 1:2

Position Size:
- Max 2% account at risk
- Example: $10k account = $200 at risk
- Per-share risk: $50
- Shares: 40

Expiration: 2026-04-18
Type: CALL
Strike: 5200
Max Loss:  $200 (if expired worthless)
Max Profit: $400 (if target hit)

Failure Conditions:
- SPX breaks below 5150 → Exit immediately
- VIX > 30 → Reduce size by 50%
- News event overrides technical → Re-evaluate

Execution Checklist:
[ ] Confirm entry above key level
[ ] Check VIX < 20
[ ] Verify no major news during market hours
[ ] Set stop loss immediately after entry
[ ] Log trade in journal
