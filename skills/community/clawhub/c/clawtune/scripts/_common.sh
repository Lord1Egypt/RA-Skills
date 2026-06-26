#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STATE_DIR="${CLAWTUNE_STATE_DIR:-$HOME/.openclaw/clawtune}"
SESSION_FILE="$STATE_DIR/session.json"
AUTH_FILE="$STATE_DIR/auth.json"

ensure_state_dir() {
  mkdir -p "$STATE_DIR"
}

now_utc() {
  python3 - <<'PY'
from datetime import datetime, timezone
print(datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'))
PY
}

json_get_file_value() {
  local file="$1"
  local key="$2"
  python3 - "$file" "$key" <<'PY'
import json, sys
from pathlib import Path
path = Path(sys.argv[1])
key = sys.argv[2]
if not path.exists():
    print("")
    raise SystemExit(0)
with path.open('r', encoding='utf-8') as f:
    data = json.load(f)
value = data.get(key, "")
if value is None:
    value = ""
elif isinstance(value, bool):
    value = 'true' if value else 'false'
elif isinstance(value, (dict, list)):
    value = json.dumps(value, ensure_ascii=False)
else:
    value = str(value)
print(value)
PY
}

json_get_string() {
  local json_payload="$1"
  local key="$2"
  python3 - "$json_payload" "$key" <<'PY'
import json, sys
payload = json.loads(sys.argv[1])
key = sys.argv[2]
value = payload
for part in key.split('.'):
    if isinstance(value, dict):
        value = value.get(part, "")
    else:
        value = ""
        break
if value is None:
    value = ""
elif isinstance(value, bool):
    value = 'true' if value else 'false'
elif isinstance(value, (dict, list)):
    value = json.dumps(value, ensure_ascii=False)
else:
    value = str(value)
print(value)
PY
}

json_assert_nonempty() {
  local json_payload="$1"
  local key="$2"
  local value
  value="$(json_get_string "$json_payload" "$key")"
  if [[ -z "$value" ]]; then
    echo "required JSON key missing or empty: $key" >&2
    return 1
  fi
}

json_assert_in() {
  local json_payload="$1"
  local key="$2"
  local allowed_csv="$3"
  local value
  value="$(json_get_string "$json_payload" "$key")"
  python3 - "$value" "$allowed_csv" "$key" <<'PY'
import sys
value, allowed_csv, key = sys.argv[1:4]
allowed = [item for item in allowed_csv.split(',') if item]
if value not in allowed:
    raise SystemExit(f"invalid value for {key}: {value!r}; expected one of {allowed}")
PY
}

json_pretty() {
  local json_payload="$1"
  python3 - "$json_payload" <<'PY'
import json, sys
print(json.dumps(json.loads(sys.argv[1]), ensure_ascii=False, indent=2))
PY
}

ensure_evidence_dir() {
  if [[ -n "${CLAWTUNE_EVIDENCE_DIR:-}" ]]; then
    mkdir -p "$CLAWTUNE_EVIDENCE_DIR"
  fi
}

save_evidence_text() {
  local basename="$1"
  local content="$2"
  if [[ -z "${CLAWTUNE_EVIDENCE_DIR:-}" ]]; then
    return 0
  fi
  ensure_evidence_dir
  printf '%s\n' "$content" > "$CLAWTUNE_EVIDENCE_DIR/$basename"
}

save_evidence_json() {
  local basename="$1"
  local json_payload="$2"
  if [[ -z "${CLAWTUNE_EVIDENCE_DIR:-}" ]]; then
    return 0
  fi
  ensure_evidence_dir
  python3 - "$CLAWTUNE_EVIDENCE_DIR/$basename" "$json_payload" <<'PY'
import json, sys
path, payload = sys.argv[1:3]
with open(path, 'w', encoding='utf-8') as f:
    json.dump(json.loads(payload), f, ensure_ascii=False, indent=2)
    f.write('\n')
PY
}

append_log() {
  local basename="$1"
  local message="$2"
  if [[ -z "${CLAWTUNE_EVIDENCE_DIR:-}" ]]; then
    return 0
  fi
  ensure_evidence_dir
  printf '%s %s\n' "$(now_utc)" "$message" >> "$CLAWTUNE_EVIDENCE_DIR/$basename"
}

save_session_snapshot() {
  if [[ -z "${CLAWTUNE_EVIDENCE_DIR:-}" ]]; then
    return 0
  fi
  ensure_state_dir
  if [[ -f "$SESSION_FILE" ]]; then
    cp "$SESSION_FILE" "$CLAWTUNE_EVIDENCE_DIR/session.snapshot.json"
  fi
}

random_idempotency_key() {
  local prefix="$1"
  python3 - "$prefix" <<'PY'
import sys, uuid
print(f"{sys.argv[1]}-{uuid.uuid4().hex[:12]}")
PY
}
