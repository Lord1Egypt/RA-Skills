#!/usr/bin/env bash
set -euo pipefail

# claim.sh — Standalone task claim by reference (#N, UUID, or title fragment).
#
# Usage:
#   bash claim.sh "#21"              Match title containing "#21"
#   bash claim.sh <uuid>             Claim by exact task_id
#   bash claim.sh "web scraping"     Match title fragment (case-insensitive)
#
# Reads pending_wake_actions.json first; falls back to GET /api/lobster/tasks.
# Outputs structured JSON to stdout; logs to stderr.

SKILL_DIR="$HOME/.openclaw/workspace/skills/clawgrid-connector"
source "$SKILL_DIR/scripts/_clawgrid_env.sh"

if [ ! -f "$CONFIG" ]; then
  echo '{"action":"error","message":"Config not found — run setup first"}' ; exit 1
fi

API_KEY=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_key'])")
API_BASE=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_base'])")

REF="${1:-}"
if [ -z "$REF" ]; then
  echo '{"action":"error","message":"Usage: claim.sh <reference> — #N, UUID, or title fragment"}' ; exit 1
fi

PENDING_FILE="$CLAWGRID_HOME/state/pending_wake_actions.json"

# --- Step 1: Resolve task_id from reference ---
RESOLVED=$(python3 -c "
import json, sys, re, os
from datetime import datetime, timezone

ref = sys.argv[1]
pending_path = sys.argv[2]
TTL_SECONDS = 1800

def match_action(action, ref):
    p = action.get('payload', {})
    tid = p.get('task_id', '')
    title = p.get('title', '')
    atype = action.get('type', '')
    if atype not in ('claim_task', 'execute_task', 'notification'):
        return None
    if tid and tid == ref:
        return tid
    ref_lower = ref.lower().strip()
    if ref_lower.startswith('#'):
        if ref_lower in title.lower():
            return tid
    else:
        uuid_re = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.I)
        if uuid_re.match(ref):
            if tid == ref:
                return tid
            return None
        if ref_lower in title.lower():
            return tid
    return None

result = {'task_id': '', 'source': '', 'title': ''}
now = datetime.now(timezone.utc)

if os.path.exists(pending_path):
    try:
        with open(pending_path) as f:
            data = json.load(f)
        for a in data.get('actions', []):
            written = a.get('_written_at', '')
            if written:
                try:
                    age = (now - datetime.fromisoformat(written)).total_seconds()
                    if age > TTL_SECONDS:
                        continue
                except Exception:
                    pass
            tid = match_action(a, ref)
            if tid:
                result = {
                    'task_id': tid,
                    'source': 'pending_wake_actions',
                    'title': a.get('payload', {}).get('title', ''),
                    'action_index': data.get('actions', []).index(a),
                }
                break
    except Exception:
        pass

print(json.dumps(result))
" "$REF" "$PENDING_FILE" 2>/dev/null || echo '{"task_id":"","source":""}')

TASK_ID=$(echo "$RESOLVED" | python3 -c "import json,sys; print(json.load(sys.stdin).get('task_id',''))" 2>/dev/null || true)
SOURCE=$(echo "$RESOLVED" | python3 -c "import json,sys; print(json.load(sys.stdin).get('source',''))" 2>/dev/null || true)
TITLE=$(echo "$RESOLVED" | python3 -c "import json,sys; print(json.load(sys.stdin).get('title',''))" 2>/dev/null || true)

# --- Step 2: Fallback — search via API ---
if [ -z "$TASK_ID" ]; then
  echo "[claim] No match in pending_wake_actions, searching API..." >&2
  SEARCH_RESP=$(curl -s -w "\n%{http_code}" \
    "$API_BASE/api/lobster/tasks?status=queued&limit=20" \
    -H "Authorization: Bearer $API_KEY" \
    --max-time 15 2>/dev/null || echo -e "\n000")

  SEARCH_CODE=$(echo "$SEARCH_RESP" | tail -1)
  SEARCH_BODY=$(echo "$SEARCH_RESP" | sed '$d')

  if [ "$SEARCH_CODE" -ge 200 ] && [ "$SEARCH_CODE" -lt 300 ]; then
    TASK_ID=$(echo "$SEARCH_BODY" | python3 -c "
import json, sys, re

ref = sys.argv[1]
data = json.load(sys.stdin)
items = data if isinstance(data, list) else data.get('items', data.get('tasks', []))
ref_lower = ref.lower().strip()
uuid_re = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.I)

for t in items:
    tid = t.get('id', '')
    title = t.get('title', '')
    if uuid_re.match(ref) and tid == ref:
        print(json.dumps({'task_id': tid, 'title': title})); sys.exit(0)
    if ref_lower.startswith('#') and ref_lower in title.lower():
        print(json.dumps({'task_id': tid, 'title': title})); sys.exit(0)
    if not ref_lower.startswith('#') and not uuid_re.match(ref) and ref_lower in title.lower():
        print(json.dumps({'task_id': tid, 'title': title})); sys.exit(0)
print(json.dumps({'task_id': '', 'title': ''}))
" "$REF" 2>/dev/null || echo '{"task_id":"","title":""}')

    TASK_ID_VAL=$(echo "$TASK_ID" | python3 -c "import json,sys; print(json.load(sys.stdin).get('task_id',''))" 2>/dev/null || true)
    TITLE=$(echo "$TASK_ID" | python3 -c "import json,sys; print(json.load(sys.stdin).get('title',''))" 2>/dev/null || true)
    TASK_ID="$TASK_ID_VAL"
    SOURCE="api_search"
  else
    echo "[claim] API search failed: HTTP $SEARCH_CODE" >&2
  fi
fi

if [ -z "$TASK_ID" ]; then
  echo "{\"action\":\"not_found\",\"reference\":\"$REF\",\"message\":\"No task matching '$REF' found in pending actions or API.\"}"
  exit 0
fi

echo "[claim] Resolved: task_id=$TASK_ID title=$TITLE source=$SOURCE" >&2

# --- Step 3: Claim the task ---
CLAIM_RESP=$(curl -s -w "\n%{http_code}" -X POST "$API_BASE/api/lobster/tasks/$TASK_ID/claim" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  --max-time 15)

CLAIM_CODE=$(echo "$CLAIM_RESP" | tail -1)
CLAIM_BODY=$(echo "$CLAIM_RESP" | sed '$d')

echo "[claim] HTTP $CLAIM_CODE: $CLAIM_BODY" >&2

if [ "$CLAIM_CODE" -ge 200 ] && [ "$CLAIM_CODE" -lt 300 ]; then
  # --- Step 4: Remove claimed task from pending file ---
  python3 -c "
import json, sys, os
path = sys.argv[1]
task_id = sys.argv[2]
if not os.path.exists(path):
    sys.exit(0)
try:
    with open(path) as f:
        data = json.load(f)
    before = len(data.get('actions', []))
    data['actions'] = [
        a for a in data.get('actions', [])
        if a.get('payload', {}).get('task_id') != task_id
    ]
    after = len(data['actions'])
    if after != before:
        with open(path, 'w') as f:
            json.dump(data, f, ensure_ascii=False)
except Exception:
    pass
" "$PENDING_FILE" "$TASK_ID" 2>/dev/null || true

  echo "{\"action\":\"claimed\",\"task_id\":\"$TASK_ID\",\"title\":\"$TITLE\",\"source\":\"$SOURCE\",\"claim_response\":$CLAIM_BODY}"
else
  CLAIM_ACTION=$(echo "$CLAIM_BODY" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    print(d.get('error', {}).get('action', 'unknown'))
except:
    print('unknown')
" 2>/dev/null || echo "unknown")
  echo "{\"action\":\"claim_failed\",\"task_id\":\"$TASK_ID\",\"title\":\"$TITLE\",\"http_code\":$CLAIM_CODE,\"server_action\":\"$CLAIM_ACTION\",\"message\":\"Claim failed (HTTP $CLAIM_CODE). Task may already be taken.\"}"
fi
