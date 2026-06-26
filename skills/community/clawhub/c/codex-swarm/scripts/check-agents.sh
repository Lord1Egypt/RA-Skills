#!/usr/bin/env bash
# Claude Swarm — Check status of all running agents
set -euo pipefail

echo "=== Active Swarm Agents ==="
tmux ls 2>/dev/null | grep "^codex-" | while read -r line; do
  SESSION=$(echo "$line" | cut -d: -f1)
  TASK_ID="${SESSION#codex-}"
  # Check if process is still running
  if tmux has-session -t "$SESSION" 2>/dev/null; then
    LAST_LINE=$(tmux capture-pane -t "$SESSION" -p 2>/dev/null | grep -v "^$" | tail -1)
    if echo "$LAST_LINE" | grep -qi "done\|complete\|✅\|error\|❌"; then
      echo "  ✅ $TASK_ID — DONE"
    else
      echo "  🟢 $TASK_ID — RUNNING"
    fi
  else
    echo "  ⚪ $TASK_ID — SESSION ENDED"
  fi
done

if ! tmux ls 2>/dev/null | grep -q "^codex-"; then
  echo "  (no active agents)"
fi
