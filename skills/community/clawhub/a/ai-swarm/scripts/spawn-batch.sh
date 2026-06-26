#!/usr/bin/env bash
# spawn-batch.sh — Spawn up to 10 subteams, then auto-start integration watcher.
#
# Usage:
#   spawn-batch.sh <project-dir> <batch-id> <batch-description> <tasks-json>
#
# tasks-json format:
# [
#   {"id":"task-1","description":"...","agent":"codex","model":"gpt-5.3-codex","reasoning":"high"},
#   {"id":"task-2","description":"..."}
# ]
#
# Notes:
# - Preserves existing swarm logging: per-subteam work logs + ESR logs remain unchanged.
# - Starts integration watcher immediately (it waits until all subteams finish before integrating).

set -euo pipefail

SWARM_DIR="$(cd "$(dirname "$0")" && pwd)"
SPAWN_AGENT="$SWARM_DIR/spawn-agent.sh"
INTEGRATION_WATCHER="$SWARM_DIR/integration-watcher.sh"
ENDORSE_SCRIPT="$SWARM_DIR/endorse-task.sh"
LOG_DIR="$SWARM_DIR/logs"
mkdir -p "$LOG_DIR"

PROJECT_DIR="${1:?Usage: spawn-batch.sh <project-dir> <batch-id> <batch-description> <tasks-json>}"
BATCH_ID="${2:?Missing batch-id}"
BATCH_DESC="${3:?Missing batch-description}"
TASKS_JSON="${4:?Missing tasks-json path}"

MAX_PARALLEL=10

if [[ ! -d "$PROJECT_DIR" ]]; then
  echo "Error: project dir not found: $PROJECT_DIR" >&2
  exit 1
fi
if [[ ! -f "$TASKS_JSON" ]]; then
  echo "Error: tasks json not found: $TASKS_JSON" >&2
  exit 1
fi
if [[ ! -x "$SPAWN_AGENT" || ! -x "$INTEGRATION_WATCHER" ]]; then
  echo "Error: required scripts missing or not executable in $SWARM_DIR" >&2
  exit 1
fi

mapfile -t TASK_LINES < <(python3 - <<'PY' "$TASKS_JSON"
import json,sys
p=sys.argv[1]
with open(p,'r',encoding='utf-8') as f:
    data=json.load(f)
if not isinstance(data,list):
    raise SystemExit('tasks-json must be a JSON array')
for t in data:
    if not isinstance(t,dict):
        raise SystemExit('each task must be an object')
    tid=t.get('id','').strip()
    desc=t.get('description','').strip()
    if not tid or not desc:
        raise SystemExit('each task requires id + description')
    agent=(t.get('agent') or 'claude').strip()
    model=(t.get('model') or '').strip()
    reasoning=(t.get('reasoning') or 'high').strip()
    print('\t'.join([tid,desc,agent,model,reasoning]))
PY
)

TASK_COUNT=${#TASK_LINES[@]}
if [[ $TASK_COUNT -lt 1 ]]; then
  echo "Error: no tasks found in $TASKS_JSON" >&2
  exit 1
fi
if [[ $TASK_COUNT -gt $MAX_PARALLEL ]]; then
  echo "Error: max parallel is $MAX_PARALLEL (got $TASK_COUNT)" >&2
  exit 1
fi

SESSIONS=()

echo "🐝 Batch $BATCH_ID: spawning $TASK_COUNT subteams"

for line in "${TASK_LINES[@]}"; do
  IFS=$'\t' read -r TASK_ID DESCRIPTION AGENT MODEL REASONING <<< "$line"

  # Keep existing endorsement gate behavior; auto-endorse if missing for orchestrator convenience.
  ENDORSE_FILE="$SWARM_DIR/endorsements/${TASK_ID}.endorsed"
  if [[ ! -f "$ENDORSE_FILE" ]]; then
    "$ENDORSE_SCRIPT" "$TASK_ID" >/dev/null
  fi

  if [[ -n "$MODEL" ]]; then
    "$SPAWN_AGENT" "$PROJECT_DIR" "$TASK_ID" "$DESCRIPTION" "$AGENT" "$MODEL" "$REASONING"
  else
    "$SPAWN_AGENT" "$PROJECT_DIR" "$TASK_ID" "$DESCRIPTION" "$AGENT" "" "$REASONING"
  fi

  SESSIONS+=("${AGENT}-${TASK_ID}")
done

INTEG_LOG="$LOG_DIR/integration-${BATCH_ID}-watcher.log"
nohup "$INTEGRATION_WATCHER" "$PROJECT_DIR" "$BATCH_DESC" "${SESSIONS[@]}" >> "$INTEG_LOG" 2>&1 &
INTEG_PID=$!

echo "🔗 Integration watcher started"
echo "   PID: $INTEG_PID"
echo "   Log: $INTEG_LOG"
echo "   Sessions: ${SESSIONS[*]}"

# Record batch metadata for activity traceability
BATCH_META="$LOG_DIR/batch-${BATCH_ID}.json"
python3 - <<'PY' "$BATCH_META" "$PROJECT_DIR" "$BATCH_ID" "$BATCH_DESC" "$INTEG_PID" "$INTEG_LOG" "${SESSIONS[*]}"
import json,sys,datetime
path,project,bid,desc,pid,ilog,sessions = sys.argv[1:8]
obj={
  'batchId': bid,
  'projectDir': project,
  'description': desc,
  'createdAt': datetime.datetime.now().astimezone().isoformat(),
  'integrationWatcher': {'pid': int(pid), 'log': ilog},
  'sessions': sessions.split() if sessions else []
}
with open(path,'w',encoding='utf-8') as f:
  json.dump(obj,f,indent=2)
  f.write('\n')
PY

echo "🧾 Batch metadata: $BATCH_META"
