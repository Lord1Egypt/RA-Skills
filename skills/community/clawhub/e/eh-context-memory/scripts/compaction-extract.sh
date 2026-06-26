#!/usr/bin/env bash
# compaction-extract.sh — Stop hook: extract decisions to handoff file periodically
# Writes last assistant context to handoff document every N stops.
# Since Claude Code doesn't expose context_window_size to hooks, this fires
# periodically as a precaution rather than at a threshold.

set -euo pipefail

SESSIONS_DIR="${HOME}/.openclaw/shared-context/sessions"
EXTRACT_INTERVAL="${COMPACTION_EXTRACT_INTERVAL:-15}"  # Every 15 stops

INPUT=$(head -c 20000)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // ""' 2>/dev/null)
[ -z "$SESSION_ID" ] && SESSION_ID="${NC_SESSION:-}"
[ -z "$SESSION_ID" ] && echo '{"continue":true}' && exit 0

SESSION_DIR="${SESSIONS_DIR}/${SESSION_ID}"
HANDOFFS_DIR="${SESSION_DIR}/handoffs"
STATE_FILE="${SESSION_DIR}/compaction-extract.json"
mkdir -p "$HANDOFFS_DIR"

# Track stop count
STOP_COUNT=0
if [ -f "$STATE_FILE" ]; then
  STOP_COUNT=$(jq -r '.stop_count // 0' "$STATE_FILE" 2>/dev/null)
fi
STOP_COUNT=$((STOP_COUNT + 1))

# Update state
TMP="${STATE_FILE}.${$}.tmp"
jq -n --argjson count "$STOP_COUNT" '{"stop_count":$count}' > "$TMP"
mv "$TMP" "$STATE_FILE"

# Only extract every N stops
if [ $((STOP_COUNT % EXTRACT_INTERVAL)) -ne 0 ]; then
  echo '{"continue":true}'
  exit 0
fi

# Extract last assistant message as knowledge to preserve
LAST_MSG=$(echo "$INPUT" | jq -r '.last_assistant_message // ""' 2>/dev/null | head -c 5000)
[ -z "$LAST_MSG" ] && echo '{"continue":true}' && exit 0

TIMESTAMP=$(date +%s)
HANDOFF_FILE="${HANDOFFS_DIR}/pre-compact-${TIMESTAMP}.md"

cat > "$HANDOFF_FILE" << EOF
# Pre-Compaction Knowledge Extract
Timestamp: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
Session: ${SESSION_ID}
Stop count: ${STOP_COUNT}

## Context Summary
${LAST_MSG}
EOF

jq -n --arg ctx "Knowledge snapshot saved to handoffs/pre-compact-${TIMESTAMP}.md (stop #${STOP_COUNT})." \
  '{"hookSpecificOutput":{"additionalContext":$ctx}}'
