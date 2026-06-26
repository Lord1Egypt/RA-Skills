#!/usr/bin/env bash
set -euo pipefail

# Browse open_bid tasks in the marketplace and output bid instructions.
#
# Usage: bash marketplace.sh [task_type]
# Example: bash marketplace.sh raw_fetch

SKILL_DIR="$HOME/.openclaw/workspace/skills/clawgrid-connector"
source "$SKILL_DIR/scripts/_clawgrid_env.sh"

if [ ! -f "$CONFIG" ]; then
  echo "Config not found at $CONFIG — run setup first" >&2
  exit 1
fi

API_KEY=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_key'])")
API_BASE=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_base'])")

TASK_TYPE_FILTER="${1:-}"
QUERY_PARAMS="limit=20"
if [ -n "$TASK_TYPE_FILTER" ]; then
  QUERY_PARAMS="${QUERY_PARAMS}&task_type=$TASK_TYPE_FILTER"
fi

RESP=$(curl -s -w "\n%{http_code}" \
  "$API_BASE/api/lobster/marketplace/open-tasks?$QUERY_PARAMS" \
  -H "Authorization: Bearer $API_KEY" \
  --max-time 15)

HTTP_CODE=$(echo "$RESP" | tail -1)
BODY=$(echo "$RESP" | sed '$d')

if [ "$HTTP_CODE" -lt 200 ] || [ "$HTTP_CODE" -ge 300 ]; then
  echo "Failed to browse marketplace (HTTP $HTTP_CODE): $BODY" >&2
  exit 1
fi

python3 -c "
import json, sys

data = json.loads('''$BODY''')
items = data.get('items', [])
total = data.get('total', 0)

if not items:
    print(json.dumps({
        'action': 'marketplace_empty',
        'notify_owner': True,
        'total': 0,
        'message': 'No open bid tasks available in the marketplace right now.',
    }))
    sys.exit(0)

task_summaries = []
for t in items:
    task_summaries.append({
        'id': t['id'],
        'title': t.get('title', 'Untitled'),
        'task_type': t.get('task_type', ''),
        'budget_max': t.get('budget_max'),
        'budget_currency': t.get('budget_currency', 'USD'),
        'deadline': t.get('deadline'),
        'description_preview': (t.get('natural_language_desc', '') or '')[:200],
    })

bid_script = '$SKILL_DIR/scripts/bid.sh'
result = {
    'action': 'marketplace_browse',
    'notify_owner': True,
    'total': total,
    'tasks': task_summaries,
    'bid_command': f'bash {bid_script} <task_id> <amount> [message]',
    'message': f'Found {total} open bid task(s) in the marketplace. '
               f'To place a bid: bash {bid_script} <task_id> <your_bid_amount> \"optional message\"',
}
print(json.dumps(result))
" 2>/dev/null
