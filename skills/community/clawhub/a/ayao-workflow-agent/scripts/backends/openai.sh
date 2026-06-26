#!/bin/bash
# openai.sh — OpenAI image generation backend

set -euo pipefail

PROMPT="${1:-}"
OUTPUT="${2:-}"
STYLE="${3:-}"
API_KEY="${OPENAI_API_KEY:-}"
MODEL="${OPENAI_IMAGE_MODEL:-dall-e-3}"
FULL_PROMPT="$PROMPT"
PAYLOAD=""
RESPONSE=""
URL=""

if [[ -z "$PROMPT" || -z "$OUTPUT" ]]; then
  echo "Usage: openai.sh <prompt> <output> [style]" >&2
  exit 1
fi

if [[ -z "$API_KEY" ]]; then
  echo "⚠️  OPENAI_API_KEY not set" >&2
  exit 1
fi

if [[ -n "$STYLE" ]]; then
  FULL_PROMPT="${PROMPT}. Style: ${STYLE}"
fi

PAYLOAD="$(python3 - "$MODEL" "$FULL_PROMPT" <<'PYEOF'
import json
import sys

print(json.dumps({
    "model": sys.argv[1],
    "prompt": sys.argv[2],
    "n": 1,
    "size": "1024x1024",
}))
PYEOF
)"

RESPONSE="$(curl -fsS -X POST "https://api.openai.com/v1/images/generations" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD")"

URL="$(RESPONSE_JSON="$RESPONSE" python3 - <<'PYEOF'
import json
import os
import sys

try:
    data = json.loads(os.environ["RESPONSE_JSON"])
    print(data["data"][0]["url"])
except Exception as exc:
    print(f"Failed to parse OpenAI image response: {exc}", file=sys.stderr)
    raise SystemExit(1)
PYEOF
)"

curl -fsS -o "$OUTPUT" "$URL"
