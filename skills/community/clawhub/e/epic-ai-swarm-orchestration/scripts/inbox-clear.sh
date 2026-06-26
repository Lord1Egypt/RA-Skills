#!/usr/bin/env bash
# inbox-clear.sh — Remove task(s) from inbox
# Usage: inbox-clear.sh <task-id> [task-id2 ...]
#        inbox-clear.sh --all

set -euo pipefail

SWARM_DIR="$(cd "$(dirname "$0")" && pwd)"
INBOX="$SWARM_DIR/inbox.json"

if [[ $# -lt 1 ]]; then
  echo "Usage: inbox-clear.sh <task-id> [task-id2 ...]" >&2
  echo "       inbox-clear.sh --all" >&2
  exit 1
fi

if [[ ! -f "$INBOX" ]]; then
  echo "📥 Inbox is empty — nothing to clear"
  exit 0
fi

if [[ "$1" == "--all" ]]; then
  python3 - <<'PY' "$INBOX"
import json, sys

inbox_path = sys.argv[1]

with open(inbox_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

removed = len(data.get('tasks', []))
data['tasks'] = []

with open(inbox_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)
    f.write('\n')

print(f"🗑️  Cleared {removed} task{'s' if removed != 1 else ''} from inbox")
PY
  exit 0
fi

python3 - "$INBOX" "$@" <<'PY'
import json, sys

inbox_path = sys.argv[1]
ids_to_remove = set(sys.argv[2:])

with open(inbox_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

before = len(data.get('tasks', []))
remaining = [t for t in data['tasks'] if t.get('id') not in ids_to_remove]
removed_ids = [t['id'] for t in data['tasks'] if t.get('id') in ids_to_remove]
not_found = ids_to_remove - set(removed_ids)

data['tasks'] = remaining

with open(inbox_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)
    f.write('\n')

for rid in removed_ids:
    print(f"🗑️  Removed: {rid}")

for nf in sorted(not_found):
    print(f"⚠️  Not found: {nf}", file=sys.stderr)

after = len(remaining)
print(f"📋 Inbox: {after} task{'s' if after != 1 else ''} queued")

if not_found:
    sys.exit(1)
PY
