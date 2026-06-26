#!/bin/bash
# squad-stop.sh — Stop a squad (keep all data)
# Usage: squad-stop.sh <squad-name>

set -euo pipefail

SQUAD_NAME="${1:?Usage: squad-stop.sh <squad-name>}"

# --- Validate squad name ---
if [[ ! "$SQUAD_NAME" =~ ^[a-z0-9][a-z0-9-]*$ ]]; then
  echo "ERROR: Invalid squad name '$SQUAD_NAME'. Use lowercase alphanumeric with hyphens."
  exit 1
fi

TMUX_SESSION="squad-${SQUAD_NAME}"
SQUAD_DIR="${HOME}/.openclaw/workspace/agent-squad/squads/${SQUAD_NAME}"
CRON_NAME="squad-watchdog-${SQUAD_NAME}"

# --- Kill tmux session ---
if tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
  tmux kill-session -t "$TMUX_SESSION"
  echo "Stopped tmux session: $TMUX_SESSION"
else
  echo "tmux session '$TMUX_SESSION' was not running."
fi

# --- Remove watchdog cron ---
if command -v openclaw &>/dev/null; then
  openclaw cron remove --name "$CRON_NAME" 2>/dev/null && \
    echo "Removed watchdog cron: $CRON_NAME" || \
    echo "No watchdog cron found for '$CRON_NAME'."
fi

# --- Log the stop event ---
if [ -d "$SQUAD_DIR/logs" ]; then
  echo "[$(date -u +%Y-%m-%dT%H:%M:%S+00:00)] Squad stopped by user." >> "$SQUAD_DIR/logs/watchdog.log"
fi

echo ""
echo "Squad '$SQUAD_NAME' stopped. All data preserved at:"
echo "  $SQUAD_DIR"
echo ""
echo "To restart, just say: \"Restart $SQUAD_NAME\""
