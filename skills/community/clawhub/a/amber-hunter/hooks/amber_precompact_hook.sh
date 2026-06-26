#!/bin/bash
# AMBER PRE-COMPACT HOOK — Emergency save before context compression
#
# Claude Code "PreCompact" hook. Fires RIGHT BEFORE the conversation
# gets compressed to free up context window space.
#
# This is the safety net. When compaction happens, the AI loses detailed
# context. This hook forces one final auto-extraction before that happens.
#
# === INSTALL ===
# Add to ~/.claude/settings.local.json:
#
#   "hooks": {
#     "PreCompact": [{
#       "hooks": [{
#         "type": "command",
#         "command": "/Users/leo/.openclaw/skills/amber-hunter/hooks/amber_precompact_hook.sh",
#         "timeout": 30
#       }]
#     }]
#   }
#
# === HOW IT WORKS ===
# Claude Code sends JSON on stdin:
#   session_id — unique session identifier
#
# We call amber-hunter /extract/auto synchronously (waits for completion)
# then return block so AI can also do a final save before compaction.

STATE_DIR="$HOME/.amber-hunter/hook_state"
mkdir -p "$STATE_DIR"

AMBER_API="http://127.0.0.1:18998"
AMBER_TOKEN_FILE="$HOME/.amber-hunter/.api_token"

INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('session_id','unknown'))" 2>/dev/null)

echo "[$(date '+%H:%M:%S')] amber-precompact: triggered for session $SESSION_ID" >> "$STATE_DIR/hook.log"

# Synchronous auto-extract (waits for completion — compaction is imminent)
TOKEN=""
[ -f "$AMBER_TOKEN_FILE" ] && TOKEN=$(cat "$AMBER_TOKEN_FILE")

if [ -n "$TOKEN" ]; then
    RESULT=$(curl -s -X POST "$AMBER_API/extract/auto?token=$TOKEN" \
        -H "Content-Type: application/json" \
        --max-time 25 2>&1)
else
    RESULT=$(curl -s -X POST "$AMBER_API/extract/auto" \
        -H "Content-Type: application/json" \
        --max-time 25 2>&1)
fi
echo "[$(date '+%H:%M:%S')] amber-precompact result: $RESULT" >> "$STATE_DIR/hook.log"

# Always block — let AI do a final save then compaction proceeds
cat << 'HOOKJSON'
{"decision": "block", "reason": "CONTEXT COMPACTION IMMINENT. amber-hunter has auto-saved memories from this session. You may now add a brief executive summary of this session before compaction erases detailed context. After your summary, compaction will proceed automatically."}
HOOKJSON
