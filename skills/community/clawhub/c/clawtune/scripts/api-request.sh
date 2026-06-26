#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_URL="${CLAWTUNE_BASE_URL:-https://clawtune.aqifun.com/api/v1}"
STATE_DIR="${CLAWTUNE_STATE_DIR:-$HOME/.openclaw/clawtune}"
AUTH_FILE="$STATE_DIR/auth.json"

if [[ $# -lt 2 ]]; then
  echo "usage: $0 METHOD PATH [JSON_BODY]" >&2
  echo "example: $0 GET /orders/ord_xxx/status" >&2
  echo "example: $0 POST /playlists/generate '{\"intent_text\":\"late night emo\"}'" >&2
  exit 1
fi

METHOD="$1"
PATH_PART="$2"
BODY="${3:-}"

"$SCRIPT_DIR/auth-bootstrap.sh" ensure >/dev/null
ACCESS_TOKEN=$(python3 - "$AUTH_FILE" <<'PY'
import json, sys
with open(sys.argv[1], 'r', encoding='utf-8') as f:
    print(json.load(f)["access_token"])
PY
)

URL="$BASE_URL$PATH_PART"
TMP_HEADERS=$(mktemp)
trap 'rm -f "$TMP_HEADERS"' EXIT

CURL_ARGS=(
  -sS
  -X "$METHOD"
  "$URL"
  -D "$TMP_HEADERS"
  -H "Authorization: Bearer $ACCESS_TOKEN"
  -H "Accept: application/json"
)

if [[ -n "${CLAWTUNE_IDEMPOTENCY_KEY:-}" ]]; then
  CURL_ARGS+=( -H "Idempotency-Key: ${CLAWTUNE_IDEMPOTENCY_KEY}" )
fi

if [[ -n "$BODY" ]]; then
  CURL_ARGS+=( -H "Content-Type: application/json" -d "$BODY" )
fi

RESPONSE=$(curl "${CURL_ARGS[@]}")
STATUS=$(python3 - "$TMP_HEADERS" <<'PY'
import sys
status = "000"
with open(sys.argv[1], 'r', encoding='utf-8', errors='ignore') as f:
    for line in f:
        if line.startswith('HTTP/'):
            parts = line.split()
            if len(parts) >= 2:
                status = parts[1]
print(status)
PY
)

if [[ "$STATUS" =~ ^2 ]]; then
  printf '%s\n' "$RESPONSE"
else
  echo "HTTP $STATUS" >&2
  printf '%s\n' "$RESPONSE" >&2
  exit 1
fi
