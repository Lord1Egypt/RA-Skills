#!/usr/bin/env bash
# Claude Swarm — Spawn a single agent in an isolated worktree
#
# Usage: spawn-agent.sh <project-dir> <task-id> <description> [role] [model] [effort]
#   project-dir: absolute path to the project root (must be a git repo)
#   task-id:     unique identifier (used for branch name + tmux session)
#   description: task prompt text or path to a .md prompt file
#   role:        architect | builder | reviewer | integrator | speedster (default: builder)
#   model:       model override — opus | sonnet (default: from duty table)
#   effort:      low | medium | high (default: from duty table)

set -euo pipefail

SWARM_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPTS_DIR="$SWARM_DIR/scripts"

# Source config
[ -f "$SWARM_DIR/config/swarm.conf" ] && source "$SWARM_DIR/config/swarm.conf"
source "$SCRIPTS_DIR/_lib.sh" 2>/dev/null || true

# ─── Parse arguments ─────────────────────────────────────────────────────────

PROJECT_DIR="${1:?Usage: spawn-agent.sh <project-dir> <task-id> <description> [role] [model] [effort]}"
TASK_ID="${2:?Missing task-id}"
DESCRIPTION="${3:?Missing description}"
ROLE="${4:-builder}"
MODEL="${5:-}"
EFFORT="${6:-}"

PROJECT_NAME="$(basename "$PROJECT_DIR")"
BRANCH="feat/$TASK_ID"
TMUX_SESSION="claude-$TASK_ID"

# ─── Load duty table ─────────────────────────────────────────────────────────

DUTY_TABLE="$SWARM_DIR/config/duty-table.json"
if [ -f "$DUTY_TABLE" ] && command -v jq &>/dev/null; then
  # Map role names to duty table keys
  case "$ROLE" in
    architect|builder|reviewer|integrator|speedster) DUTY_KEY="$ROLE" ;;
    *) DUTY_KEY="builder" ;;
  esac
  [ -z "$MODEL" ] && MODEL=$(jq -r ".dutyTable.${DUTY_KEY}.model // \"sonnet\"" "$DUTY_TABLE")
  [ -z "$EFFORT" ] && EFFORT=$(jq -r ".dutyTable.${DUTY_KEY}.effort // \"high\"" "$DUTY_TABLE")
fi

# Defaults
MODEL="${MODEL:-sonnet}"
EFFORT="${EFFORT:-high}"

# ─── Endorsement check ───────────────────────────────────────────────────────

ENDORSEMENT_FILE="$SWARM_DIR/endorsements/$TASK_ID.endorsed"
if [ ! -f "$ENDORSEMENT_FILE" ]; then
  echo "⛔ ENDORSEMENT REQUIRED"
  echo "   Task '$TASK_ID' has not been endorsed."
  echo ""
  echo "   To endorse:"
  echo "     bash $SCRIPTS_DIR/endorse-task.sh $TASK_ID"
  exit 1
fi

# Cooldown check
COOLDOWN="${SWARM_ENDORSEMENT_COOLDOWN:-30}"
if command -v stat &>/dev/null; then
  ENDORSE_AGE=$(( $(date +%s) - $(stat -c %Y "$ENDORSEMENT_FILE" 2>/dev/null || stat -f %m "$ENDORSEMENT_FILE" 2>/dev/null || echo 0) ))
  if [ "$ENDORSE_AGE" -lt "$COOLDOWN" ]; then
    echo "⛔ COOLDOWN: Endorsement is only ${ENDORSE_AGE}s old (minimum ${COOLDOWN}s)."
    echo "   Wait $((COOLDOWN - ENDORSE_AGE))s."
    exit 1
  fi
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

## 📝 WORK LOG — MANDATORY
Maintain a work log at: ${WORKLOG}
At the end, append a structured handoff with what changed, how to verify, known issues, and decisions made.

## ✅ WHEN DONE:
1. Finalize your work log
2. Commit all changes with a clear commit message
3. Push the branch: git push origin ${BRANCH}
4. Open a PR: gh pr create --fill
5. Exit when complete"

# ─── Create worktree ─────────────────────────────────────────────────────────

echo "🐝 Spawning agent: claude/$MODEL ($EFFORT) for task: $TASK_ID"
echo "   Role: $ROLE"
echo "   Project: $PROJECT_NAME ($PROJECT_DIR)"

WORKTREE_DIR="${PROJECT_DIR}-worktrees/${TASK_ID}"

if [ -d "$PROJECT_DIR/.git" ]; then
  mkdir -p "$(dirname "$WORKTREE_DIR")"
  cd "$PROJECT_DIR"
  git fetch origin main 2>/dev/null || git fetch origin 2>/dev/null || true
  
  if [ -d "$WORKTREE_DIR" ]; then
    echo "   Worktree already exists, reusing..."
    cd "$WORKTREE_DIR"
  else
    git worktree add "$WORKTREE_DIR" -b "$BRANCH" origin/main 2>/dev/null || {
      git branch -D "$BRANCH" 2>/dev/null || true
      git worktree add "$WORKTREE_DIR" -b "$BRANCH" origin/main
    }
    cd "$WORKTREE_DIR"
  fi
  WORK_DIR="$WORKTREE_DIR"
else
  WORK_DIR="$PROJECT_DIR"
fi

# ─── Install dependencies if needed ─────────────────────────────────────────

if [ -f "requirements.txt" ] && [ ! -d "venv" ] && [ ! -d ".venv" ]; then
  pip install -r requirements.txt 2>/dev/null || true
elif [ -f "package.json" ] && [ ! -d "node_modules" ]; then
  if [ -f "yarn.lock" ]; then
    yarn install 2>/dev/null || true
  elif [ -f "package-lock.json" ]; then
    npm install 2>/dev/null || true
  fi
fi

# ─── Save prompt to file ────────────────────────────────────────────────────

PROMPT_FILE="$SWARM_DIR/logs/${TMUX_SESSION}-prompt.md"
mkdir -p "$SWARM_DIR/logs"
printf '%s' "$PROMPT" > "$PROMPT_FILE"

# ─── Create runner script ───────────────────────────────────────────────────

RUNNER_SCRIPT="$SWARM_DIR/logs/${TMUX_SESSION}-run.sh"
cat > "$RUNNER_SCRIPT" << RUNNER_EOF
#!/usr/bin/env bash
set -o pipefail

WORK_DIR="$WORK_DIR"
PROMPT_FILE="$PROMPT_FILE"
MODEL="$MODEL"
EFFORT="$EFFORT"
MAX_RETRIES=2
RETRY=0

cd "\$WORK_DIR"
PROMPT=\$(cat "\$PROMPT_FILE")

run_agent() {
  echo "[runner] Starting claude/\$MODEL (effort: \$EFFORT) ..."
  claude --model "\$MODEL" --effort "\$EFFORT" --permission-mode bypassPermissions --print "\$PROMPT"
}

while true; do
  OUTPUT_FILE=\$(mktemp)
  run_agent 2>&1 | tee "\$OUTPUT_FILE"
  EXIT_CODE=\${PIPESTATUS[0]}
  OUTPUT=\$(tail -50 "\$OUTPUT_FILE")
  rm -f "\$OUTPUT_FILE"

  if [ "\$EXIT_CODE" -eq 0 ]; then
    echo "[runner] ✅ Agent completed successfully"
    break
  fi

  # Check for rate limit / token errors
  if echo "\$OUTPUT" | grep -qi "rate.limit\|429\|quota\|token.limit\|overloaded"; then
    RETRY=\$((RETRY + 1))
    if [ "\$RETRY" -gt "\$MAX_RETRIES" ]; then
      echo "[runner] ❌ Max retries reached"
      break
    fi
    # Fallback: opus → sonnet, sonnet → haiku
    if [ "\$MODEL" = "opus" ]; then
      MODEL="sonnet"
    elif [ "\$MODEL" = "sonnet" ]; then
      MODEL="haiku"
    fi
    echo "[runner] 🔄 Retrying with \$MODEL (attempt \$RETRY/\$MAX_RETRIES)..."
    sleep 10
    continue
  fi

  echo "[runner] ❌ Agent failed (exit \$EXIT_CODE)"
  break
done
RUNNER_EOF
chmod +x "$RUNNER_SCRIPT"

# ─── Spawn in tmux ──────────────────────────────────────────────────────────

tmux new-session -d -s "$TMUX_SESSION" -c "$WORK_DIR" "bash $RUNNER_SCRIPT" 2>/dev/null || {
  tmux kill-session -t "$TMUX_SESSION" 2>/dev/null || true
  sleep 1
  tmux new-session -d -s "$TMUX_SESSION" -c "$WORK_DIR" "bash $RUNNER_SCRIPT"
}

# ─── Start completion watcher ────────────────────────────────────────────────

if [ -f "$SCRIPTS_DIR/notify-on-complete.sh" ]; then
  bash "$SCRIPTS_DIR/notify-on-complete.sh" "$TMUX_SESSION" "$TASK_ID" "$WORK_DIR" "$PROJECT_DIR" "$BRANCH" &
  WATCHER_PID=$!
  echo "👁️ Watcher PID: $WATCHER_PID (polls every 60s, auto-notifies on completion)"
fi

# ─── Register task ──────────────────────────────────────────────────────────

TASKS_FILE="$SWARM_DIR/state/active-tasks.json"
mkdir -p "$SWARM_DIR/state"
if command -v jq &>/dev/null; then
  [ -f "$TASKS_FILE" ] || echo '[]' > "$TASKS_FILE"
  jq ". + [{\"id\": \"$TASK_ID\", \"tmux\": \"$TMUX_SESSION\", \"branch\": \"$BRANCH\", \"role\": \"$ROLE\", \"model\": \"$MODEL\", \"project\": \"$PROJECT_NAME\", \"started\": \"$(date -Iseconds)\"}]" "$TASKS_FILE" > "${TASKS_FILE}.tmp" && mv "${TASKS_FILE}.tmp" "$TASKS_FILE"
fi

echo "✅ Agent running in tmux session: $TMUX_SESSION"
echo "   Work dir: $WORK_DIR"
echo "   Branch: $BRANCH"
echo "   Log: $SWARM_DIR/logs/$TMUX_SESSION.log"
