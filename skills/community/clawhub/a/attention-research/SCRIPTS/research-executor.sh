#!/bin/bash
#
# attention-research: Research Executor
# Usage:
#   research-executor.sh --check --slot morning|afternoon   # check freshness, write state
#   research-executor.sh --complete --slot morning|afternoon  # mark META.json done, notify

set -euo pipefail

SKILL_ROOT="${ATTENTION_RESEARCH_ROOT:-$HOME/.openclaw/skills/attention-research}"
RESEARCH_ROOT="${RESEARCH_ROOT:-$HOME/.openclaw/workspace/notes/research-v2}"
CONFIG_DIR="$SKILL_ROOT/CONFIG"
STATE_FILE="$HOME/.openclaw/workspace/memory/attention-research-state.json"
TODAY=$(date +%Y-%m-%d)
NOW=$(date +%Y-%m-%dT%H:%M:%S%z)
TZ="${TZ:-Asia/Hong_Kong}"

ACTION=""
SLOT=""

usage() {
  echo "Usage: $0 --check --slot morning|afternoon"
  echo "       $0 --complete --slot morning|afternoon"
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --check) ACTION="check"; shift ;;
    --complete) ACTION="complete"; shift ;;
    --slot) SLOT="$2"; shift 2 ;;
    --help) usage ;;
    *) echo "Unknown: $1"; usage ;;
  esac
done

[[ -z "$ACTION" ]] && { echo "ERROR: --check or --complete required"; usage; }
[[ -z "$SLOT" ]] && { echo "ERROR: --slot required"; usage; }
[[ "$SLOT" != "morning" && "$SLOT" != "afternoon" ]] && { echo "ERROR: --slot must be morning or afternoon"; exit 1; }

slot_field_name() {
  case "$SLOT" in
    morning) echo "lastMorningUpdate" ;;
    afternoon) echo "lastAfternoonUpdate" ;;
  esac
}

get_topics() {
  python3 -c "
import yaml
with open('$CONFIG_DIR/topics.yaml') as f:
    cfg = yaml.safe_load(f)
for t, v in cfg.get('topics', {}).items():
    if v.get('enabled', True):
        print(t)
" 2>/dev/null
}

meta_file() {
  echo "$RESEARCH_ROOT/topics/$1/META.json"
}

check_topic_freshness() {
  local topic="$1"
  local mf
  mf=$(meta_file "$topic")
  local sf
  sf=$(slot_field_name)
  [[ ! -f "$mf" ]] && { echo "fresh"; return; }
  local last_update
  last_update=$(python3 -c "import json; d=json.load(open('$mf')); print(d.get('$sf') or '')" 2>/dev/null || echo "")
  [[ "$last_update" == "$TODAY" ]] && { echo "fresh"; return; }
  local retry_count retry_date
  retry_count=$(python3 -c "import json; d=json.load(open('$mf')); print(d.get('retryCount', 0))" 2>/dev/null || echo "0")
  retry_date=$(python3 -c "import json; d=json.load(open('$mf')); print(d.get('retryDate', ''))" 2>/dev/null || echo "")
  if [[ "$retry_date" == "$TODAY" && "$retry_count" -ge 2 ]]; then
    echo "exhausted"
  else
    echo "stale"
  fi
}

init_topic_meta() {
  local topic="$1"
  local mf
  mf=$(meta_file "$topic")
  [[ -f "$mf" ]] && return
  mkdir -p "$(dirname "$mf")"
  python3 - <<PY
import json
meta = {
    "schema": "attention-research.v1",
    "topic": "$topic",
    "lastHeartbeatUpdate": None,
    "lastMorningUpdate": None,
    "lastAfternoonUpdate": None,
    "retryCount": 0,
    "retryDate": None,
    "lastError": None,
    "note": None
}
print(json.dumps(meta, indent=2))
PY
  echo "  Created: $mf"
}

write_state() {
  local pending="$1"
  mkdir -p "$(dirname "$STATE_FILE")"
  python3 - <<PY
import json, sys
from datetime import datetime
now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')
pending_list = $(echo "$pending" | python3 -c "import json,sys; print(json.dumps(sys.stdin.read().strip().split()))" 2>/dev/null || echo "[]")
state = {
    "slot": "$SLOT",
    "date": "$TODAY",
    "checkedAt": now,
    "pending": [t for t in pending_list if t],
    "completed": [],
    "researchDone": False
}
with open('$STATE_FILE', 'w') as f:
    json.dump(state, f, indent=2)
PY
}

mark_done() {
  local topic="$1"
  local mf
  mf=$(meta_file "$topic")
  [[ ! -f "$mf" ]] && return
  local sf
  sf=$(slot_field_name)
  python3 - <<PY
import json
meta = json.load(open('$mf'))
meta['retryCount'] = 0
meta['lastError'] = None
meta['lastHeartbeatUpdate'] = '$NOW'
meta['$sf'] = '$TODAY'
json.dump(meta, open('$mf', 'w'), indent=2)
PY
}

mark_failed() {
  local topic="$1"
  local msg="$2"
  local mf
  mf=$(meta_file "$topic")
  [[ ! -f "$mf" ]] && return
  local sf
  sf=$(slot_field_name)
  python3 - <<PY
import json
meta = json.load(open('$mf'))
meta['retryCount'] = meta.get('retryCount', 0) + 1
meta['retryDate'] = '$TODAY'
meta['lastError'] = '$msg'
meta['lastHeartbeatUpdate'] = '$NOW'
meta['$sf'] = None  # clear so it retries
json.dump(meta, open('$mf', 'w'), indent=2)
PY
}

do_check() {
  echo "=== attention-research check: $SLOT $TODAY ==="
  [[ ! -d "$RESEARCH_ROOT" ]] && { echo "ERROR: RESEARCH_ROOT not found: $RESEARCH_ROOT"; exit 1; }

  local pending=()
  for topic in $(get_topics); do
    init_topic_meta "$topic"
    local freshness
    freshness=$(check_topic_freshness "$topic")
    echo "Topic $topic: $freshness"
    case "$freshness" in
      fresh|exhausted) echo "  SKIP" ;;
      stale) pending+=("$topic"); echo "  PENDING" ;;
    esac
  done

  if [[ ${#pending[@]} -eq 0 ]]; then
    echo "No pending topics. All done."
    write_state ""
  else
    echo "Pending (${#pending[@]}): ${pending[*]}"
    write_state "$(printf '%s\n' "${pending[@]}")"
  fi
  echo "=== Check complete ==="
  echo "State: $STATE_FILE"
}

do_complete() {
  echo "=== attention-research complete: $SLOT $TODAY ==="
  [[ ! -f "$STATE_FILE" ]] && { echo "ERROR: No state file found. Run --check first."; exit 1; }

  python3 - <<PY
import json
import os
state = json.load(open('$STATE_FILE'))
slot_field = 'lastMorningUpdate' if state.get('slot') == 'morning' else 'lastAfternoonUpdate'
research_root = '$RESEARCH_ROOT'
for topic in state.get('pending', []):
    print(f"Marking done: {topic}")
    meta_file = os.path.join(research_root, 'topics', topic, 'META.json')
    if not os.path.exists(meta_file):
        continue
    with open(meta_file) as f:
        meta = json.load(f)
    meta['retryCount'] = 0
    meta['retryDate'] = None
    meta['lastError'] = None
    meta['lastHeartbeatUpdate'] = state.get('checkedAt')
    meta[slot_field] = state.get('date')
    with open(meta_file, 'w') as f:
        json.dump(meta, f, indent=2)

state['completed'] = state.get('pending', [])
state['researchDone'] = True
state['completedAt'] = '$NOW'
with open('$STATE_FILE', 'w') as f:
    json.dump(state, f, indent=2)
print(f"Completed {len(state.get('pending', []))} topics.")
PY
  echo "=== Complete ==="
}

case "$ACTION" in
  check) do_check ;;
  complete) do_complete ;;
esac