#!/bin/bash
# AMBER SAVE HOOK — Auto-extract memories every N exchanges
#
# Claude Code "Stop" hook. After every assistant response:
# 1. Counts human messages in the session transcript
# 2. Every SAVE_INTERVAL messages, calls amber-hunter /extract/auto
# 3. AI does the save (amber-hunter auto-extracts via pattern matching)
# 4. Next Stop fires with stop_hook_active=true → lets AI stop normally
#
# === INSTALL ===
# Add to ~/.claude/settings.local.json:
#
#   "hooks": {
#     "Stop": [{
#       "matcher": "*",
#       "hooks": [{
#         "type": "command",
#         "command": "/Users/leo/.openclaw/skills/amber-hunter/hooks/amber_save_hook.sh",
#         "timeout": 30
#       }]
#     }]
#   }
#
# === HOW IT WORKS ===
# Claude Code sends JSON on stdin:
#   session_id       — unique session identifier
#   stop_hook_active — true if AI is already in a save cycle
#   transcript_path  — path to the JSONL transcript file
#
# When stop_hook_active=true we let the AI stop (prevents infinite loop).

SAVE_INTERVAL=15   # Auto-extract every N human messages
STATE_DIR="$HOME/.amber-hunter/hook_state"
mkdir -p "$STATE_DIR"

# amber-hunter API endpoint
AMBER_API="http://127.0.0.1:18998"
AMBER_TOKEN_FILE="$HOME/.amber-hunter/.api_token"

# Read JSON input from stdin
INPUT=$(cat)

# Parse fields
SESSION_ID=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('session_id','unknown'))" 2>/dev/null)
STOP_HOOK_ACTIVE=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('stop_hook_active', False))" 2>/dev/null)
TRANSCRIPT_PATH=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('transcript_path',''))" 2>/dev/null)
TRANSCRIPT_PATH="${TRANSCRIPT_PATH/#\~/$HOME}"

# Infinite-loop prevention
if [ "$STOP_HOOK_ACTIVE" = "True" ] || [ "$STOP_HOOK_ACTIVE" = "true" ]; then
    echo "{}"
    exit 0
fi

# Count human messages in transcript
if [ -f "$TRANSCRIPT_PATH" ]; then
    EXCHANGE_COUNT=$(python3 -c "
import json, sys
count = 0
with open('$TRANSCRIPT_PATH') as f:
    for line in f:
        try:
            entry = json.loads(line)
            msg = entry.get('message', {})
            if isinstance(msg, dict) and msg.get('role') == 'user':
                content = msg.get('content', '')
                if isinstance(content, str) and '<command-message>' in content:
                    continue
                count += 1
        except:
            pass
print(count)
" 2>/dev/null)
else
    EXCHANGE_COUNT=0
fi

# Track last save point
LAST_SAVE_FILE="$STATE_DIR/${SESSION_ID}_last_save"
LAST_SAVE=0
[ -f "$LAST_SAVE_FILE" ] && LAST_SAVE=$(cat "$LAST_SAVE_FILE")

SINCE_LAST=$((EXCHANGE_COUNT - LAST_SAVE))

echo "[$(date '+%H:%M:%S')] amber-save: $EXCHANGE_COUNT exch, $SINCE_LAST since last" >> "$STATE_DIR/hook.log"

# Time to auto-extract?
if [ "$SINCE_LAST" -ge "$SAVE_INTERVAL" ] && [ "$EXCHANGE_COUNT" -gt 0 ]; then
    echo "$EXCHANGE_COUNT" > "$LAST_SAVE_FILE"
    echo "[$(date '+%H:%M:%S')] amber-save: triggering auto-extract" >> "$STATE_DIR/hook.log"

    # Call amber-hunter /extract/auto (fire-and-forget in background)
    TOKEN=""
    [ -f "$AMBER_TOKEN_FILE" ] && TOKEN=$(cat "$AMBER_TOKEN_FILE")
    if [ -n "$TOKEN" ]; then
        curl -s -X POST "$AMBER_API/extract/auto?token=$TOKEN" \
            -H "Content-Type: application/json" \
            --max-time 20 >> "$STATE_DIR/hook.log" 2>&1 &
    else
        curl -s -X POST "$AMBER_API/extract/auto" \
            -H "Content-Type: application/json" \
            --max-time 20 >> "$STATE_DIR/hook.log" 2>&1 &
    fi

    # Block AI once so it can do a final summary save if needed
    cat << 'HOOKJSON'
{"decision": "block", "reason": "Auto-saving memories to amber-hunter. Feel free to stop, or add any final summary before ending."}
HOOKJSON
else
    # Not time yet — let AI stop normally
    echo "{}"
fi
