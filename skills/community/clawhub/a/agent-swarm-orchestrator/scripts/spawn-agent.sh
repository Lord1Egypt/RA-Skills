#!/bin/bash
# spawn-agent.sh - Create task, worktree, and launch coding agent in tmux
# Usage: ./spawn-agent.sh <project-name> "<task-description>" [base-branch] [priority] [task-name] [note-file] [task-key]

set -e
source "$(dirname "$0")/config.sh"

PROJECT_NAME=$1
TASK_DESCRIPTION=$2
BASE_BRANCH=${3:-""}
PRIORITY=${4:-"normal"}
TASK_NAME=${5:-""}
NOTE_FILE=${6:-""}
TASK_KEY=${7:-""}

if [ -z "$PROJECT_NAME" ] || [ -z "$TASK_DESCRIPTION" ]; then
    echo "Usage: $0 <project-name> '<task-description>' [base-branch] [priority]"
    echo "Available projects:"
    jq -r '.projects | keys[]' "$REGISTRY" 2>/dev/null | sed 's/^/  - /'
    exit 1
fi

# Read project config from registry
PROJECT_CONFIG=$(jq -r --arg p "$PROJECT_NAME" '.projects[$p] // empty' "$REGISTRY")
if [ -z "$PROJECT_CONFIG" ]; then
    echo "Error: Project '$PROJECT_NAME' not found in registry"
    exit 1
fi

REPO_URL=$(echo "$PROJECT_CONFIG" | jq -r '.repo // empty')
LOCAL_REPO=$(echo "$PROJECT_CONFIG" | jq -r '.local_repo // empty')
CONTEXT_PATH=$(echo "$PROJECT_CONFIG" | jq -r '.context_path // "context.md"')
BASE_BRANCH_CFG=$(echo "$PROJECT_CONFIG" | jq -r '.base_branch // "main"')
BASE_BRANCH="${BASE_BRANCH:-$BASE_BRANCH_CFG}"

if [ -z "$REPO_URL" ] || [ "$REPO_URL" = "null" ]; then
    echo "Error: Project '$PROJECT_NAME' has no remote configured"
    exit 1
fi

# Generate task ID (ASCII-safe)
SAFE_DESC=$(echo "$TASK_DESCRIPTION" | tr '[:upper:]' '[:lower:]' | \
    tr -cs 'a-z0-9' '-' | tr -s '-' | sed 's/^-//;s/-$//' | cut -c1-28)
[ -z "$SAFE_DESC" ] && SAFE_DESC="task-$(echo "$TASK_DESCRIPTION" | md5 | cut -c1-8)"

TASK_ID="$(date +%s)-${SAFE_DESC}"
TMUX_SESSION="agent-${TASK_ID}"
WORKTREE="${SWARM_WORKTREE_BASE}/${TASK_ID}"
LOG_FILE="${LOGS_DIR}/${TASK_ID}.log"
PROMPT_FILE="${LOGS_DIR}/${TASK_ID}.prompt"
BRANCH_NAME="feat/${TASK_ID}"

touch "$LOG_FILE"

echo "========================================"
echo "🚀 Spawning Agent (${SWARM_CODING_AGENT})"
echo "========================================"
echo "Project:  $PROJECT_NAME"
echo "Task ID:  $TASK_ID"
echo "Branch:   $BRANCH_NAME"
echo "Worktree: $WORKTREE"
echo ""

# Register task
jq --arg id "$TASK_ID" \
   --arg project "$PROJECT_NAME" \
   --arg session "$TMUX_SESSION" \
   --arg worktree "$WORKTREE" \
   --arg desc "$TASK_DESCRIPTION" \
   --arg branch "$BRANCH_NAME" \
   --arg priority "$PRIORITY" \
   --arg taskName "$TASK_NAME" \
   --arg noteFile "$NOTE_FILE" \
   --arg taskKey "$TASK_KEY" \
   '.tasks += [{
     "id": $id,
     "project": $project,
     "tmuxSession": $session,
     "worktree": $worktree,
     "description": $desc,
     "branch": $branch,
     "priority": $priority,
     "taskName": $taskName,
     "noteFile": $noteFile,
     "taskKey": $taskKey,
     "status": "starting",
     "startedAt": (now * 1000 | floor),
     "retryCount": 0,
     "notifyOnComplete": true
   }]' "$TASKS_FILE" > "${TASKS_FILE}.tmp" && mv "${TASKS_FILE}.tmp" "$TASKS_FILE"

# ── Phase 1: Prepare worktree ────────────────────────────────────────
echo "⏳ Preparing worktree..."

mkdir -p "$(dirname "$LOCAL_REPO")" "$SWARM_WORKTREE_BASE"

if [ ! -d "$LOCAL_REPO" ]; then
    echo "  Cloning $REPO_URL..."
    git clone "$REPO_URL" "$LOCAL_REPO" 2>&1 | tee -a "$LOG_FILE"
fi

cd "$LOCAL_REPO"
git fetch origin >> "$LOG_FILE" 2>&1
git checkout "$BASE_BRANCH" >> "$LOG_FILE" 2>&1
git pull origin "$BASE_BRANCH" >> "$LOG_FILE" 2>&1

if [ -d "$WORKTREE" ]; then
    git worktree remove -f "$WORKTREE" 2>/dev/null || rm -rf "$WORKTREE"
fi
git branch -D "$BRANCH_NAME" 2>/dev/null || true

git worktree add -b "$BRANCH_NAME" "$WORKTREE" "$BASE_BRANCH" >> "$LOG_FILE" 2>&1
echo "  ✓ Worktree ready (branch: $BRANCH_NAME)"

# ── Phase 2: Install dependencies ────────────────────────────────────
cd "$WORKTREE"
if [ -f package.json ]; then
    echo "⏳ Installing dependencies..."
    npm install >> "$LOG_FILE" 2>&1
    echo "  ✓ Done"
fi

# ── Phase 3: Build prompt file ────────────────────────────────────────
CONTEXT_SECTION=""
CONTEXT_FILE="${LOCAL_REPO}/${CONTEXT_PATH}"
[ -f "$CONTEXT_FILE" ] && CONTEXT_SECTION=$(cat "$CONTEXT_FILE")

{
    echo "You are working on project: ${PROJECT_NAME}"
    echo "Task: ${TASK_DESCRIPTION}"
    echo "Priority: ${PRIORITY}"
    echo "Working directory: ${WORKTREE}"
    echo "Branch: ${BRANCH_NAME}"
    echo ""
    echo "--- PROJECT CONTEXT ---"
    echo "${CONTEXT_SECTION}"
    echo "--- END CONTEXT ---"
    echo ""
    echo "Instructions:"
    echo "1. Read existing code carefully before making changes"
    echo "2. Follow existing code style and architecture"
    echo "3. Make clean atomic commits with clear messages"
    echo "4. When done: push branch to origin"
    echo "5. Do NOT create MR/PR — that will be handled automatically after review"
    echo "6. Run tests if available"
    echo "7. Definition of done: code committed + pushed to origin"
    echo "8. After completing all work, summarize what you did."
    echo "9. If your changes introduce new features, gameplay changes, new modules, architecture changes, or add key files, update context.md (${CONTEXT_PATH}) in the project root accordingly. Only skip for trivial config/formatting changes."
    echo ""
    echo "Start working now."
} > "$PROMPT_FILE"

echo "  ✓ Prompt ready"

# ── Phase 4: Launch tmux session ──────────────────────────────────────
jq --arg id "$TASK_ID" \
   '.tasks |= map(if .id == $id then .status = "running" else . end)' \
   "$TASKS_FILE" > "${TASKS_FILE}.tmp" && mv "${TASKS_FILE}.tmp" "$TASKS_FILE"

/usr/local/bin/tmux new-session -d -s "$TMUX_SESSION" -c "$WORKTREE" \
    "$SCRIPTS_DIR/run-agent.sh" "$TASK_ID" "$PROMPT_FILE" "$LOG_FILE"

# Notification: task started
{
    echo "🚀 TASK_STARTED"
    echo "Project: ${PROJECT_NAME}"
    echo "Task: ${TASK_DESCRIPTION:0:80}"
    echo "Task ID: ${TASK_ID}"
    echo "Agent: ${SWARM_CODING_AGENT}"
    echo "tmux: tmux attach -t ${TMUX_SESSION}"
    echo "tail: tail -f ${LOG_FILE}"
} > "${LOGS_DIR}/${TASK_ID}.notification"
[ -x "${SCRIPTS_DIR}/send-notifications.sh" ] && "${SCRIPTS_DIR}/send-notifications.sh" >/dev/null 2>&1 || true

echo ""
echo "✅ Agent launched!"
echo ""
echo "Monitor:"
echo "  tmux attach -t ${TMUX_SESSION}"
echo "  tail -f ${LOG_FILE}"
echo ""
echo "Task ID: $TASK_ID"
