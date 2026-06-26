#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${CLAWTUNE_BASE_URL:-https://clawtune.aqifun.com/api/v1}"
STATE_DIR="${CLAWTUNE_STATE_DIR:-$HOME/.openclaw/clawtune}"
AUTH_FILE="$STATE_DIR/auth.json"
CHANNEL="${CLAWTUNE_CHANNEL:-openclaw}"
USER_REF="${CLAWTUNE_USER_REF:-}"
MODE="${1:-ensure}"

mkdir -p "$STATE_DIR"

json_get() {
  local file="$1"
  local key="$2"
  python3 - "$file" "$key" <<'PY'
import json, sys
path, key = sys.argv[1], sys.argv[2]
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)
value = data.get(key, "")
if value is None:
    value = ""
print(value)
PY
}

is_future_iso() {
  local value="$1"
  python3 - "$value" <<'PY'
from datetime import datetime, timezone
import sys
value = sys.argv[1].strip()
if not value:
    print("false")
    raise SystemExit(0)
try:
    dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    print("true" if dt > datetime.now(timezone.utc) else "false")
except Exception:
    print("false")
PY
}

write_auth() {
  local installation_id="$1"
  local access_token="$2"
  local expires_in="$3"
  local refresh_token="$4"
  local refresh_expires_in="$5"
  local channel="$6"
  local user_ref="$7"
  python3 - "$AUTH_FILE" "$installation_id" "$access_token" "$expires_in" "$refresh_token" "$refresh_expires_in" "$channel" "$user_ref" <<'PY'
from datetime import datetime, timezone, timedelta
import json, sys
path, installation_id, access_token, expires_in, refresh_token, refresh_expires_in, channel, user_ref = sys.argv[1:]
now = datetime.now(timezone.utc)
data = {
    "installation_id": installation_id,
    "access_token": access_token,
    "access_token_expires_at": (now + timedelta(seconds=int(expires_in))).isoformat().replace('+00:00', 'Z'),
    "refresh_token": refresh_token,
    "refresh_token_expires_at": (now + timedelta(seconds=int(refresh_expires_in))).isoformat().replace('+00:00', 'Z'),
    "channel": channel,
    "user_ref": user_ref or None,
    "updated_at": now.isoformat().replace('+00:00', 'Z')
}
with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write('\n')
PY
}

call_bootstrap() {
  local payload
  payload=$(python3 - "$CHANNEL" "$USER_REF" <<'PY'
import json, sys
channel, user_ref = sys.argv[1], sys.argv[2]
payload = {"channel": channel}
if user_ref:
    payload["user_ref"] = user_ref
print(json.dumps(payload, ensure_ascii=False))
PY
)
  local response
  response=$(curl -fsSL -X POST "$BASE_URL/bootstrap" -H 'Content-Type: application/json' -d "$payload")
  python3 - <<'PY' "$response" "$AUTH_FILE"
import json, sys
response = json.loads(sys.argv[1])
auth_file = sys.argv[2]
data = response["data"]
print(json.dumps({
    "installation_id": data["installation_id"],
    "access_token": data["access_token"],
    "expires_in": data["expires_in"],
    "refresh_token": data["refresh_token"],
    "refresh_expires_in": data.get("refresh_expires_in", 2592000),
    "channel": data.get("channel", "openclaw"),
    "user_ref": data.get("user_ref") or ""
}))
PY
}

call_refresh() {
  local installation_id="$1"
  local refresh_token="$2"
  local payload
  payload=$(python3 - "$installation_id" "$refresh_token" "$CHANNEL" "$USER_REF" <<'PY'
import json, sys
installation_id, refresh_token, channel, user_ref = sys.argv[1:]
payload = {
    "installation_id": installation_id,
    "refresh_token": refresh_token,
    "channel": channel,
}
if user_ref:
    payload["user_ref"] = user_ref
print(json.dumps(payload, ensure_ascii=False))
PY
)
  local response
  response=$(curl -fsSL -X POST "$BASE_URL/token/refresh" -H 'Content-Type: application/json' -d "$payload")
  python3 - <<'PY' "$response"
import json, sys
response = json.loads(sys.argv[1])
data = response["data"]
print(json.dumps({
    "installation_id": data["installation_id"],
    "access_token": data["access_token"],
    "expires_in": data["expires_in"],
    "refresh_token": data["refresh_token"],
    "refresh_expires_in": data.get("refresh_expires_in", 2592000),
    "channel": data.get("channel", "openclaw"),
    "user_ref": data.get("user_ref") or ""
}))
PY
}

persist_from_json() {
  local result_json="$1"
  local installation_id access_token expires_in refresh_token refresh_expires_in channel user_ref
  installation_id=$(python3 -c 'import json,sys; print(json.loads(sys.argv[1])["installation_id"])' "$result_json")
  access_token=$(python3 -c 'import json,sys; print(json.loads(sys.argv[1])["access_token"])' "$result_json")
  expires_in=$(python3 -c 'import json,sys; print(json.loads(sys.argv[1])["expires_in"])' "$result_json")
  refresh_token=$(python3 -c 'import json,sys; print(json.loads(sys.argv[1])["refresh_token"])' "$result_json")
  refresh_expires_in=$(python3 -c 'import json,sys; print(json.loads(sys.argv[1])["refresh_expires_in"])' "$result_json")
  channel=$(python3 -c 'import json,sys; print(json.loads(sys.argv[1])["channel"])' "$result_json")
  user_ref=$(python3 -c 'import json,sys; print(json.loads(sys.argv[1])["user_ref"])' "$result_json")
  write_auth "$installation_id" "$access_token" "$expires_in" "$refresh_token" "$refresh_expires_in" "$channel" "$user_ref"
}

ensure_auth() {
  if [[ -f "$AUTH_FILE" ]]; then
    local access_expires refresh_expires installation_id refresh_token
    access_expires=$(json_get "$AUTH_FILE" "access_token_expires_at")
    if [[ "$(is_future_iso "$access_expires")" == "true" ]]; then
      printf '%s\n' "$AUTH_FILE"
      return 0
    fi

    refresh_expires=$(json_get "$AUTH_FILE" "refresh_token_expires_at")
    if [[ "$(is_future_iso "$refresh_expires")" == "true" ]]; then
      installation_id=$(json_get "$AUTH_FILE" "installation_id")
      refresh_token=$(json_get "$AUTH_FILE" "refresh_token")
      persist_from_json "$(call_refresh "$installation_id" "$refresh_token")"
      printf '%s\n' "$AUTH_FILE"
      return 0
    fi
  fi

  persist_from_json "$(call_bootstrap)"
  printf '%s\n' "$AUTH_FILE"
}

case "$MODE" in
  ensure)
    ensure_auth
    ;;
  bootstrap)
    persist_from_json "$(call_bootstrap)"
    printf '%s\n' "$AUTH_FILE"
    ;;
  refresh)
    if [[ ! -f "$AUTH_FILE" ]]; then
      echo "auth file not found: $AUTH_FILE" >&2
      exit 1
    fi
    persist_from_json "$(call_refresh "$(json_get "$AUTH_FILE" "installation_id")" "$(json_get "$AUTH_FILE" "refresh_token")")"
    printf '%s\n' "$AUTH_FILE"
    ;;
  print)
    ensure_auth >/dev/null
    cat "$AUTH_FILE"
    ;;
  *)
    echo "usage: $0 [ensure|bootstrap|refresh|print]" >&2
    exit 1
    ;;
esac
