#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=/dev/null
source "$SCRIPT_DIR/_common.sh"

MODE="${1:-show}"
KEY="${2:-}"
VALUE="${3:-}"

ensure_state_dir

init_session() {
  python3 - "$SESSION_FILE" <<'PY'
import json, sys
from datetime import datetime, timezone
path = sys.argv[1]
now = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
data = {
    "skill_session_id": "",
    "session_ref": "",
    "current_phase": "",
    "current_playlist_id": "",
    "current_draft_id": "",
    "current_order_id": "",
    "source_context_playlist_id": "",
    "source_context_song_id": "",
    "last_user_intent_summary": "",
    "updated_at": now,
}
with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write('\n')
PY
}

ensure_session() {
  if [[ ! -f "$SESSION_FILE" ]]; then
    init_session
  fi
}

set_value() {
  local key="$1"
  local value="$2"
  ensure_session
  python3 - "$SESSION_FILE" "$key" "$value" <<'PY'
import json, sys
from datetime import datetime, timezone
path, key, value = sys.argv[1:4]
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)
data[key] = value
data['updated_at'] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write('\n')
PY
}

clear_value() {
  local key="$1"
  set_value "$key" ""
}

merge_values() {
  shift
  ensure_session
  python3 - "$SESSION_FILE" "$@" <<'PY'
import json, sys
from datetime import datetime, timezone
path = sys.argv[1]
items = sys.argv[2:]
if len(items) % 2 != 0:
    raise SystemExit('merge requires key value pairs')
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)
for i in range(0, len(items), 2):
    data[items[i]] = items[i+1]
data['updated_at'] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write('\n')
PY
}

case "$MODE" in
  init)
    init_session
    cat "$SESSION_FILE"
    ;;
  ensure)
    ensure_session
    printf '%s\n' "$SESSION_FILE"
    ;;
  show)
    ensure_session
    cat "$SESSION_FILE"
    ;;
  get)
    if [[ -z "$KEY" ]]; then
      echo "usage: $0 get <key>" >&2
      exit 1
    fi
    ensure_session
    json_get_file_value "$SESSION_FILE" "$KEY"
    ;;
  set)
    if [[ -z "$KEY" ]]; then
      echo "usage: $0 set <key> <value>" >&2
      exit 1
    fi
    set_value "$KEY" "$VALUE"
    cat "$SESSION_FILE"
    ;;
  clear)
    if [[ -z "$KEY" ]]; then
      echo "usage: $0 clear <key>" >&2
      exit 1
    fi
    clear_value "$KEY"
    cat "$SESSION_FILE"
    ;;
  merge)
    if [[ $# -lt 3 ]]; then
      echo "usage: $0 merge <key> <value> [<key> <value> ...]" >&2
      exit 1
    fi
    merge_values "$@"
    cat "$SESSION_FILE"
    ;;
  *)
    echo "usage: $0 [init|ensure|show|get|set|clear|merge]" >&2
    exit 1
    ;;
esac
