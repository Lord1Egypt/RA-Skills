#!/bin/bash
# Read AI state tracking file
# Usage: ./read-state.sh [PID]

STATE_FILE="$HOME/.openclaw/skills/ai-mother/ai-state.txt"

if [ ! -f "$STATE_FILE" ]; then
    echo "No state file found"
    exit 0
fi

PID=$1

if [ -n "$PID" ]; then
    # Show specific PID
    grep "^$PID|" "$STATE_FILE"
else
    # Show all
    echo "PID|AI_TYPE|WORKDIR|TASK|STATUS|LAST_CHECK|NOTES"
    echo "---"
    cat "$STATE_FILE"
fi
