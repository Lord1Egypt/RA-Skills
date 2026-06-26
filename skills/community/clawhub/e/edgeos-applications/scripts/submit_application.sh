#!/usr/bin/env bash
set -euo pipefail

# Requires:
#   EDGEOS_BASE_URL (optional; default below)
#   JWT
# Arguments:
#   --payload-file <path-to-json>

source "$(dirname "$0")/env.sh"
JWT="${JWT:-}"
load_jwt_from_state
PAYLOAD_FILE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --payload-file)
      PAYLOAD_FILE="$2"; shift 2 ;;
    *)
      echo "Unknown arg: $1" >&2; exit 2 ;;
  esac
done

if [[ -z "$JWT" ]]; then
  echo '{"ok":false,"error":"JWT is required in env"}'
  exit 1
fi

if [[ -z "$PAYLOAD_FILE" || ! -f "$PAYLOAD_FILE" ]]; then
  echo '{"ok":false,"error":"--payload-file is required and must exist"}'
  exit 1
fi

HTTP_CODE=$(mktemp)
RESP_FILE=$(mktemp)

curl -sS -L -X POST "$BASE_URL/applications" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT" \
  --data-binary "@$PAYLOAD_FILE" \
  -o "$RESP_FILE" \
  -w '%{http_code}' > "$HTTP_CODE"

code=$(cat "$HTTP_CODE")
body=$(cat "$RESP_FILE")

rm -f "$HTTP_CODE" "$RESP_FILE"

if [[ "$code" -ge 200 && "$code" -lt 300 ]]; then
  app_id=$(echo "$body" | grep -o '"id"[[:space:]]*:[[:space:]]*[0-9]\+' | head -n1 | grep -o '[0-9]\+')
  status=$(echo "$body" | grep -o '"status"[[:space:]]*:[[:space:]]*"[^"]*"' | head -n1 | sed 's/.*"status"[[:space:]]*:[[:space:]]*"\([^"]*\)"/\1/')
  printf '{"ok":true,"http":%s,"application_id":"%s","status":"%s"}\n' "$code" "${app_id:-}" "${status:-}"
  exit 0
fi

# Duplicate application fallback: fetch existing application status instead of hard-failing.
if [[ "$code" == "409" ]]; then
  citizen_id=$(sed -n 's/.*"citizen_id"[[:space:]]*:[[:space:]]*\([0-9][0-9]*\).*/\1/p' "$PAYLOAD_FILE" | head -n1)
  popup_city_id=$(sed -n 's/.*"popup_city_id"[[:space:]]*:[[:space:]]*\([0-9][0-9]*\).*/\1/p' "$PAYLOAD_FILE" | head -n1)

  if [[ -n "${citizen_id:-}" && -n "${popup_city_id:-}" ]]; then
    lookup=$(curl -sS "$BASE_URL/applications?citizen_id=$citizen_id&popup_city_id=$popup_city_id" \
      -H "Authorization: Bearer $JWT")

    existing_id=$(echo "$lookup" | grep -o '"id"[[:space:]]*:[[:space:]]*[0-9]\+' | head -n1 | grep -o '[0-9]\+')
    existing_status=$(echo "$lookup" | grep -o '"status"[[:space:]]*:[[:space:]]*"[^"]*"' | head -n1 | sed 's/.*"status"[[:space:]]*:[[:space:]]*"\([^"]*\)"/\1/')

    if [[ -n "${existing_id:-}" ]]; then
      printf '{"ok":true,"http":409,"duplicate":true,"application_id":"%s","status":"%s"}\n' "${existing_id}" "${existing_status:-}"
      exit 0
    fi
  fi
fi

printf '{"ok":false,"http":%s,"error":"application_submit_failed"}\n' "$code"
exit 1
