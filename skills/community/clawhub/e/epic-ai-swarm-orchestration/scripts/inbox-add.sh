#!/usr/bin/env bash
# inbox-add.sh — Add a task to the swarm inbox for later batching
#
# Usage: inbox-add.sh <project-dir> <task-id> <description> [priority]
#   priority: high | medium | low (default: medium)
#
# Examples:
#   inbox-add.sh "/path/to/project" fix-rotate "Fix screen rotation crash" high
#   inbox-add.sh "/path/to/project" add-export "Add CSV export button"

set -euo pipefail

SWARM_DIR="$(cd "$(dirname "$0")" && pwd)"
INBOX="$SWARM_DIR/inbox.json"

PROJECT_DIR="${1:?Usage: inbox-add.sh <project-dir> <task-id> <description> [priority]}"
TASK_ID="${2:?Missing task-id}"
DESCRIPTION="${3:?Missing description}"
PRIORITY="${4:-medium}"

if [[ ! "$PRIORITY" =~ ^(high|medium|low)$ ]]; then
  echo "Error: priority must be high, medium, or low (got: $PRIORITY)" >&2
  exit 1
fi

if [[ ! -f "$INBOX" ]]; then
  echo '{"tasks":[],"schema_version":1}' > "$INBOX"
fi

python3 - <<PY "$INBOX" "$PROJECT_DIR" "$TASK_ID" "$DESCRIPTION" "$PRIORITY"
import json, sys, datetime, os

inbox_path, project_dir, task_id, description, priority = sys.argv[1:6]

with open(inbox_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Check for duplicate id
for t in data['tasks']:
    if t['id'] == task_id:
        print(f"Error: task id '{task_id}' already exists in inbox", file=sys.stderr)
        sys.exit(1)

project = os.path.basename(project_dir.rstrip('/'))
entry = {
    'id': task_id,
    'project': project,
    'projectDir': project_dir,
    'description': description,
    'priority': priority,
    'addedAt': datetime.datetime.now().astimezone().isoformat(),
    'status': 'queued'
}
data['tasks'].append(entry)

with open(inbox_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)
    f.write('\n')

count = len(data['tasks'])
print(f"📥 Added to inbox: {task_id} ({project}) — priority: {priority}")
print(f"📋 Inbox: {count} task{'s' if count != 1 else ''} queued")
PY
