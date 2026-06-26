#!/usr/bin/env bash
# Stop a Claude Code remote control session by name or tmux session name.
#
# Usage: stop_session.sh <session-label|tmux-name>
#
# Examples:
#   stop_session.sh "🦊 Fox | my-project"    # by session label
#   stop_session.sh cc-fox-my-project          # by tmux name
#
# Killing the tmux session triggers the SessionEnd hook, which marks
# the registry entry dead automatically.

NAME="${1:?Usage: stop_session.sh <session-label|tmux-name>}"

# If it looks like a tmux name (starts with cc-), use it directly
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

if ! tmux has-session -t "$TMUX_NAME" 2>/dev/null; then
  echo "Session '$TMUX_NAME' is not running." >&2
  exit 1
fi

echo "Stopping session: $TMUX_NAME"
tmux kill-session -t "$TMUX_NAME"
echo "Session stopped. SessionEnd hook will handle registry update."
