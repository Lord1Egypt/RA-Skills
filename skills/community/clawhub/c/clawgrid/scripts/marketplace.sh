#!/usr/bin/env bash
set -euo pipefail

# Marketplace operations: browse, accept, decline requests and offerings.
#
# Usage:
#   bash marketplace.sh [task_type]              # browse open_bid tasks (default)
#   bash marketplace.sh offerings [keyword]      # browse other lobsters' services
#   bash marketplace.sh detail <offering_id>     # view offering detail + provider stats
#   bash marketplace.sh request <target_agent_id> --title ... --description ... [--offering_id ...] [--budget_max 1.5] [--quantity 500]
#   bash marketplace.sh list-requests            # list incoming service requests
#   bash marketplace.sh accept <request_id>      # accept a service request
#   bash marketplace.sh decline <request_id> [reason]  # decline a service request
#   bash marketplace.sh decline-all [reason]     # decline all pending requests

SKILL_DIR="$HOME/.openclaw/workspace/skills/clawgrid-connector"
source "$SKILL_DIR/scripts/_clawgrid_env.sh"

if [ ! -f "$CONFIG" ]; then
  echo "Config not found at $CONFIG — run setup first" >&2
  exit 1
fi

API_KEY=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_key'])")
API_BASE=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_base'])")

# --- List-requests subcommand ---
if [ "${1:-}" = "list-requests" ]; then
  RESP=$(curl -s -w "\n%{http_code}" \
    "$API_BASE/api/lobster/marketplace/requests" \
    -H "Authorization: Bearer $API_KEY" \
    --max-time 15)

  HTTP_CODE=$(echo "$RESP" | tail -1)
  BODY=$(echo "$RESP" | sed '$d')

  if [ "$HTTP_CODE" -ge 200 ] && [ "$HTTP_CODE" -lt 300 ]; then
    echo "$BODY"
    exit 0
  else
    echo "List requests failed (HTTP $HTTP_CODE): $BODY" >&2
    exit 1
  fi
fi

# --- Accept subcommand ---
if [ "${1:-}" = "accept" ]; then
  if [ $# -lt 2 ]; then
    echo "Usage: bash $0 accept <request_id>" >&2
    exit 1
  fi
  REQUEST_ID="$2"

  RESP=$(curl -s -w "\n%{http_code}" -X POST \
    "$API_BASE/api/lobster/marketplace/requests/$REQUEST_ID/accept" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    --max-time 15)

  HTTP_CODE=$(echo "$RESP" | tail -1)
  BODY=$(echo "$RESP" | sed '$d')

  if [ "$HTTP_CODE" -ge 200 ] && [ "$HTTP_CODE" -lt 300 ]; then
    echo "$BODY"
    exit 0
  else
    echo "Accept request failed (HTTP $HTTP_CODE): $BODY" >&2
    exit 1
  fi
fi

# --- Decline subcommand ---
if [ "${1:-}" = "decline" ]; then
  if [ $# -lt 2 ]; then
    echo "Usage: bash $0 decline <request_id> [reason]" >&2
    exit 1
  fi
  REQUEST_ID="$2"
  REASON="${3:-Declined by lobster}"

  RESP=$(curl -s -w "\n%{http_code}" -X POST \
    "$API_BASE/api/lobster/marketplace/requests/$REQUEST_ID/decline" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"reason\": \"$REASON\"}" \
    --max-time 15)

  HTTP_CODE=$(echo "$RESP" | tail -1)
  BODY=$(echo "$RESP" | sed '$d')

  if [ "$HTTP_CODE" -ge 200 ] && [ "$HTTP_CODE" -lt 300 ]; then
    echo "$BODY"
    exit 0
  else
    echo "Decline request failed (HTTP $HTTP_CODE): $BODY" >&2
    exit 1
  fi
fi

# --- Decline-all subcommand ---
if [ "${1:-}" = "decline-all" ]; then
  REASON="${2:-Declined by lobster}"

  RESP=$(curl -s -w "\n%{http_code}" \
    "$API_BASE/api/lobster/marketplace/requests" \
    -H "Authorization: Bearer $API_KEY" \
    --max-time 15)

  HTTP_CODE=$(echo "$RESP" | tail -1)
  BODY=$(echo "$RESP" | sed '$d')

  if [ "$HTTP_CODE" -lt 200 ] || [ "$HTTP_CODE" -ge 300 ]; then
    echo "List requests failed (HTTP $HTTP_CODE): $BODY" >&2
    exit 1
  fi

  PENDING_IDS=$(python3 -c "
import json, sys
data = json.loads(sys.argv[1])
reqs = data.get('requests', data if isinstance(data, list) else [])
for r in reqs:
    if r.get('status') == 'pending':
        print(r['id'])
" "$BODY" 2>/dev/null)

  if [ -z "$PENDING_IDS" ]; then
    echo '{"action":"decline_all","count":0,"message":"No pending requests to decline."}'
    exit 0
  fi

  COUNT=0
  FAILED=0
  while IFS= read -r rid; do
    DR=$(curl -s -w "\n%{http_code}" -X POST \
      "$API_BASE/api/lobster/marketplace/requests/$rid/decline" \
      -H "Authorization: Bearer $API_KEY" \
      -H "Content-Type: application/json" \
      -d "{\"reason\": \"$REASON\"}" \
      --max-time 10)
    DC=$(echo "$DR" | tail -1)
    if [ "$DC" -ge 200 ] && [ "$DC" -lt 300 ]; then
      COUNT=$((COUNT + 1))
    else
      FAILED=$((FAILED + 1))
    fi
  done <<< "$PENDING_IDS"

  echo "{\"action\":\"decline_all\",\"declined\":$COUNT,\"failed\":$FAILED,\"message\":\"Declined $COUNT pending request(s).\"}"
  exit 0
fi

# --- Detail subcommand ---
if [ "${1:-}" = "detail" ]; then
  if [ $# -lt 2 ]; then
    echo "Usage: bash $0 detail <offering_id>" >&2
    exit 1
  fi
  OFFERING_ID="$2"

  RESP=$(curl -s -w "\n%{http_code}" \
    "$API_BASE/api/lobster/marketplace/offerings/$OFFERING_ID" \
    -H "Authorization: Bearer $API_KEY" \
    --max-time 15)

  HTTP_CODE=$(echo "$RESP" | tail -1)
  BODY=$(echo "$RESP" | sed '$d')

  if [ "$HTTP_CODE" -ge 200 ] && [ "$HTTP_CODE" -lt 300 ]; then
    echo "$BODY"
    exit 0
  else
    echo "View offering detail failed (HTTP $HTTP_CODE): $BODY" >&2
    exit 1
  fi
fi

# --- Request subcommand (send a task request to another lobster) ---
if [ "${1:-}" = "request" ]; then
  if [ $# -lt 2 ]; then
    echo "Usage: bash $0 request <target_agent_id> --title ... --description ... [--offering_id ...] [--budget_max 1.5] [--quantity 500]" >&2
    exit 1
  fi
  TARGET_AGENT_ID="$2"
  shift 2

  TITLE=""; DESCRIPTION=""; OFFERING_ID=""; BUDGET_MAX=""; QUANTITY=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --title)       TITLE="$2";       shift 2 ;;
      --description) DESCRIPTION="$2"; shift 2 ;;
      --offering_id) OFFERING_ID="$2"; shift 2 ;;
      --budget_max)  BUDGET_MAX="$2";  shift 2 ;;
      --quantity)    QUANTITY="$2";     shift 2 ;;
      *) shift ;;
    esac
  done

  [ -z "$TITLE" ] && echo "ERROR: --title required" >&2 && exit 1
  [ -z "$DESCRIPTION" ] && echo "ERROR: --description required" >&2 && exit 1

  REQ_BODY=$(python3 -c "
import json
body = {
    'target_agent_id': '$TARGET_AGENT_ID',
    'title': '$TITLE',
    'description': '$DESCRIPTION',
    'budget_currency': 'USD',
}
if '$OFFERING_ID': body['offering_id'] = '$OFFERING_ID'
if '$BUDGET_MAX':  body['budget_max'] = float('$BUDGET_MAX')
if '$QUANTITY':    body['quantity'] = int('$QUANTITY')
print(json.dumps(body))
")

  RESP=$(curl -s -w "\n%{http_code}" -X POST \
    "$API_BASE/api/lobster/marketplace/requests" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d "$REQ_BODY" \
    --max-time 15)

  HTTP_CODE=$(echo "$RESP" | tail -1)
  BODY=$(echo "$RESP" | sed '$d')

  if [ "$HTTP_CODE" -ge 200 ] && [ "$HTTP_CODE" -lt 300 ]; then
    echo "$BODY"
    exit 0
  else
    echo "Send task request failed (HTTP $HTTP_CODE): $BODY" >&2
    exit 1
  fi
fi

# --- Offerings subcommand ---
if [ "${1:-}" = "offerings" ]; then
  KEYWORD="${2:-}"
  QUERY_PARAMS="limit=20"
  [ -n "$KEYWORD" ] && QUERY_PARAMS="${QUERY_PARAMS}&q=$KEYWORD"

  RESP=$(curl -s -w "\n%{http_code}" \
    "$API_BASE/api/lobster/marketplace/offerings?$QUERY_PARAMS" \
    -H "Authorization: Bearer $API_KEY" \
    --max-time 15)

  HTTP_CODE=$(echo "$RESP" | tail -1)
  BODY=$(echo "$RESP" | sed '$d')

  if [ "$HTTP_CODE" -lt 200 ] || [ "$HTTP_CODE" -ge 300 ]; then
    echo "Failed to browse offerings (HTTP $HTTP_CODE): $BODY" >&2
    exit 1
  fi

  python3 -c "
import json, sys
data = json.loads('''$BODY''')
items = data.get('items', data.get('offerings', []))
total = data.get('total', len(items))
if not items:
    print(json.dumps({'action':'offerings_empty','notify_owner':True,'total':0,'message':'No service offerings found.'}))
else:
    summaries = []
    for o in items:
        summaries.append({'id':o.get('id',''),'title':o.get('title',''),'task_type':o.get('task_type',''),'price':o.get('price'),'currency':o.get('currency','USD'),'description':(o.get('description','') or '')[:200],'agent_name':o.get('agent_name','')})
    print(json.dumps({'action':'offerings_browse','notify_owner':True,'total':total,'offerings':summaries,'message':f'Found {total} service offering(s).'}))
" 2>/dev/null
  exit 0
fi

# --- Default: open_bid tasks ---
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
