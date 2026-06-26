#!/usr/bin/env bash
set -euo pipefail

SERVICE=""
URL=""
ENV_VAR=""
CRED_FILE=""
TIMEOUT="15"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --service) SERVICE="$2"; shift 2 ;;
    --url) URL="$2"; shift 2 ;;
    --env-var) ENV_VAR="$2"; shift 2 ;;
    --cred-file) CRED_FILE="$2"; shift 2 ;;
    --timeout) TIMEOUT="$2"; shift 2 ;;
    *) echo "Unknown arg: $1" >&2; exit 2 ;;
  esac
done

if [[ -z "$SERVICE" || -z "$URL" || -z "$ENV_VAR" || -z "$CRED_FILE" ]]; then
  echo "Usage: auth_check.sh --service <name> --url <url> --env-var <ENV> --cred-file <path> [--timeout 15]" >&2
  exit 2
fi

for bin in curl python3; do
  command -v "$bin" >/dev/null 2>&1 || { echo "AUTH_ERROR missing_binary=$bin"; exit 2; }
done

if [[ ! "$URL" =~ ^https:// ]]; then
  echo "AUTH_ERROR invalid_url=https_required"
  exit 2
fi

if [[ "$CRED_FILE" != "$HOME/.config/"* ]]; then
  echo "AUTH_ERROR untrusted_cred_path=$CRED_FILE allowed_prefix=$HOME/.config/"
  exit 2
fi

get_key() {
  local from_env="${!ENV_VAR:-}"
  if [[ -n "$from_env" ]]; then
    printf '%s' "$from_env"
    return 0
  fi

  if [[ -f "$CRED_FILE" ]]; then
    python3 - "$CRED_FILE" <<'PY'
import json, sys
p = sys.argv[1]
try:
    d = json.load(open(p, 'r', encoding='utf-8'))
except Exception:
    print('', end='')
    raise SystemExit(0)
for k in ('apiKey', 'api_key', 'token', 'accessToken'):
    v = d.get(k)
    if isinstance(v, str) and v.strip():
        print(v.strip(), end='')
        break
PY
    return 0
  fi

  printf ''
}

KEY="$(get_key || true)"
if [[ -z "$KEY" ]]; then
  echo "AUTH_MISSING service=$SERVICE env=$ENV_VAR cred_file=$CRED_FILE"
  exit 0
fi

STATUS=$(curl -sS -o /dev/null -w "%{http_code}" --max-time "$TIMEOUT" -H "Authorization: Bearer $KEY" "$URL" || true)

if [[ "$STATUS" == "200" ]]; then
  echo "AUTH_OK service=$SERVICE status=$STATUS"
elif [[ "$STATUS" == "401" || "$STATUS" == "403" ]]; then
  echo "AUTH_FAIL_UNAUTHORIZED service=$SERVICE status=$STATUS"
else
  echo "AUTH_FAIL_OTHER service=$SERVICE status=$STATUS"
fi
