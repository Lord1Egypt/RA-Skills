#!/usr/bin/env bash
# Claude Swarm — Watch a tmux session and notify + review on completion
# Called automatically by spawn-agent.sh
#
# Usage: notify-on-complete.sh <tmux-session> <task-id> <work-dir> <project-dir> <branch>

set -euo pipefail

SWARM_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPTS_DIR="$SWARM_DIR/scripts"
[ -f "$SWARM_DIR/config/swarm.conf" ] && source "$SWARM_DIR/config/swarm.conf"

TMUX_SESSION="${1:?Missing tmux session}"
TASK_ID="${2:?Missing task-id}"
WORK_DIR="${3:?Missing work-dir}"
PROJECT_DIR="${4:?Missing project-dir}"
BRANCH="${5:?Missing branch}"

MAX_REVIEW_ROUNDS="${SWARM_MAX_REVIEW_ROUNDS:-3}"
POLL_INTERVAL=60

# ─── Poll for completion ────────────────────────────────────────────────────

while true; do
  sleep "$POLL_INTERVAL"

  if ! tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
    echo "[watcher] Session $TMUX_SESSION ended"
    break
  fi

  # Check if agent finished (look for runner completion message)
  LAST_LINES=$(tmux capture-pane -t "$TMUX_SESSION" -p -S -20 2>/dev/null || echo "")
  if echo "$LAST_LINES" | grep -q "\[runner\] ✅\|\[runner\] ❌"; then
    echo "[watcher] Agent completed"
    break
  fi
done

# ─── Notify completion ──────────────────────────────────────────────────────

PROJECT_NAME="$(basename "$PROJECT_DIR")"
bash "$SCRIPTS_DIR/notify.sh" "✅ Agent $TASK_ID completed ($PROJECT_NAME)" 2>/dev/null || true

# ─── Auto-review ────────────────────────────────────────────────────────────

for ROUND in $(seq 1 "$MAX_REVIEW_ROUNDS"); do
  echo "[watcher] 🔍 Review round $ROUND/$MAX_REVIEW_ROUNDS for $TASK_ID"
  bash "$SCRIPTS_DIR/notify.sh" "🔍 Review round $ROUND/$MAX_REVIEW_ROUNDS for $TASK_ID" 2>/dev/null || true

  REVIEW_OUTPUT=$(mktemp)
  cd "$WORK_DIR"

  # Get diff for review
  DIFF=$(git diff origin/main...HEAD --stat 2>/dev/null || echo "no diff")

  claude --model sonnet --effort medium --permission-mode bypassPermissions --print \
    "Review the changes in this branch ($BRANCH) of $PROJECT_NAME.

Files changed:
$DIFF

Check for:
1. Bugs or logic errors
2. Security issues
3. Missing error handling
4. Code style issues

If you find issues, fix them directly, commit with message 'review fix (round $ROUND)', and push.
If everything looks good, just say 'LGTM' and exit.
Do NOT modify files unrelated to this task's changes." 2>&1 | tee "$REVIEW_OUTPUT"

  if grep -qi "LGTM\|looks good\|no issues\|clean" "$REVIEW_OUTPUT"; then
    echo "[watcher] ✅ Review passed (round $ROUND)"
    bash "$SCRIPTS_DIR/notify.sh" "✅ Review passed for $TASK_ID (round $ROUND)" 2>/dev/null || true
    rm -f "$REVIEW_OUTPUT"
    break
  fi

  rm -f "$REVIEW_OUTPUT"
  echo "[watcher] Review found issues, fixed in round $ROUND"
done

# ─── Push final state ───────────────────────────────────────────────────────

cd "$WORK_DIR"
git push origin "$BRANCH" --force-with-lease 2>/dev/null || git push origin "$BRANCH" 2>/dev/null || true

echo "[watcher] Done with $TASK_ID"
