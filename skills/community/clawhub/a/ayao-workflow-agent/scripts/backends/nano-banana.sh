#!/bin/bash
# nano-banana.sh — Gemini Imagen backend

set -euo pipefail

PROMPT="${1:-}"
OUTPUT="${2:-}"
STYLE="${3:-}"
API_KEY="${GEMINI_API_KEY:-}"
SWARM_CONFIG=""
FULL_PROMPT="$PROMPT"
PAYLOAD=""
RESPONSE=""

if [[ -z "$PROMPT" || -z "$OUTPUT" ]]; then
  echo "Usage: nano-banana.sh <prompt> <output> [style]" >&2
  exit 1
fi

if [[ -z "$API_KEY" ]]; then
  if command -v swarm-config.sh >/dev/null 2>&1; then
    SWARM_CONFIG="$(command -v swarm-config.sh)"
  else
    BACKEND_DIR="$(cd "$(dirname "$0")" && pwd)"
    if [[ -x "$BACKEND_DIR/../swarm-config.sh" ]]; then
      SWARM_CONFIG="$BACKEND_DIR/../swarm-config.sh"
    fi
  fi
fi

if [[ -z "$API_KEY" && -n "$SWARM_CONFIG" ]]; then
  API_KEY="$("$SWARM_CONFIG" resolve image_generation.backends.nano-banana.api_key 2>/dev/null || true)"
fi

if [[ -z "$API_KEY" ]]; then
  echo "⚠️  GEMINI_API_KEY not set" >&2
  exit 1
fi

if [[ -n "$STYLE" ]]; then
  FULL_PROMPT="${PROMPT}. Style: ${STYLE}"
fi

PAYLOAD="$(python3 - "$FULL_PROMPT" <<'PYEOF'
import json
import sys

print(json.dumps({
    "instances": [{"prompt": sys.argv[1]}],
    "parameters": {"sampleCount": 1},
}))
PYEOF
)"

RESPONSE="$(curl -fsS -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-001:predict?key=${API_KEY}" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD")"

RESPONSE_JSON="$RESPONSE" python3 - "$OUTPUT" <<'PYEOF'
import base64
import json
import os
import sys

output_path = sys.argv[1]

try:
    data = json.loads(os.environ["RESPONSE_JSON"])
    img_b64 = data["predictions"][0]["bytesBase64Encoded"]
except Exception as exc:
    print(f"Failed to parse Gemini image response: {exc}", file=sys.stderr)
    raise SystemExit(1)

with open(output_path, "wb") as f:
    f.write(base64.b64decode(img_b64))
PYEOF
