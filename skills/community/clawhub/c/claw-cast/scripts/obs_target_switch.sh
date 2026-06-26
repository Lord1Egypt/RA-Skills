#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$SCRIPT_DIR/require_obs_mcp.sh"

HOST="${1:-}"
PORT="${2:-4455}"
DB="${3:-}"
ACK="${4:-}"

if [[ -z "$HOST" || -z "$DB" ]]; then
  echo "Usage: ./scripts/obs_target_switch.sh <obs-host> [obs-port] <agentic-obs-db-path> --allow-cross-component-write"
  echo "Example: ./scripts/obs_target_switch.sh 192.168.1.50 4455 \"$HOME/.agentic-obs/db.sqlite\" --allow-cross-component-write"
  exit 1
fi

if [[ ! -f "$DB" ]]; then
  echo "ERROR: DB file not found: $DB"
  exit 1
fi

if [[ "$ACK" != "--allow-cross-component-write" ]]; then
  echo "ERROR: This script writes to an external agentic-obs DB."
  echo "Add explicit acknowledgement flag: --allow-cross-component-write"
  exit 1
fi

sqlite3 "$DB" "update config set value='$HOST', updated_at=datetime('now') where key='obs_host';"
sqlite3 "$DB" "update config set value='$PORT', updated_at=datetime('now') where key='obs_port';"

echo "Updated agentic-obs target in $DB to $HOST:$PORT"
mcporter call 'obs.get_obs_status()'
