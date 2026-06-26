#!/bin/bash
# Detect permission prompt format from tmux content
# Usage: ./detect-permission-format.sh <PID>

PID=$1
SKILL_DIR="$HOME/.openclaw/skills/ai-mother"

if [ -z "$PID" ]; then
    echo "Usage: $0 <PID>"
    exit 1
fi

# Get tmux content
TMUX_CONTENT=$("$SKILL_DIR/scripts/check-tmux-waiting.sh" "$PID" 2>/dev/null | tail -n +3)

if [ -z "$TMUX_CONTENT" ]; then
    echo "FORMAT=unknown"
    echo "ERROR=No tmux content"
    exit 1
fi

# Detect format patterns
if echo "$TMUX_CONTENT" | grep -qi "allow once\|allow always\|deny"; then
    echo "FORMAT=opencode_permission"
    echo "OPTIONS=allow-once,allow-always,deny"
    # Extract option numbers if present
    OPTIONS=$(echo "$TMUX_CONTENT" | grep -E "^[0-9]+\)" | sed 's/).*$//')
    echo "NUMBERS=$OPTIONS"
    
elif echo "$TMUX_CONTENT" | grep -q "1).*[Yy]es.*2).*[Nn]o"; then
    echo "FORMAT=numbered_yes_no"
    echo "OPTIONS=yes,no"
    echo "NUMBERS=1,2"
    
elif echo "$TMUX_CONTENT" | grep -qi "(y/n)\|(yes/no)"; then
    echo "FORMAT=text_yn"
    echo "OPTIONS=y,n"
    
elif echo "$TMUX_CONTENT" | grep -qi "press.*enter\|hit.*enter"; then
    echo "FORMAT=press_enter"
    echo "OPTIONS=enter"
    
else
    echo "FORMAT=unknown"
    echo "PROMPT_SAMPLE=$(echo "$TMUX_CONTENT" | tail -5 | head -3 | tr '\n' ' ')"
fi

# Output full content for debugging
echo "---CONTENT---"
echo "$TMUX_CONTENT" | tail -15
