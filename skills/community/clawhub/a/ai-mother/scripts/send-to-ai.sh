#!/bin/bash
# Send a message to an AI agent, reusing its existing session (no context loss)
# Supports: Claude Code (--resume), OpenCode (db inject), stdin fallback
#
# Usage:
#   ./send-to-ai.sh <PID> <message>
#   ./send-to-ai.sh <PID> --yes
#   ./send-to-ai.sh <PID> --continue
#   ./send-to-ai.sh <PID> --enter

PID=$1
MSG=$2
SKILL_DIR="$HOME/.openclaw/skills/ai-mother"
TRACKER="$SKILL_DIR/scripts/track-conversation.sh"

if [ -z "$PID" ] || [ -z "$MSG" ]; then
    echo "Usage: $0 <PID> <message|--yes|--no|--continue|--enter>"
    exit 1
fi

if ! ps -p "$PID" > /dev/null 2>&1; then
    echo "Error: Process $PID not found"
    exit 1
fi

# Check if conversation already escalated - block further messages
STATE_FILE="$SKILL_DIR/conversations/${PID}.state"
if [ -f "$STATE_FILE" ] && grep -q "ESCALATED=true" "$STATE_FILE"; then
    REASON=$(grep "ESCALATION_REASON=" "$STATE_FILE" | cut -d'"' -f2)
    echo "🚨 Conversation limit reached, cannot send more messages"
    echo "   Reason: ${REASON:-unknown}"
    echo "   To reset: @AI Mother: reset $PID"
    exit 1
fi

# Track outgoing message (skip for --enter, it's just a nudge)
if [ "$MSG" != "--enter" ] && [ -n "$TRACKER" ]; then
    "$TRACKER" "$PID" "to_baby" "$MSG"
    TRACKER_EXIT=$?
    if [ "$TRACKER_EXIT" -eq 2 ]; then
        echo "🚨 Escalated to owner - message not sent"
        exit 1
    fi
    
    # Trigger frequency check after each message (background, non-blocking)
    "$SKILL_DIR/scripts/manage-patrol-frequency.sh" > /dev/null 2>&1 &
fi

CMD=$(ps -o cmd= -p "$PID" | awk '{print $1}' | xargs basename)
WORKDIR=$(pwdx "$PID" 2>/dev/null | cut -d: -f2 | xargs)

# Detect communication method
COMM_INFO=$("$SKILL_DIR/scripts/detect-comm-method.sh" "$PID" 2>/dev/null)
COMM_METHOD=$(echo "$COMM_INFO" | grep "^COMM_METHOD=" | cut -d= -f2)
TMUX_SESSION=$(echo "$COMM_INFO" | grep "^TMUX_SESSION=" | cut -d= -f2)

# Resolve shortcut messages
case "$MSG" in
    --enter)    SEND_MSG="" ;;
    --yes)      SEND_MSG="yes" ;;
    --no)       SEND_MSG="no" ;;
    --continue) SEND_MSG="continue" ;;
    *)          SEND_MSG="$MSG" ;;
esac

echo "AI Type: $CMD | PID: $PID | Workdir: $WORKDIR"

# ─── Priority 1: Use tmux if available ───────────────────────────────────────
if [ "$COMM_METHOD" = "tmux" ] && [ -n "$TMUX_SESSION" ]; then
    if [ -n "$SEND_MSG" ]; then
        tmux send-keys -t "$TMUX_SESSION" "$SEND_MSG"
        tmux send-keys -t "$TMUX_SESSION" Enter
        echo "✅ Sent to $CMD PID $PID via tmux: $SEND_MSG"
    else
        tmux send-keys -t "$TMUX_SESSION" Enter
        echo "✅ Sent Enter to $CMD PID $PID via tmux"
    fi
    exit 0
fi

# ─── TUI apps without tmux: Cannot send automatically ────────────────────────
if [ "$CMD" = "opencode" ] || [ "$CMD" = "claude" ] || [ "$COMM_METHOD" = "notify_only" ]; then
    echo "❌ Cannot send message to $CMD PID $PID"
    echo "   Reason: Interactive TUI app not running in tmux"
    echo "   Solution: Run $CMD inside tmux for AI Mother to communicate with it"
    echo "   Example: tmux new-session -s ai-session '$CMD'"
    exit 1
fi

# ─── Codex: stdin ────────────────────────────────────────────────────────────
if [ "$CMD" = "codex" ]; then
    if [ -n "$SEND_MSG" ]; then
        printf '%s\n' "$SEND_MSG" > "/proc/$PID/fd/0" 2>/dev/null
        echo "✅ Sent to Codex PID $PID via stdin: $SEND_MSG"
    else
        printf '\n' > "/proc/$PID/fd/0" 2>/dev/null
        echo "✅ Sent Enter to Codex PID $PID"
    fi
    exit 0
fi

# ─── Fallback: stdin ─────────────────────────────────────────────────────────
if [ -n "$SEND_MSG" ]; then
    printf '%s\n' "$SEND_MSG" > "/proc/$PID/fd/0" 2>/dev/null
    echo "✅ Sent to PID $PID via stdin (fallback): $SEND_MSG"
else
    printf '\n' > "/proc/$PID/fd/0" 2>/dev/null
    echo "✅ Sent Enter to PID $PID (fallback)"
fi
