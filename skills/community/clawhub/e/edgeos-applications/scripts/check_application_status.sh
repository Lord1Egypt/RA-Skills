#!/usr/bin/env bash
set -euo pipefail

# Requires:
#   EDGEOS_BASE_URL (optional)
#   JWT
# Arguments:
#   --application-id <id>
#   OR
#   --citizen-id <id> --popup-city-id <id>

source "$(dirname "$0")/env.sh"
JWT="${JWT:-}"
load_jwt_from_state
APPLICATION_ID=""
CITIZEN_ID=""
POPUP_CITY_ID=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --application-id)
      APPLICATION_ID="$2"; shift 2 ;;
    --citizen-id)
      CITIZEN_ID="$2"; shift 2 ;;
    --popup-city-id)
      POPUP_CITY_ID="$2"; shift 2 ;;
    *)
      echo "Unknown arg: $1" >&2; exit 2 ;;
  esac
done

if [[ -z "$JWT" ]]; then
  echo '{"ok":false,"error":"JWT is required in env"}'
  exit 1
fi

if [[ -z "$APPLICATION_ID" ]]; then
  if [[ -n "$CITIZEN_ID" && -n "$POPUP_CITY_ID" ]]; then
    lookup=$(curl -sS "$BASE_URL/applications?citizen_id=$CITIZEN_ID&popup_city_id=$POPUP_CITY_ID" \
      -H "Authorization: Bearer $JWT")
    APPLICATION_ID=$(echo "$lookup" | grep -o '"id"[[:space:]]*:[[:space:]]*[0-9]\+' | head -n1 | grep -o '[0-9]\+')

    if [[ -z "${APPLICATION_ID:-}" ]]; then
      printf '{"ok":false,"error":"No application found for citizen_id=%s popup_city_id=%s"}\n' "$CITIZEN_ID" "$POPUP_CITY_ID"
      exit 1
    fi
  else
    echo '{"ok":false,"error":"Provide --application-id OR (--citizen-id and --popup-city-id)"}'
    exit 1
  fi
fi

HTTP_CODE=$(mktemp)
RESP_FILE=$(mktemp)

curl -sS "$BASE_URL/applications/$APPLICATION_ID" \
  -H "Authorization: Bearer $JWT" \
  -o "$RESP_FILE" \
  -w '%{http_code}' > "$HTTP_CODE"

code=$(cat "$HTTP_CODE")
body=$(cat "$RESP_FILE")

rm -f "$HTTP_CODE" "$RESP_FILE"

if [[ "$code" -ge 200 && "$code" -lt 300 ]]; then
  status=$(echo "$body" | grep -o '"status"[[:space:]]*:[[:space:]]*"[^"]*"' | head -n1 | sed 's/.*"status"[[:space:]]*:[[:space:]]*"\([^"]*\)"/\1/')
  printf '{"ok":true,"http":%s,"application_id":"%s","status":"%s"}\n' "$code" "$APPLICATION_ID" "${status:-}"
else
  printf '{"ok":false,"http":%s,"application_id":"%s","error":"application_status_check_failed"}\n' "$code" "$APPLICATION_ID"
  exit 1
fi
