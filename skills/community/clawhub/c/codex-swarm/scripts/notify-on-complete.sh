#!/usr/bin/env bash
# Codex Swarm — Watch agent + auto-review on completion
set -euo pipefail

SWARM_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPTS_DIR="$SWARM_DIR/scripts"
[ -f "$SWARM_DIR/config/swarm.conf" ] && source "$SWARM_DIR/config/swarm.conf"

TMUX_SESSION="${1:?}"; TASK_ID="${2:?}"; WORK_DIR="${3:?}"; PROJECT_DIR="${4:?}"; BRANCH="${5:?}"
MAX_ROUNDS="${SWARM_MAX_REVIEW_ROUNDS:-3}"

# Poll for completion
while true; do
  sleep 60
  tmux has-session -t "$TMUX_SESSION" 2>/dev/null || break
  LAST=$(tmux capture-pane -t "$TMUX_SESSION" -p -S -20 2>/dev/null || echo "")
  echo "$LAST" | grep -q "\[runner\] ✅\|\[runner\] ❌" && break
done

bash "$SCRIPTS_DIR/notify.sh" "✅ Agent $TASK_ID completed" 2>/dev/null || true

# Auto-review using Codex native review
for ROUND in $(seq 1 "$MAX_ROUNDS"); do
  bash "$SCRIPTS_DIR/notify.sh" "🔍 Review round $ROUND for $TASK_ID" 2>/dev/null || true
  cd "$WORK_DIR"
  
  REVIEW=$(mktemp)
  codex exec review 2>&1 | tee "$REVIEW"
  
  if grep -qi "no issues\|LGTM\|looks good\|clean\|approved" "$REVIEW"; then
    bash "$SCRIPTS_DIR/notify.sh" "✅ Review passed for $TASK_ID" 2>/dev/null || true
    rm -f "$REVIEW"; break
  fi
  
  # If issues found, Codex review may auto-fix. Commit and retry.
  git add -A 2>/dev/null && git commit -m "review fix (round $ROUND)" 2>/dev/null || true
  rm -f "$REVIEW"
done

cd "$WORK_DIR"
git push origin "$BRANCH" --force-with-lease 2>/dev/null || git push origin "$BRANCH" 2>/dev/null || true
