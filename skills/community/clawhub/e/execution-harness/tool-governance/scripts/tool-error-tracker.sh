#!/usr/bin/env bash
# tool-error-tracker.sh — PostToolUseFailure hook: track consecutive tool failures
# Writes to sessions/<session-id>/tool-errors.json
# Outputs additionalContext when failure count >= threshold

set -euo pipefail

SESSIONS_DIR="${HOME}/.openclaw/shared-context/sessions"
SOFT_THRESHOLD=3
HARD_THRESHOLD=5

INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // ""' 2>/dev/null)
[ -z "$SESSION_ID" ] && SESSION_ID="${NC_SESSION:-}"
[ -z "$SESSION_ID" ] && exit 0

SESSION_DIR="${SESSIONS_DIR}/${SESSION_ID}"
mkdir -p "$SESSION_DIR"
STATE_FILE="${SESSION_DIR}/tool-errors.json"

TOOL=$(echo "$INPUT" | jq -r '.tool_name // ""')
ERROR=$(echo "$INPUT" | jq -r '.error // ""' | head -c 500)
# Use compact sorted JSON for deterministic hashing
INPUT_RAW=$(echo "$INPUT" | jq -Sc '.tool_input // ""' | head -c 200)
INPUT_HASH=$(echo "$INPUT_RAW" | md5 2>/dev/null || echo "$INPUT_RAW" | md5sum 2>/dev/null | cut -d' ' -f1 || echo "$INPUT_RAW" | shasum 2>/dev/null | cut -d' ' -f1 || echo "unknown")
NOW=$(date -u +%FT%TZ)

# Read existing state
if [ -f "$STATE_FILE" ]; then
  PREV_TOOL=$(jq -r '.tool_name // ""' "$STATE_FILE")
  PREV_HASH=$(jq -r '.input_hash // ""' "$STATE_FILE")
  PREV_COUNT=$(jq -r '.count // 0' "$STATE_FILE")

  if [ "$PREV_TOOL" = "$TOOL" ] && [ "$PREV_HASH" = "$INPUT_HASH" ]; then
    # Same tool+input — increment
    COUNT=$(( PREV_COUNT + 1 ))
  else
    # Different tool or input — reset
    COUNT=1
  fi
else
  COUNT=1
fi

# Write state atomically
TMP="${STATE_FILE}.${$}.$(date +%s).tmp"
jq -n \
  --arg tool "$TOOL" \
  --arg hash "$INPUT_HASH" \
  --arg error "$ERROR" \
  --argjson count "$COUNT" \
  --arg first "$(jq -r '.first_at // ""' "$STATE_FILE" 2>/dev/null || echo "$NOW")" \
  --arg last "$NOW" \
  '{tool_name: $tool, input_hash: $hash, error: $error, count: $count, first_at: (if $first == "" then $last else $first end), last_at: $last}' \
  > "$TMP"
mv "$TMP" "$STATE_FILE"

# Output context injection based on threshold (using jq for safe JSON)
if [ "$COUNT" -ge "$HARD_THRESHOLD" ]; then
  jq -n --arg ctx "MUST use an alternative approach. The tool '${TOOL}' with similar input has failed ${COUNT} times consecutively. Last error: ${ERROR:0:200}. Do NOT retry the same command — use a completely different method, tool, or library." \
    '{"hookSpecificOutput":{"hookEventName":"PostToolUseFailure","additionalContext":$ctx}}'
elif [ "$COUNT" -ge "$SOFT_THRESHOLD" ]; then
  jq -n --arg ctx "The tool '${TOOL}' has failed ${COUNT} times with similar input. Consider: different parameters? different path? missing dependency? Last error: ${ERROR:0:200}" \
    '{"hookSpecificOutput":{"hookEventName":"PostToolUseFailure","additionalContext":$ctx}}'
fi
