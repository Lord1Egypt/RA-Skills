---
name: backtest-poller
description: Background daemon that monitors QuantConnect backtests with adaptive polling, real-time equity tracking, drawdown early-stop, auto-download, and auto-diagnosis — survives terminal disconnection.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - QC_USER_ID
        - QC_API_TOKEN
        - QC_PROJECT_ID
      bins:
        - python3
    primaryEnv: QC_API_TOKEN
    emoji: "\U0001F440"
    os:
      - macos
      - linux
---

# Backtest Poller

Never babysit a 3-hour backtest again. This skill runs a background daemon that monitors your QuantConnect backtests, auto-stops on excessive drawdown, downloads results when done, runs forensic diagnosis, and sends you a system notification.

## When to use

- After submitting a backtest: "Monitor this backtest in the background"
- "Start the poller daemon"
- "Check backtest status"
- "Show me the poller logs"

## Architecture

The poller runs as a `nohup` background process that survives terminal disconnection. All state is persisted to `state.json` with file-locking to prevent CLI/poller race conditions.

```
User submits backtest
        |
        v
  [Poller Daemon] (nohup, runs independently)
        |
        |-- Every 30-180s: check QC API
        |-- Track equity & peak equity
        |-- Calculate live drawdown
        |
        |-- If DD > threshold at 20%+ progress:
        |     |-- Delete backtest (early stop)
        |     |-- Record result
        |     \-- Send notification
        |
        |-- If completed:
        |     |-- Download orders.csv + result.json
        |     |-- Run OrderForensics diagnosis
        |     |-- Generate diagnosis.txt
        |     |-- Update state.json
        |     \-- Send macOS notification
        |
        \-- If no active backtests: exit gracefully
```

## Adaptive Polling Intervals

Instead of a fixed 30s interval (360 API calls for a 3-hour backtest), the poller adapts based on progress:

| Phase | Progress | Interval | Rationale |
|-------|----------|----------|-----------|
| Startup | 0%, < 2min elapsed | 30s | Confirm backtest actually started |
| Normal | 0-30% | 120s | Steady tracking |
| Midgame | 30-80% | 180s | Low frequency, save API quota |
| Endgame | > 80% | 60s | Nearly done, check frequently |

**Result**: ~50 API calls instead of ~360 for a 3-hour backtest.

## CLI Commands

### Submit a backtest (auto-starts poller)
```bash
python3 cli.py submit \
  --main-file strategy.py \
  --name "MyStrategy_v1" \
  --max-dd 40
```

### Check status of all backtests
```bash
python3 cli.py status
```

Shows a table with: name, status, progress %, current equity, live drawdown, elapsed time.

### View poller logs
```bash
python3 cli.py logs --lines 30
```

### View completed results
```bash
python3 cli.py results --name "MyStrategy_v1" --full
```

### Manually start/stop the poller
```bash
python3 cli.py start-poller
python3 cli.py stop-poller
```

### Clean up completed records
```bash
python3 cli.py clear
```

## State Management

All state is stored in `state.json`:

```json
{
  "poller_pid": 12345,
  "poller_running": true,
  "poller_started": "2026-03-17T10:00:00",
  "backtests": [
    {
      "backtest_id": "abc123",
      "name": "MyStrategy_v1",
      "status": "running",
      "progress": 0.45,
      "peak_equity": 12500,
      "current_equity": 11200,
      "live_drawdown": 0.104,
      "max_dd_threshold": 0.40,
      "auto_download": true,
      "auto_diagnose": true
    }
  ]
}
```

File-locking (`fcntl.flock`) prevents race conditions between the CLI and the poller daemon writing to the same file.

## Auto-Diagnosis

When a backtest completes, the poller automatically:

1. Downloads `orders.csv` and `result.json` to `results/<name>/`
2. Runs `OrderForensics.full_diagnosis()` to generate `diagnosis.txt`
3. Extracts a summary: order count, option ROI, zero rate, windfall count
## Notifications

On macOS, the poller sends a system notification via `osascript` when a backtest finishes.

## Graceful Shutdown

The daemon handles SIGTERM and SIGINT for clean exit. It clears its PID from `state.json` only if the PID still matches (prevents stale cleanup from a different process).

## Rules

- **Never submit more than one backtest at a time.** QuantConnect free tier only allows one concurrent backtest per project. Submitting a second will silently queue or fail.
- **Never manually edit `state.json`** while the poller is running. Use the CLI commands (`submit`, `clear`) to modify state. The file uses `fcntl.flock` locking — manual edits bypass the lock and can corrupt state.
- **Never run multiple poller instances simultaneously.** The CLI checks for an existing PID before starting. If you force-start a second poller, both will race on state.json writes.
- **Do not delete files in `results/`** while the poller is actively downloading. Wait for the "completed" status.
- **Early-stop deletes the backtest permanently** from QuantConnect. There is no "pause" API — early-stopped backtests cannot be resumed or recovered.
- **Environment variables `QC_USER_ID`, `QC_API_TOKEN`, and `QC_PROJECT_ID` must be set** before running any command. The skill will fail with a clear error if they are missing.
