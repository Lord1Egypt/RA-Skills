#!/bin/bash
# Test if message actually reaches AI and gets processed
# Usage: ./test-send.sh <PID> <message>

PID=$1
MSG=$2

if [ -z "$PID" ] || [ -z "$MSG" ]; then
    echo "Usage: $0 <PID> <message>"
    exit 1
fi

CMD=$(ps -o cmd= -p "$PID" 2>/dev/null | awk '{print $1}' | xargs basename)
WORKDIR=$(pwdx "$PID" 2>/dev/null | cut -d: -f2 | xargs)

echo "=== Testing message delivery to PID $PID ($CMD) ==="
echo "Message: $MSG"
echo ""

# Get baseline
if [ "$CMD" = "claude" ]; then
    SAFE_PATH=$(echo "$WORKDIR" | sed 's|/|-|g' | sed 's|^-||')
    SESSION_DIR="$HOME/.claude/projects/$SAFE_PATH"
    SESSION_FILE=$(ls -t "$SESSION_DIR"/*.jsonl 2>/dev/null | head -1)
    
    if [ -z "$SESSION_FILE" ]; then
        echo "❌ No session file found"
        exit 1
    fi
    
    echo "Session: $SESSION_FILE"
    BASELINE_SIZE=$(stat -c %s "$SESSION_FILE" 2>/dev/null)
    BASELINE_TIME=$(stat -c %Y "$SESSION_FILE" 2>/dev/null)
    echo "Baseline: size=$BASELINE_SIZE, mtime=$BASELINE_TIME"
    echo ""
fi

# Check stdin status
echo "Checking stdin..."
if [ -e "/proc/$PID/fd/0" ]; then
    FD_INFO=$(ls -l "/proc/$PID/fd/0" 2>/dev/null)
    echo "stdin: $FD_INFO"
else
    echo "❌ stdin not accessible"
    exit 1
fi
echo ""

# Send message
echo "Sending message..."
printf '%s\n' "$MSG" > "/proc/$PID/fd/0" 2>&1
SEND_EXIT=$?
echo "Send exit code: $SEND_EXIT"
echo ""

# Wait and check for changes
echo "Waiting 5 seconds for response..."
sleep 5

if [ "$CMD" = "claude" ]; then
    CURRENT_SIZE=$(stat -c %s "$SESSION_FILE" 2>/dev/null)
    CURRENT_TIME=$(stat -c %Y "$SESSION_FILE" 2>/dev/null)
    
    echo "After send: size=$CURRENT_SIZE, mtime=$CURRENT_TIME"
    
    if [ "$CURRENT_SIZE" -gt "$BASELINE_SIZE" ]; then
        echo "✅ Session file grew by $((CURRENT_SIZE - BASELINE_SIZE)) bytes"
        echo ""
        echo "New content:"
        tail -3 "$SESSION_FILE" | jq -r 'select(.role != null) | .role + ": " + (if .message.content then (if (.message.content | type) == "array" then .message.content[0].text else .message.content end) else "?" end)[:300]' 2>/dev/null
    elif [ "$CURRENT_TIME" -gt "$BASELINE_TIME" ]; then
        echo "⚠️  File modified but size unchanged (possible empty response)"
    else
        echo "❌ No change detected - message may not have been processed"
        echo ""
        echo "Possible reasons:"
        echo "1. AI is not in input-waiting state"
        echo "2. AI needs different input format (e.g., double newline)"
        echo "3. stdin is buffered and not flushed"
        echo "4. AI is stuck/frozen"
    fi
fi
