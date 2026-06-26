#!/usr/bin/env bash
set -euo pipefail

source "$(dirname "$0")/env.sh"
EMAIL="${1:-}"
CODE="${2:-}"

if [[ -z "$EMAIL" || -z "$CODE" ]]; then
  echo '{"ok":false,"error":"Usage: auth_login.sh <email> <otp_code>"}'
  exit 1
fi

EMAIL_ENC="$(EMAIL="$EMAIL" python3 -c 'import urllib.parse,os; print(urllib.parse.quote(os.environ["EMAIL"], safe=""))' )"

body=$(curl -sS -X POST "$BASE_URL/citizens/login?email=$EMAIL_ENC&code=$CODE")

jwt=$(echo "$body" | grep -o '"access_token"[[:space:]]*:[[:space:]]*"[^"]*"' | head -n1 | sed 's/.*"access_token"[[:space:]]*:[[:space:]]*"\([^"]*\)"/\1/')

if [[ -z "${jwt:-}" ]]; then
  echo '{"ok":false,"error":"No access_token in response"}'
  exit 1
fi

save_jwt_to_state "$jwt" "$EMAIL"
printf '{"ok":true,"token_saved":true,"email":"%s"}\n' "$EMAIL"
