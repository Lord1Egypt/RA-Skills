#!/usr/bin/env bash
# Codex Swarm — Spawn batch + integration watcher
# Usage: spawn-batch.sh <project-dir> <batch-id> <description> <tasks-json>
set -euo pipefail

SWARM_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPTS_DIR="$SWARM_DIR/scripts"
[ -f "$SWARM_DIR/config/swarm.conf" ] && source "$SWARM_DIR/config/swarm.conf"

PROJECT_DIR="${1:?Usage: spawn-batch.sh <project-dir> <batch-id> <desc> <tasks.json>}"
BATCH_ID="${2:?Missing batch-id}"
BATCH_DESC="${3:?Missing description}"
TASKS_JSON="${4:?Missing tasks JSON}"

TASK_COUNT=$(jq length "$TASKS_JSON")
echo "🐝 Batch $BATCH_ID: spawning $TASK_COUNT agents"

TMUX_SESSIONS=()
for i in $(seq 0 $((TASK_COUNT - 1))); do
  TASK_ID=$(jq -r ".[$i].id" "$TASKS_JSON")
  bash "$SCRIPTS_DIR/endorse-task.sh" "$TASK_ID"
done

sleep "${SWARM_ENDORSEMENT_COOLDOWN:-30}"

for i in $(seq 0 $((TASK_COUNT - 1))); do
  TASK_ID=$(jq -r ".[$i].id" "$TASKS_JSON")
  TASK_DESC=$(jq -r ".[$i].description" "$TASKS_JSON")
  TASK_ROLE=$(jq -r ".[$i].role // \"builder\"" "$TASKS_JSON")
  TASK_MODEL=$(jq -r ".[$i].model // \"\"" "$TASKS_JSON")
  TASK_REASONING=$(jq -r ".[$i].reasoning // \"\"" "$TASKS_JSON")
  bash "$SCRIPTS_DIR/spawn-agent.sh" "$PROJECT_DIR" "$TASK_ID" "$TASK_DESC" "$TASK_ROLE" "$TASK_MODEL" "$TASK_REASONING"
  TMUX_SESSIONS+=("codex-$TASK_ID")
done

if [ -f "$SCRIPTS_DIR/integration-watcher.sh" ]; then
  SESSIONS_STR="${TMUX_SESSIONS[*]}"
  bash "$SCRIPTS_DIR/integration-watcher.sh" "$PROJECT_DIR" "$BATCH_ID" "$SESSIONS_STR" &
  echo "🔗 Integration watcher started (PID: $!)"
fi

mkdir -p "$SWARM_DIR/logs"
cat > "$SWARM_DIR/logs/batch-${BATCH_ID}.json" << EOF
{"batchId":"$BATCH_ID","project":"$PROJECT_DIR","desc":"$BATCH_DESC","created":"$(date -Iseconds)","sessions":$(printf '%s\n' "${TMUX_SESSIONS[@]}" | jq -R . | jq -s .)}
EOF
echo "🧾 Batch: $SWARM_DIR/logs/batch-${BATCH_ID}.json"
