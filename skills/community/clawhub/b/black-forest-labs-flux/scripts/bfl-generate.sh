#!/usr/bin/env bash
set -euo pipefail

if [[ -f /root/.clawdbot/.env ]]; then
  # shellcheck disable=SC1091
  source /root/.clawdbot/.env
fi

if [[ -z "${BFL_API_KEY:-}" ]]; then
  echo "Error: BFL_API_KEY not set" >&2
  exit 1
fi

PROMPT="${1:-}"
OUTFILE="${2:-/root/clawd/output/bfl-image-$(date +%s).jpg}"
MODEL="${BFL_MODEL:-flux-2-pro-preview}"
WIDTH="${BFL_WIDTH:-1536}"
HEIGHT="${BFL_HEIGHT:-1024}"

if [[ -z "$PROMPT" ]]; then
  echo "Usage: $0 \"prompt\" [outfile]" >&2
  exit 1
fi

mkdir -p "$(dirname "$OUTFILE")"

PAYLOAD=$(python3 - "$PROMPT" "$WIDTH" "$HEIGHT" <<'PY'
import json, sys
prompt, width, height = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
print(json.dumps({"prompt": prompt, "width": width, "height": height}))
PY
)

REQUEST_JSON=$(curl -sS -X POST "https://api.bfl.ai/v1/${MODEL}" \
  -H 'accept: application/json' \
  -H "x-key: ${BFL_API_KEY}" \
  -H 'Content-Type: application/json' \
  -d "$PAYLOAD")

POLLING_URL=$(python3 - "$REQUEST_JSON" <<'PY'
import json,sys
obj=json.loads(sys.argv[1])
print(obj.get('polling_url',''))
PY
)
REQUEST_ID=$(python3 - "$REQUEST_JSON" <<'PY'
import json,sys
obj=json.loads(sys.argv[1])
print(obj.get('id',''))
PY
)

if [[ -z "$POLLING_URL" ]]; then
  echo "BFL request failed:" >&2
  echo "$REQUEST_JSON" >&2
  exit 1
fi

echo "Request ID: $REQUEST_ID" >&2

for _ in $(seq 1 240); do
  sleep 1
  RESULT_JSON=$(curl -sS -X GET "$POLLING_URL" \
    -H 'accept: application/json' \
    -H "x-key: ${BFL_API_KEY}")
  STATUS=$(python3 - "$RESULT_JSON" <<'PY'
import json,sys
obj=json.loads(sys.argv[1])
print(obj.get('status',''))
PY
)
  if [[ "$STATUS" == "Ready" ]]; then
    IMAGE_URL=$(python3 - "$RESULT_JSON" <<'PY'
import json,sys
obj=json.loads(sys.argv[1])
res=obj.get('result',{})
print(res.get('sample') or res.get('image') or '')
PY
)
    if [[ -z "$IMAGE_URL" ]]; then
      echo "BFL returned Ready but no image URL:" >&2
      echo "$RESULT_JSON" >&2
      exit 1
    fi
    curl -sS "$IMAGE_URL" -o "$OUTFILE"
    echo "$OUTFILE"
    exit 0
  elif [[ "$STATUS" == "Error" || "$STATUS" == "Failed" || "$STATUS" == "Content Moderated" ]]; then
    echo "Generation failed:" >&2
    echo "$RESULT_JSON" >&2
    exit 1
  fi
done

echo "Timed out waiting for BFL result" >&2
exit 1
