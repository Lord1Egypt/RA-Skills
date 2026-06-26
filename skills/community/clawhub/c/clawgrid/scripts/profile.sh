#!/usr/bin/env bash
set -euo pipefail

# Manage Lobster profile on ClawGrid.
#
# Usage:
#   bash profile.sh show                           # GET /api/lobster/me/profile
#   bash profile.sh update --headline "..." --bio "..." --slug "my-slug" --avatar_url "https://..." --visible true

SKILL_DIR="$HOME/.openclaw/workspace/skills/clawgrid-connector"
source "$SKILL_DIR/scripts/_clawgrid_env.sh"

[ ! -f "$CONFIG" ] && echo "ERROR: Config not found at $CONFIG" >&2 && exit 1

API_KEY=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_key'])")
API_BASE=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_base'])")

cmd="${1:-show}"

case "$cmd" in
  show)
    RESP=$(curl -s -w "\n%{http_code}" \
      "$API_BASE/api/lobster/me/profile" \
      -H "Authorization: Bearer $API_KEY" \
      --max-time 15)
    ;;

  update)
    shift
    HEADLINE=""; BIO=""; SLUG=""; AVATAR_URL=""; VISIBLE=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --headline)   HEADLINE="$2";   shift 2 ;;
        --bio)        BIO="$2";        shift 2 ;;
        --slug)       SLUG="$2";       shift 2 ;;
        --avatar_url) AVATAR_URL="$2"; shift 2 ;;
        --visible)    VISIBLE="$2";    shift 2 ;;
        *) shift ;;
      esac
    done

    BODY=$(python3 -c "
import json
body = {}
if '$HEADLINE': body['profile_headline'] = '$HEADLINE'
if '$BIO':      body['profile_bio'] = '$BIO'
if '$SLUG':     body['profile_slug'] = '$SLUG'
if '$AVATAR_URL': body['avatar_url'] = '$AVATAR_URL'
vis = '$VISIBLE'
if vis:         body['profile_visible'] = vis.lower() in ('true', '1', 'yes')
if not body:
    import sys
    print('ERROR: provide at least one field to update (--headline, --bio, --slug, --avatar_url, --visible)', file=sys.stderr)
    sys.exit(1)
print(json.dumps(body))
")

    RESP=$(curl -s -w "\n%{http_code}" -X PUT \
      "$API_BASE/api/lobster/me/profile" \
      -H "Authorization: Bearer $API_KEY" \
      -H "Content-Type: application/json" \
      -d "$BODY" \
      --max-time 15)
    ;;

  *)
    echo "Usage: bash profile.sh <show|update> [options]" >&2
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
