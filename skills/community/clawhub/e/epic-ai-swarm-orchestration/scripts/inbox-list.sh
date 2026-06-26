#!/usr/bin/env bash
# inbox-list.sh — Show current inbox contents
# Usage: inbox-list.sh [--json]

set -euo pipefail

SWARM_DIR="$(cd "$(dirname "$0")" && pwd)"
INBOX="$SWARM_DIR/inbox.json"

if [[ ! -f "$INBOX" ]]; then
  echo "📥 Inbox is empty"
  exit 0
fi

FLAG="${1:-}"

if [[ "$FLAG" == "--json" ]]; then
  cat "$INBOX"
  exit 0
fi

python3 - <<'PY' "$INBOX"
import json, sys

inbox_path = sys.argv[1]

with open(inbox_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

tasks = data.get('tasks', [])

if not tasks:
    print("📥 Inbox is empty")
    sys.exit(0)

count = len(tasks)
print(f"📥 Swarm Inbox ({count} task{'s' if count != 1 else ''})")
print("─" * 53)

PRIORITY_ICON = {
    'high':   '🔴 HIGH',
    'medium': '🟡 MED ',
    'low':    '🟢 LOW ',
}

for t in tasks:
    icon = PRIORITY_ICON.get(t.get('priority', 'medium'), '⚪ ???  ')
    tid = t.get('id', '')[:14].ljust(14)
    proj = t.get('project', '')[:12].ljust(12)
    desc = t.get('description', '')
    print(f"{icon} | {tid} | {proj} | {desc}")
PY
