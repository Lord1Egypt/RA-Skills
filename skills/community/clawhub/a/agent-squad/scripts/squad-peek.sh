#!/bin/bash
# squad-peek.sh — Peek at a squad's live tmux screen
# Usage: squad-peek.sh <squad-name> [lines]

set -euo pipefail

SQUAD_NAME="${1:?Usage: squad-peek.sh <squad-name> [lines]}"
LINES="${2:-20}"

# --- Validate squad name ---
if [[ ! "$SQUAD_NAME" =~ ^[a-z0-9][a-z0-9-]*$ ]]; then
  echo "ERROR: Invalid squad name '$SQUAD_NAME'. Use lowercase alphanumeric with hyphens."
  exit 1
fi

TMUX_SESSION="squad-${SQUAD_NAME}"

# --- Check tmux session exists ---
if ! tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
  echo "ERROR: Squad '$SQUAD_NAME' is not running (no tmux session found)."
  exit 1
fi

# --- Capture screen ---
SCREEN_OUTPUT=$(tmux capture-pane -t "$TMUX_SESSION" -p 2>/dev/null | sed '/^$/d' | tail -"$LINES") || true

if [ -z "$SCREEN_OUTPUT" ]; then
  echo "Screen is empty — the squad may still be initializing."
else
  echo "Live screen of '$SQUAD_NAME' (last $LINES lines):"
  echo ""
  echo "$SCREEN_OUTPUT"
fi
