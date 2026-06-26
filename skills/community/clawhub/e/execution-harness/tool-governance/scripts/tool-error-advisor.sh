#!/usr/bin/env bash
# tool-error-advisor.sh — PreToolUse hook: inject advice when tool has recent failures
# Reads sessions/<session-id>/tool-errors.json
# Returns additionalContext if the same tool+input pattern is about to be retried

set -euo pipefail

SESSIONS_DIR="${HOME}/.openclaw/shared-context/sessions"
HARD_THRESHOLD=5

INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // ""' 2>/dev/null)
[ -z "$SESSION_ID" ] && SESSION_ID="${NC_SESSION:-}"
[ -z "$SESSION_ID" ] && echo '{"continue":true}' && exit 0

STATE_FILE="${SESSIONS_DIR}/${SESSION_ID}/tool-errors.json"
[ -f "$STATE_FILE" ] || { echo '{"continue":true}'; exit 0; }

TOOL=$(echo "$INPUT" | jq -r '.tool_name // ""')
INPUT_RAW=$(echo "$INPUT" | jq -Sc '.tool_input // ""' | head -c 200)
INPUT_HASH=$(echo "$INPUT_RAW" | md5 2>/dev/null || echo "$INPUT_RAW" | md5sum 2>/dev/null | cut -d' ' -f1 || echo "$INPUT_RAW" | shasum 2>/dev/null | cut -d' ' -f1 || echo "unknown")

PREV_TOOL=$(jq -r '.tool_name // ""' "$STATE_FILE")
PREV_HASH=$(jq -r '.input_hash // ""' "$STATE_FILE")
PREV_COUNT=$(jq -r '.count // 0' "$STATE_FILE")
PREV_ERROR=$(jq -r '.error // ""' "$STATE_FILE" | head -c 200)

# Only advise if same tool+input pattern is being retried
if [ "$PREV_TOOL" = "$TOOL" ] && [ "$PREV_HASH" = "$INPUT_HASH" ] && [ "$PREV_COUNT" -ge "$HARD_THRESHOLD" ]; then
  jq -n --arg reason "BLOCKED: '${TOOL}' with this input has failed ${PREV_COUNT} times. Last error: ${PREV_ERROR}. You MUST use a completely different approach." \
    '{"hookSpecificOutput":{"permissionDecision":"deny","reason":$reason}}'
else
  echo '{"continue":true}'
fi
