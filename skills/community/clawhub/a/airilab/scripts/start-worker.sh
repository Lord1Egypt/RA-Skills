#!/bin/bash
# Start AiriLab worker in background.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

if [ -z "${AIRILAB_HOME:-}" ]; then
  export AIRILAB_HOME="$HOME/.openclaw/skills/airilab"
fi

mkdir -p "$AIRILAB_HOME/scheduler"

WORKER_SCRIPT="$SKILL_DIR/scheduler/worker.py"
LOG_FILE="$AIRILAB_HOME/scheduler/worker.log"
PID_FILE="$AIRILAB_HOME/scheduler/worker.pid"

echo "AiriLab worker launcher"
echo "skill_dir: $SKILL_DIR"
echo "airilab_home: $AIRILAB_HOME"

echo "Preflight health check:"
python3 "$SKILL_DIR/core/config.py" health || true

if [ -f "$PID_FILE" ]; then
  OLD_PID=$(cat "$PID_FILE" || true)
  if [ -n "${OLD_PID}" ] && ps -p "$OLD_PID" > /dev/null 2>&1; then
    echo "Worker already running (PID: $OLD_PID)"
    exit 0
  fi
  rm -f "$PID_FILE"
fi

if [ ! -f "$WORKER_SCRIPT" ]; then
  echo "Missing worker script: $WORKER_SCRIPT"
  exit 1
fi

nohup python3 "$WORKER_SCRIPT" >> "$LOG_FILE" 2>&1 &
NEW_PID=$!
echo "$NEW_PID" > "$PID_FILE"

sleep 2
if ps -p "$NEW_PID" > /dev/null 2>&1; then
  echo "Worker started (PID: $NEW_PID)"
  echo "log: $LOG_FILE"
else
  echo "Worker failed to start"
  tail -20 "$LOG_FILE" || true
  rm -f "$PID_FILE"
  exit 1
fi
