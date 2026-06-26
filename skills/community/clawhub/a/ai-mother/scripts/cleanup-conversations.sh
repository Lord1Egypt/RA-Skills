#!/bin/bash
# Clean up old conversation logs (>24h)
# Usage: ./cleanup-conversations.sh

SKILL_DIR="$HOME/.openclaw/skills/ai-mother"
CONV_DIR="$SKILL_DIR/conversations"
CUTOFF=$(($(date +%s) - 86400))  # 24 hours ago

if [ ! -d "$CONV_DIR" ]; then
    exit 0
fi

CLEANED=0

for STATE_FILE in "$CONV_DIR"/*.state; do
    [ -f "$STATE_FILE" ] || continue
    
    # Extract PID from filename
    PID=$(basename "$STATE_FILE" .state)
    
    # Check if process still exists
    if ! ps -p "$PID" > /dev/null 2>&1; then
        # Process dead - check age
        source "$STATE_FILE"
        if [ -n "$STARTED_AT" ] && [ "$STARTED_AT" -lt "$CUTOFF" ]; then
            rm -f "$CONV_DIR/${PID}.log" "$CONV_DIR/${PID}.state" 2>/dev/null
            CLEANED=$((CLEANED + 1))
        fi
    fi
done

[ "$CLEANED" -gt 0 ] && echo "✅ Cleaned up $CLEANED old conversation(s)"
exit 0
