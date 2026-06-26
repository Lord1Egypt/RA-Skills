#!/bin/bash
# Yuri Session Ensurer — lazy recreation of tmux sessions
# Usage: ensure-session.sh <type> <project_root>
#   type: "planning" or "dev"
set +e

TYPE="$1"
PROJECT_ROOT="$2"

if [ -z "$TYPE" ] || [ -z "$PROJECT_ROOT" ]; then
  echo "Usage: ensure-session.sh <planning|dev> <project_root>"
  exit 1
fi

PROJECT_ROOT=$(cd "$PROJECT_ROOT" && pwd)

if [ "$TYPE" = "planning" ]; then
  PROJECT_NAME=$(basename "$PROJECT_ROOT")
  SESSION="op-$(echo "$PROJECT_NAME" | tr -cd 'a-zA-Z0-9_-')"

  if tmux has-session -t "$SESSION" 2>/dev/null; then
    echo "$SESSION"
    exit 0
  fi

  # Recreate planning session
  tmux new-session -d -s "$SESSION" -n "Plan" -c "$PROJECT_ROOT"
  tmux send-keys -t "$SESSION:0" "cc" C-m

  # Wait for Claude Code to start, auto-accepting trust dialog if it appears.
  # The trust prompt shows "Do you trust" and blocks until user responds.
  # We poll the pane every 2s and send Enter if we detect trust-related text.
  for i in $(seq 1 6); do
    sleep 2
    PANE_TEXT=$(tmux capture-pane -t "$SESSION:0" -p -S -10 2>/dev/null || true)
    if echo "$PANE_TEXT" | grep -qi "trust this folder\|safety check"; then
      tmux send-keys -t "$SESSION:0" Enter
      sleep 2
      break
    fi
    # Already past trust dialog (❯ prompt visible)
    if echo "$PANE_TEXT" | grep -q "❯"; then
      break
    fi
  done

  echo "$SESSION"

elif [ "$TYPE" = "dev" ]; then
  CONFIG="$PROJECT_ROOT/.orchestrix-core/core-config.yaml"
  REPO_ID=""

  if [ -f "$CONFIG" ]; then
    REPO_ID=$(grep -E '^\s*repository_id:' "$CONFIG" 2>/dev/null | head -1 | sed "s/.*repository_id:[[:space:]]*//" | tr -d "'" | tr -d '"' | tr -d ' ')
  fi

  if [ -z "$REPO_ID" ]; then
    REPO_ID=$(basename "$PROJECT_ROOT")
  fi

  REPO_ID=$(echo "$REPO_ID" | tr -cd 'a-zA-Z0-9_-')
  SESSION="orchestrix-${REPO_ID}"

  if tmux has-session -t "$SESSION" 2>/dev/null; then
    echo "$SESSION"
    exit 0
  fi

  # Recreate dev session
  cd "$PROJECT_ROOT"
  bash .orchestrix-core/scripts/start-orchestrix.sh &
  sleep 30
  echo "$SESSION"

else
  echo "Unknown type: $TYPE. Use 'planning' or 'dev'."
  exit 1
fi
