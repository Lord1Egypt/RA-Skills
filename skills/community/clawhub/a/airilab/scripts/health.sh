#!/bin/bash
# One-shot runtime health check for AiriLab.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

if [ -z "${AIRILAB_HOME:-}" ]; then
  export AIRILAB_HOME="$HOME/.openclaw/skills/airilab"
fi

LOG_FILE="$AIRILAB_HOME/scheduler/worker.log"
PID_FILE="$AIRILAB_HOME/scheduler/worker.pid"

echo "AiriLab health check"
echo "skill_dir: $SKILL_DIR"
echo "airilab_home: $AIRILAB_HOME"
echo

python3 "$SKILL_DIR/core/config.py" status || true
echo
python3 "$SKILL_DIR/core/config.py" health || true
echo

if [ -f "$PID_FILE" ]; then
  PID="$(cat "$PID_FILE" || true)"
  if [ -n "${PID}" ] && ps -p "$PID" > /dev/null 2>&1; then
    echo "worker_process: running (pid=$PID)"
  else
    echo "worker_process: pid file exists but process not running"
  fi
else
  echo "worker_process: no pid file"
fi

echo
if [ -f "$LOG_FILE" ]; then
  echo "recent_worker_log:"
  tail -20 "$LOG_FILE" || true
else
  echo "recent_worker_log: log file not found ($LOG_FILE)"
fi

