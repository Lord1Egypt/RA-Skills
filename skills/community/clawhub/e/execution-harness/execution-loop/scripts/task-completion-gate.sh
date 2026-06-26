#!/usr/bin/env bash
# task-completion-gate.sh — Stop hook: block stop if task checklist has unchecked items
# Reads .harness-tasks.json from working directory or session state.
# Stale checklists (>24h) auto-allow.

set -euo pipefail

SESSIONS_DIR="${HOME}/.openclaw/shared-context/sessions"

INPUT=$(head -c 20000)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // ""' 2>/dev/null)
[ -z "$SESSION_ID" ] && SESSION_ID="${NC_SESSION:-}"
[ -z "$SESSION_ID" ] && echo '{"continue":true}' && exit 0

# Look for task file in CWD first, then session dir
TASK_FILE=""
if [ -f ".harness-tasks.json" ]; then
  TASK_FILE=".harness-tasks.json"
elif [ -f "${SESSIONS_DIR}/${SESSION_ID}/.harness-tasks.json" ]; then
  TASK_FILE="${SESSIONS_DIR}/${SESSION_ID}/.harness-tasks.json"
fi

# No task file = no gate
if [ -z "$TASK_FILE" ]; then
  echo '{"continue":true}'
  exit 0
fi

# Check staleness (>24h = auto-allow)
if command -v stat &>/dev/null; then
  FILE_AGE=$(( $(date +%s) - $(stat -f %m "$TASK_FILE" 2>/dev/null || stat -c %Y "$TASK_FILE" 2>/dev/null || echo "0") ))
  if [ "$FILE_AGE" -gt 86400 ]; then
    echo '{"continue":true}'
    exit 0
  fi
fi

# Count remaining tasks
REMAINING=$(jq '[.tasks[] | select(.done == false)] | length' "$TASK_FILE" 2>/dev/null || echo "0")
REMAINING_NAMES=$(jq -r '[.tasks[] | select(.done == false) | .name] | join(", ")' "$TASK_FILE" 2>/dev/null || echo "")

if [ "$REMAINING" -gt 0 ]; then
  jq -n --arg reason "Task checklist has ${REMAINING} unchecked item(s): ${REMAINING_NAMES}. Complete these before stopping." \
    '{"decision":"block","reason":$reason}'
else
  echo '{"continue":true}'
fi
