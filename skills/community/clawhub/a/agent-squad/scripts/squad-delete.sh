#!/bin/bash
# squad-delete.sh — Archive a stopped squad (non-destructive)
# Usage: squad-delete.sh <squad-name> [--confirm]
# Moves squad data to .archive/, preserving everything.
# Project code in projects/ is NEVER touched.

set -euo pipefail

BASE_DIR="${HOME}/.openclaw/workspace/agent-squad"
SQUADS_DIR="${BASE_DIR}/squads"
ARCHIVE_DIR="${BASE_DIR}/.archive"

SQUAD_NAME="${1:?Usage: squad-delete.sh <squad-name> [--confirm]}"
CONFIRM="${2:-}"

# --- Validate squad name ---
if [[ ! "$SQUAD_NAME" =~ ^[a-z0-9][a-z0-9-]*$ ]]; then
  echo "ERROR: Invalid squad name '$SQUAD_NAME'. Use lowercase alphanumeric with hyphens."
  exit 1
fi
SQUAD_DIR="${SQUADS_DIR}/${SQUAD_NAME}"
TMUX_SESSION="squad-${SQUAD_NAME}"

# --- Check squad exists ---
if [ ! -d "$SQUAD_DIR" ]; then
  echo "ERROR: Squad '$SQUAD_NAME' not found."
  exit 1
fi

# --- Refuse to delete running squad ---
if tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
  echo "ERROR: Squad '$SQUAD_NAME' is still running. Stop it first, e.g.: \"Stop $SQUAD_NAME\""
  exit 1
fi

# --- Count tasks and show summary ---
PENDING=$(find "$SQUAD_DIR/tasks/pending" -maxdepth 1 -name "task-*.md" -type f 2>/dev/null | wc -l | tr -d ' ')
IN_PROG=$(find "$SQUAD_DIR/tasks/in-progress" -maxdepth 1 -name "task-*.md" -type f 2>/dev/null | wc -l | tr -d ' ')
DONE=$(find "$SQUAD_DIR/tasks/done" -maxdepth 1 -name "task-*.md" -type f 2>/dev/null | wc -l | tr -d ' ')

# Read project dir
PROJECT_DIR=""
if [ -f "$SQUAD_DIR/squad.json" ] && command -v python3 &>/dev/null; then
  PROJECT_DIR=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1])).get('project_dir', ''))" "$SQUAD_DIR/squad.json" 2>/dev/null || echo "")
fi

echo "Squad '$SQUAD_NAME' summary:"
echo "  Tasks: ${PENDING} pending, ${IN_PROG} in-progress, ${DONE} done"
echo "  Squad data: $SQUAD_DIR"
if [ -n "$PROJECT_DIR" ]; then
  echo "  Project code: $PROJECT_DIR (will NOT be deleted)"
fi
echo ""

if [ "$IN_PROG" -gt 0 ]; then
  echo "WARNING: There are ${IN_PROG} tasks still in-progress!"
fi

if [ "$CONFIRM" != "--confirm" ]; then
  echo "This will archive the squad data (tasks, reports, logs) to:"
  echo "  ${ARCHIVE_DIR}/${SQUAD_NAME}/"
  echo ""
  echo "Project code at '${PROJECT_DIR}' will NOT be touched."
  echo ""
  echo "To proceed, confirm: \"Yes, delete $SQUAD_NAME\""
  exit 0
fi

# --- Archive ---
mkdir -p "$ARCHIVE_DIR"

# Handle collision in archive
ARCHIVE_TARGET="${ARCHIVE_DIR}/${SQUAD_NAME}"
if [ -d "$ARCHIVE_TARGET" ]; then
  ARCHIVE_TARGET="${ARCHIVE_DIR}/${SQUAD_NAME}-$(date +%Y%m%d-%H%M%S)"
fi

mv "$SQUAD_DIR" "$ARCHIVE_TARGET"

# Remove watchdog cron if openclaw is available
CRON_NAME="squad-watchdog-${SQUAD_NAME}"
if command -v openclaw &>/dev/null; then
  openclaw cron remove --name "$CRON_NAME" 2>/dev/null || true
fi

echo "Squad '$SQUAD_NAME' archived to:"
echo "  $ARCHIVE_TARGET"
if [ -n "$PROJECT_DIR" ]; then
  echo ""
  echo "Project code is still at: $PROJECT_DIR"
fi
