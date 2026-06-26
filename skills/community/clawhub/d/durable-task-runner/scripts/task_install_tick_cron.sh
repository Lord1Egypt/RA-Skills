#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"
INTERVAL_SEC="${INTERVAL_SEC:-60}"

if ! [[ "$INTERVAL_SEC" =~ ^[0-9]+$ ]] || [ "$INTERVAL_SEC" -le 0 ]; then
  echo "INTERVAL_SEC must be a positive integer number of seconds" >&2
  exit 2
fi

if [ $((INTERVAL_SEC % 60)) -ne 0 ]; then
  echo "cron helper only supports whole-minute intervals; got INTERVAL_SEC=${INTERVAL_SEC}" >&2
  exit 2
fi

INTERVAL_MIN=$((INTERVAL_SEC / 60))
if [ "$INTERVAL_MIN" -lt 1 ]; then
  INTERVAL_MIN=1
fi

CRON_CMD="*/${INTERVAL_MIN} * * * * cd ${REPO_ROOT} && ${PYTHON_BIN} scripts/task_tick_all.py >/dev/null 2>&1"

usage() {
  cat <<EOF
Install or print a cron entry for recurring durable-task status ticks.

Environment overrides:
  PYTHON_BIN     Python executable (default: python3)
  INTERVAL_SEC   Tick interval in seconds, whole-minute values only for cron (default: 60)

Usage:
  $0 --print   Print the cron entry only
  $0 --apply   Install/update the cron entry for the current user
EOF
}

case "${1:-}" in
  --print)
    printf '%s\n' "$CRON_CMD"
    ;;
  --apply)
    current="$(crontab -l 2>/dev/null || true)"
    filtered="$(printf '%s\n' "$current" | grep -Fv 'scripts/task_tick_all.py' || true)"
    {
      printf '%s\n' "$filtered"
      printf '%s\n' "$CRON_CMD"
    } | sed '/^$/N;/^\n$/D' | crontab -
    echo "Installed cron entry: $CRON_CMD"
    ;;
  *)
    usage
    exit 2
    ;;
esac
