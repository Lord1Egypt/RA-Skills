#!/usr/bin/env bash
# Universal spawn-agent.sh — Works with ANY project repo
#
# Usage: spawn-agent.sh <project-dir> <task-id> <description> [agent] [model] [reasoning]
#   project-dir: absolute path to the project root
#   task-id:     unique identifier for this task (used for branch name + tmux session)
#   description: task prompt (or path to a .md prompt file)
#   agent:       claude | codex | gemini  (default: claude)
#   model:       model name override (default: per-agent from duty table)
#   reasoning:   low | medium | high (default: high)

set -euo pipefail

[ -f "$HOME/.bashrc" ] && source "$HOME/.bashrc" 2>/dev/null || true

SWARM_DIR="$(cd "$(dirname "$0")" && pwd)"
DUTY_TABLE="$SWARM_DIR/duty-table.json"
USAGE_LOG="$SWARM_DIR/usage-log.json"
TASKS_FILE="$SWARM_DIR/active-tasks.json"

PROJECT_DIR="${1:?Usage: spawn-agent.sh <project-dir> <task-id> <description> [agent] [model] [reasoning]}"
TASK_ID="${2:?Missing task-id}"
DESCRIPTION="${3:?Missing description}"
AGENT="${4:-claude}"
MODEL="${5:-}"
REASONING="${6:-high}"

# Strip empty model arg passed by spawn-batch
[[ -z "$MODEL" ]] && MODEL=""

# ============================================================
# ENDORSEMENT GATE — WB must approve before any work starts
# ============================================================
ENDORSE_FILE="$SWARM_DIR/endorsements/${TASK_ID}.endorsed"
if [[ ! -f "$ENDORSE_FILE" ]]; then
  echo ""
  echo "⛔ ENDORSEMENT REQUIRED"
  echo "   Task '$TASK_ID' has not been endorsed by WB."
  echo ""
  echo "   To endorse, create the file:"
  echo "     mkdir -p $SWARM_DIR/endorsements"
  echo "     echo 'Endorsed by WB at $(date)' > $ENDORSE_FILE"
  echo ""
  echo "   Or use: endorse-task.sh $TASK_ID"
  echo ""
  echo "   This gate exists because the orchestrator must:"
  echo "   1. Read project context (EOR, Obsidian, codebase)"
  echo "   2. Research and pressure-test the approach"
  echo "   3. Present a refined plan to WB"
  echo "   4. Get explicit approval BEFORE spawning agents"
  echo ""
  exit 1
fi
echo "✅ Endorsement verified: $ENDORSE_FILE"

PROJECT_NAME="$(basename "$PROJECT_DIR")"
BRANCH="feat/${TASK_ID}"
WORKTREE_DIR="${PROJECT_DIR}-worktrees/${TASK_ID}"
TMUX_SESSION="${AGENT}-${TASK_ID}"

# Load model from duty table if not specified
if [[ -z "$MODEL" ]] && [[ -f "$DUTY_TABLE" ]] && command -v python3 &>/dev/null; then
  # Map agent to duty role
  DUTY_ROLE=$(python3 -c "
import json
agent_map = {'claude': 'builder', 'codex': 'builder', 'gemini': 'builder'}
print(agent_map.get('$AGENT', 'builder'))
" 2>/dev/null || echo "builder")

  # Use fallback-swap to test + get working model (swaps duty table if primary fails)
  if [[ -x "$SWARM_DIR/fallback-swap.sh" ]]; then
    RESOLVED_CMD=$("$SWARM_DIR/fallback-swap.sh" "$DUTY_ROLE" 2>/dev/null) || true
    if [[ -n "$RESOLVED_CMD" ]]; then
      # Extract model from the resolved command
      MODEL=$(echo "$RESOLVED_CMD" | grep -oP '(?<=--model )\S+|(?<=-m )\S+' || true)
      # Also detect if agent changed (e.g. gemini fallback to claude)
      if echo "$RESOLVED_CMD" | grep -q "^claude"; then
        AGENT="claude"
      elif echo "$RESOLVED_CMD" | grep -q "^gemini"; then
        AGENT="gemini"
      elif echo "$RESOLVED_CMD" | grep -q "^codex"; then
        AGENT="codex"
      fi
    fi
  fi

  # If fallback-swap didn't resolve, try reading duty table directly
  if [[ -z "$MODEL" ]]; then
    MODEL=$(python3 -c "
import json
try:
  with open('$DUTY_TABLE') as f: d = json.load(f)
  table = d.get('dutyTable', {})
  print(table.get('$DUTY_ROLE', {}).get('model', ''))
except Exception:
  pass
" 2>/dev/null)
  fi
fi

# Sanitize: reasoning values are NOT model names
if [[ "$MODEL" == "high" || "$MODEL" == "medium" || "$MODEL" == "low" ]]; then
  REASONING="$MODEL"
  MODEL=""
fi

# Fallback defaults (last resort)
if [[ -z "$MODEL" ]]; then
  case "$AGENT" in
    codex)  MODEL="gpt-5.3-codex" ;;
    claude) MODEL="claude-sonnet-4-6" ;;
    gemini) MODEL="gemini-2.5-pro" ;;
    *)      MODEL="claude-sonnet-4-6" ;;
  esac
fi

# Update tmux session name in case agent changed
TMUX_SESSION="${AGENT}-${TASK_ID}"

echo "🐝 Spawning agent: $AGENT ($MODEL) for task: $TASK_ID"
echo "   Project: $PROJECT_NAME ($PROJECT_DIR)"

# Check if description is a file path
if [[ -f "$DESCRIPTION" ]]; then
  PROMPT=$(cat "$DESCRIPTION")
else
  PROMPT="$DESCRIPTION"
fi

# Work log path for this session
WORKLOG="/tmp/worklog-${TMUX_SESSION}.md"

# Append work log + completion instructions
PROMPT="${PROMPT}

## 📝 WORK LOG — MANDATORY

You MUST maintain a work log throughout your session at: ${WORKLOG}

**At the START of your work**, initialize the log:
\`\`\`bash
cat > ${WORKLOG} << 'EOF'
# Work Log: ${TMUX_SESSION}
## Task: ${TASK_ID} (${PROJECT_NAME})
## Branch: ${BRANCH}
---
EOF
\`\`\`

**As you work**, append entries to the log after each significant step:
\`\`\`bash
cat >> ${WORKLOG} << 'EOF'

### [Step N] <what you did>
- **Files changed:** list of files
- **What:** brief description of the change
- **Why:** reasoning / problem being solved
- **Decisions:** any tradeoffs or choices made
- **Issues found:** anything unexpected
EOF
\`\`\`

**At the END**, append a summary:
\`\`\`bash
cat >> ${WORKLOG} << 'EOF'

## Summary
- **Total files changed:** N
- **Key changes:** bullet list of what was built/fixed
- **Build status:** pass/fail
- **Known issues:** any remaining concerns
- **Integration notes:** what the next agent (reviewer/integrator) should know
EOF
\`\`\`

This work log is READ BY OTHER AGENTS in the pipeline (reviewers, integrators). Write it for them — be specific about what you changed and why. Vague notes like \"fixed stuff\" are useless. Include file paths, function names, and reasoning.

## ✅ WHEN YOU ARE DONE:
1. Finalize your work log with the summary section above
2. Commit all changes with a clear commit message
3. Push the branch: git push origin ${BRANCH}
4. Open a PR if applicable: gh pr create --fill
5. If this is a UI change, include a screenshot in the PR description
6. Exit when complete"

# Set up worktree if project has git
if [[ -d "$PROJECT_DIR/.git" ]]; then
  mkdir -p "$(dirname "$WORKTREE_DIR")"
  cd "$PROJECT_DIR"
  git fetch origin main 2>/dev/null || git fetch origin 2>/dev/null || true
  git worktree add "$WORKTREE_DIR" -b "$BRANCH" origin/main 2>/dev/null || {
    if [[ -d "$WORKTREE_DIR" ]]; then
      echo "⚠️  Worktree exists, reusing..."
    else
      git worktree add "$WORKTREE_DIR" -b "$BRANCH" HEAD 2>/dev/null || {
        echo "⚠️  Using project dir directly (no worktree)"
        WORKTREE_DIR="$PROJECT_DIR"
      }
    fi
  }
  WORK_DIR="$WORKTREE_DIR"
else
  echo "⚠️  No git repo — working in project dir directly"
  WORK_DIR="$PROJECT_DIR"
fi

# Install deps if needed
if [[ -f "$WORK_DIR/package.json" ]]; then
  cd "$WORK_DIR"
  if [[ -f "pnpm-lock.yaml" ]]; then
    pnpm install 2>/dev/null || true
  elif [[ -f "yarn.lock" ]]; then
    yarn install 2>/dev/null || true
  elif [[ -f "package-lock.json" ]]; then
    npm install 2>/dev/null || true
  fi
fi

# Write prompt to a file to avoid shell expansion issues with special chars
PROMPT_FILE="$SWARM_DIR/logs/${TMUX_SESSION}-prompt.md"
printf '%s' "$PROMPT" > "$PROMPT_FILE"

# Write a runner script that reads from the prompt file
NOTIFY_FILE="$SWARM_DIR/pending-notifications.txt"
RUNNER_SCRIPT="$SWARM_DIR/logs/${TMUX_SESSION}-run.sh"
cat > "$RUNNER_SCRIPT" << RUNNER_EOF
#!/bin/bash
cd "$WORK_DIR"
PROMPT=\$(cat "$PROMPT_FILE")
case "$AGENT" in
  codex)
    codex --model $MODEL -c "model_reasoning_effort=$REASONING" --full-auto "\$PROMPT"
    ;;
  claude)
    claude --model $MODEL --permission-mode bypassPermissions --print "\$PROMPT"
    ;;
  gemini)
    GEMINI_API_KEY="${GEMINI_API_KEY:-}" gemini --model $MODEL -p "\$PROMPT"
    ;;
esac
# NOTE: Do NOT write to pending-notifications.txt here.
# notify-on-complete.sh watcher handles all completion notifications
# (including Telegram). Writing here causes duplicate notifications.
RUNNER_EOF
chmod +x "$RUNNER_SCRIPT"

WRAPPED_CMD="bash $RUNNER_SCRIPT"

# Spawn tmux session
tmux new-session -d -s "$TMUX_SESSION" -c "$WORK_DIR" "$WRAPPED_CMD" 2>/dev/null || {
  echo "⚠️  tmux session $TMUX_SESSION already exists"
  exit 1
}

# Enable logging
mkdir -p "$SWARM_DIR/logs"
tmux pipe-pane -t "$TMUX_SESSION" "cat >> $SWARM_DIR/logs/${TMUX_SESSION}.log"

# AUTO-NOTIFICATION: Start background watcher that polls every 60s
# This is the REAL fix — doesn't depend on heartbeat or DZ remembering
nohup "$SWARM_DIR/notify-on-complete.sh" "$TMUX_SESSION" "Agent $TMUX_SESSION completed task: $TASK_ID ($PROJECT_NAME)" --review "$PROJECT_DIR" \
  >> "$SWARM_DIR/logs/${TMUX_SESSION}-watcher.log" 2>&1 &
WATCHER_PID=$!
echo "👁️ Watcher PID: $WATCHER_PID (polls every 60s, auto-notifies on completion)"

echo "✅ Agent running in tmux session: $TMUX_SESSION"
echo "   Work dir: $WORK_DIR"
echo "   Branch: $BRANCH"
echo "   Log: $SWARM_DIR/logs/${TMUX_SESSION}.log"
echo "   Watcher: PID $WATCHER_PID (auto-notify on complete)"

# Register task
TIMESTAMP=$(date +%s)000
mkdir -p "$SWARM_DIR"
[[ -f "$TASKS_FILE" ]] || echo '{"tasks":[]}' > "$TASKS_FILE"

python3 -c "
import json
task = {
  'id': '$TASK_ID',
  'tmuxSession': '$TMUX_SESSION',
  'agent': '$AGENT',
  'model': '$MODEL',
  'description': '''$DESCRIPTION'''[:200],
  'project': '$PROJECT_NAME',
  'projectDir': '$PROJECT_DIR',
  'worktree': '$WORK_DIR',
  'branch': '$BRANCH',
  'startedAt': $TIMESTAMP,
  'status': 'running',
  'retries': 0,
  'notifyOnComplete': True
}
with open('$TASKS_FILE') as f: data = json.load(f)
data['tasks'].append(task)
with open('$TASKS_FILE', 'w') as f: json.dump(data, f, indent=2)
" 2>/dev/null && echo "📋 Task registered" || echo "⚠️  Task registration failed (non-critical)"

# Log usage
[[ -f "$USAGE_LOG" ]] || echo '[]' > "$USAGE_LOG"
python3 -c "
import json
from datetime import datetime
entry = {
  'timestamp': datetime.now().isoformat(),
  'taskId': '$TASK_ID',
  'agent': '$AGENT',
  'model': '$MODEL',
  'project': '$PROJECT_NAME'
}
with open('$USAGE_LOG') as f: data = json.load(f)
data.append(entry)
with open('$USAGE_LOG', 'w') as f: json.dump(data, f, indent=2)
" 2>/dev/null && echo "📊 Usage logged" || true
