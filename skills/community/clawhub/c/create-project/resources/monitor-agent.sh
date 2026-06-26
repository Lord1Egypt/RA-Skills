#!/bin/bash
# Yuri Agent Completion Monitor
# Polls a tmux pane for agent completion signals.
# Usage: monitor-agent.sh <session> <window> [expected_file] [timeout_min] [poll_sec]
set +e

SESSION="$1"
WINDOW="$2"
EXPECTED_FILE="${3:-}"
TIMEOUT_MIN="${4:-30}"
POLL_SEC="${5:-30}"

MAX_POLLS=$((TIMEOUT_MIN * 60 / POLL_SEC))
STABLE_COUNT=0
LAST_HASH=""

for i in $(seq 1 $MAX_POLLS); do
  OUTPUT=$(tmux capture-pane -t "$SESSION:$WINDOW" -p -S -200 2>/dev/null)
  LAST_LINES=$(echo "$OUTPUT" | tail -10)

  # Priority 1: Claude Code completion message ("Baked for 31s", "Worked for 2m", etc.)
  if echo "$LAST_LINES" | grep -qE '[A-Z][a-z]*ed for [0-9]'; then
    if [ -z "$EXPECTED_FILE" ] || [ -f "$EXPECTED_FILE" ]; then
      echo "COMPLETE"
      exit 0
    fi
  fi

  # Priority 2: TUI idle indicator
  if echo "$LAST_LINES" | grep -q '○'; then
    if [ -z "$EXPECTED_FILE" ] || [ -f "$EXPECTED_FILE" ]; then
      echo "IDLE"
      exit 0
    fi
  fi

  # Priority 3: Handle approval prompt — auto-approve
  if echo "$LAST_LINES" | grep -q '◐'; then
    tmux send-keys -t "$SESSION:$WINDOW" "y" Enter
    sleep 2
    continue
  fi

  # Priority 4: Content stability fallback
  HASH=$(echo "$OUTPUT" | md5 2>/dev/null || echo "$OUTPUT" | md5sum 2>/dev/null | cut -d' ' -f1)
  if [ "$HASH" = "$LAST_HASH" ]; then
    STABLE_COUNT=$((STABLE_COUNT + 1))
    if [ $STABLE_COUNT -ge 3 ]; then
      echo "STABLE_IDLE"
      exit 0
    fi
  else
    STABLE_COUNT=0
  fi
  LAST_HASH="$HASH"

  sleep "$POLL_SEC"
done

echo "TIMEOUT"
exit 1
