#!/usr/bin/env bash
# Send a task/message to a running Claude Code remote control session.
#
# Usage: send_task.sh <session-label|tmux-name> <message>
#
# Examples:
#   send_task.sh "🦊 Fox | my-project" "Do an analysis of the codebase"
#   send_task.sh cc-fox-my-project "Fix the issues you identified"

set -euo pipefail

NAME="${1:?Usage: send_task.sh <session-label|tmux-name> <message>}"
MESSAGE="${2:?Missing message}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ── Resolve tmux session name ────────────────────────────────────────────────

if [[ "$NAME" =~ ^cc- ]]; then
  TMUX_NAME="$NAME"
else
  # Derive tmux name from session label (same logic as start_session.sh)
  EMOJI_AND_ANIMAL=$(echo "$NAME" | cut -d'|' -f1 | xargs)
  ANIMAL_SLUG=$(echo "$EMOJI_AND_ANIMAL" | sed 's/[^ ]* //' | tr '[:upper:]' '[:lower:]')
  DIRBASE=$(echo "$NAME" | cut -d'|' -f2 | xargs)
  TMUX_NAME="cc-${ANIMAL_SLUG}-${DIRBASE}"
  TMUX_NAME=$(echo "$TMUX_NAME" | tr ' ' '-' | tr -cd '[:alnum:]-')
fi

# ── Verify session is alive ──────────────────────────────────────────────────

if ! tmux has-session -t "$TMUX_NAME" 2>/dev/null; then
  echo "Error: session '$TMUX_NAME' is not running." >&2
  exit 1
fi

# ── Check that Claude is at the prompt (not mid-response) ────────────────────

PANE_TAIL=$(tmux capture-pane -t "$TMUX_NAME" -p -l 5 2>/dev/null || true)

if echo "$PANE_TAIL" | grep -q '^\s*>\s*$'; then
  :
elif echo "$PANE_TAIL" | grep -qiE '(thinking|working|running)'; then
  echo "Warning: session may still be working. Message will queue." >&2
fi

# ── Send the message via tmux ────────────────────────────────────────────────
# We use tmux's send-keys with literal flag (-l) to avoid interpreting
# special characters in the message, then send Enter separately.

tmux send-keys -t "$TMUX_NAME" -l "$MESSAGE"
# Brief pause so Claude's TUI finishes processing the bracketed paste before
# we send Enter — without this, Enter can fire before the paste buffer is
# flushed and get swallowed.
sleep 0.15
tmux send-keys -t "$TMUX_NAME" Enter

echo "Task sent to $TMUX_NAME"
