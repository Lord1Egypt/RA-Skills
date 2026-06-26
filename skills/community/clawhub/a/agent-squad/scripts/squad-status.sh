#!/bin/bash
# squad-status.sh — Check squad status, peek at screen, nudge if needed
# Usage: squad-status.sh <squad-name>

set -euo pipefail

SQUAD_NAME="${1:?Usage: squad-status.sh <squad-name>}"

# --- Validate squad name ---
if [[ ! "$SQUAD_NAME" =~ ^[a-z0-9][a-z0-9-]*$ ]]; then
  echo "ERROR: Invalid squad name '$SQUAD_NAME'. Use lowercase alphanumeric with hyphens."
  exit 1
fi

SQUAD_DIR="${HOME}/.openclaw/workspace/agent-squad/squads/${SQUAD_NAME}"
TMUX_SESSION="squad-${SQUAD_NAME}"

# --- Check squad exists ---
if [ ! -d "$SQUAD_DIR" ]; then
  echo "ERROR: Squad '$SQUAD_NAME' not found."
  exit 1
fi

# --- Read engine and project_dir from squad.json (safe via sys.argv) ---
ENGINE="unknown"
PROJECT_DIR=""
if [ -f "$SQUAD_DIR/squad.json" ] && command -v python3 &>/dev/null; then
  ENGINE=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1])).get('engine', 'unknown'))" "$SQUAD_DIR/squad.json" 2>/dev/null || echo "unknown")
  PROJECT_DIR=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1])).get('project_dir', ''))" "$SQUAD_DIR/squad.json" 2>/dev/null || echo "")
fi

# --- tmux status ---
if tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
  TMUX_STATUS="running"
else
  TMUX_STATUS="stopped"
fi

# --- Count tasks ---
count_files() {
  local dir="$1"
  find "$dir" -maxdepth 1 -name "task-*.md" -type f 2>/dev/null | wc -l | tr -d ' '
}

PENDING=$(count_files "$SQUAD_DIR/tasks/pending")
IN_PROGRESS=$(count_files "$SQUAD_DIR/tasks/in-progress")
DONE=$(count_files "$SQUAD_DIR/tasks/done")

# --- Current status from reports ---
CURRENT_REPORT=""
for report in "$SQUAD_DIR"/reports/task-*.md; do
  [ -f "$report" ] || continue
  if grep -qi "in-progress" "$report" 2>/dev/null; then
    CURRENT_SECTION=$(sed -n '/^## Current/,/^## /{ /^## Current/d; /^## /d; p; }' "$report" 2>/dev/null | head -5) || true
    if [ -n "$CURRENT_SECTION" ]; then
      REPORT_NAME=$(basename "$report")
      CURRENT_REPORT="  Report: ${REPORT_NAME}
${CURRENT_SECTION}"
    fi
  fi
done

# --- Output ---
echo "Squad: ${SQUAD_NAME}"
echo "Engine: ${ENGINE}"
echo "Status: ${TMUX_STATUS}"
if [ -n "$PROJECT_DIR" ]; then
  echo "Project: ${PROJECT_DIR}"
fi
echo "Tasks: ${PENDING} pending, ${IN_PROGRESS} in-progress, ${DONE} done"

if [ -n "$CURRENT_REPORT" ]; then
  echo ""
  echo "Current activity:"
  echo "$CURRENT_REPORT"
fi

# --- Peek at live screen (if running) ---
if [ "$TMUX_STATUS" = "running" ]; then
  SCREEN_OUTPUT=$(tmux capture-pane -t "$TMUX_SESSION" -p 2>/dev/null | sed '/^$/d' | tail -5) || true
  if [ -n "$SCREEN_OUTPUT" ]; then
    echo ""
    echo "Live screen (last 5 lines):"
    echo "$SCREEN_OUTPUT" | sed 's/^/  /'
  fi
fi

# --- Check for blocked tasks ---
for report in "$SQUAD_DIR"/reports/task-*.md; do
  [ -f "$report" ] || continue
  if grep -qi "^## Blocked" "$report" 2>/dev/null; then
    echo ""
    echo "WARNING: $(basename "$report") has a ## Blocked section!"
  fi
done

# --- Nudge: remind to keep working if tasks remain ---
if [ "$TMUX_STATUS" = "running" ]; then
  REMAINING=$((PENDING + IN_PROGRESS))
  if [ "$REMAINING" -gt 0 ]; then
    {
      tmux send-keys -t "$TMUX_SESSION" Escape 2>/dev/null || true
      sleep 0.5
      tmux send-keys -t "$TMUX_SESSION" "You have ${REMAINING} task(s) remaining (${PENDING} pending, ${IN_PROGRESS} in-progress). Keep working — do not stop until all tasks are done. Update your report with current progress." Enter
    } 2>/dev/null || true
  fi
fi
