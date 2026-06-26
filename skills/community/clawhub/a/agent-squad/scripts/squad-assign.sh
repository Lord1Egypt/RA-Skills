#!/bin/bash
# squad-assign.sh — Assign a task to a squad
# Usage: squad-assign.sh <squad-name> <task-title> <objective> [priority]

set -euo pipefail

SQUAD_NAME="${1:?Usage: squad-assign.sh <squad-name> <task-title> <objective> [priority]}"
TASK_TITLE="${2:?Usage: squad-assign.sh <squad-name> <task-title> <objective> [priority]}"
OBJECTIVE="${3:?Usage: squad-assign.sh <squad-name> <task-title> <objective> [priority]}"
PRIORITY="${4:-normal}"

# --- Validate squad name ---
if [[ ! "$SQUAD_NAME" =~ ^[a-z0-9][a-z0-9-]*$ ]]; then
  echo "ERROR: Invalid squad name '$SQUAD_NAME'. Use lowercase alphanumeric with hyphens."
  exit 1
fi

SQUAD_DIR="${HOME}/.openclaw/workspace/agent-squad/squads/${SQUAD_NAME}"
TMUX_SESSION="squad-${SQUAD_NAME}"

# --- Check squad exists ---
if [ ! -d "$SQUAD_DIR" ]; then
  echo "ERROR: Squad '$SQUAD_NAME' not found. Start it first, e.g.: \"Start a squad called $SQUAD_NAME using claude\""
  exit 1
fi

# --- Generate filename ---
DATE=$(date +%Y%m%d)
KEBAB_TITLE=$(echo "$TASK_TITLE" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g; s/-\{2,\}/-/g; s/^-//; s/-$//')
TASK_FILE="task-${DATE}-${KEBAB_TITLE}.md"
TASK_PATH="${SQUAD_DIR}/tasks/pending/${TASK_FILE}"

# --- Find unique filename ---
COUNTER=0
while [ -f "$TASK_PATH" ]; do
  COUNTER=$((COUNTER + 1))
  TASK_FILE="task-${DATE}-${KEBAB_TITLE}-${COUNTER}.md"
  TASK_PATH="${SQUAD_DIR}/tasks/pending/${TASK_FILE}"
done

# --- Write task file (atomic) ---
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%S+00:00)
TMP_PATH="${TASK_PATH}.${$}.tmp"

python3 -c "
import sys
title, timestamp, objective, priority, out = sys.argv[1:6]
content = f'''# Task: {title}

## Created
{timestamp}

## Context
Assigned by user via agent-squad.

## Objective
{objective}

## Acceptance Criteria
- [ ] Objective completed as described
- [ ] All changes committed and pushed
- [ ] Report updated with results

## Priority
{priority}
'''
with open(out, 'w') as f:
    f.write(content)
" "$TASK_TITLE" "$TIMESTAMP" "$OBJECTIVE" "$PRIORITY" "$TMP_PATH"

if ! mv "$TMP_PATH" "$TASK_PATH"; then
  echo "ERROR: Failed to write task file."
  rm -f "$TMP_PATH"
  exit 1
fi

# --- Notify squad via tmux if running ---
if tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
  {
    tmux send-keys -t "$TMUX_SESSION" Escape 2>/dev/null || true
    sleep 1
    tmux send-keys -t "$TMUX_SESSION" "New task assigned: check ${SQUAD_DIR}/tasks/pending/${TASK_FILE} and start working on it." Enter
  } 2>/dev/null && echo "Task assigned and squad notified." || echo "Task assigned. Could not notify squad via tmux (it may still be initializing)."
else
  echo "Task assigned. Squad is not currently running — it will pick up the task when restarted."
fi

echo ""
echo "  Squad:    ${SQUAD_NAME}"
echo "  Task:     ${TASK_TITLE}"
echo "  File:     ${TASK_PATH}"
echo "  Priority: ${PRIORITY}"
