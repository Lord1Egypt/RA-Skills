#!/usr/bin/env bash
set -euo pipefail

# Requires: JWT, EDGEOS_BASE_URL (optional)
# Args: --payment-id <id>

source "$(dirname "$0")/env.sh"
JWT="${JWT:-}"
load_jwt_from_state
PAYMENT_ID=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --payment-id) PAYMENT_ID="$2"; shift 2 ;;
    *) echo "Unknown arg: $1" >&2; exit 2 ;;
  esac
done

if [[ -z "$JWT" ]]; then
  echo '{"ok":false,"error":"JWT is required in env"}'
  exit 1
fi
if [[ -z "$PAYMENT_ID" ]]; then
  echo '{"ok":false,"error":"--payment-id is required"}'
  exit 1
fi

body=$(curl -sS "$BASE_URL/payments/$PAYMENT_ID" -H "Authorization: Bearer $JWT")
status=$(echo "$body" | grep -o '"status"[[:space:]]*:[[:space:]]*"[^"]*"' | head -n1 | sed 's/.*"status"[[:space:]]*:[[:space:]]*"\([^"]*\)"/\1/')
checkout_url=$(echo "$body" | grep -o '"checkout_url"[[:space:]]*:[[:space:]]*"[^"]*"' | head -n1 | sed 's/.*"checkout_url"[[:space:]]*:[[:space:]]*"\([^"]*\)"/\1/')

printf '{"ok":true,"payment_id":"%s","status":"%s","checkout_url":"%s"}\n' "$PAYMENT_ID" "${status:-}" "${checkout_url:-}"
