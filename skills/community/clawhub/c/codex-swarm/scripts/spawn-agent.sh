#!/usr/bin/env bash
# Codex Swarm — Spawn a single agent in an isolated worktree
#
# Usage: spawn-agent.sh <project-dir> <task-id> <description> [role] [model] [reasoning]

set -euo pipefail

SWARM_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPTS_DIR="$SWARM_DIR/scripts"
[ -f "$SWARM_DIR/config/swarm.conf" ] && source "$SWARM_DIR/config/swarm.conf"

PROJECT_DIR="${1:?Usage: spawn-agent.sh <project-dir> <task-id> <description> [role] [model] [reasoning]}"
TASK_ID="${2:?Missing task-id}"
DESCRIPTION="${3:?Missing description}"
ROLE="${4:-builder}"
MODEL="${5:-}"
REASONING="${6:-}"

PROJECT_NAME="$(basename "$PROJECT_DIR")"
BRANCH="feat/$TASK_ID"
TMUX_SESSION="codex-$TASK_ID"

# ─── Load duty table ─────────────────────────────────────────────────────────

DUTY_TABLE="$SWARM_DIR/config/duty-table.json"
if [ -f "$DUTY_TABLE" ] && command -v jq &>/dev/null; then
  case "$ROLE" in
    architect|builder|reviewer|integrator) DUTY_KEY="$ROLE" ;;
    *) DUTY_KEY="builder" ;;
  esac
  [ -z "$MODEL" ] && MODEL=$(jq -r ".dutyTable.${DUTY_KEY}.model // \"codex-mini\"" "$DUTY_TABLE")
  [ -z "$REASONING" ] && REASONING=$(jq -r ".dutyTable.${DUTY_KEY}.reasoning // \"medium\"" "$DUTY_TABLE")
fi
MODEL="${MODEL:-codex-mini}"
REASONING="${REASONING:-medium}"

# ─── Endorsement check ───────────────────────────────────────────────────────

ENDORSEMENT_FILE="$SWARM_DIR/endorsements/$TASK_ID.endorsed"
if [ ! -f "$ENDORSEMENT_FILE" ]; then
  echo "⛔ ENDORSEMENT REQUIRED — run: bash $SCRIPTS_DIR/endorse-task.sh $TASK_ID"
  exit 1
fi

COOLDOWN="${SWARM_ENDORSEMENT_COOLDOWN:-30}"
ENDORSE_AGE=$(( $(date +%s) - $(stat -c %Y "$ENDORSEMENT_FILE" 2>/dev/null || stat -f %m "$ENDORSEMENT_FILE" 2>/dev/null || echo 0) ))
if [ "$ENDORSE_AGE" -lt "$COOLDOWN" ]; then
  echo "⛔ COOLDOWN: Wait $((COOLDOWN - ENDORSE_AGE))s"
  exit 1
fi
echo "✅ Endorsement verified"

# ─── Load prompt ─────────────────────────────────────────────────────────────

if [ -f "$DESCRIPTION" ]; then
  PROMPT=$(cat "$DESCRIPTION")
else
  PROMPT="$DESCRIPTION"
fi

WORKLOG="/tmp/worklog-${TMUX_SESSION}.md"
PROMPT="${PROMPT}

## WORK LOG
Maintain a work log at: ${WORKLOG}

## WHEN DONE:
1. Commit all changes: git add -A && git commit -m 'description'
2. Push: git push origin ${BRANCH}
3. Create PR: gh pr create --fill"

# ─── Create worktree ─────────────────────────────────────────────────────────

echo "🐝 Spawning codex/$MODEL (reasoning: $REASONING) for $TASK_ID"
echo "   Role: $ROLE | Project: $PROJECT_NAME"

WORKTREE_DIR="${PROJECT_DIR}-worktrees/${TASK_ID}"
cd "$PROJECT_DIR"
git fetch origin main 2>/dev/null || true
if [ ! -d "$WORKTREE_DIR" ]; then
  mkdir -p "$(dirname "$WORKTREE_DIR")"
  git worktree add "$WORKTREE_DIR" -b "$BRANCH" origin/main 2>/dev/null || {
    git branch -D "$BRANCH" 2>/dev/null || true
    git worktree add "$WORKTREE_DIR" -b "$BRANCH" origin/main
  }
fi

# ─── Save prompt ─────────────────────────────────────────────────────────────

mkdir -p "$SWARM_DIR/logs"
PROMPT_FILE="$SWARM_DIR/logs/${TMUX_SESSION}-prompt.md"
printf '%s' "$PROMPT" > "$PROMPT_FILE"

# ─── Runner script ───────────────────────────────────────────────────────────

RUNNER="$SWARM_DIR/logs/${TMUX_SESSION}-run.sh"
cat > "$RUNNER" << RUNEOF
#!/usr/bin/env bash
set -o pipefail
cd "$WORKTREE_DIR"
echo "[runner] Starting codex/$MODEL ..."

MAX_RETRIES=2
RETRY=0
CUR_MODEL="$MODEL"

while true; do
  codex exec --full-auto -c "model=\$CUR_MODEL" -c "model_reasoning_effort=$REASONING" - < "$PROMPT_FILE" 2>&1
  EXIT=\$?
  
  if [ "\$EXIT" -eq 0 ]; then
    echo "[runner] ✅ Agent completed successfully"
    break
  fi

  RETRY=\$((RETRY + 1))
  if [ "\$RETRY" -gt "\$MAX_RETRIES" ]; then
    echo "[runner] ❌ Max retries reached"
    break
  fi

  echo "[runner] 🔄 Retry \$RETRY/\$MAX_RETRIES ..."
  sleep 10
done
RUNEOF
chmod +x "$RUNNER"

# ─── Spawn in tmux ──────────────────────────────────────────────────────────

tmux new-session -d -s "$TMUX_SESSION" -c "$WORKTREE_DIR" "bash $RUNNER" 2>/dev/null || {
  tmux kill-session -t "$TMUX_SESSION" 2>/dev/null; sleep 1
  tmux new-session -d -s "$TMUX_SESSION" -c "$WORKTREE_DIR" "bash $RUNNER"
}

# ─── Start watcher ──────────────────────────────────────────────────────────

if [ -f "$SCRIPTS_DIR/notify-on-complete.sh" ]; then
  bash "$SCRIPTS_DIR/notify-on-complete.sh" "$TMUX_SESSION" "$TASK_ID" "$WORKTREE_DIR" "$PROJECT_DIR" "$BRANCH" &
  echo "👁️ Watcher started (PID: $!)"
fi

echo "✅ Agent running: tmux=$TMUX_SESSION branch=$BRANCH"
