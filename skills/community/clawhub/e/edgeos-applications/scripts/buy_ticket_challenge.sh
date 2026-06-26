#!/usr/bin/env bash
set -euo pipefail

# Get x402 payment challenge for /agent/buy-ticket
#
# Requires:
#   JWT (or SESSION_EMAIL + saved state token)
# Args:
#   --payload-file <path-to-json>

source "$(dirname "$0")/env.sh"
JWT="${JWT:-}"
load_jwt_from_state
PAYLOAD_FILE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --payload-file) PAYLOAD_FILE="$2"; shift 2 ;;
    *) echo "Unknown arg: $1" >&2; exit 2 ;;
  esac
done

if [[ -z "$JWT" ]]; then
  echo '{"ok":false,"error":"JWT is required in env"}'
  exit 1
fi
if [[ -z "$PAYLOAD_FILE" || ! -f "$PAYLOAD_FILE" ]]; then
  echo '{"ok":false,"error":"--payload-file is required and must exist"}'
  exit 1
fi

HDR_FILE=$(mktemp)
RESP_FILE=$(mktemp)
HTTP_CODE=$(mktemp)

curl -sS -X POST "$BASE_URL/agent/buy-ticket" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT" \
  --data-binary "@$PAYLOAD_FILE" \
  -D "$HDR_FILE" \
  -o "$RESP_FILE" \
  -w '%{http_code}' > "$HTTP_CODE"

code=$(cat "$HTTP_CODE")
body=$(cat "$RESP_FILE")
payment_required=$(grep -i '^PAYMENT-REQUIRED:' "$HDR_FILE" | tail -n1 | sed -E 's/^PAYMENT-REQUIRED:[[:space:]]*//I' | tr -d '\r')

rm -f "$HDR_FILE" "$RESP_FILE" "$HTTP_CODE"

if [[ "$code" != "402" ]]; then
  safe_body=$(BODY="$body" python3 - <<'PY'
import json, os
print(json.dumps(os.environ.get('BODY','')))
PY
)
  printf '{"ok":false,"http":%s,"error":"expected_402_payment_required","response_body":%s}\n' "$code" "$safe_body"
  exit 1
fi

printf '%s' "$body" | python3 - "$code" "$payment_required" <<'PY'
import json, sys

http = int(sys.argv[1])
payment_required = sys.argv[2]
raw = sys.stdin.read().strip() or '{}'

try:
    data = json.loads(raw)
except Exception:
    data = {}

accept = (data.get('accepts') or [{}])[0] if isinstance(data.get('accepts'), list) else {}
resource = data.get('resource') or {}
extra = accept.get('extra') or {}
agentkit = (data.get('extensions') or {}).get('agentkit') or {}
mode = agentkit.get('mode') or {}

out = {
    'ok': True,
    'http': http,
    'x402_version': data.get('x402Version'),
    'resource_url': resource.get('url'),
    'amount_atomic': accept.get('amount'),
    'pay_to': accept.get('payTo'),
    'network': accept.get('network'),
    'asset': accept.get('asset'),
    'max_timeout_seconds': accept.get('maxTimeoutSeconds'),
    'asset_name': extra.get('name'),
    'asset_version': extra.get('version'),
    'asset_transfer_method': extra.get('assetTransferMethod'),
    'discount_type': mode.get('type'),
    'discount_percent': mode.get('percent'),
    'payment_required_header_b64': payment_required,
    'challenge': data,
}

print(json.dumps(out, separators=(',', ':')))
PY
