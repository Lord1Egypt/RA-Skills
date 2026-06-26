#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="${SCRIPT_DIR}/../data"
MEMORY_FILE="${DATA_DIR}/emotional_memory.json"

mkdir -p "$DATA_DIR"
[ -f "$MEMORY_FILE" ] || echo '{"patterns":[],"growth":[],"preferences":[]}' > "$MEMORY_FILE"

ACTION="${1:-help}"
shift || true

case "$ACTION" in

  store)
    OBSERVATION="${1:?Usage: emotion_memory.sh store <observation> [--importance <level>] [--tags <csv>]}"
    shift
    IMPORTANCE="medium"
    TAGS=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --importance) IMPORTANCE="$2"; shift 2 ;;
        --tags)       TAGS="$2";       shift 2 ;;
        *)            shift ;;
      esac
    done

    ID="em_$(date +%s)_$$"
    TIMESTAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

    ENTRY=$(cat <<EOJSON
{
  "id": "$ID",
  "timestamp": "$TIMESTAMP",
  "observation": $(printf '%s' "$OBSERVATION" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))'),
  "importance": "$IMPORTANCE",
  "tags": $(printf '%s' "$TAGS" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read().split(",") if sys.stdin.read().strip() else []))' 2>/dev/null || echo '[]')
}
EOJSON
    )

    python3 -c "
import json, sys
with open('$MEMORY_FILE', 'r') as f:
    data = json.load(f)
entry = json.loads('''$ENTRY''')
data['patterns'].append(entry)
with open('$MEMORY_FILE', 'w') as f:
    json.dump(data, f, indent=2)
print(f'Stored: {entry[\"id\"]}')
"
    ;;

  search)
    QUERY="${1:?Usage: emotion_memory.sh search <query>}"
    python3 -c "
import json
with open('$MEMORY_FILE', 'r') as f:
    data = json.load(f)
query = '$QUERY'.lower()
results = []
for p in data['patterns']:
    if query in p.get('observation','').lower() or any(query in t.lower() for t in p.get('tags',[])):
        results.append(p)
if not results:
    print('No matching patterns found.')
else:
    for r in results[-10:]:
        print(f\"[{r['timestamp']}] ({r['importance']}) {r['observation']}\")
        if r.get('tags'):
            print(f\"  tags: {', '.join(r['tags'])}\")
"
    ;;

  summary)
    python3 -c "
import json
from collections import Counter
with open('$MEMORY_FILE', 'r') as f:
    data = json.load(f)
patterns = data.get('patterns', [])
if not patterns:
    print('No emotional patterns recorded yet.')
else:
    print(f'Total patterns: {len(patterns)}')
    imp = Counter(p['importance'] for p in patterns)
    print(f'  High: {imp.get(\"high\",0)}  Medium: {imp.get(\"medium\",0)}  Low: {imp.get(\"low\",0)}')
    tags = Counter(t for p in patterns for t in p.get('tags',[]) if t)
    if tags:
        print('Top tags:')
        for tag, count in tags.most_common(10):
            print(f'  {tag}: {count}')
    print()
    print('Recent patterns:')
    for p in patterns[-5:]:
        print(f\"  [{p['timestamp']}] {p['observation'][:80]}\")
"
    ;;

  list)
    LIMIT=10
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --limit) LIMIT="$2"; shift 2 ;;
        *)       shift ;;
      esac
    done
    python3 -c "
import json
with open('$MEMORY_FILE', 'r') as f:
    data = json.load(f)
patterns = data.get('patterns', [])
for p in patterns[-$LIMIT:]:
    print(f\"[{p['id']}] {p['timestamp']} ({p['importance']})\")
    print(f\"  {p['observation']}\")
    if p.get('tags'):
        print(f\"  tags: {', '.join(p['tags'])}\")
"
    ;;

  forget)
    MEMORY_ID="${1:?Usage: emotion_memory.sh forget <memory_id>}"
    python3 -c "
import json
with open('$MEMORY_FILE', 'r') as f:
    data = json.load(f)
before = len(data['patterns'])
data['patterns'] = [p for p in data['patterns'] if p['id'] != '$MEMORY_ID']
after = len(data['patterns'])
with open('$MEMORY_FILE', 'w') as f:
    json.dump(data, f, indent=2)
if before > after:
    print(f'Forgotten: $MEMORY_ID')
else:
    print(f'Not found: $MEMORY_ID')
"
    ;;

  help|*)
    cat <<EOF
emotional-persona: Emotion Memory Manager

Usage:
  emotion_memory.sh store <observation> [--importance low|medium|high] [--tags tag1,tag2]
  emotion_memory.sh search <query>
  emotion_memory.sh summary
  emotion_memory.sh list [--limit N]
  emotion_memory.sh forget <memory_id>

Examples:
  emotion_memory.sh store "User needs Grounding on Monday mornings" --importance high --tags "pattern,temporal"
  emotion_memory.sh search "work stress"
  emotion_memory.sh summary
EOF
    ;;
esac
