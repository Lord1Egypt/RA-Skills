#!/bin/bash
# squad-list.sh — List all squads and their status
# Usage: squad-list.sh

set -euo pipefail

SQUADS_DIR="${HOME}/.openclaw/workspace/agent-squad/squads"

# --- Check squads directory ---
if [ ! -d "$SQUADS_DIR" ]; then
  echo "No squads found. Try: \"Start a squad called my-squad using claude\" or \"/agent-squad start my-squad claude\""
  exit 0
fi

# --- Find all squads ---
SQUAD_COUNT=0
for squad_dir in "$SQUADS_DIR"/*/; do
  [ -d "$squad_dir" ] || continue
  SQUAD_NAME=$(basename "$squad_dir")
  TMUX_SESSION="squad-${SQUAD_NAME}"

  # Skip hidden dirs and .archive
  [[ "$SQUAD_NAME" == .* ]] && continue

  # Read engine (safe via sys.argv)
  ENGINE="?"
  if [ -f "$squad_dir/squad.json" ] && command -v python3 &>/dev/null; then
    ENGINE=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1])).get('engine', '?'))" "$squad_dir/squad.json" 2>/dev/null || echo "?")
  fi

  # tmux status
  if tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
    STATUS="running"
  else
    STATUS="stopped"
  fi

  # Count tasks
  PENDING=$(find "$squad_dir/tasks/pending" -maxdepth 1 -name "task-*.md" -type f 2>/dev/null | wc -l | tr -d ' ')
  IN_PROG=$(find "$squad_dir/tasks/in-progress" -maxdepth 1 -name "task-*.md" -type f 2>/dev/null | wc -l | tr -d ' ')
  DONE=$(find "$squad_dir/tasks/done" -maxdepth 1 -name "task-*.md" -type f 2>/dev/null | wc -l | tr -d ' ')

  if [ "$SQUAD_COUNT" -eq 0 ]; then
    printf "%-20s %-12s %-10s %s\n" "SQUAD" "ENGINE" "STATUS" "TASKS (P/A/D)"
    printf "%-20s %-12s %-10s %s\n" "-----" "------" "------" "-------------"
  fi

  printf "%-20s %-12s %-10s %s/%s/%s\n" "$SQUAD_NAME" "$ENGINE" "$STATUS" "$PENDING" "$IN_PROG" "$DONE"
  SQUAD_COUNT=$((SQUAD_COUNT + 1))
done

if [ "$SQUAD_COUNT" -eq 0 ]; then
  echo "No squads found. Try: \"Start a squad called my-squad using claude\" or \"/agent-squad start my-squad claude\""
fi
