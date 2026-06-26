#!/usr/bin/env bash
# Claude Swarm — Watch all agents in a batch, then auto-integrate
#
# Usage: integration-watcher.sh <project-dir> <batch-id> <tmux-sessions...>

set -euo pipefail

SWARM_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPTS_DIR="$SWARM_DIR/scripts"
[ -f "$SWARM_DIR/config/swarm.conf" ] && source "$SWARM_DIR/config/swarm.conf"

PROJECT_DIR="${1:?Missing project-dir}"
BATCH_ID="${2:?Missing batch-id}"
shift 2
SESSIONS=("$@")

POLL_INTERVAL=60
MAX_INTEGRATION_ROUNDS="${SWARM_MAX_REVIEW_ROUNDS:-3}"

echo "[integration] Watching ${#SESSIONS[@]} sessions: ${SESSIONS[*]}"

# ─── Wait for all agents to complete ────────────────────────────────────────

while true; do
  sleep "$POLL_INTERVAL"
  ALL_DONE=true

  for SESSION in "${SESSIONS[@]}"; do
    if tmux has-session -t "$SESSION" 2>/dev/null; then
      LAST=$(tmux capture-pane -t "$SESSION" -p -S -10 2>/dev/null || echo "")
      if ! echo "$LAST" | grep -q "\[runner\] ✅\|\[runner\] ❌\|DONE"; then
        ALL_DONE=false
        break
      fi
    fi
  done

  if $ALL_DONE; then
    echo "[integration] All agents completed"
    break
  fi
done

bash "$SCRIPTS_DIR/notify.sh" "🔗 All subteams done for batch $BATCH_ID. Starting integration..." 2>/dev/null || true

# ─── Collect branches ───────────────────────────────────────────────────────

cd "$PROJECT_DIR"
git fetch origin 2>/dev/null || true

BRANCHES=()
for SESSION in "${SESSIONS[@]}"; do
  TASK_ID="${SESSION#claude-}"
  BRANCH="feat/$TASK_ID"
  if git rev-parse "origin/$BRANCH" &>/dev/null; then
    BRANCHES+=("$BRANCH")
  fi
done

if [ ${#BRANCHES[@]} -eq 0 ]; then
  echo "[integration] No branches found to integrate"
  exit 0
fi

echo "[integration] Integrating ${#BRANCHES[@]} branches: ${BRANCHES[*]}"

# ─── Merge branches sequentially ────────────────────────────────────────────

git checkout main 2>/dev/null || git checkout -b main origin/main
git pull origin main 2>/dev/null || true

MERGE_FAILURES=()
for BRANCH in "${BRANCHES[@]}"; do
  echo "[integration] Merging $BRANCH..."
  if git merge "origin/$BRANCH" --no-edit 2>/dev/null; then
    echo "[integration] ✅ $BRANCH merged cleanly"
  else
    echo "[integration] ⚠️ Conflict in $BRANCH — attempting auto-resolve..."
    
    # Use Claude to resolve conflicts
    CONFLICTS=$(git diff --name-only --diff-filter=U 2>/dev/null || echo "")
    if [ -n "$CONFLICTS" ]; then
      claude --model opus --effort high --permission-mode bypassPermissions --print \
        "Resolve the merge conflicts in these files: $CONFLICTS
         
         Keep the most complete version. For i18n files, combine both sets of translations.
         For code files, keep both features working.
         After resolving, run: git add . && git commit --no-edit" 2>/dev/null || {
        git merge --abort 2>/dev/null || true
        MERGE_FAILURES+=("$BRANCH")
        continue
      }
    fi
    echo "[integration] ✅ $BRANCH merged (conflicts resolved)"
  fi
done

# ─── Integration review ─────────────────────────────────────────────────────

for ROUND in $(seq 1 "$MAX_INTEGRATION_ROUNDS"); do
  echo "[integration] 🔍 Integration review round $ROUND/$MAX_INTEGRATION_ROUNDS"

  REVIEW=$(mktemp)
  DIFF_STAT=$(git diff origin/main...HEAD --stat 2>/dev/null || echo "no changes")

  claude --model opus --effort high --permission-mode bypassPermissions --print \
    "Integration review for batch $BATCH_ID.

Changes merged from ${#BRANCHES[@]} branches:
$DIFF_STAT

Check for:
1. Cross-branch conflicts or duplicate code
2. API contract mismatches between subteams
3. Import errors or missing dependencies
4. Build/compile issues (run build command if applicable)

If issues found, fix them and commit with 'integration fix (round $ROUND)'.
If all good, say 'INTEGRATION PASSED'." 2>&1 | tee "$REVIEW"

  if grep -qi "INTEGRATION PASSED\|PASSED\|LGTM\|all good\|no issues" "$REVIEW"; then
    echo "[integration] ✅ Integration review passed (round $ROUND)"
    bash "$SCRIPTS_DIR/notify.sh" "✅ Integration passed for batch $BATCH_ID (round $ROUND)" 2>/dev/null || true
    rm -f "$REVIEW"
    break
  fi
  rm -f "$REVIEW"
done

# ─── Push to main ───────────────────────────────────────────────────────────

AUTO_MERGE="${SWARM_AUTO_MERGE:-true}"
if [ "$AUTO_MERGE" = "true" ]; then
  git push origin main 2>/dev/null && {
    echo "[integration] ✅ Pushed to main"
    bash "$SCRIPTS_DIR/notify.sh" "✅ Batch $BATCH_ID integrated and pushed to main" 2>/dev/null || true
  } || {
    echo "[integration] ❌ Push failed"
    bash "$SCRIPTS_DIR/notify.sh" "❌ Batch $BATCH_ID integration push failed" 2>/dev/null || true
  }
else
  echo "[integration] Auto-merge disabled. Review and push manually."
fi

# ─── Report failures ────────────────────────────────────────────────────────

if [ ${#MERGE_FAILURES[@]} -gt 0 ]; then
  echo "[integration] ⚠️ Failed to merge: ${MERGE_FAILURES[*]}"
  bash "$SCRIPTS_DIR/notify.sh" "⚠️ Merge failures in batch $BATCH_ID: ${MERGE_FAILURES[*]}" 2>/dev/null || true
fi
