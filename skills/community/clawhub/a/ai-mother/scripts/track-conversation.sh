#!/bin/bash
# Track conversations between AI Mother and AI babies
# Auto-escalates when limits are hit
# Usage: ./track-conversation.sh <PID> <direction> <message>
#   direction: "to_baby" or "from_baby"

PID=$1
DIRECTION=$2
MESSAGE=$3
SKILL_DIR="$HOME/.openclaw/skills/ai-mother"
CONV_DIR="$SKILL_DIR/conversations"
LOG_FILE="$CONV_DIR/${PID}.log"
STATE_FILE="$CONV_DIR/${PID}.state"
NOTIFY_SCRIPT="$SKILL_DIR/scripts/notify-owner.sh"

# Limits
MAX_ROUNDS=10
MAX_SAME_ERROR=3
MAX_NO_PROGRESS_ROUNDS=5

if [ -z "$PID" ] || [ -z "$DIRECTION" ]; then
    echo "Usage: $0 <PID> <to_baby|from_baby> <message>"
    exit 1
fi

mkdir -p "$CONV_DIR"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Initialize state if not exists
if [ ! -f "$STATE_FILE" ]; then
    cat > "$STATE_FILE" <<EOF
ROUND_COUNT=0
LAST_ERROR=""
ERROR_COUNT=0
LAST_PROGRESS_ROUND=0
STARTED_AT=$(date +%s)
EOF
fi

# Load current state
source "$STATE_FILE"

# Log the message
echo "[$TIMESTAMP] $DIRECTION: $MESSAGE" >> "$LOG_FILE"

# Update round count
if [ "$DIRECTION" = "to_baby" ]; then
    ROUND_COUNT=$((ROUND_COUNT + 1))
fi

# Check for escalation triggers
SHOULD_ESCALATE=false
ESCALATION_REASON=""

# Trigger 1: Max rounds exceeded
if [ "$ROUND_COUNT" -ge "$MAX_ROUNDS" ]; then
    SHOULD_ESCALATE=true
    ESCALATION_REASON="Max rounds ($MAX_ROUNDS) exceeded"
fi

# Trigger 2: Same error repeated (only check responses from baby)
if [ "$DIRECTION" = "from_baby" ]; then
    # Extract error patterns
    if echo "$MESSAGE" | grep -qi "error\|failed\|exception\|denied"; then
        CURRENT_ERROR=$(echo "$MESSAGE" | grep -ioE "(error|failed|exception|denied)[^.]*" | head -1)
        
        if [ "$CURRENT_ERROR" = "$LAST_ERROR" ]; then
            ERROR_COUNT=$((ERROR_COUNT + 1))
            if [ "$ERROR_COUNT" -ge "$MAX_SAME_ERROR" ]; then
                SHOULD_ESCALATE=true
                ESCALATION_REASON="Same error repeated $ERROR_COUNT times: $CURRENT_ERROR"
            fi
        else
            LAST_ERROR="$CURRENT_ERROR"
            ERROR_COUNT=1
        fi
    fi
    
    # Trigger 3: Baby says it's stuck
    if echo "$MESSAGE" | grep -qi "stuck\|don't know\|can't\|unable to\|impossible"; then
        SHOULD_ESCALATE=true
        ESCALATION_REASON="Baby indicated it's stuck or unable to proceed"
    fi
    
    # Trigger 4: Credentials/permissions request (explicit ask, not just an error)
    if echo "$MESSAGE" | grep -qi "can you.*password\|need.*token\|provide.*api.key\|give me.*credential\|need.*secret"; then
        SHOULD_ESCALATE=true
        ESCALATION_REASON="Baby requested credentials or secrets"
    fi
    
    # Trigger 5: No progress detection
    if echo "$MESSAGE" | grep -qi "done\|completed\|fixed\|working\|success"; then
        LAST_PROGRESS_ROUND=$ROUND_COUNT
    fi
    
    if [ "$ROUND_COUNT" -gt 5 ] && [ $((ROUND_COUNT - LAST_PROGRESS_ROUND)) -ge "$MAX_NO_PROGRESS_ROUNDS" ]; then
        SHOULD_ESCALATE=true
        ESCALATION_REASON="No progress for $MAX_NO_PROGRESS_ROUNDS rounds"
    fi
fi

# Save updated state (always, before escalation check)
cat > "$STATE_FILE" <<EOF
ROUND_COUNT=$ROUND_COUNT
LAST_ERROR="$LAST_ERROR"
ERROR_COUNT=$ERROR_COUNT
LAST_PROGRESS_ROUND=$LAST_PROGRESS_ROUND
STARTED_AT=$STARTED_AT
EOF

# Escalate if needed
if [ "$SHOULD_ESCALATE" = true ]; then
    echo "🚨 ESCALATION TRIGGERED: $ESCALATION_REASON" >> "$LOG_FILE"
    
    # Mark as escalated immediately so no more messages go through
    echo "ESCALATED=true" >> "$STATE_FILE"
    echo "ESCALATION_REASON=\"$ESCALATION_REASON\"" >> "$STATE_FILE"
    
    # Get AI context
    AI_TYPE=$(ps -o cmd= -p "$PID" 2>/dev/null | awk '{print $1}' | xargs -I{} basename {} 2>/dev/null || echo "unknown")
    WORKDIR=$(pwdx "$PID" 2>/dev/null | cut -d: -f2 | xargs || echo "unknown")
    
    # Get last 10 lines of conversation
    CONV_SUMMARY=$(tail -20 "$LOG_FILE" | sed 's/^/  /')
    
    "$NOTIFY_SCRIPT" "🚨 AI Mother Escalation

Reason: $ESCALATION_REASON

AI Baby Details:
- PID: $PID
- Type: $AI_TYPE
- Project: $WORKDIR
- Rounds: $ROUND_COUNT

Recent conversation:
$CONV_SUMMARY

Please review and provide guidance." 2>/dev/null
    
    echo "✅ Owner notified - conversation escalated"
    
    exit 2  # Exit code 2 = escalated
fi

# Output current state
echo "Round $ROUND_COUNT/$MAX_ROUNDS"
[ -n "$LAST_ERROR" ] && echo "Last error: $LAST_ERROR (count: $ERROR_COUNT)"

exit 0
