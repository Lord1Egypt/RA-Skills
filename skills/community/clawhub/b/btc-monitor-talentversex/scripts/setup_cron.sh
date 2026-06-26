#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_FILE="$ROOT_DIR/config.json"
LOG_DIR="$ROOT_DIR/logs"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required."
  exit 1
fi

if ! command -v crontab >/dev/null 2>&1; then
  echo "crontab is required."
  exit 1
fi

SCHEDULE=$(python3 - <<PY
import json
from pathlib import Path

config = json.loads(Path(r"$CONFIG_FILE").read_text(encoding="utf-8"))
print(config.get("schedule", "0 8 * * *"))
PY
)

mkdir -p "$LOG_DIR"
CRON_MARKER="# btc-monitor-skill"
CRON_JOB="$SCHEDULE cd $ROOT_DIR && /usr/bin/env python3 scripts/monitor.py >> $LOG_DIR/monitor.log 2>&1 $CRON_MARKER"

(crontab -l 2>/dev/null | grep -v "$CRON_MARKER" || true; echo "$CRON_JOB") | crontab -

echo "Cron installed: $SCHEDULE"
echo "Log file: $LOG_DIR/monitor.log"
