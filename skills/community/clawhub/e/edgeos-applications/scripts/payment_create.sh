#!/usr/bin/env bash
set -euo pipefail

# Requires: JWT, EDGEOS_BASE_URL (optional)
# Args:
#   --application-id <id>
#   --product-id <id>
#   --attendee-id <id>
#   [--quantity <n>] (default 1)
#   [--insurance true|false] (default false)
#   [--custom-amount <number>] (optional)

source "$(dirname "$0")/env.sh"
JWT="${JWT:-}"
load_jwt_from_state
APPLICATION_ID=""
PRODUCT_ID=""
ATTENDEE_ID=""
QUANTITY="1"
INSURANCE="false"
CUSTOM_AMOUNT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --application-id) APPLICATION_ID="$2"; shift 2 ;;
    --product-id) PRODUCT_ID="$2"; shift 2 ;;
    --attendee-id) ATTENDEE_ID="$2"; shift 2 ;;
    --quantity) QUANTITY="$2"; shift 2 ;;
    --insurance) INSURANCE="$2"; shift 2 ;;
    --custom-amount) CUSTOM_AMOUNT="$2"; shift 2 ;;
    *) echo "Unknown arg: $1" >&2; exit 2 ;;
  esac
done

if [[ -z "$JWT" ]]; then
  echo '{"ok":false,"error":"JWT is required in env"}'
  exit 1
fi
if [[ -z "$APPLICATION_ID" || -z "$PRODUCT_ID" || -z "$ATTENDEE_ID" ]]; then
  echo '{"ok":false,"error":"Missing required args: --application-id --product-id --attendee-id"}'
  exit 1
fi

if [[ -n "$CUSTOM_AMOUNT" ]]; then
  PAYLOAD=$(cat <<JSON
{"application_id":$APPLICATION_ID,"products":[{"product_id":$PRODUCT_ID,"attendee_id":$ATTENDEE_ID,"quantity":$QUANTITY,"custom_amount":$CUSTOM_AMOUNT}],"insurance":$INSURANCE}
JSON
)
else
  PAYLOAD=$(cat <<JSON
{"application_id":$APPLICATION_ID,"products":[{"product_id":$PRODUCT_ID,"attendee_id":$ATTENDEE_ID,"quantity":$QUANTITY}],"insurance":$INSURANCE}
JSON
)
fi

body=$(curl -sS -L -X POST "$BASE_URL/payments" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT" \
  -d "$PAYLOAD")

payment_id=$(echo "$body" | grep -o '"id"[[:space:]]*:[[:space:]]*[0-9]\+' | head -n1 | grep -o '[0-9]\+')
status=$(echo "$body" | grep -o '"status"[[:space:]]*:[[:space:]]*"[^"]*"' | head -n1 | sed 's/.*"status"[[:space:]]*:[[:space:]]*"\([^"]*\)"/\1/')
checkout_url=$(echo "$body" | grep -o '"checkout_url"[[:space:]]*:[[:space:]]*"[^"]*"' | head -n1 | sed 's/.*"checkout_url"[[:space:]]*:[[:space:]]*"\([^"]*\)"/\1/')

printf '{"ok":true,"payment_id":"%s","status":"%s","checkout_url":"%s"}\n' "${payment_id:-}" "${status:-}" "${checkout_url:-}"
