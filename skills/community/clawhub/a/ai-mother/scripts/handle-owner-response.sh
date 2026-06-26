#!/bin/bash
# Handle owner's response to permission confirmation
# Usage: ./handle-owner-response.sh <PID> <response>
# Response: "yes", "no", "1", "2", "y", "n", or any custom text

PID=$1
RESPONSE=$2
SKILL_DIR="$HOME/.openclaw/skills/ai-mother"

if [ -z "$PID" ] || [ -z "$RESPONSE" ]; then
    echo "Usage: $0 <PID> <response>"
    echo "  response can be: yes, no, 1, 2, y, n, or any custom text"
    exit 1
fi

if ! ps -p "$PID" > /dev/null 2>&1; then
    echo "❌ Process $PID not found (may have exited)"
    exit 1
fi

# Get tmux session
COMM_INFO=$("$SKILL_DIR/scripts/detect-comm-method.sh" "$PID" 2>/dev/null)
TMUX_SESSION=$(echo "$COMM_INFO" | grep "^TMUX_SESSION=" | cut -d= -f2)

if [ -z "$TMUX_SESSION" ]; then
    echo "❌ AI is not in tmux, cannot send response"
    exit 1
fi

# Check if still waiting
TMUX_CHECK=$("$SKILL_DIR/scripts/check-tmux-waiting.sh" "$PID" 2>/dev/null | head -1)
if [ "$TMUX_CHECK" != "WAITING_INPUT" ]; then
    echo "⚠️  AI is no longer waiting for input (status: $TMUX_CHECK)"
    echo "   The confirmation may have already been handled"
    exit 0
fi

echo "✅ Sending response to AI (PID $PID): $RESPONSE"

# Send the response exactly as provided by owner — no format guessing
tmux send-keys -t "$TMUX_SESSION" "$RESPONSE"
sleep 0.5
tmux send-keys -t "$TMUX_SESSION" Enter
echo "   Sent: $RESPONSE + Enter"

# Verify AI resumed
sleep 2
TMUX_CHECK_AFTER=$("$SKILL_DIR/scripts/check-tmux-waiting.sh" "$PID" 2>/dev/null | head -1)
if [ "$TMUX_CHECK_AFTER" != "WAITING_INPUT" ]; then
    echo "✅ AI has resumed (no longer waiting)"
else
    echo "⚠️  AI still waiting - response may not have been processed"
fi
