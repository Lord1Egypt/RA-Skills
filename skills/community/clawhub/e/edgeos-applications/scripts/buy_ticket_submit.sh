#!/usr/bin/env bash
set -euo pipefail

# Submit x402 payment for /agent/buy-ticket
#
# Requires:
#   JWT (or SESSION_EMAIL + saved state token)
# Args:
#   --payload-file <path-to-json>                 (must be identical to challenge request body)
#   --payment-signature-b64 <base64-json>
#     OR --payment-signature-file <path-to-json>  (raw JSON; script base64-encodes it)
#   [--agentkit-b64 <base64-json>]
#   [--agentkit-file <path-to-json>]              (raw JSON; script base64-encodes it)

source "$(dirname "$0")/env.sh"
JWT="${JWT:-}"
load_jwt_from_state
PAYLOAD_FILE=""
PAYMENT_SIGNATURE_B64=""
PAYMENT_SIGNATURE_FILE=""
AGENTKIT_B64=""
AGENTKIT_FILE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --payload-file) PAYLOAD_FILE="$2"; shift 2 ;;
    --payment-signature-b64) PAYMENT_SIGNATURE_B64="$2"; shift 2 ;;
    --payment-signature-file) PAYMENT_SIGNATURE_FILE="$2"; shift 2 ;;
    --agentkit-b64) AGENTKIT_B64="$2"; shift 2 ;;
    --agentkit-file) AGENTKIT_FILE="$2"; shift 2 ;;
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

if [[ -z "$PAYMENT_SIGNATURE_B64" && -z "$PAYMENT_SIGNATURE_FILE" ]]; then
  echo '{"ok":false,"error":"Provide --payment-signature-b64 or --payment-signature-file"}'
  exit 1
fi
if [[ -n "$PAYMENT_SIGNATURE_FILE" && ! -f "$PAYMENT_SIGNATURE_FILE" ]]; then
  echo '{"ok":false,"error":"--payment-signature-file must exist"}'
  exit 1
fi
if [[ -n "$AGENTKIT_FILE" && ! -f "$AGENTKIT_FILE" ]]; then
  echo '{"ok":false,"error":"--agentkit-file must exist"}'
  exit 1
fi

if [[ -z "$PAYMENT_SIGNATURE_B64" && -n "$PAYMENT_SIGNATURE_FILE" ]]; then
  PAYMENT_SIGNATURE_B64=$(base64 -w 0 "$PAYMENT_SIGNATURE_FILE")
fi
if [[ -z "$AGENTKIT_B64" && -n "$AGENTKIT_FILE" ]]; then
  AGENTKIT_B64=$(base64 -w 0 "$AGENTKIT_FILE")
fi

HDR_FILE=$(mktemp)
RESP_FILE=$(mktemp)
HTTP_CODE=$(mktemp)

curl_cmd=(curl -sS -X POST "$BASE_URL/agent/buy-ticket"
  -H "Content-Type: application/json"
  -H "Authorization: Bearer $JWT"
  -H "PAYMENT-SIGNATURE: $PAYMENT_SIGNATURE_B64"
  --data-binary "@$PAYLOAD_FILE"
  -D "$HDR_FILE"
  -o "$RESP_FILE"
  -w '%{http_code}')

if [[ -n "$AGENTKIT_B64" ]]; then
  curl_cmd+=( -H "AGENTKIT: $AGENTKIT_B64" )
fi

"${curl_cmd[@]}" > "$HTTP_CODE"

code=$(cat "$HTTP_CODE")
body=$(cat "$RESP_FILE")
payment_response=$(grep -i '^PAYMENT-RESPONSE:' "$HDR_FILE" | tail -n1 | sed -E 's/^PAYMENT-RESPONSE:[[:space:]]*//I' | tr -d '\r')

rm -f "$HDR_FILE" "$RESP_FILE" "$HTTP_CODE"

if [[ "$code" -lt 200 || "$code" -ge 300 ]]; then
  safe_body=$(BODY="$body" python3 - <<'PY'
import json, os
print(json.dumps(os.environ.get('BODY','')))
PY
)
  printf '{"ok":false,"http":%s,"error":"buy_ticket_submit_failed","response_body":%s}\n' "$code" "$safe_body"
  exit 1
fi

printf '%s' "$body" | python3 - "$code" "$payment_response" <<'PY'
import base64, json, sys

http = int(sys.argv[1])
payment_response_b64 = sys.argv[2]
raw = sys.stdin.read().strip() or '{}'

try:
    data = json.loads(raw)
except Exception:
    data = {}

header_data = {}
if payment_response_b64:
    try:
        header_data = json.loads(base64.b64decode(payment_response_b64).decode('utf-8'))
    except Exception:
        header_data = {}

out = {
    'ok': True,
    'http': http,
    'payment_id': data.get('id'),
    'status': data.get('status'),
    'amount': data.get('amount'),
    'currency': data.get('currency'),
    'source': data.get('source'),
    'external_id': data.get('external_id'),
    'transaction': header_data.get('transaction') or data.get('external_id'),
    'network': header_data.get('network'),
    'payment_response_header_b64': payment_response_b64,
    'response': data,
}

print(json.dumps(out, separators=(',', ':')))
PY
