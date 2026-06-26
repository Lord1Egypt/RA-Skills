#!/bin/bash
# Detect if AI is stuck and suggest recovery actions
# Usage: ./detect-stuck.sh <PID>

PID=$1
if [ -z "$PID" ]; then
    echo "Usage: $0 <PID>"
    exit 1
fi

SKILL_DIR="$HOME/.openclaw/skills/ai-mother"
CMD=$(ps -o cmd= -p "$PID" 2>/dev/null | awk '{print $1}' | xargs basename)
WORKDIR=$(pwdx "$PID" 2>/dev/null | cut -d: -f2 | xargs)
WCHAN=$(cat /proc/$PID/wchan 2>/dev/null)
STATE=$(ps -o stat= -p "$PID" 2>/dev/null | head -c 1)
RUNTIME=$(ps -o etimes= -p "$PID" 2>/dev/null | xargs)

echo "=== AI Stuck Detection: PID $PID ==="
echo "Type: $CMD"
echo "State: $STATE | wchan: $WCHAN | Runtime: ${RUNTIME}s"
echo ""

# Get last session activity
if [ "$CMD" = "claude" ]; then
    SAFE_PATH=$(echo "$WORKDIR" | sed 's|^/||' | sed 's|/|-|g')
    SESSION_FILE=$(ls -t ~/.claude/projects/*$SAFE_PATH*/*.jsonl 2>/dev/null | head -1)
    
    if [ -n "$SESSION_FILE" ]; then
        LAST_MOD=$(stat -c %Y "$SESSION_FILE" 2>/dev/null)
        NOW=$(date +%s)
        IDLE_TIME=$((NOW - LAST_MOD))
        
        echo "Session: $SESSION_FILE"
        echo "Last activity: ${IDLE_TIME}s ago"
        echo ""
        
        # Check last message
        LAST_MSG=$(tail -3 "$SESSION_FILE" | jq -r 'select(.type == "user" or .type == "assistant") | .type + ": " + (if .message.content then (if (.message.content | type) == "array" then (.message.content[0].text // .message.content[0].type) else .message.content end) else "?" end)[:200]' 2>/dev/null | tail -1)
        echo "Last message: $LAST_MSG"
        echo ""
        
        # Detect stuck patterns
        STUCK=false
        REASON=""
        
        if echo "$LAST_MSG" | grep -qi "interrupted by user"; then
            STUCK=true
            REASON="AI was interrupted (Ctrl+C) and may not be in input-ready state"
        fi
        
        if [ "$WCHAN" = "ep_poll" ] && [ $IDLE_TIME -gt 300 ]; then
            STUCK=true
            REASON="AI in ep_poll for >5min - likely waiting for API that won't come"
        fi
        
        if [ "$WCHAN" = "ep_poll" ] && [ $IDLE_TIME -gt 60 ]; then
            echo "⚠️  AI in ep_poll for ${IDLE_TIME}s - may be stuck waiting for API"
        fi
        
        if [ "$STUCK" = true ]; then
            echo "🚨 AI appears STUCK"
            echo "   Reason: $REASON"
            echo ""
            echo "💡 Suggested actions:"
            echo "   1. Manual: Go to terminal (pts/1) and press Enter"
            echo "   2. Send Ctrl+C: kill -INT $PID"
            echo "   3. If frozen: kill -9 $PID (last resort)"
            exit 1
        else
            echo "✅ AI appears healthy (may just be busy)"
            exit 0
        fi
    fi
fi
