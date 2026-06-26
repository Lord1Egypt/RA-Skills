#!/bin/bash
# Check if AI is waiting for input by examining tmux pane content
# Usage: ./check-tmux-waiting.sh <PID>

PID=$1
if [ -z "$PID" ]; then
    echo "Usage: $0 <PID>"
    exit 1
fi

SKILL_DIR="$HOME/.openclaw/skills/ai-mother"

# Get tmux session
COMM_INFO=$("$SKILL_DIR/scripts/detect-comm-method.sh" "$PID" 2>/dev/null)
TMUX_SESSION=$(echo "$COMM_INFO" | grep "^TMUX_SESSION=" | cut -d= -f2)

if [ -z "$TMUX_SESSION" ]; then
    echo "NOT_IN_TMUX"
    exit 1
fi

# Capture tmux pane content
PANE_CONTENT=$(tmux capture-pane -t "$TMUX_SESSION" -p 2>/dev/null | tail -30)

# Check for waiting patterns
if echo "$PANE_CONTENT" | grep -qi "permission required\|allow once\|allow always\|do you want\|proceed\|yes/no\|y/n\|press enter\|hit enter\|continue?"; then
    echo "WAITING_INPUT"
    echo "---"
    echo "$PANE_CONTENT" | tail -10
    exit 0
fi

# Check if idle (no recent activity)
if echo "$PANE_CONTENT" | grep -qi "^$\|^[[:space:]]*$" | tail -5 | grep -c "^$" | grep -q "^[45]$"; then
    echo "IDLE"
    exit 0
fi

echo "ACTIVE"
exit 0
