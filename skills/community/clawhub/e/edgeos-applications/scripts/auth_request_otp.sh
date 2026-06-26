#!/usr/bin/env bash
set -euo pipefail

source "$(dirname "$0")/env.sh"
EMAIL="${1:-}"

if [[ -z "$EMAIL" ]]; then
  echo '{"ok":false,"error":"Usage: auth_request_otp.sh <email>"}'
  exit 1
fi

body=$(curl -sS -X POST "$BASE_URL/citizens/authenticate" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$EMAIL\",\"use_code\":true}")

message=$(echo "$body" | grep -o '"message"[[:space:]]*:[[:space:]]*"[^"]*"' | head -n1 | sed 's/.*"message"[[:space:]]*:[[:space:]]*"\([^"]*\)"/\1/')
printf '{"ok":true,"message":"%s"}\n' "${message:-otp_sent}"
