---
name: ta-signal-engine
description: Generate technical-analysis trade setups from OHLCV CSV using SMA/EMA/RSI/MACD/ATR with clear entry, stop, target, and position size.
---

# TA Signal Engine

Use this skill when the user wants technical-analysis based entry/exit signals and risk-defined trade setup proposals.

## Inputs

- OHLCV CSV with headers including: `date, open, high, low, close` (case-insensitive)
- Strategy mode: `trend`, `mean-reversion`, or `breakout`

## Run

```bash
python3 scripts/ta_signal_engine.py \
  --csv /abs/path/prices.csv \
  --symbol BTCUSDT \
  --strategy trend \
  --account-size 100000 \
  --risk-per-trade 0.01 \
  --json
```

## Workflow

1. Run the script and inspect `signal` and `confidence`.
2. If `signal=flat`, explain why (no edge from current indicators).
3. If signal is active, use generated `entry/stop/target/size` as the candidate plan.
4. Do not claim certainty; frame it as probabilistic setup.

## Notes

- This skill only produces analysis and paper-trade plans.
- For historical evaluation, use `ta-backtest` skill.
- For ledger/order lifecycle, use `ta-paper-executor` skill.
