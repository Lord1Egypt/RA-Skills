#!/bin/bash
# squad-ping.sh — Ask a squad to update its status report
# Usage: squad-ping.sh <squad-name>

set -euo pipefail

SQUAD_NAME="${1:?Usage: squad-ping.sh <squad-name>}"

# --- Validate squad name ---
if [[ ! "$SQUAD_NAME" =~ ^[a-z0-9][a-z0-9-]*$ ]]; then
  echo "ERROR: Invalid squad name '$SQUAD_NAME'. Use lowercase alphanumeric with hyphens."
  exit 1
fi

SQUAD_DIR="${HOME}/.openclaw/workspace/agent-squad/squads/${SQUAD_NAME}"
TMUX_SESSION="squad-${SQUAD_NAME}"

# --- Check tmux session exists ---
if ! tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
  echo "ERROR: Squad '$SQUAD_NAME' is not running (no tmux session '$TMUX_SESSION')."
  exit 1
fi

# --- Send ping ---
{
  tmux send-keys -t "$TMUX_SESSION" Escape 2>/dev/null || true
  sleep 1
  tmux send-keys -t "$TMUX_SESSION" "Please update your report now: write your current progress, completed items, any issues, and next steps to ${SQUAD_DIR}/reports/. Update the ## Current section so it reflects your real-time state." Enter
} 2>/dev/null || true

echo "Pinged squad '$SQUAD_NAME'. Check status in a minute to see the updated report."
