#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$HOME/.openclaw/workspace/skills/clawgrid-connector"
source "$SKILL_DIR/scripts/_clawgrid_env.sh"
DEBUG_REPORT_SCRIPT="$SKILL_DIR/scripts/debug-report.sh"
DIRECTIVES_CACHE=""

mkdir -p "$LOG_DIR"

task_log() {
  local tid="$1"
  local phase="$2"
  local status="$3"
  local detail="${4:-}"
  [ -z "$tid" ] && return 0
  python3 - "$LOG_DIR/$tid.log" "$tid" "$phase" "$status" "$detail" <<'PYEOF'
import json
import sys
from datetime import datetime, timezone

path, task_id, phase, status, detail = sys.argv[1:]
line = {
    "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "phase": phase,
    "status": status,
    "detail": detail,
}
with open(path, "a", encoding="utf-8") as f:
    f.write(json.dumps(line, ensure_ascii=False) + "\n")
PYEOF
}

_update_state() {
  python3 -c "
import json, sys, os
from datetime import datetime, timezone

state_path = '$STATE_FILE'
now = datetime.now(timezone.utc)
today_str = now.strftime('%Y-%m-%d')
now_iso = now.isoformat()

state = {}
if os.path.exists(state_path):
    try:
        state = json.load(open(state_path))
    except Exception:
        state = {}

if state.get('today') != today_str:
    state['today'] = today_str
    state['tasks_completed_today'] = 0
    state['earned_today_usd'] = '0'
    state['daily_progress'] = ''
    state['daily_limit'] = 0
    state['daily_quota_filled'] = False

state['updated_at'] = now_iso

try:
    updates = json.load(sys.stdin)
except Exception:
    updates = {}

for k, v in updates.items():
    if k == 'tasks_completed_today_inc':
        state['tasks_completed_today'] = state.get('tasks_completed_today', 0) + 1
    elif k == 'earned_today_usd_add':
        from decimal import Decimal
        cur = Decimal(state.get('earned_today_usd', '0'))
        state['earned_today_usd'] = str(cur + Decimal(str(v)))
    else:
        state[k] = v

tmp_path = state_path + '.tmp'
with open(tmp_path, 'w') as f:
    json.dump(state, f, indent=2)
os.replace(tmp_path, state_path)
" 2>/dev/null || true
}

_extract_directives() {
  local body="$1"
  echo "$body" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    dirs = d.get('_directives', [])
    if dirs:
        print(json.dumps(dirs))
    else:
        print('')
except:
    print('')
" 2>/dev/null || echo ""
}

_persist_directives_to_state() {
  if [ -z "$DIRECTIVES_CACHE" ]; then
    return
  fi
  echo "$DIRECTIVES_CACHE" | python3 -c "
import json, sys, os
dirs = json.load(sys.stdin)
notify_dirs = [d for d in dirs if d.get('notify_owner')]
if not notify_dirs:
    sys.exit(0)
state_path = '$STATE_FILE'
state = {}
if os.path.exists(state_path):
    try:
        state = json.load(open(state_path))
    except Exception:
        state = {}
existing_ids = {d['id'] for d in state.get('pending_directives', [])}
new_dirs = [d for d in notify_dirs if d.get('id') not in existing_ids]
if new_dirs:
    state.setdefault('pending_directives', []).extend(new_dirs)
    tmp = state_path + '.tmp'
    with open(tmp, 'w') as f:
        json.dump(state, f, indent=2)
    os.replace(tmp, state_path)
" 2>/dev/null || true
}

_inject_directives() {
  local json_output="$1"
  if [ -n "$DIRECTIVES_CACHE" ]; then
    _persist_directives_to_state
    echo "$json_output" | python3 -c "
import json, sys
d = json.load(sys.stdin)
dirs = json.loads('$DIRECTIVES_CACHE')
d['_directives'] = dirs
if any(di.get('notify_owner') for di in dirs):
    d['notify_owner'] = True
print(json.dumps(d))
" 2>/dev/null || echo "$json_output"
  else
    echo "$json_output"
  fi
}

# Inline debug report: build & POST directly, bypassing local_debugger.py
# which cannot parse poll.sh's programmatic HTTP calls from session logs.
_post_debug_report() {
  local tid="$1" ttype="$2" executor="$3" success="$4" start_time="$5" budget="${6:-}" target_url="${7:-}"
  [ -z "$API_KEY" ] || [ -z "$API_BASE" ] && return 0
  local end_time
  end_time=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  local report
  report=$(python3 -c "
import json
from datetime import datetime
outcome = 'submitted' if '$success' == 'true' else 'submit_failed'
submitted = '$success' == 'true'
start = '$start_time'
end = '$end_time'
duration = None
try:
    t0 = datetime.fromisoformat(start.replace('Z', '+00:00'))
    t1 = datetime.fromisoformat(end.replace('Z', '+00:00'))
    duration = round((t1 - t0).total_seconds(), 1)
except Exception:
    pass
print(json.dumps({
    'task_id': '$tid',
    'task_type': '$ttype',
    'executor': '$executor',
    'outcome': outcome,
    'submitted': submitted,
    'submit_success': submitted,
    'start_time': start,
    'end_time': end,
    'duration_seconds': duration,
    'budget': '$budget',
    'target_url': '$target_url',
    'report_phase': 1,
    'api_calls': [
        {'type': 'claim', 'method': 'POST', 'endpoint': '/api/lobster/tasks/$tid/claim'},
        {'type': 'submit', 'method': 'POST', 'endpoint': '/api/lobster/tasks/$tid/artifacts'},
    ],
}))
" 2>/dev/null) || return 0
  curl -s -X POST "$API_BASE/api/lobster/tasks/$tid/debug-report" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d "$report" --max-time 10 > /dev/null 2>&1 || true
  echo "[POLL] Debug report sent for $tid (executor=$executor, success=$success)" >&2
}

if [ ! -f "$CONFIG" ]; then
  echo "Config not found at $CONFIG — run setup first" >&2
  exit 1
fi

# --- Circuit breaker: check auth_invalid flag ---
if [ -f "$AUTH_INVALID_FLAG" ]; then
  echo "[POLL] Skipping — agent identity is invalid. Details:" >&2
  cat "$AUTH_INVALID_FLAG" >&2
  echo "" >&2
  echo "[POLL] Run setup/re-registration to fix this." >&2
  echo '{"status":"circuit_breaker"}' | _update_state
  # Dedup: notify_owner true only on first trigger, then silent
  if [ -f "$CIRCUIT_BREAKER_NOTIFIED_FLAG" ]; then
    echo '{"action":"circuit_breaker","notify_owner":false,"message":"Agent identity invalid. Re-registration needed."}'
  else
    touch "$CIRCUIT_BREAKER_NOTIFIED_FLAG"
    echo '{"action":"circuit_breaker","notify_owner":true,"message":"Agent identity invalid. Re-registration needed."}'
  fi
  exit 1
fi

# --- Circuit breaker: check cooldown period ---
if [ -f "$COOLDOWN_FILE" ]; then
  COOLDOWN_UNTIL=$(cat "$COOLDOWN_FILE")
  NOW_EPOCH=$(date +%s)
  if [ "$NOW_EPOCH" -lt "$COOLDOWN_UNTIL" ]; then
    REMAINING=$((COOLDOWN_UNTIL - NOW_EPOCH))
    echo "{\"action\":\"cooldown\",\"notify_owner\":false,\"remaining_seconds\":$REMAINING}"
    exit 0
  else
    rm -f "$COOLDOWN_FILE"
  fi
fi

# --- Pre-flight: exec approval check (first run only) ---
_EA_FLAG="$CLAWGRID_HOME/state/.exec_approval_checked"
if [ ! -f "$_EA_FLAG" ]; then
  CHECK_EXEC="$SKILL_DIR/scripts/check-exec-approval.sh"
  if [ -x "$CHECK_EXEC" ]; then
    _EA_STATUS=$(bash "$CHECK_EXEC" 2>/dev/null | head -1 || echo "OK")
    if [ "$_EA_STATUS" != "OK" ]; then
      echo '{"action":"exec_approval_missing","notify_owner":true,"message":"Exec approval not configured for automated tasks. Cron-triggered sessions will fail. Run: bash scripts/setup-exec-approval.sh"}'
      mkdir -p "$CLAWGRID_HOME/state"
      touch "$_EA_FLAG"
      exit 0
    fi
  fi
  mkdir -p "$CLAWGRID_HOME/state"
  touch "$_EA_FLAG"
fi

API_KEY=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_key'])")
API_BASE=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_base'])")
# Behavioral settings (auto_claim, allow_types, min_budget) are now server-side.
# Server filters tasks in poll response; auto_claim L1 uses server-side auto-assign.
# Client defaults for backward compatibility with configs not yet migrated:
AUTO_CLAIM=$(python3 -c "import json; print(json.load(open('$CONFIG')).get('auto_claim', True))")
MIN_BUDGET=$(python3 -c "import json; print(json.load(open('$CONFIG')).get('min_budget', 0))")
ALLOW_TYPES=$(python3 -c "import json; print(','.join(json.load(open('$CONFIG')).get('allow_types', [])))")

# --- Notification check: runs independently of poll throttle ---
# Pulls pending server-side notifications (task requests, status changes, etc.)
# and surfaces them to the agent even when the main poll loop is throttled.
NOTIF_CHECK_FILE="$CLAWGRID_HOME/state/.last_notif_epoch"
_NOTIF_SKIP=false
if [ -f "$NOTIF_CHECK_FILE" ]; then
  _NOTIF_LAST=$(cat "$NOTIF_CHECK_FILE")
  _NOTIF_NOW=$(date +%s)
  _NOTIF_ELAPSED=$((_NOTIF_NOW - _NOTIF_LAST))
  [ "$_NOTIF_ELAPSED" -lt 55 ] && _NOTIF_SKIP=true
fi

if [ "$_NOTIF_SKIP" = "false" ]; then
  date +%s > "$NOTIF_CHECK_FILE"
  _NOTIF_RESP=$(curl -s -w "\n%{http_code}" "$API_BASE/api/lobster/notifications/pending?limit=10" \
    -H "Authorization: Bearer $API_KEY" \
    --max-time 10 2>/dev/null || echo -e "{}\n000")
  _NOTIF_CODE=$(echo "$_NOTIF_RESP" | tail -1)
  _NOTIF_BODY=$(echo "$_NOTIF_RESP" | sed '$d')

  if [ "$_NOTIF_CODE" -ge 200 ] 2>/dev/null && [ "$_NOTIF_CODE" -lt 300 ] 2>/dev/null; then
    _NOTIF_OUTPUT=$(echo "$_NOTIF_BODY" | python3 -c "
import json, sys

try:
    data = json.load(sys.stdin)
    items = data.get('notifications', [])
except Exception:
    items = []

if not items:
    sys.exit(0)

ids_to_ack = []
parts = []
task_request_notif = None

for n in items:
    payload = n.get('payload', {})
    event = n.get('event', '')
    msg = payload.get('message', '')
    title = payload.get('title', '')
    nid = n.get('id')
    if nid:
        ids_to_ack.append(nid)

    # Detect task_request.new — needs dedicated action output
    if event == 'task_request.new' and not task_request_notif:
        task_request_notif = {
            'action': 'has_task_request',
            'notify_owner': True,
            'request_id': payload.get('request_id', ''),
            'title': payload.get('request_title', title),
            'requester_name': payload.get('requester_name', ''),
            'budget_max': payload.get('budget_max', ''),
            'offering_title': payload.get('offering_title', ''),
            'accept_endpoint': payload.get('accept_endpoint', ''),
            'decline_endpoint': payload.get('decline_endpoint', ''),
            'negotiation_rules': payload.get('negotiation_rules', ''),
            'next_actions': payload.get('next_actions', ['accept', 'decline']),
            'message': msg or f'New task request: \"{payload.get(\"request_title\", \"\")}\" from {payload.get(\"requester_name\", \"unknown\")}. Use accept or decline endpoints to respond.',
        }
        continue

    entry = {'event': event, 'payload': payload}
    if title:
        entry['title'] = title
    if msg:
        entry['message'] = msg
    parts.append(entry)

# If we found a task_request, output it as dedicated action
if task_request_notif:
    task_request_notif['ids_to_ack'] = ids_to_ack
    if parts:
        task_request_notif['other_notifications'] = parts
    print(json.dumps(task_request_notif))
else:
    result = {
        'action': 'notifications',
        'notify_owner': True,
        'count': len(parts),
        'notifications': parts,
        'ids_to_ack': ids_to_ack,
        'message': 'You have ' + str(len(parts)) + ' pending notification(s). '
                   + ' | '.join(
                       (p.get('title', '') + ': ' + p.get('message', '')).strip(': ')
                       for p in parts
                   ),
    }
    print(json.dumps(result))
" 2>/dev/null || echo "")

    if [ -n "$_NOTIF_OUTPUT" ]; then
      _ACK_IDS=$(echo "$_NOTIF_OUTPUT" | python3 -c "import json,sys; print(json.dumps(json.load(sys.stdin).get('ids_to_ack',[])))" 2>/dev/null || echo "[]")
      if [ "$_ACK_IDS" != "[]" ]; then
        curl -s -X POST "$API_BASE/api/lobster/notifications/ack" \
          -H "Authorization: Bearer $API_KEY" \
          -H "Content-Type: application/json" \
          -d "{\"ids\":$_ACK_IDS}" \
          --max-time 10 > /dev/null 2>&1 || true
      fi
      echo "$_NOTIF_OUTPUT" | python3 -c "
import json, sys
d = json.load(sys.stdin)
d.pop('ids_to_ack', None)
print(json.dumps(d))
" 2>/dev/null
      exit 0
    fi
  fi
fi

# --- Local throttle: skip if polled too recently (avoids 429 from cron/manual collision) ---
if [ -f "$LAST_POLL_FILE" ]; then
  _LAST_EPOCH=$(cat "$LAST_POLL_FILE")
  _NOW_EPOCH=$(date +%s)
  _ELAPSED=$((_NOW_EPOCH - _LAST_EPOCH))
  if [ "$_ELAPSED" -lt 55 ]; then
    _WAIT=$((60 - _ELAPSED))
    echo "{\"action\":\"throttled\",\"notify_owner\":false,\"message\":\"Skipped — last poll was ${_ELAPSED}s ago. Retry in ${_WAIT}s.\"}"
    exit 0
  fi
fi

# --- Self-healing: ensure heartbeat scheduler + keepalive are running ---
HEARTBEAT_CTL="$SKILL_DIR/scripts/heartbeat-ctl.sh"
if [ -f "$HEARTBEAT_CTL" ]; then
  _HB_STATUS=$(bash "$HEARTBEAT_CTL" status 2>/dev/null || echo '{}')
  _HB_RUNNING=$(echo "$_HB_STATUS" | python3 -c "import json,sys; print(json.load(sys.stdin).get('heartbeat',{}).get('running',False))" 2>/dev/null || echo "False")
  if [ "$_HB_RUNNING" != "True" ]; then
    bash "$HEARTBEAT_CTL" start --quiet >/dev/null 2>&1 || true
    echo "[POLL] Heartbeat scheduler was missing — restored via heartbeat-ctl" >&2
  fi
fi

# --- Skill update notification: scan ALL installed skills for .skill_updated flags ---
SKILLS_BASE="$HOME/.openclaw/workspace/skills"
SKILL_UPDATE_OUTPUT=$(python3 - "$SKILLS_BASE" <<'PYEOF'
import json, sys, os, glob

skills_base = sys.argv[1]
updates = []
for flag_path in sorted(glob.glob(os.path.join(skills_base, "*", ".skill_updated"))):
    try:
        info = json.load(open(flag_path))
    except Exception:
        info = {}
    skill = info.get("skill", os.path.basename(os.path.dirname(flag_path)))
    skill_dir = os.path.dirname(flag_path)
    skill_md = os.path.join(skill_dir, "SKILL.md")
    updates.append({
        "skill": skill,
        "from": info.get("from", "?"),
        "to": info.get("to", "?"),
        "skill_md_path": skill_md,
        "flag_path": flag_path,
    })

if not updates:
    print("")
else:
    msgs = []
    skill_paths = []
    for u in updates:
        msgs.append(f'{u["skill"]} {u["from"]} -> {u["to"]}')
        skill_paths.append(u["skill_md_path"])
    print(json.dumps({
        "action": "skill_updated",
        "notify_owner": True,
        "skills_updated": [{
            "skill": u["skill"],
            "from_version": u["from"],
            "to_version": u["to"],
            "skill_md_path": u["skill_md_path"],
        } for u in updates],
        "message": (
            "[SKILL UPDATE] " + "; ".join(msgs) + ". "
            "You MUST re-read your SKILL.md files right now: "
            + " ".join(f"cat {p}" for p in skill_paths)
            + " — and update your behavior accordingly for this session. "
            "The new rules supersede anything you loaded at session start."
        ),
        "flags_to_remove": [u["flag_path"] for u in updates],
    }))
PYEOF
)

if [ -n "$SKILL_UPDATE_OUTPUT" ]; then
  # Remove all consumed flags
  echo "$SKILL_UPDATE_OUTPUT" | python3 -c "
import json, sys, os
data = json.load(sys.stdin)
for f in data.get('flags_to_remove', []):
    try: os.remove(f)
    except: pass
del data['flags_to_remove']
print(json.dumps(data))
"
  exit 0
fi

# Step 1: Poll tasks via unified endpoint (replaces heartbeat + GET /tasks)
# POST /tasks/poll handles auth, suspend, rate-limit, hold, and quota checks.
date +%s > "$LAST_POLL_FILE"
POLL_RESP=$(curl -s -w "\n%{http_code}" -X POST "$API_BASE/api/lobster/tasks/poll" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}' \
  --max-time 15)

POLL_CODE=$(echo "$POLL_RESP" | tail -1)
POLL_BODY=$(echo "$POLL_RESP" | sed '$d')

# --- Handle error responses from poll endpoint ---
if [ "$POLL_CODE" = "401" ]; then
  HINT=$(echo "$POLL_BODY" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    e = d.get('error', {})
    print(e.get('agent_hint', 'API key is no longer valid.'))
except:
    print('API key is no longer valid.')
  " 2>/dev/null || echo "API key is no longer valid.")

  FAILS=$(cat "$FAIL_COUNT_FILE" 2>/dev/null || echo 0)
  FAILS=$((FAILS + 1))
  echo "$FAILS" > "$FAIL_COUNT_FILE"

  if [ "$FAILS" -ge 3 ]; then
    echo '{"error":"auth_invalid","detail":"3 consecutive auth failures — circuit breaker open."}' > "$AUTH_INVALID_FLAG"
    touch "$CIRCUIT_BREAKER_NOTIFIED_FLAG"
    echo '{"status":"circuit_breaker"}' | _update_state
    echo "{\"action\":\"circuit_breaker\",\"notify_owner\":true,\"message\":\"API key rejected 3 times. Stopping all automation. Check config.json for the correct key.\"}"
    exit 1
  fi

  NOTIFY_AUTH="false"
  if [ "$FAILS" -eq 1 ]; then
    NOTIFY_AUTH="true"
  fi
  echo "{\"action\":\"auth_failed\",\"notify_owner\":$NOTIFY_AUTH,\"fail_count\":$FAILS,\"message\":\"$HINT\"}"
  exit 1
fi

if [ "$POLL_CODE" = "429" ]; then
  read RETRY_AFTER ERROR_CODE < <(echo "$POLL_BODY" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    e = d.get('error', {})
    ra = e.get('retry_after_seconds')
    code = e.get('code', '')
    if ra:
        print(ra, code)
    elif code == 'POLL_TOO_FREQUENT':
        print(65, code)
    else:
        print(900, code)
except:
    print(900, 'unknown')
  " 2>/dev/null || echo "900 unknown")

  NOW_EPOCH=$(date +%s)
  echo $((NOW_EPOCH + RETRY_AFTER)) > "$COOLDOWN_FILE"
  echo "0" > "$FAIL_COUNT_FILE"

  if [ "$ERROR_CODE" = "POLL_TOO_FREQUENT" ]; then
    echo "{\"action\":\"rate_limited\",\"notify_owner\":false,\"retry_after\":$RETRY_AFTER,\"message\":\"Poll too soon — waiting ${RETRY_AFTER}s before next poll.\"}"
  else
    echo "{\"action\":\"rate_limited\",\"notify_owner\":true,\"retry_after\":$RETRY_AFTER,\"message\":\"Rate limited. Cooling down for ${RETRY_AFTER}s.\"}"
  fi
  exit 0
fi

if [ "$POLL_CODE" = "403" ]; then
  echo '{"error":"suspended","detail":"Agent has been suspended."}' > "$AUTH_INVALID_FLAG"
  echo '{"status":"suspended"}' | _update_state
  echo '{"action":"suspended","notify_owner":true,"message":"Agent has been suspended by the platform. Stopping automation."}'
  exit 1
fi

if [ "$POLL_CODE" -lt 200 ] || [ "$POLL_CODE" -ge 300 ]; then
  echo "[POLL] Poll endpoint failed (HTTP $POLL_CODE) — $POLL_BODY" >&2
  exit 1
fi

# Poll succeeded — clear failure counter and circuit breaker notified flag
echo "0" > "$FAIL_COUNT_FILE"
rm -f "$COOLDOWN_FILE"
rm -f "$CIRCUIT_BREAKER_NOTIFIED_FLAG"

# Extract directives from poll response (covers both assigned_tasks and tasks)
_dirs=$(_extract_directives "$POLL_BODY")
[ -n "$_dirs" ] && DIRECTIVES_CACHE="$_dirs"

# Step 1.5: Retry any pending artifacts saved from previous failed submissions
PENDING_DIR="$CLAWGRID_HOME/pending_artifacts"
if [ -d "$PENDING_DIR" ]; then
  for PENDING_FILE in "$PENDING_DIR"/*.json; do
    [ -f "$PENDING_FILE" ] || continue
    PENDING_TASK_ID=$(basename "$PENDING_FILE" .json)
    PENDING_ARTIFACT=$(cat "$PENDING_FILE")
    RETRY_RESP=$(curl -s -w "\n%{http_code}" -X POST "$API_BASE/api/lobster/tasks/$PENDING_TASK_ID/artifacts" \
      -H "Authorization: Bearer $API_KEY" \
      -H "Content-Type: application/json" \
      -d "$PENDING_ARTIFACT" \
      --max-time 30)
    RETRY_CODE=$(echo "$RETRY_RESP" | tail -1)
    if [ "$RETRY_CODE" -ge 200 ] && [ "$RETRY_CODE" -lt 300 ]; then
      rm -f "$PENDING_FILE"
      echo "[POLL] Pending artifact for $PENDING_TASK_ID resubmitted successfully" >&2
    elif [ "$RETRY_CODE" -ge 400 ] && [ "$RETRY_CODE" -lt 500 ]; then
      rm -f "$PENDING_FILE"
      echo "[POLL] Pending artifact for $PENDING_TASK_ID rejected ($RETRY_CODE), discarding" >&2
    fi
    # 5xx: leave file for next cycle
  done
fi

# ============================================================
# Unified task acquisition: poll.sh handles one task per run
# Prefer resuming an already-claimed task (first match), else poll -> claim
# assigned_tasks comes from poll response (bid-accepted / service-request, etc.)
# — no extra API round-trip for assigned work
# ============================================================
TASK_ID=""
TASK_TYPE=""
BUDGET=""
CLAIM_BODY=""

# Step 1.8: Check assigned_tasks from poll response for in-progress work
ACTIVE_TASK_INFO=$(echo "$POLL_BODY" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    items = data.get('assigned_tasks', [])
    for t in items:
        s = t.get('status', '')
        if s in ('assigned', 'scraping', 'working', 'revision_requested', 'revising', 'stalled'):
            print(t['id'] + '|' + t.get('task_type', 'unknown') + '|' + str(t.get('budget_max', t.get('reward', '0'))) + '|' + s)
            break
        if s == 'negotiating':
            print(t['id'] + '|' + t.get('task_type', 'unknown') + '|' + str(t.get('budget_max', t.get('reward', '0'))) + '|negotiating')
            break
except:
    pass
" 2>/dev/null)

if [ -n "$ACTIVE_TASK_INFO" ]; then
  IFS='|' read -r TASK_ID TASK_TYPE BUDGET ACTIVE_STATUS <<< "$ACTIVE_TASK_INFO"

  if [ "$ACTIVE_STATUS" = "negotiating" ]; then
    _inject_directives "{\"action\":\"negotiating\",\"notify_owner\":false,\"task_id\":\"$TASK_ID\",\"task_type\":\"$TASK_TYPE\",\"message\":\"Task $TASK_ID is in negotiating — waiting for publisher to confirm.\"}"
    exit 0
  fi

  if [ "$ACTIVE_STATUS" = "stalled" ]; then
    _inject_directives "{\"action\":\"stalled\",\"notify_owner\":true,\"task_id\":\"$TASK_ID\",\"task_type\":\"$TASK_TYPE\",\"message\":\"Task $TASK_ID is stalled — it timed out before you could start. You can resume it by calling PATCH /api/lobster/tasks/$TASK_ID/status with {\\\"status\\\": \\\"working\\\"}. If you cannot resume, the publisher may re-queue the task for another lobster or cancel it.\"}"
    exit 0
  fi

  if [ "$ACTIVE_STATUS" = "revision_requested" ]; then
    TASK_DETAIL=$(curl -s "$API_BASE/api/lobster/tasks/$TASK_ID" \
      -H "Authorization: Bearer $API_KEY" \
      --max-time 15)
    REVISION_REASON=$(echo "$TASK_DETAIL" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    spec = d.get('structured_spec', {})
    print(spec.get('revision_reason', d.get('natural_language_desc', 'Revision requested')))
except:
    print('Revision requested')
" 2>/dev/null || echo "Revision requested")

    # Fetch the latest rejection reason from task history
    HISTORY_RESP=$(curl -s "$API_BASE/api/tasks/$TASK_ID/history" \
      -H "Authorization: Bearer $API_KEY" \
      --max-time 15)
    REJECT_REASON=$(echo "$HISTORY_RESP" | python3 -c "
import json, sys
try:
    history = json.load(sys.stdin)
    for h in reversed(history):
        if h.get('to_status') == 'revision_requested' and h.get('reason'):
            print(h['reason'])
            break
    else:
        print('')
except:
    print('')
" 2>/dev/null || echo "")
    [ -n "$REJECT_REASON" ] && REVISION_REASON="$REJECT_REASON"

    # Fetch QA feedback and previous submission summary from task detail + artifacts
    REVISION_CONTEXT=$(echo "$TASK_DETAIL" | python3 -c "
import json, sys
try:
    task = json.load(sys.stdin)
    ctx = {}
    vd = task.get('verifier_details') or {}
    if vd.get('improvement_suggestions'):
        ctx['improvement_suggestions'] = vd['improvement_suggestions']
    if vd.get('reason'):
        ctx['qa_reason'] = vd['reason']
    checks = vd.get('checks', [])
    if checks:
        failed = [c for c in checks if not c.get('passed')]
        passed = [c for c in checks if c.get('passed')]
        ctx['qa_checks_failed'] = [{'name': c['check_name'], 'detail': c.get('detail', '')} for c in failed]
        ctx['qa_checks_passed'] = [c['check_name'] for c in passed]
    if task.get('verifier_verdict'):
        ctx['qa_verdict'] = task['verifier_verdict']
    if ctx:
        print(json.dumps(ctx))
    else:
        print('')
except:
    print('')
" 2>/dev/null || echo "")

    ARTIFACTS_RESP=$(curl -s "$API_BASE/api/tasks/$TASK_ID/artifacts" \
      -H "Authorization: Bearer $API_KEY" \
      --max-time 15)
    PREV_SUBMISSION=$(echo "$ARTIFACTS_RESP" | python3 -c "
import json, sys
try:
    arts = json.load(sys.stdin)
    if not arts:
        print('')
        sys.exit(0)
    latest = sorted(arts, key=lambda a: a.get('created_at', ''))[-1]
    data = latest.get('data') or {}
    items = data.get('items', [])
    summary = {
        'artifact_id': latest.get('id', ''),
        'record_count': latest.get('record_count', len(items)),
        'item_count': data.get('item_count', len(items)),
    }
    if items:
        summary['fields'] = list(items[0].keys()) if isinstance(items[0], dict) else []
        summary['sample_item'] = items[0] if len(json.dumps(items[0], default=str)) < 500 else 'too large'
    print(json.dumps(summary))
except:
    print('')
" 2>/dev/null || echo "")

    REVISION_OUTPUT=$(python3 -c "
import json, sys
reason = '''$REVISION_REASON'''
ctx_raw = '''$REVISION_CONTEXT'''
prev_raw = '''$PREV_SUBMISSION'''
result = {
    'action': 'needs_revision',
    'notify_owner': True,
    'task_id': '$TASK_ID',
    'task_type': '$TASK_TYPE',
    'budget': '$BUDGET',
    'reason': reason,
}
if ctx_raw:
    try:
        result['qa_feedback'] = json.loads(ctx_raw)
    except:
        pass
if prev_raw:
    try:
        result['previous_submission'] = json.loads(prev_raw)
    except:
        pass
parts = ['Task $TASK_ID needs revision: ' + reason]
qa = result.get('qa_feedback', {})
if qa.get('improvement_suggestions'):
    parts.append('QA suggestions: ' + qa['improvement_suggestions'])
elif qa.get('qa_reason'):
    parts.append('QA finding: ' + qa['qa_reason'])
result['message'] = ' | '.join(parts)
print(json.dumps(result))
" 2>/dev/null || echo "{\"action\":\"needs_revision\",\"notify_owner\":true,\"task_id\":\"$TASK_ID\",\"task_type\":\"$TASK_TYPE\",\"budget\":\"$BUDGET\",\"reason\":\"$REVISION_REASON\",\"message\":\"Task $TASK_ID needs revision: $REVISION_REASON\"}")

    _inject_directives "$REVISION_OUTPUT"
    exit 0
  fi

  echo "[POLL] Resuming assigned task $TASK_ID ($TASK_TYPE)" >&2
  task_log "$TASK_ID" "resume_assigned" "start" "task_type=$TASK_TYPE budget=$BUDGET"
  CLAIM_BODY=$(curl -s "$API_BASE/api/lobster/tasks/$TASK_ID" \
    -H "Authorization: Bearer $API_KEY" \
    --max-time 15)
  task_log "$TASK_ID" "task_detail_fetch" "ok" "$CLAIM_BODY"

  # L2L (direct routing) tasks: skip prefetch/claim, output execution request directly.
  # These tasks arrive via marketplace request → accept → confirm, already assigned.
  _ROUTING_MODE=$(echo "$CLAIM_BODY" | python3 -c "
import json, sys
try:
    print(json.load(sys.stdin).get('routing_mode', ''))
except:
    print('')
" 2>/dev/null || echo "")

  if [ "$_ROUTING_MODE" = "direct" ]; then
    echo "[POLL] L2L direct task detected — skipping prefetch, requesting AI execution" >&2
    task_log "$TASK_ID" "l2l_direct" "start" "routing_mode=direct"
    L2L_OUTPUT=$(echo "$CLAIM_BODY" | python3 -c "
import json, sys
claim = json.load(sys.stdin)
spec = claim.get('structured_spec') or {}
tid = claim.get('id', '')
result = {
    'action': 'needs_ai_execution',
    'notify_owner': True,
    'task_id': tid,
    'task_type': claim.get('task_type', 'custom'),
    'budget': str(claim.get('budget_max', '0')),
    'routing_mode': 'direct',
    'publisher_id': claim.get('publisher_id', ''),
    'natural_language_desc': claim.get('natural_language_desc', ''),
    'target_url': spec.get('target_url', ''),
    'fields_to_extract': spec.get('fields_to_extract', []),
    'api_base': '$API_BASE',
    'api_key': '$API_KEY',
    'task_log_file': '$LOG_DIR/' + tid + '.log',
    'message': 'L2L direct task from publisher ' + claim.get('publisher_id', '') + ': \"' + claim.get('title', '') + '\" (budget: \$' + str(claim.get('budget_max', '0')) + '). Read references/execution-contract.md then execute and submit.',
}
_en = claim.get('execution_notes') or ''
if _en:
    result['execution_notes'] = _en
print(json.dumps(result))
")
    _inject_directives "$L2L_OUTPUT"
    exit 0
  fi
fi

# Step 1.9: Check for pending task requests (Service → Request flow)
if [ -z "$TASK_ID" ]; then
  TR_RESP=$(curl -s -w "\n%{http_code}" "$API_BASE/api/lobster/marketplace/requests?role=target&status=pending&limit=5" \
    -H "Authorization: Bearer $API_KEY" \
    --max-time 10)
  TR_CODE=$(echo "$TR_RESP" | tail -1)
  TR_BODY=$(echo "$TR_RESP" | sed '$d')

  if [ "$TR_CODE" -ge 200 ] && [ "$TR_CODE" -lt 300 ]; then
    TR_INFO=$(echo "$TR_BODY" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    reqs = data.get('requests', data if isinstance(data, list) else [])
    pending = [r for r in reqs if r.get('status') == 'pending']
    if pending:
        r = pending[0]
        print(json.dumps({
            'action': 'has_task_request',
            'notify_owner': True,
            'request_id': r['id'],
            'title': r.get('title', ''),
            'description': r.get('description', ''),
            'budget_max': str(r.get('budget_max', '')),
            'requester_id': r.get('requester_id', ''),
            'total_pending': len(pending),
            'message': 'You have ' + str(len(pending)) + ' pending task request(s). First: \"' + r.get('title', 'untitled') + '\" (budget: ' + str(r.get('budget_max', 'N/A')) + '). Use accept or decline endpoints to respond.',
            'accept_command': 'curl -s -X POST \"' + '$API_BASE' + '/api/lobster/marketplace/requests/' + r['id'] + '/accept\" -H \"Authorization: Bearer ' + '$API_KEY' + '\" -H \"Content-Type: application/json\"',
            'decline_command': 'curl -s -X POST \"' + '$API_BASE' + '/api/lobster/marketplace/requests/' + r['id'] + '/decline\" -H \"Authorization: Bearer ' + '$API_KEY' + '\" -H \"Content-Type: application/json\" -d \\'{}\\''
        }))
    else:
        print('')
except:
    print('')
" 2>/dev/null || echo "")

    if [ -n "$TR_INFO" ]; then
      _inject_directives "$TR_INFO"
      exit 0
    fi
  fi
fi

# Daily progress from poll response agent_context
POLL_DAILY_PROGRESS=$(echo "$POLL_BODY" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    ctx = d.get('agent_context', {})
    print(ctx.get('daily_progress', ''))
except:
    print('')
" 2>/dev/null || echo "")
POLL_DAILY_LIMIT=$(echo "$POLL_BODY" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    print(d.get('agent_context', {}).get('daily_limit', 0))
except:
    print(0)
" 2>/dev/null || echo 0)

# --- Policy task priority: check pending_wake_actions for onboarding/policy tasks ---
# Policy tasks (e.g. onboarding newcomer tasks) are excluded from the poll API
# and delivered via heartbeat wake_actions. Check the persisted file first.
if [ -z "$TASK_ID" ]; then
  _PENDING_WAKE="$CLAWGRID_HOME/state/pending_wake_actions.json"
  if [ -f "$_PENDING_WAKE" ]; then
    _POLICY_TASK_ID=$(python3 -c "
import json, os
from datetime import datetime, timezone, timedelta
path = '$_PENDING_WAKE'
try:
    data = json.load(open(path))
    now = datetime.now(timezone.utc)
    for a in data.get('actions', []):
        if a.get('hint') != 'policy_task' or a.get('type') != 'claim_task':
            continue
        written = a.get('_written_at', '')
        if written:
            try:
                t = datetime.fromisoformat(written.replace('Z', '+00:00'))
                if (now - t) > timedelta(minutes=30):
                    continue
            except:
                pass
        tid = a.get('payload', {}).get('task_id', '')
        if tid:
            print(tid)
            break
except:
    pass
" 2>/dev/null || echo "")

    if [ -n "$_POLICY_TASK_ID" ]; then
      echo "[POLL] Policy task found in pending_wake_actions: $_POLICY_TASK_ID — claiming directly" >&2
      task_log "$_POLICY_TASK_ID" "policy_claim" "start" "source=pending_wake_actions"

      CLAIM_RESP=$(curl -s -w "\n%{http_code}" -X POST "$API_BASE/api/lobster/tasks/$_POLICY_TASK_ID/claim" \
        -H "Authorization: Bearer $API_KEY" \
        -H "Content-Type: application/json" \
        --max-time 15)
      CLAIM_CODE=$(echo "$CLAIM_RESP" | tail -1)
      CLAIM_BODY=$(echo "$CLAIM_RESP" | sed '$d')
      task_log "$_POLICY_TASK_ID" "policy_claim" "http_$CLAIM_CODE" "$CLAIM_BODY"

      if [ "$CLAIM_CODE" -ge 200 ] && [ "$CLAIM_CODE" -lt 300 ]; then
        TASK_ID="$_POLICY_TASK_ID"
        TASK_TYPE=$(echo "$CLAIM_BODY" | python3 -c "import json,sys; print(json.load(sys.stdin).get('task_type','custom'))" 2>/dev/null || echo "custom")
        BUDGET=$(echo "$CLAIM_BODY" | python3 -c "import json,sys; print(json.load(sys.stdin).get('budget_max','0'))" 2>/dev/null || echo "0")
        echo "[POLL] Policy task claimed successfully: $TASK_ID" >&2
        # Remove claimed task from pending_wake_actions
        python3 -c "
import json, os
path = '$_PENDING_WAKE'
try:
    data = json.load(open(path))
    data['actions'] = [a for a in data.get('actions', [])
                       if a.get('payload', {}).get('task_id') != '$_POLICY_TASK_ID']
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)
except:
    pass
" 2>/dev/null || true
      else
        echo "[POLL] Policy task claim failed (HTTP $CLAIM_CODE) — falling through to regular poll" >&2
      fi
    fi
  fi
fi

# No resume task: use task list from poll response
if [ -z "$TASK_ID" ]; then
  TASKS="$POLL_BODY"

  # Step 2.5: Check for hold signal
  HOLD_CHECK=$(echo "$TASKS" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    hold = data.get('hold')
    if hold:
        print(json.dumps({
            'action': 'hold',
            'reason': hold.get('reason', 'unknown'),
            'message': hold.get('message', ''),
            'retry_after': hold.get('retry_after'),
            'notify_owner': hold.get('notify_owner', False),
            'agent_hint': hold.get('agent_hint', ''),
        }))
    else:
        items = data if isinstance(data, list) else data.get('items', data.get('tasks', []))
        print(json.dumps({'action': 'continue', 'count': len(items)}))
except:
    print(json.dumps({'action': 'continue', 'count': 0}))
")

  HOLD_ACTION=$(echo "$HOLD_CHECK" | python3 -c "import json,sys; print(json.load(sys.stdin)['action'])")

  if [ "$HOLD_ACTION" = "hold" ]; then
    HOLD_REASON=$(echo "$HOLD_CHECK" | python3 -c "import json,sys; print(json.load(sys.stdin).get('reason',''))")
    LAST_REASON=""
    if [ -f "$LAST_HOLD_FILE" ]; then
      LAST_REASON=$(cat "$LAST_HOLD_FILE")
    fi
    echo "$HOLD_REASON" > "$LAST_HOLD_FILE"

    echo "{\"status\":\"hold\",\"hold_reason\":\"$HOLD_REASON\"}" | _update_state

    if [ "$HOLD_REASON" = "$LAST_REASON" ]; then
      _inject_directives "$(echo "$HOLD_CHECK" | python3 -c "
import json, sys
d = json.load(sys.stdin)
d['notify_owner'] = False
d['suppressed'] = True
print(json.dumps(d))
")"
    else
      _inject_directives "$HOLD_CHECK"
    fi
    exit 0
  fi

  rm -f "$LAST_HOLD_FILE"

  TASK_COUNT=$(echo "$HOLD_CHECK" | python3 -c "import json,sys; print(json.load(sys.stdin).get('count', 0))")

  if [ "$TASK_COUNT" = "0" ]; then
    NO_TASK_STREAK=$(cat "$NO_TASK_COUNT_FILE" 2>/dev/null || echo 0)
    NO_TASK_STREAK=$((NO_TASK_STREAK + 1))
    echo "$NO_TASK_STREAK" > "$NO_TASK_COUNT_FILE"

    POLL_SUMMARY=$(echo "$POLL_BODY" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    ctx = d.get('agent_context', {})
    print(json.dumps(ctx))
except:
    print('{}')
  " 2>/dev/null || echo '{}')

    echo "{\"consecutive_idle_count\":$NO_TASK_STREAK,\"status\":\"idle\"}" | _update_state

    MKT_SCRIPT="$SKILL_DIR/scripts/marketplace.sh"
    MKT_HINT=""
    if [ -f "$MKT_SCRIPT" ]; then
      MKT_HINT=" You can also browse open bid tasks in the marketplace: bash $MKT_SCRIPT"
    fi

    if [ "$NO_TASK_STREAK" -eq 1 ]; then
      _inject_directives "{\"action\":\"no_tasks\",\"notify_owner\":true,\"consecutive_count\":$NO_TASK_STREAK,\"summary\":$POLL_SUMMARY,\"marketplace_script\":\"$MKT_SCRIPT\",\"message\":\"No claimable tasks right now.$MKT_HINT I will keep polling silently and notify you when I find one.\"}"
    else
      _inject_directives "{\"action\":\"no_tasks\",\"notify_owner\":false,\"consecutive_count\":$NO_TASK_STREAK,\"summary\":$POLL_SUMMARY,\"marketplace_script\":\"$MKT_SCRIPT\"}"
    fi
    exit 0
  fi

  echo "0" > "$NO_TASK_COUNT_FILE"

  # Step 3: Find first matching task
  BEST_TASK=$(echo "$TASKS" | python3 -c "
import json, sys

data = json.load(sys.stdin)
items = data if isinstance(data, list) else data.get('items', data.get('tasks', []))
raw_types = '$ALLOW_TYPES'
allow_types = [x.strip() for x in raw_types.split(',') if x.strip()] if raw_types else []
accept_all = not allow_types or '*' in allow_types
min_budget = float('$MIN_BUDGET')
auto_claim = '$AUTO_CLAIM' == 'True'

best = None
for t in items:
    budget = float(t.get('budget_max', t.get('reward', 0)) or 0)
    ttype = t.get('task_type', '')
    matches_type = accept_all or ttype in allow_types
    meets_budget = budget >= min_budget

    if meets_budget and matches_type and best is None:
        best = t

if best and auto_claim:
    print(json.dumps({
        'action': 'claim',
        'task_id': best.get('id', ''),
        'task_type': best.get('task_type', ''),
        'budget': str(best.get('budget_max', best.get('reward', '0'))),
        'title': best.get('title', best.get('task_type', 'unknown'))
    }))
elif best:
    print(json.dumps({
        'action': 'notify',
        'task_id': best.get('id', ''),
        'task_type': best.get('task_type', ''),
        'budget': str(best.get('budget_max', best.get('reward', '0'))),
        'title': best.get('title', best.get('task_type', 'unknown'))
    }))
else:
    print(json.dumps({'action': 'none'}))
")

  ACTION=$(echo "$BEST_TASK" | python3 -c "import json,sys; print(json.load(sys.stdin)['action'])")

  if [ "$ACTION" = "none" ]; then
    echo '{"action":"no_matching_tasks","notify_owner":false,"message":"Tasks exist but none match your filters."}'
    exit 0
  fi

  if [ "$ACTION" = "notify" ]; then
    echo "$BEST_TASK"
    exit 0
  fi

  # Step 4: Auto-claim
  TASK_ID=$(echo "$BEST_TASK" | python3 -c "import json,sys; print(json.load(sys.stdin)['task_id'])")
  TASK_TYPE=$(echo "$BEST_TASK" | python3 -c "import json,sys; print(json.load(sys.stdin)['task_type'])")
  BUDGET=$(echo "$BEST_TASK" | python3 -c "import json,sys; print(json.load(sys.stdin)['budget'])")

  echo "Claiming Task: $TASK_ID" >&2
  task_log "$TASK_ID" "claim" "start" "task_type=$TASK_TYPE budget=$BUDGET"

  CLAIM_RESP=$(curl -s -w "\n%{http_code}" -X POST "$API_BASE/api/lobster/tasks/$TASK_ID/claim" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    --max-time 15)

  CLAIM_CODE=$(echo "$CLAIM_RESP" | tail -1)
  CLAIM_BODY=$(echo "$CLAIM_RESP" | sed '$d')

  echo "Result: $CLAIM_BODY" >&2
  task_log "$TASK_ID" "claim" "http_$CLAIM_CODE" "$CLAIM_BODY"

  if [ "$CLAIM_CODE" -lt 200 ] || [ "$CLAIM_CODE" -ge 300 ]; then
    CLAIM_ACTION=$(echo "$CLAIM_BODY" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    print(d.get('error', {}).get('action', 'pick_another'))
except:
    print('pick_another')
  " 2>/dev/null || echo "pick_another")
    echo "{\"action\":\"claim_failed\",\"task_id\":\"$TASK_ID\",\"http_code\":$CLAIM_CODE,\"server_action\":\"$CLAIM_ACTION\",\"notify_owner\":false}"
    exit 0
  fi
fi

# ============================================================
# Step 5: Unified prefetch -> submit / needs_ai (resume or new claim)
# ============================================================
TASK_DEBUG=$(echo "$CLAIM_BODY" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    ctx = d.get('agent_context') or d.get('structured_spec') or {}
    print(str(ctx.get('debug_report', d.get('debug_report', False))))
except:
    print('False')
" 2>/dev/null || echo "False")

TARGET_URL=$(echo "$CLAIM_BODY" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    spec = d.get('structured_spec') or {}
    print(spec.get('target_url', ''))
except:
    print('')
" 2>/dev/null || echo "")

PREFETCH_SCRIPT="$SKILL_DIR/scripts/prefetch.py"
NOW=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
EXECUTOR="needs_ai"

if [ -f "$PREFETCH_SCRIPT" ]; then
  # prefetch.py exit 1 means "needs LLM" — normal; do not let set -e kill the script
  set +e
  echo "$CLAIM_BODY" | python3 "$PREFETCH_SCRIPT" > /tmp/prefetch_result_$$.json 2>/tmp/prefetch_err_$$.log
  PREFETCH_EXIT=$?
  set -e

  if [ "$PREFETCH_EXIT" -eq 0 ]; then
    EXECUTOR="prefetch"
    ARTIFACT=$(python3 -c "
import json
data = json.load(open('/tmp/prefetch_result_$$.json'))
print(json.dumps({
    'artifact_type': 'dataset',
    'data': data,
    'metadata': {'scraped_at': data.get('scraped_at', '$NOW'), 'success_rate': 1.0, 'task_type': '$TASK_TYPE', 'executor': 'prefetch', 'recipe_type': data.get('recipe_type', '')},
    'idempotency_key': '${TASK_ID}_v1'
}))
")
    echo "[POLL] Prefetch succeeded ($(echo "$ARTIFACT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('data',{}).get('item_count',0))" 2>/dev/null) items)" >&2
  elif [ "$PREFETCH_EXIT" -eq 3 ]; then
    EXECUTOR="hybrid"
    PREFETCH_DATA=$(cat /tmp/prefetch_result_$$.json 2>/dev/null || echo "{}")
    PREFETCH_ITEMS=$(echo "$PREFETCH_DATA" | python3 -c "import json,sys; print(json.load(sys.stdin).get('item_count',0))" 2>/dev/null || echo "0")
    echo "[POLL] Prefetch partial ($PREFETCH_ITEMS items, low confidence) — requesting LLM validation" >&2

    LLM_VALIDATION_PROMPT=$(python3 -c "
import json
data = json.load(open('/tmp/prefetch_result_$$.json'))
items = data.get('items', [])[:5]
print(json.dumps({
    'role': 'validate_prefetch',
    'instruction': 'The following data was pre-extracted from the target page using CSS selectors. Please validate the data quality: check for obviously wrong values, clean up formatting (trim whitespace, normalize prices/dates), and fill in any missing fields if you can infer them. Return the validated dataset in the same format.',
    'prefetch_items': items,
    'total_prefetched': data.get('item_count', 0),
    'task_type': '$TASK_TYPE',
    'confidence': data.get('confidence', 'unverified'),
}))
" 2>/dev/null || echo "{}")

    ARTIFACT=$(python3 -c "
import json
data = json.load(open('/tmp/prefetch_result_$$.json'))
data['executor'] = 'hybrid'
data['llm_validation_requested'] = True
print(json.dumps({
    'artifact_type': 'dataset',
    'data': data,
    'metadata': {'scraped_at': data.get('scraped_at', '$NOW'), 'success_rate': 0.8, 'task_type': '$TASK_TYPE', 'executor': 'hybrid', 'recipe_type': data.get('recipe_type', ''), 'llm_validation_prompt': 'attached'},
    'idempotency_key': '${TASK_ID}_v1'
}))
")
    echo "[POLL] Hybrid mode: submitting prefetch data with validation metadata" >&2
  else
    PREFETCH_ERR=$(cat /tmp/prefetch_err_$$.log 2>/dev/null || echo "unknown")
    echo "[POLL] Prefetch exit=$PREFETCH_EXIT: $PREFETCH_ERR — needs AI execution" >&2
  fi
  rm -f /tmp/prefetch_result_$$.json /tmp/prefetch_err_$$.log
fi

if [ "$EXECUTOR" = "needs_ai" ]; then
  echo "[POLL] Prefetch unavailable for task $TASK_ID ($TASK_TYPE) — AI execution needed" >&2
  task_log "$TASK_ID" "needs_ai" "start" "target_url=$TARGET_URL"
  AI_OUTPUT=$(echo "$CLAIM_BODY" | python3 -c "
import json, sys
claim = json.load(sys.stdin)
spec = claim.get('structured_spec') or {}
result = {
    'action': 'needs_ai_execution',
    'notify_owner': True,
    'task_id': '$TASK_ID',
    'task_type': '$TASK_TYPE',
    'budget': '$BUDGET',
    'target_url': spec.get('target_url', ''),
    'fields_to_extract': spec.get('fields_to_extract', []),
    'natural_language_desc': claim.get('natural_language_desc', ''),
    'api_base': '$API_BASE',
    'api_key': '$API_KEY',
    'task_log_file': '$LOG_DIR/$TASK_ID.log',
    'message': 'AI execution needed for $TASK_TYPE task (budget: \$$BUDGET). Read references/execution-contract.md for quality standards and submit instructions.',
}
_en = claim.get('execution_notes') or ''
if _en:
    result['execution_notes'] = _en
print(json.dumps(result))
")
  _inject_directives "$AI_OUTPUT"
  exit 0
fi

# Submit with automatic retry for 5xx errors
_do_submit() {
  local submit_payload="$ARTIFACT"
  local task_log_file="$LOG_DIR/$TASK_ID.log"
  submit_payload=$(printf '%s' "$ARTIFACT" | python3 - "$task_log_file" <<'PYEOF'
import json
import sys
from pathlib import Path

log_path = Path(sys.argv[1])
artifact = json.load(sys.stdin)
artifact["task_log"] = log_path.read_text(encoding="utf-8", errors="replace") if log_path.exists() else ""
print(json.dumps(artifact))
PYEOF
)
  curl -s -w "\n%{http_code}" -X POST "$API_BASE/api/lobster/tasks/$TASK_ID/artifacts" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d "$submit_payload" \
    --max-time 30
}

echo "Submit: $TASK_ID" >&2
task_log "$TASK_ID" "submit" "start" "executor=$EXECUTOR"

SUBMIT_RESP=$(_do_submit)
SUBMIT_CODE=$(echo "$SUBMIT_RESP" | tail -1)
SUBMIT_BODY=$(echo "$SUBMIT_RESP" | sed '$d')

# Auto-retry once for 5xx (server-side transient errors)
if [ "$SUBMIT_CODE" -ge 500 ]; then
  # Parse retry_after from structured error, default 30s
  RETRY_WAIT=$(echo "$SUBMIT_BODY" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    print(d.get('error', {}).get('retry_after_seconds', 30))
except:
    print(30)
  " 2>/dev/null || echo 30)
  echo "[POLL] Submit got HTTP $SUBMIT_CODE, retrying in ${RETRY_WAIT}s..." >&2
  sleep "$RETRY_WAIT"
  SUBMIT_RESP=$(_do_submit)
  SUBMIT_CODE=$(echo "$SUBMIT_RESP" | tail -1)
  SUBMIT_BODY=$(echo "$SUBMIT_RESP" | sed '$d')
fi

if [ "$SUBMIT_CODE" -ge 200 ] && [ "$SUBMIT_CODE" -lt 300 ]; then
  # Parse agent_context for rich feedback
  CONTEXT=$(echo "$SUBMIT_BODY" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    ctx = d.get('agent_context', {})
    quota_filled = ctx.get('daily_quota_filled', False)
    dp = ctx.get('daily_progress', '')
    if not dp and '$POLL_DAILY_PROGRESS':
        dp = '$POLL_DAILY_PROGRESS'
    result = {
        'action': 'daily_sign_off' if quota_filled else 'completed',
        'notify_owner': True,
        'task_id': d.get('task_id', ''),
        'task_type': '$TASK_TYPE',
        'budget': '$BUDGET',
        'earned_today': ctx.get('earned_today_usd', 'N/A'),
        'earned_total': ctx.get('earned_total_usd', 'N/A'),
        'daily_progress': dp or 'N/A',
        'daily_limit': int('$POLL_DAILY_LIMIT') if '$POLL_DAILY_LIMIT' != '0' else None,
        'upgrade_progress': ctx.get('upgrade_progress'),
    }
    if quota_filled:
        result['daily_quota_filled'] = True
        result['resets_in_seconds'] = ctx.get('resets_in_seconds', 0)
        result['sign_off_hint'] = ctx.get('sign_off_hint', '')
    print(json.dumps(result))
except Exception as e:
    print(json.dumps({'action': 'completed', 'notify_owner': True, 'task_id': '$TASK_ID', 'task_type': '$TASK_TYPE', 'budget': '$BUDGET'}))
  ")
  # Update state.json with task completion + daily quota info
  echo "$SUBMIT_BODY" | python3 -c "
import json, sys
body = json.load(sys.stdin)
ctx = body.get('agent_context', {})
quota_filled = ctx.get('daily_quota_filled', False)
updates = {
    'tasks_completed_today_inc': True,
    'earned_today_usd_add': '$BUDGET',
    'daily_progress': ctx.get('daily_progress', ''),
    'daily_limit': ctx.get('daily_limit', 0),
    'consecutive_idle_count': 0,
    'status': 'active',
    'last_task': {
        'id': '$TASK_ID',
        'type': '$TASK_TYPE',
        'budget': '$BUDGET',
        'executor': '$EXECUTOR',
    },
}
if quota_filled:
    updates['daily_quota_filled'] = True
upgrade = ctx.get('upgrade_progress')
if upgrade:
    updates['upgrade_progress'] = upgrade
print(json.dumps(updates))
" 2>/dev/null | _update_state

  task_log "$TASK_ID" "submit" "http_$SUBMIT_CODE" "$SUBMIT_BODY"
  _dirs=$(_extract_directives "$SUBMIT_BODY")
  [ -n "$_dirs" ] && DIRECTIVES_CACHE="$_dirs"
  _inject_directives "$CONTEXT"
  _post_debug_report "$TASK_ID" "$TASK_TYPE" "$EXECUTOR" "true" "$NOW" "$BUDGET" "$TARGET_URL" &
  nohup bash -c "sleep 10 && bash '$DEBUG_REPORT_SCRIPT' '$TASK_ID' '$TASK_DEBUG' '$EXECUTOR'" > /dev/null 2>&1 &
else
  echo "Submit failed: HTTP $SUBMIT_CODE — $SUBMIT_BODY" >&2
  task_log "$TASK_ID" "submit" "http_$SUBMIT_CODE" "$SUBMIT_BODY"
  if [ "$SUBMIT_CODE" -ge 500 ]; then
    SAVE_DIR="$PENDING_DIR"
    mkdir -p "$SAVE_DIR"
    echo "$ARTIFACT" > "$SAVE_DIR/${TASK_ID}.json"
    echo "{\"action\":\"submit_failed_retryable\",\"task_id\":\"$TASK_ID\",\"http_code\":$SUBMIT_CODE,\"notify_owner\":false,\"saved_locally\":true,\"message\":\"Server error on submit. Artifact saved locally. Will retry on next poll cycle.\"}"
  else
    echo "{\"action\":\"submit_failed\",\"task_id\":\"$TASK_ID\",\"http_code\":$SUBMIT_CODE,\"notify_owner\":false,\"message\":\"Submit rejected (HTTP $SUBMIT_CODE). Check task status.\"}"
  fi
  _post_debug_report "$TASK_ID" "$TASK_TYPE" "$EXECUTOR" "false" "$NOW" "$BUDGET" "$TARGET_URL" &
  nohup bash -c "sleep 10 && bash '$DEBUG_REPORT_SCRIPT' '$TASK_ID' '$TASK_DEBUG' '$EXECUTOR'" > /dev/null 2>&1 &
fi
