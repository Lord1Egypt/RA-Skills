#!/bin/bash
# Smart message sender with verification
# Usage: ./smart-send.sh <PID> <message> [expected_keyword] [timeout]
#
# This wraps send-to-ai.sh with response verification
# Returns same exit codes as verify-response.sh

PID=$1
MSG=$2
KEYWORD=${3:-""}
TIMEOUT=${4:-15}

SKILL_DIR="$HOME/.openclaw/skills/ai-mother"
SEND_SCRIPT="$SKILL_DIR/scripts/send-to-ai.sh"
VERIFY_SCRIPT="$SKILL_DIR/scripts/verify-response.sh"

if [ -z "$PID" ] || [ -z "$MSG" ]; then
    echo "Usage: $0 <PID> <message> [expected_keyword] [timeout]"
    exit 1
fi

# Get AI context first to make smarter decisions
CMD=$(ps -o cmd= -p "$PID" 2>/dev/null | awk '{print $1}' | xargs basename)
WORKDIR=$(pwdx "$PID" 2>/dev/null | cut -d: -f2 | xargs)

echo "📤 Sending to PID $PID ($CMD in $WORKDIR)"
echo "   Message: $MSG"

# Check if AI is actually waiting for input
WCHAN=$(cat /proc/$PID/wchan 2>/dev/null)
if [ "$WCHAN" != "wait_woken" ] && [ "$WCHAN" != "read" ] && [ "$WCHAN" != "poll_schedule_timeout" ]; then
    echo "⚠️  Warning: AI is in '$WCHAN' state (not waiting for stdin)"
    echo "   It's likely waiting for API response or network I/O"
    echo "   Sending message anyway, but it may not be processed..."
fi

# Check if AI is actually waiting for input
STATE=$(ps -o stat= -p "$PID" | head -c 1)
if [ "$STATE" != "S" ] && [ "$STATE" != "R" ]; then
    echo "⚠️  Warning: AI is in state '$STATE' (not sleeping/running)"
    echo "   It might not be waiting for input"
fi

# Get last output to understand context
if [ "$CMD" = "claude" ]; then
    SAFE_PATH=$(echo "$WORKDIR" | sed 's|/|-|g' | sed 's|^-||')
    SESSION_DIR="$HOME/.claude/projects/$SAFE_PATH"
    LATEST=$(ls -t "$SESSION_DIR"/*.jsonl 2>/dev/null | head -1)
    
    if [ -n "$LATEST" ]; then
        LAST_MSG=$(tail -3 "$LATEST" 2>/dev/null | python3 -c "
import sys, json
for line in sys.stdin:
    try:
        d = json.loads(line.strip())
        role = d.get('role','?')
        content = d.get('message', d).get('content', '')
        if isinstance(content, list):
            for b in content:
                if isinstance(b, dict) and b.get('type') == 'text':
                    print(f'[{role}]: {b[\"text\"][:200]}')
        elif isinstance(content, str) and content:
            print(f'[{role}]: {content[:200]}')
    except: pass
" 2>/dev/null | tail -1)
        
        echo "   Last message: $LAST_MSG"
        
        # Smart keyword inference if not provided
        if [ -z "$KEYWORD" ]; then
            case "$MSG" in
                --continue|continue)
                    # If last message was asking for confirmation, expect "yes" or action
                    if echo "$LAST_MSG" | grep -qi "continue\|proceed\|should I"; then
                        KEYWORD="."  # Any response is good
                    else
                        echo "⚠️  Warning: Sending 'continue' but AI might not have context"
                        echo "   Consider sending a more specific message"
                    fi
                    ;;
                --yes|yes)
                    KEYWORD="."  # Expect any acknowledgment
                    ;;
                *)
                    KEYWORD="."  # For custom messages, any response is progress
                    ;;
            esac
        fi
    fi
fi

# Send the message
"$SEND_SCRIPT" "$PID" "$MSG"
SEND_EXIT=$?

if [ $SEND_EXIT -ne 0 ]; then
    echo "❌ Failed to send message"
    exit $SEND_EXIT
fi

# Verify response if keyword provided
if [ -n "$KEYWORD" ]; then
    echo ""
    "$VERIFY_SCRIPT" "$PID" "$KEYWORD" "$TIMEOUT"
    exit $?
else
    echo "✅ Message sent (no verification requested)"
    exit 0
fi
