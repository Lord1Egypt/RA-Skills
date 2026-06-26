#!/usr/bin/env bash
# denial-tracker.sh — Stop hook: track tool denials inferred from conversation
# Checks if the last assistant message mentions being denied/blocked.
# Warns at 3 denials of same tool, suggests alternative at 5.
# NOTE: Claude Code does not provide a dedicated denial hook event.
# This script infers denials from the stop context.

set -euo pipefail

SESSIONS_DIR="${HOME}/.openclaw/shared-context/sessions"
SOFT_THRESHOLD=3
HARD_THRESHOLD=5

INPUT=$(head -c 20000)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // ""' 2>/dev/null)
[ -z "$SESSION_ID" ] && SESSION_ID="${NC_SESSION:-}"
[ -z "$SESSION_ID" ] && echo '{"continue":true}' && exit 0

# Extract last assistant message to detect denial patterns
LAST_MSG=$(echo "$INPUT" | jq -r '.last_assistant_message // ""' 2>/dev/null)
[ -z "$LAST_MSG" ] && echo '{"continue":true}' && exit 0

# Check for denial indicators in the message
if ! echo "$LAST_MSG" | grep -qiE '(permission denied|was denied|user denied|not allowed|denied by user|blocked by hook|cannot proceed)'; then
  echo '{"continue":true}'
  exit 0
fi

# Try to extract the tool name from denial context
TOOL=$(echo "$LAST_MSG" | grep -oiE '(Bash|Write|Edit|Read|Glob|Grep|Agent)\b' | head -1)
[ -z "$TOOL" ] && TOOL="unknown"

SESSION_DIR="${SESSIONS_DIR}/${SESSION_ID}"
STATE_FILE="${SESSION_DIR}/denials.json"
mkdir -p "$SESSION_DIR"

NOW=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Read or init state
if [ -f "$STATE_FILE" ]; then
  COUNT=$(jq -r --arg t "$TOOL" '.patterns[$t].count // 0' "$STATE_FILE" 2>/dev/null)
else
  COUNT=0
fi
COUNT=$((COUNT + 1))

# Write state atomically
TMP="${STATE_FILE}.${$}.$(date +%s).tmp"
if [ -f "$STATE_FILE" ]; then
  jq --arg t "$TOOL" --argjson c "$COUNT" --arg ts "$NOW" \
    '.patterns[$t] = {count: $c, last: $ts}' "$STATE_FILE" > "$TMP"
else
  jq -n --arg t "$TOOL" --argjson c "$COUNT" --arg ts "$NOW" \
    '{patterns: {($t): {count: $c, last: $ts}}}' > "$TMP"
fi
mv "$TMP" "$STATE_FILE"

# Output based on threshold
if [ "$COUNT" -ge "$HARD_THRESHOLD" ]; then
  jq -n --arg ctx "Tool '${TOOL}' has been denied ${COUNT} times. You MUST use a completely different approach." \
    '{"hookSpecificOutput":{"additionalContext":$ctx}}'
elif [ "$COUNT" -ge "$SOFT_THRESHOLD" ]; then
  jq -n --arg ctx "WARNING: Tool '${TOOL}' denied ${COUNT} times. Consider an alternative approach." \
    '{"hookSpecificOutput":{"additionalContext":$ctx}}'
else
  echo '{"continue":true}'
fi
