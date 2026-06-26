#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

WORKSPACE_A="$TMP_DIR/workspace-a"
WORKSPACE_B="$TMP_DIR/workspace-b"
mkdir -p "$WORKSPACE_A" "$WORKSPACE_B"

cat > "$TMP_DIR/openclaw.json" <<EOF
{
  "agents": {
    "defaults": {
      "workspace": "$WORKSPACE_A"
    },
    "list": [
      {"id": "alpha", "workspace": "$WORKSPACE_A", "identity": {"name": "Alpha"}},
      {"id": "beta", "workspace": "$WORKSPACE_B", "identity": {"name": "Beta"}}
    ]
  }
}
EOF

mkdir -p "$WORKSPACE_A/.agent-todo" "$WORKSPACE_B/.agent-todo"
cat > "$WORKSPACE_A/.agent-todo/local.json" <<EOF
{"agent_id":"alpha","label":"Alpha"}
EOF
cat > "$WORKSPACE_B/.agent-todo/local.json" <<EOF
{"agent_id":"beta","label":"Beta"}
EOF

cd "$ROOT"
export OPENCLAW_CONFIG="$TMP_DIR/openclaw.json"
export AGENT_TODO_WORKSPACE="$WORKSPACE_A"

bash ./script.sh init >/dev/null
bash ./script.sh add "Publish release" \
  --task-type publish \
  --source "forum:#19/reply:88" \
  --next-action "Push GitHub and publish ClawHub" \
  --success-criteria "GitHub and ClawHub updated" >/tmp/agent-todo-smoke-add.out

ADD_ID=$(sed -n 's/.*\[\([0-9a-f-]\+\)\].*/\1/p' /tmp/agent-todo-smoke-add.out | head -1)
[[ -n "$ADD_ID" ]]
[[ -f "$WORKSPACE_A/.agent-todo/tasks.json" ]]

grep -q 'owner_agent_id' "$WORKSPACE_A/.agent-todo/tasks.json"

authored=$(python3 - <<PY
import json
from pathlib import Path
print(json.loads(Path("$WORKSPACE_A/.agent-todo/tasks.json").read_text())["tasks"][0]["owner_agent_id"])
PY
)
[[ "$authored" == "alpha" ]]

bash ./script.sh plan "Open-source release" \
  --task-type publish \
  --source "chat:direct" \
  --steps "Update README; Push GitHub; Publish ClawHub" >/tmp/agent-todo-smoke-plan.out

grep -q 'step 1' /tmp/agent-todo-smoke-plan.out
grep -q 'step 2' /tmp/agent-todo-smoke-plan.out
grep -q 'step 3' /tmp/agent-todo-smoke-plan.out

bash ./script.sh run-pending --claim >/tmp/agent-todo-smoke-run.out
grep -q 'EXECUTE_NOW' /tmp/agent-todo-smoke-run.out

bash ./script.sh done "$ADD_ID" --note "GitHub pushed and ClawHub published" >/tmp/agent-todo-smoke-done.out
bash ./script.sh report "$ADD_ID" >/tmp/agent-todo-smoke-report.out
grep -q '【回帖内容】' /tmp/agent-todo-smoke-report.out

bash ./script.sh dispatch "Review release" \
  --to-agent beta \
  --task-type review \
  --source "chat:direct" \
  --next-action "Review release artifacts" \
  --success-criteria "Feedback delivered" >/tmp/agent-todo-smoke-dispatch.out

grep -q 'task dispatched' /tmp/agent-todo-smoke-dispatch.out
grep -q 'Review release' "$WORKSPACE_B/.agent-todo/tasks.json"

bash ./script.sh setup-heartbeat --all --write >/tmp/agent-todo-smoke-heartbeat.out
grep -q 'agent-todo:begin' "$WORKSPACE_A/HEARTBEAT.md"
grep -q 'agent-todo:begin' "$WORKSPACE_B/HEARTBEAT.md"
grep -Fq "AGENT_TODO_WORKSPACE=$WORKSPACE_A bash $ROOT/script.sh run-pending --claim" "$WORKSPACE_A/HEARTBEAT.md"
grep -Fq "AGENT_TODO_WORKSPACE=$WORKSPACE_B bash $ROOT/script.sh run-pending --claim" "$WORKSPACE_B/HEARTBEAT.md"

echo 'smoke test passed'
