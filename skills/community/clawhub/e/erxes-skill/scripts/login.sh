#!/bin/bash
# erxes OAuth Device Flow login
# Usage: ERXES_BASE_URL=https://example.next.erxes.io/gateway bash scripts/login.sh
set -euo pipefail

BASE="${ERXES_BASE_URL%/}"
CLIENT="${ERXES_CLIENT_ID:-erxes-local}"

if [ -z "$BASE" ]; then
  echo "ERXES_BASE_URL is required" >&2
  exit 1
fi

# Extract subdomain from a gateway URL like https://demo.next.erxes.io/gateway -> demo
SUB=$(echo "$BASE" | sed -E 's|https?://([^./]+).*|\1|')

RESP=$(curl -sf -X POST "$BASE/oauth/device/code" \
  -H "Content-Type: application/json" \
  -H "erxes-subdomain: $SUB" \
  -d "{\"client_id\":\"$CLIENT\"}")

DC=$(echo "$RESP" | grep -o '"device_code":"[^"]*"' | cut -d'"' -f4)
URI=$(echo "$RESP" | grep -o '"verification_uri_complete":"[^"]*"' | cut -d'"' -f4 \
  | sed "s/<subdomain>/$SUB/g")

if [ -z "$DC" ] || [ -z "$URI" ]; then
  echo "Failed to start OAuth device flow" >&2
  echo "$RESP" >&2
  exit 1
fi

echo "Open this URL in your browser to approve access:" >&2
echo "$URI" >&2
open "$URI" 2>/dev/null || true

echo "Waiting for approval..." >&2
while true; do
  sleep 5
  TOK=$(curl -s -X POST "$BASE/oauth/token" \
    -H "Content-Type: application/json" \
    -H "erxes-subdomain: $SUB" \
    -d "{\"grant_type\":\"urn:ietf:params:oauth:grant-type:device_code\",\"device_code\":\"$DC\",\"client_id\":\"$CLIENT\"}")

  if echo "$TOK" | grep -q '"accessToken"'; then
    break
  elif echo "$TOK" | grep -q 'authorization_pending'; then
    continue
  else
    echo "OAuth error: $TOK" >&2
    exit 1
  fi
done

printf '{"subdomain":"%s","base_url":"%s","client_id":"%s","token":%s}\n' "$SUB" "$BASE" "$CLIENT" "$TOK"
