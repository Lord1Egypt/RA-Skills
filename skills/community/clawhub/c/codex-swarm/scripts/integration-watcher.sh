#!/usr/bin/env bash
# Codex Swarm — Integration watcher: merge all branches when batch completes
set -euo pipefail

SWARM_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPTS_DIR="$SWARM_DIR/scripts"
[ -f "$SWARM_DIR/config/swarm.conf" ] && source "$SWARM_DIR/config/swarm.conf"

PROJECT_DIR="${1:?}"; BATCH_ID="${2:?}"; shift 2; SESSIONS=("$@")
MAX_ROUNDS="${SWARM_MAX_REVIEW_ROUNDS:-3}"

# Wait for all agents
while true; do
  sleep 60
  ALL_DONE=true
  for S in "${SESSIONS[@]}"; do
    if tmux has-session -t "$S" 2>/dev/null; then
      LAST=$(tmux capture-pane -t "$S" -p -S -10 2>/dev/null || echo "")
      echo "$LAST" | grep -q "\[runner\] ✅\|\[runner\] ❌\|DONE" || { ALL_DONE=false; break; }
    fi
  done
  $ALL_DONE && break
done

bash "$SCRIPTS_DIR/notify.sh" "🔗 All agents done. Integrating batch $BATCH_ID..." 2>/dev/null || true

# Collect branches
cd "$PROJECT_DIR"; git fetch origin 2>/dev/null || true
BRANCHES=()
for S in "${SESSIONS[@]}"; do
  TASK_ID="${S#codex-}"; BRANCH="feat/$TASK_ID"
  git rev-parse "origin/$BRANCH" &>/dev/null && BRANCHES+=("$BRANCH")
done

[ ${#BRANCHES[@]} -eq 0 ] && { echo "No branches to integrate"; exit 0; }

# Merge
git checkout main 2>/dev/null || git checkout -b main origin/main
git pull origin main 2>/dev/null || true

FAILURES=()
for B in "${BRANCHES[@]}"; do
  if git merge "origin/$B" --no-edit 2>/dev/null; then
    echo "✅ Merged $B"
  else
    CONFLICTS=$(git diff --name-only --diff-filter=U 2>/dev/null || echo "")
    if [ -n "$CONFLICTS" ]; then
      # Use o3 (reasoning model) for conflict resolution
      codex exec --full-auto -c "model=o3" -c "model_reasoning_effort=high" \
        "Resolve merge conflicts in: $CONFLICTS. Keep both features working. Then: git add . && git commit --no-edit" 2>/dev/null || {
        git merge --abort 2>/dev/null; FAILURES+=("$B"); continue
      }
    fi
    echo "✅ Merged $B (conflicts resolved)"
  fi
done

# Integration review
for ROUND in $(seq 1 "$MAX_ROUNDS"); do
  REVIEW=$(mktemp)
  codex exec review 2>&1 | tee "$REVIEW"
  if grep -qi "approved\|LGTM\|no issues\|clean" "$REVIEW"; then
    bash "$SCRIPTS_DIR/notify.sh" "✅ Integration passed for $BATCH_ID" 2>/dev/null || true
    rm -f "$REVIEW"; break
  fi
  git add -A 2>/dev/null && git commit -m "integration fix (round $ROUND)" 2>/dev/null || true
  rm -f "$REVIEW"
done

# Push
if [ "${SWARM_AUTO_MERGE:-true}" = "true" ]; then
  git push origin main 2>/dev/null && bash "$SCRIPTS_DIR/notify.sh" "✅ Batch $BATCH_ID pushed to main" 2>/dev/null || true
fi

[ ${#FAILURES[@]} -gt 0 ] && bash "$SCRIPTS_DIR/notify.sh" "⚠️ Merge failures: ${FAILURES[*]}" 2>/dev/null || true
