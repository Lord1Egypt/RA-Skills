#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
SKILL_DIR=$(dirname -- "$SCRIPT_DIR")
STATE_FILE="$SKILL_DIR/data/state.json"
LOG_FILE="$SKILL_DIR/data/history.log"
JOB_ID="${DEMO_SLAP_WATCHDOG_JOB_ID:-}"

usage() {
  cat >&2 <<EOF
Usage: $0 status|tail|job

status - show local demo-slap state.json
tail   - show last 20 lines of history.log
job    - print the configured watchdog cron job id reference from DEMO_SLAP_WATCHDOG_JOB_ID, if provided by the deployment
EOF
  exit 1
}

[ $# -ge 1 ] || usage
cmd="$1"

case "$cmd" in
  status)
    if [ -f "$STATE_FILE" ]; then
      cat "$STATE_FILE"
    else
      echo '{"status":"idle"}'
    fi
    ;;
  tail)
    if [ -f "$LOG_FILE" ]; then
      tail -n 20 "$LOG_FILE"
    else
      echo "history.log not found"
    fi
    ;;
  job)
    if [ -n "$JOB_ID" ]; then
      echo "$JOB_ID"
    else
      echo "watchdog job id is not configured"
      exit 1
    fi
    ;;
  *)
    usage
    ;;
esac
