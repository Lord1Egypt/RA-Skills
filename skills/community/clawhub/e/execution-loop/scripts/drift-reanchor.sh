#!/usr/bin/env bash
# drift-reanchor.sh — Stop hook: re-inject original task every N turns
# Prevents long-session drift by anchoring to the original task description.
# Wired as Stop hook (fires every turn). Counts turns via state file.

set -euo pipefail

SESSIONS_DIR="${HOME}/.openclaw/shared-context/sessions"
INTERVAL="${REANCHOR_INTERVAL:-10}"

INPUT=$(head -c 20000)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // ""' 2>/dev/null)
[ -z "$SESSION_ID" ] && SESSION_ID="${NC_SESSION:-}"
[ -z "$SESSION_ID" ] && echo '{"continue":true}' && exit 0

SESSION_DIR="${SESSIONS_DIR}/${SESSION_ID}"
STATE_FILE="${SESSION_DIR}/reanchor.json"
mkdir -p "$SESSION_DIR"

# Get last assistant message (may contain clues about the task)
LAST_MSG=$(echo "$INPUT" | jq -r '.last_assistant_message // ""' 2>/dev/null | head -c 500)

# First call: save context as anchor and init turn count
if [ ! -f "$STATE_FILE" ]; then
  # On first stop, we don't have the original task yet — just init counter
  TMP="${STATE_FILE}.${$}.tmp"
  jq -n --argjson count 1 --arg task "" \
    '{"turn_count":$count,"original_task":$task}' > "$TMP"
  mv "$TMP" "$STATE_FILE"
  echo '{"continue":true}'
  exit 0
fi

# Increment turn count
TURN_COUNT=$(jq -r '.turn_count // 0' "$STATE_FILE" 2>/dev/null)
TURN_COUNT=$((TURN_COUNT + 1))
ORIGINAL_TASK=$(jq -r '.original_task // ""' "$STATE_FILE" 2>/dev/null)

# Update state
TMP="${STATE_FILE}.${$}.tmp"
jq -n --arg task "$ORIGINAL_TASK" --argjson count "$TURN_COUNT" \
  '{"original_task":$task,"turn_count":$count}' > "$TMP"
mv "$TMP" "$STATE_FILE"

# Every N turns, inject reminder (only if we have an anchor)
if [ $((TURN_COUNT % INTERVAL)) -eq 0 ] && [ -n "$ORIGINAL_TASK" ]; then
  jq -n --arg ctx "TASK REMINDER (turn ${TURN_COUNT}): ${ORIGINAL_TASK}" \
    '{"hookSpecificOutput":{"additionalContext":$ctx}}'
else
  echo '{"continue":true}'
fi
