---
name: ta-paper-executor
description: Execute and track paper trades from TA setups with JSONL ledger, open/close workflow, and mark-to-market status.
---

# TA Paper Executor

Use this skill when the user wants simulated execution (paper trading), not broker-connected live orders.

## Run

Place order:

```bash
python3 scripts/ta_paper_executor.py place \
  --symbol BTCUSDT --side long --entry 68000 \
  --stop 66500 --target 71000 --qty 0.5 \
  --strategy trend-follow --reason "SMA20>SMA50 + MACD"
```

Close order:

```bash
python3 scripts/ta_paper_executor.py close --id ORD-20260310-001 --exit 70500
```

Status:

```bash
python3 scripts/ta_paper_executor.py status --symbol BTCUSDT --mark 70200 --json
```

## Workflow

1. Receive setup from `ta-signal-engine`.
2. Validate historical viability via `ta-backtest`.
3. If accepted, place paper order and record rationale.
4. Update status with mark price, then close with explicit reason.
