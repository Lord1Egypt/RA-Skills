#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${1:-}"
API_KEY="${2:-}"
MODEL="${3:-}"

if [[ -z "$BASE_URL" || -z "$API_KEY" || -z "$MODEL" ]]; then
  echo "usage: $0 <base-url> <api-key> <model>" >&2
  exit 1
fi

curl -sS "$BASE_URL/models" \
  -H "Authorization: Bearer $API_KEY" | sed -n '1,40p'

echo

echo '{"model":"'"$MODEL"'","messages":[{"role":"user","content":"ping"}]}' | \
curl -sS "$BASE_URL/chat/completions" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d @- | sed -n '1,80p'
