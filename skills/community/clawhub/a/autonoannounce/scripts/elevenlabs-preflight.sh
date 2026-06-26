#!/usr/bin/env bash
set -euo pipefail

BASE="https://api.elevenlabs.io"
KEY="${ELEVENLABS_API_KEY:-}"
VOICE="${ELEVENLABS_VOICE_ID:-}"
MODEL="${ELEVENLABS_MODEL_ID:-}"

# Retry policy (bounded)
MAX_RETRIES="${SFX_MAX_RETRIES:-3}"
BASE_DELAY_MS="${SFX_BASE_DELAY_MS:-250}"
MAX_DELAY_MS="${SFX_MAX_DELAY_MS:-2000}"

# Test harness mode (no live API required)
MOCK_MODE="${ELEVENLABS_PREFLIGHT_MOCK:-0}"
MOCK_SFX_CODES="${ELEVENLABS_PREFLIGHT_MOCK_SFX_CODES:-429,429,200}"

if [[ "$MOCK_MODE" != "1" && -z "$KEY" ]]; then
  echo '{"ok":false,"error":"missing ELEVENLABS_API_KEY"}'
  exit 1
fi

h=(-H "xi-api-key: $KEY" -H 'accept: application/json')

sleep_backoff_ms() {
  local attempt="$1"
  local exp=$(( BASE_DELAY_MS * (2 ** (attempt - 1)) ))
  local capped=$(( exp > MAX_DELAY_MS ? MAX_DELAY_MS : exp ))
  local jitter=$(( RANDOM % 125 ))
  local total=$(( capped + jitter ))
  python3 - <<PY
import time
time.sleep(${total}/1000.0)
PY
}

probe_get() {
  local ep="$1"
  local code
  if [[ "$MOCK_MODE" == "1" ]]; then
    case "$ep" in
      /v1/models|/v1/user/subscription) echo 200; return 0 ;;
      /v1/voices/*) echo 200; return 0 ;;
      *) echo 404; return 0 ;;
    esac
  fi
  code=$(curl -sS -o /tmp/el_preflight.json -w '%{http_code}' "${h[@]}" "$BASE$ep")
  echo "$code"
}

probe_sfx_once() {
  local code
  code=$(curl -sS -o /tmp/el_sfx_pf.json -w '%{http_code}' -X POST "$BASE/v1/sound-generation" \
    -H "xi-api-key: $KEY" -H 'Content-Type: application/json' \
    -d '{"text":"short system chime","duration_seconds":1}')
  echo "$code"
}

models_code=$(probe_get /v1/models)
user_code=$(probe_get /v1/user/subscription)
voice_code="unset"
if [[ -n "$VOICE" ]]; then
  voice_code=$(probe_get "/v1/voices/$VOICE")
fi

sfx_code="000"
sfx_attempts=0
sfx_status="unavailable"
retry_exhausted=false

IFS=',' read -r -a MOCK_CODES_ARR <<< "$MOCK_SFX_CODES"

while :; do
  (( sfx_attempts += 1 ))
  if [[ "$MOCK_MODE" == "1" ]]; then
    idx=$((sfx_attempts-1))
    if [[ $idx -lt ${#MOCK_CODES_ARR[@]} ]]; then
      sfx_code="${MOCK_CODES_ARR[$idx]}"
    else
      last_idx=$(( ${#MOCK_CODES_ARR[@]} - 1 ))
      sfx_code="${MOCK_CODES_ARR[$last_idx]}"
    fi
  else
    sfx_code=$(probe_sfx_once)
  fi

  if [[ "$sfx_code" == "200" ]]; then
    sfx_status="ok"
    break
  fi

  # Retry only for traffic/server/transient failure classes
  if [[ "$sfx_code" =~ ^(429|500|502|503|504)$ ]] && [[ $sfx_attempts -le $MAX_RETRIES ]]; then
    sleep_backoff_ms "$sfx_attempts"
    continue
  fi

  if [[ "$sfx_code" =~ ^(429|500|502|503|504)$ ]] && [[ $sfx_attempts -gt $MAX_RETRIES ]]; then
    retry_exhausted=true
  fi
  break
done

if [[ "$sfx_status" != "ok" ]]; then
  case "$sfx_code" in
    429) sfx_status="rate_limited" ;;
    401|403) sfx_status="forbidden_or_missing_permission" ;;
    500|502|503|504) sfx_status="upstream_error" ;;
    *) sfx_status="unavailable" ;;
  esac
fi

fallback_recommendation="use_cached_or_local_earcons"
if [[ "$sfx_status" == "ok" ]]; then
  fallback_recommendation="none"
fi

ok=true
[[ "$models_code" == "200" ]] || ok=false
[[ "$user_code" == "200" ]] || ok=false
if [[ -n "$VOICE" && "$voice_code" != "200" ]]; then ok=false; fi

cat <<EOF
{"ok":$ok,"models_http":$models_code,"subscription_http":$user_code,"voice_http":"$voice_code","sfx_http":$sfx_code,"sfx_status":"$sfx_status","sfx_attempts":$sfx_attempts,"retry_exhausted":$retry_exhausted,"retry_policy":{"max_retries":$MAX_RETRIES,"base_delay_ms":$BASE_DELAY_MS,"max_delay_ms":$MAX_DELAY_MS},"fallback":"$fallback_recommendation","model_env_set":$([[ -n "$MODEL" ]] && echo true || echo false),"mock_mode":$([[ "$MOCK_MODE" == "1" ]] && echo true || echo false)}
EOF
