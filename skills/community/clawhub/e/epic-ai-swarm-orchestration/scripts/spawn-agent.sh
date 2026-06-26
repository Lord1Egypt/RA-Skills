#!/usr/bin/env bash
# Universal spawn-agent.sh — Works with ANY project repo
#
# Usage: spawn-agent.sh <project-dir> <task-id> <description> [role-or-agent] [model] [reasoning]
#   project-dir: absolute path to the project root
#   task-id:     unique identifier for this task (used for branch name + tmux session)
#   description: task prompt (or path to a .md prompt file)
#   role-or-agent: architect | builder | reviewer | integrator | codex | gemini | deepseek
#                  (default: builder)
#   model:       model name override (default: per-agent from duty table)
#   reasoning:   low | medium | high (default: high)

set -euo pipefail

[ -f "$HOME/.bashrc" ] && source "$HOME/.bashrc" 2>/dev/null || true

SWARM_DIR="$(cd "$(dirname "$0")" && pwd)"
[ -f "$SWARM_DIR/swarm.conf" ] && source "$SWARM_DIR/swarm.conf" 2>/dev/null || true
[[ -n "${DEEPSEEK_API_KEY:-}" ]] && export DEEPSEEK_API_KEY
DUTY_TABLE="$SWARM_DIR/duty-table.json"
USAGE_LOG="$SWARM_DIR/usage-log.json"
TASKS_FILE="$SWARM_DIR/active-tasks.json"

PROJECT_DIR="${1:?Usage: spawn-agent.sh <project-dir> <task-id> <description> [role-or-agent] [model] [reasoning]}"
TASK_ID="${2:?Missing task-id}"
DESCRIPTION="${3:?Missing description}"
ROLE_OR_AGENT="${4:-builder}"
MODEL="${5:-}"
REASONING="${6:-high}"
ROLE=""
AGENT=""

[[ -z "$MODEL" ]] && MODEL=""

ENDORSE_FILE="$SWARM_DIR/endorsements/${TASK_ID}.endorsed"
if [[ ! -f "$ENDORSE_FILE" ]]; then
  echo ""
  echo "⛔ ENDORSEMENT REQUIRED"
  echo "   Task '$TASK_ID' has not been endorsed by the human/operator."
  echo ""
  echo "   To endorse, create the file:"
  echo "     mkdir -p $SWARM_DIR/endorsements"
  echo "     echo 'Endorsed by operator at $(date)' > $ENDORSE_FILE"
  echo ""
  echo "   Or use: endorse-task.sh $TASK_ID"
  echo ""
  exit 1
fi

IS_BATCH=$(grep -oP '(?<=Batch: ).*' "$ENDORSE_FILE" 2>/dev/null || echo "false")
ENDORSE_EPOCH=$(grep -oP '(?<=Endorsed_Epoch: )\d+' "$ENDORSE_FILE" 2>/dev/null || echo "0")
NOW_EPOCH=$(date +%s)
COOLDOWN=30

if [[ "$IS_BATCH" != "true" && "$ENDORSE_EPOCH" -gt 0 ]]; then
  ELAPSED=$(( NOW_EPOCH - ENDORSE_EPOCH ))
  if [[ $ELAPSED -lt $COOLDOWN ]]; then
    echo ""
    echo "⛔ COOLDOWN: Endorsement is only ${ELAPSED}s old (minimum ${COOLDOWN}s)."
    echo ""
    echo "   Wait $(( COOLDOWN - ELAPSED ))s or use spawn-batch.sh for batch work."
    echo ""
    exit 1
  fi
fi

echo "✅ Endorsement verified: $ENDORSE_FILE"

PROJECT_NAME="$(basename "$PROJECT_DIR")"
BRANCH="feat/${TASK_ID}"
WORKTREE_DIR="${PROJECT_DIR}-worktrees/${TASK_ID}"

if [[ "$ROLE_OR_AGENT" == "architect" || "$ROLE_OR_AGENT" == "builder" || "$ROLE_OR_AGENT" == "reviewer" || "$ROLE_OR_AGENT" == "integrator" ]]; then
  ROLE="$ROLE_OR_AGENT"
else
  AGENT="$ROLE_OR_AGENT"
  ROLE="builder"
fi

RESOLVED_CMD=""
if [[ -f "$DUTY_TABLE" ]] && command -v python3 &>/dev/null; then
  if [[ -x "$SWARM_DIR/fallback-swap.sh" ]]; then
    RESOLVED_CMD=$("$SWARM_DIR/fallback-swap.sh" "$ROLE" 2>/dev/null) || true
  fi

  if [[ -n "$RESOLVED_CMD" ]]; then
    if echo "$RESOLVED_CMD" | grep -q '^gemini'; then
      AGENT="gemini"
    elif echo "$RESOLVED_CMD" | grep -q '^codex'; then
      AGENT="codex"
    elif echo "$RESOLVED_CMD" | grep -q '^deepseek'; then
      AGENT="deepseek"
    fi

    if [[ -z "$MODEL" ]]; then
      MODEL=$(echo "$RESOLVED_CMD" | grep -oP '(?<=--model )\S+|(?<=-m )\S+' || true)
    fi
  fi

  if [[ -z "$AGENT" || -z "$MODEL" ]]; then
    readarray -t DUTY_INFO < <(python3 - <<'PY' "$DUTY_TABLE" "$ROLE"
import json, sys
path, role = sys.argv[1], sys.argv[2]
with open(path) as f:
    data = json.load(f)
entry = data.get('dutyTable', {}).get(role, {})
print(entry.get('agent', ''))
print(entry.get('model', ''))
print(entry.get('nonInteractiveCmd', ''))
PY
)
    [[ -z "$AGENT" ]] && AGENT="${DUTY_INFO[0]:-}"
    [[ -z "$MODEL" ]] && MODEL="${DUTY_INFO[1]:-}"
    [[ -z "$RESOLVED_CMD" ]] && RESOLVED_CMD="${DUTY_INFO[2]:-}"
  fi
fi

if [[ "$MODEL" == "high" || "$MODEL" == "medium" || "$MODEL" == "low" ]]; then
  REASONING="$MODEL"
  MODEL=""
fi

if [[ -z "$AGENT" ]]; then
  case "$ROLE_OR_AGENT" in
    codex|gemini|deepseek) AGENT="$ROLE_OR_AGENT" ;;
    *) AGENT="codex" ;;
  esac
fi
if [[ -z "$MODEL" ]]; then
  case "$AGENT" in
    codex)    MODEL="gpt-5.5" ;;
    gemini)   MODEL="gemini-2.5-pro" ;;
    deepseek) MODEL="deepseek-v4-pro-max" ;;
    *)        MODEL="gpt-5.5" ;;
  esac
fi

TMUX_SESSION="${AGENT}-${TASK_ID}"

echo "🐝 Spawning agent: $AGENT ($MODEL) for task: $TASK_ID"
echo "   Role: $ROLE"
echo "   Project: $PROJECT_NAME ($PROJECT_DIR)"

if [[ -f "$DESCRIPTION" ]]; then
  PROMPT=$(cat "$DESCRIPTION")
else
  PROMPT="$DESCRIPTION"
fi

WORKLOG="/tmp/worklog-${TMUX_SESSION}.md"
PROMPT="${PROMPT}

## 📝 WORK LOG — MANDATORY

You MUST maintain a work log throughout your session at: ${WORKLOG}

At the END, append a structured handoff with what changed, how to verify, known issues, integration notes, decisions made, and build status.

## ✅ WHEN YOU ARE DONE:
1. Finalize your work log
2. Commit all changes with a clear commit message
3. Push the branch: git push origin ${BRANCH}
4. Open a PR if applicable: gh pr create --fill
5. If this is a UI change, include a screenshot in the PR description
6. Exit when complete"

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

PROMPT_FILE="$SWARM_DIR/logs/${TMUX_SESSION}-prompt.md"
printf '%s' "$PROMPT" > "$PROMPT_FILE"

RUNNER_SCRIPT="$SWARM_DIR/logs/${TMUX_SESSION}-run.sh"
cat > "$RUNNER_SCRIPT" << 'RUNNER_HEREDOC_EOF'
#!/bin/bash
# Auto-retry runner with token-limit fallback
set -o pipefail

WORK_DIR="PLACEHOLDER_WORK_DIR"
PROMPT_FILE="PLACEHOLDER_PROMPT_FILE"
AGENT="PLACEHOLDER_AGENT"
MODEL="PLACEHOLDER_MODEL"
REASONING="PLACEHOLDER_REASONING"
ROLE="PLACEHOLDER_ROLE"
SWARM_DIR="PLACEHOLDER_SWARM_DIR"
TMUX_SESSION="PLACEHOLDER_TMUX_SESSION"
MAX_RETRIES=2

cd "$WORK_DIR"
PROMPT=$(cat "$PROMPT_FILE")

run_agent() {
  local agent="$1" model="$2"
  echo "[runner] Starting $agent/$model ..."
  case "$agent" in
    codex)
      # Use `codex exec` for non-interactive mode; `codex --full-auto "<prompt>"`
      # fails in tmux with "stdout is not a terminal". exec is the designed
      # one-shot entry point.
      # Use --dangerously-bypass-approvals-and-sandbox so codex can write to
      # the parent repo's .git/worktrees/ metadata (required for `git commit`
      # inside a worktree). Default workspace-write sandbox blocks ORIG_HEAD.lock.
      codex exec --model "$model" -c "model_reasoning_effort=$REASONING" --dangerously-bypass-approvals-and-sandbox "$PROMPT"
      ;;
    gemini)
      gemini --model "$model" -p "$PROMPT"
      ;;
    deepseek)
      deepseek -m "$model" -y -p "$PROMPT"
      ;;
  esac
}

is_token_error() {
  local output="$1" exit_code="$2"
  # Check exit code AND output for token/rate/quota errors
  if [[ "$exit_code" -ne 0 ]]; then
    if echo "$output" | grep -qi "rate.limit\|429\|quota\|token.limit\|exceeded.*limit\|capacity.*exceeded\|too.many.requests\|billing\|budget\|overloaded\|model.*limit"; then
      return 0
    fi
  fi
  return 1
}

CURRENT_AGENT="$AGENT"
CURRENT_MODEL="$MODEL"
RETRY=0

while true; do
  OUTPUT_FILE=$(mktemp)
  run_agent "$CURRENT_AGENT" "$CURRENT_MODEL" 2>&1 | tee "$OUTPUT_FILE"
  EXIT_CODE=${PIPESTATUS[0]}
  OUTPUT=$(tail -50 "$OUTPUT_FILE")
  rm -f "$OUTPUT_FILE"

  if [[ "$EXIT_CODE" -eq 0 ]]; then
    echo "[runner] ✅ Agent completed successfully"
    break
  fi

  if is_token_error "$OUTPUT" "$EXIT_CODE" && [[ $RETRY -lt $MAX_RETRIES ]]; then
    RETRY=$((RETRY + 1))
    echo "[runner] ⚠️ Token/rate limit hit on $CURRENT_AGENT/$CURRENT_MODEL (retry $RETRY/$MAX_RETRIES)"

    # Log to notifications
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    echo "🔄 [$TIMESTAMP] $TMUX_SESSION: $CURRENT_AGENT/$CURRENT_MODEL hit token limit — finding fallback (retry $RETRY/$MAX_RETRIES)" \
      >> "$SWARM_DIR/pending-notifications.txt"

    # Find fallback
    FALLBACK=$("$SWARM_DIR/model-fallback.sh" "$ROLE" "$CURRENT_AGENT" "$CURRENT_MODEL" 2>/dev/null) || {
      echo "[runner] ❌ No fallback available — giving up"
      echo "❌ [$TIMESTAMP] $TMUX_SESSION: No fallback model available after $CURRENT_AGENT/$CURRENT_MODEL failed" \
        >> "$SWARM_DIR/pending-notifications.txt"
      exit 1
    }

    IFS='|' read -r NEW_AGENT NEW_MODEL NEW_CMD <<< "$FALLBACK"
    echo "[runner] 🔄 Switching to $NEW_AGENT/$NEW_MODEL"
    echo "🔄 [$TIMESTAMP] $TMUX_SESSION: Switched from $CURRENT_AGENT/$CURRENT_MODEL → $NEW_AGENT/$NEW_MODEL" \
      >> "$SWARM_DIR/pending-notifications.txt"

    # Update duty table so future spawns use the working model
    python3 -c "
import json, datetime
with open('$SWARM_DIR/duty-table.json') as f: d = json.load(f)
role_entry = d.get('dutyTable', {}).get('$ROLE', {})
role_entry['fallback'] = {'agent': role_entry.get('agent',''), 'model': role_entry.get('model','')}
role_entry['agent'] = '$NEW_AGENT'
role_entry['model'] = '$NEW_MODEL'
role_entry['reason'] = 'AUTO-FALLBACK: $CURRENT_AGENT/$CURRENT_MODEL hit token limit'
if '$NEW_AGENT' == 'codex':
    role_entry['nonInteractiveCmd'] = 'codex exec --model $NEW_MODEL --full-auto'
elif '$NEW_AGENT' == 'gemini':
    role_entry['nonInteractiveCmd'] = 'gemini -m $NEW_MODEL -p'
elif '$NEW_AGENT' == 'deepseek':
    role_entry['nonInteractiveCmd'] = 'deepseek -m $NEW_MODEL -y -p'
d.setdefault('history', []).append({
    'date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
    'changes': 'AUTO-FALLBACK for $ROLE: $CURRENT_AGENT/$CURRENT_MODEL → $NEW_AGENT/$NEW_MODEL (token limit)',
    'dutyAssignments': '$ROLE=$NEW_AGENT/$NEW_MODEL'
})
with open('$SWARM_DIR/duty-table.json', 'w') as f: json.dump(d, f, indent=2)
" 2>/dev/null || echo "[runner] ⚠️ Duty table update failed (non-critical)"

    CURRENT_AGENT="$NEW_AGENT"
    CURRENT_MODEL="$NEW_MODEL"
    sleep 5  # Brief cooldown before retry
  else
    echo "[runner] Agent exited with code $EXIT_CODE (not a token error or max retries reached)"
    exit "$EXIT_CODE"
  fi
done
RUNNER_HEREDOC_EOF

# Replace placeholders with actual values
sed -i \
  -e "s|PLACEHOLDER_WORK_DIR|$WORK_DIR|g" \
  -e "s|PLACEHOLDER_PROMPT_FILE|$PROMPT_FILE|g" \
  -e "s|PLACEHOLDER_AGENT|$AGENT|g" \
  -e "s|PLACEHOLDER_MODEL|$MODEL|g" \
  -e "s|PLACEHOLDER_REASONING|$REASONING|g" \
  -e "s|PLACEHOLDER_ROLE|$ROLE|g" \
  -e "s|PLACEHOLDER_SWARM_DIR|$SWARM_DIR|g" \
  -e "s|PLACEHOLDER_TMUX_SESSION|$TMUX_SESSION|g" \
  "$RUNNER_SCRIPT"
chmod +x "$RUNNER_SCRIPT"

WRAPPED_CMD="bash $RUNNER_SCRIPT"

tmux new-session -d -s "$TMUX_SESSION" -c "$WORK_DIR" "$WRAPPED_CMD" 2>/dev/null || {
  echo "⚠️  tmux session $TMUX_SESSION already exists"
  exit 1
}

mkdir -p "$SWARM_DIR/logs"
tmux pipe-pane -t "$TMUX_SESSION" "cat >> $SWARM_DIR/logs/${TMUX_SESSION}.log"

nohup "$SWARM_DIR/notify-on-complete.sh" "$TMUX_SESSION" "Agent $TMUX_SESSION completed task: $TASK_ID ($PROJECT_NAME)" --review "$PROJECT_DIR" \
  >> "$SWARM_DIR/logs/${TMUX_SESSION}-watcher.log" 2>&1 &
WATCHER_PID=$!
echo "👁️ Watcher PID: $WATCHER_PID (polls every 60s, auto-notifies on completion)"

echo "✅ Agent running in tmux session: $TMUX_SESSION"
echo "   Work dir: $WORK_DIR"
echo "   Branch: $BRANCH"
echo "   Log: $SWARM_DIR/logs/${TMUX_SESSION}.log"
echo "   Watcher: PID $WATCHER_PID (auto-notify on complete)"

TIMESTAMP=$(date +%s)000
mkdir -p "$SWARM_DIR"
[[ -f "$TASKS_FILE" ]] || echo '{"tasks":[]}' > "$TASKS_FILE"

python3 -c "
import json
task = {
  'id': '$TASK_ID',
  'tmuxSession': '$TMUX_SESSION',
  'role': '$ROLE',
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

[[ -f "$USAGE_LOG" ]] || echo '[]' > "$USAGE_LOG"
python3 -c "
import json
from datetime import datetime
entry = {
  'timestamp': datetime.now().isoformat(),
  'taskId': '$TASK_ID',
  'role': '$ROLE',
  'agent': '$AGENT',
  'model': '$MODEL',
  'project': '$PROJECT_NAME'
}
with open('$USAGE_LOG') as f: data = json.load(f)
data.append(entry)
with open('$USAGE_LOG', 'w') as f: json.dump(data, f, indent=2)
" 2>/dev/null && echo "📊 Usage logged" || true
