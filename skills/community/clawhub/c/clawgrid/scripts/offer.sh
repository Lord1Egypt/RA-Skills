#!/usr/bin/env bash
set -euo pipefail

# Manage Service Offerings on ClawGrid
#
# Usage:
#   Fixed pricing (default):
#     bash offer.sh create --title ... --desc ... --price_min 0.5 --price_max 5 --types browser_scrape,raw_fetch [--tags ...] [--turnaround 4] [--execution_notes "..." ] [--negotiation_rules "..."]
#   Per-unit pricing:
#     bash offer.sh create --title ... --desc ... --pricing_type per_unit --unit_price 0.01 --unit_label records --quantity_min 100 --quantity_max 10000 --types raw_fetch [--tags ...]
#   bash offer.sh list
#   bash offer.sh deactivate <offering_id>
#   bash offer.sh delete <offering_id>

SKILL_DIR="$HOME/.openclaw/workspace/skills/clawgrid-connector"
source "$SKILL_DIR/scripts/_clawgrid_env.sh"

[ ! -f "$CONFIG" ] && echo "ERROR: Config not found at $CONFIG" >&2 && exit 1

API_KEY=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_key'])")
API_BASE=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_base'])")

cmd="${1:-}"

case "$cmd" in
  create)
    shift
    TITLE=""; DESC=""; PRICE_MIN="0.5"; PRICE_MAX="5"; TYPES="browser_scrape"
    TAGS=""; TURNAROUND=""; EXECUTION_NOTES=""; NEGOTIATION_RULES=""
    PRICING_TYPE="fixed"; UNIT_PRICE=""; UNIT_LABEL=""; QUANTITY_MIN=""; QUANTITY_MAX=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --title)             TITLE="$2";             shift 2 ;;
        --desc)              DESC="$2";              shift 2 ;;
        --price_min)         PRICE_MIN="$2";         shift 2 ;;
        --price_max)         PRICE_MAX="$2";         shift 2 ;;
        --pricing_type)      PRICING_TYPE="$2";      shift 2 ;;
        --unit_price)        UNIT_PRICE="$2";        shift 2 ;;
        --unit_label)        UNIT_LABEL="$2";        shift 2 ;;
        --quantity_min)      QUANTITY_MIN="$2";       shift 2 ;;
        --quantity_max)      QUANTITY_MAX="$2";       shift 2 ;;
        --types)             TYPES="$2";              shift 2 ;;
        --tags)              TAGS="$2";               shift 2 ;;
        --turnaround)        TURNAROUND="$2";        shift 2 ;;
        --execution_notes)   EXECUTION_NOTES="$2";   shift 2 ;;
        --negotiation_rules) NEGOTIATION_RULES="$2"; shift 2 ;;
        *) shift ;;
      esac
    done
    [ -z "$TITLE" ] && echo "ERROR: --title required" >&2 && exit 1
    BODY=$(python3 -c "
import json
types = '$TYPES'.split(',')
body = {
  'title': '$TITLE',
  'description': '$DESC',
  'pricing_type': '$PRICING_TYPE',
  'price_currency': 'USD',
  'task_types': types,
  'is_active': True
}
if '$PRICING_TYPE' == 'per_unit':
    body['unit_price'] = float('$UNIT_PRICE') if '$UNIT_PRICE' else None
    if '$UNIT_LABEL':
        body['unit_label'] = '$UNIT_LABEL'
    if '$QUANTITY_MIN':
        body['quantity_min'] = int('$QUANTITY_MIN')
    if '$QUANTITY_MAX':
        body['quantity_max'] = int('$QUANTITY_MAX')
else:
    body['price_min'] = float('$PRICE_MIN')
    body['price_max'] = float('$PRICE_MAX')
tags_raw = '$TAGS'
if tags_raw:
    body['tags'] = [t.strip() for t in tags_raw.split(',')]
turnaround_raw = '$TURNAROUND'
if turnaround_raw:
    body['turnaround_hours'] = int(turnaround_raw)
if '$EXECUTION_NOTES':
    body['execution_notes'] = '$EXECUTION_NOTES'
if '$NEGOTIATION_RULES':
    body['negotiation_rules'] = '$NEGOTIATION_RULES'
print(json.dumps(body))
")
    RESP=$(curl -s -w "\n%{http_code}" -X POST "$API_BASE/api/lobster/me/offerings" \
      -H "Authorization: Bearer $API_KEY" \
      -H "Content-Type: application/json" \
      -d "$BODY" --max-time 15)
    ;;

  list)
    RESP=$(curl -s -w "\n%{http_code}" -X GET "$API_BASE/api/lobster/me/offerings" \
      -H "Authorization: Bearer $API_KEY" --max-time 15)
    ;;

  deactivate)
    OID="${2:-}"
    [ -z "$OID" ] && echo "ERROR: offering_id required" >&2 && exit 1
    RESP=$(curl -s -w "\n%{http_code}" -X PUT "$API_BASE/api/lobster/me/offerings/$OID" \
      -H "Authorization: Bearer $API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"is_active": false}' --max-time 15)
    ;;

  delete)
    OID="${2:-}"
    [ -z "$OID" ] && echo "ERROR: offering_id required" >&2 && exit 1
    RESP=$(curl -s -w "\n%{http_code}" -X DELETE "$API_BASE/api/lobster/me/offerings/$OID" \
      -H "Authorization: Bearer $API_KEY" --max-time 15)
    ;;

  *)
    echo "Usage: bash offer.sh <create|list|deactivate|delete> [options]" >&2
    exit 1
    ;;
esac

HTTP_CODE=$(echo "$RESP" | tail -1)
BODY=$(echo "$RESP" | sed '$d')

if [ "$HTTP_CODE" -ge 200 ] && [ "$HTTP_CODE" -lt 300 ]; then
  echo "$BODY"
  exit 0
else
  echo "Failed (HTTP $HTTP_CODE): $BODY" >&2
  exit 1
fi
