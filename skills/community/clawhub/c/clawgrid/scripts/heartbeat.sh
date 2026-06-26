#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$HOME/.openclaw/workspace/skills/clawgrid-connector"
source "$SKILL_DIR/scripts/_clawgrid_env.sh"
LAUNCHD_LABEL="ai.clawgrid.heartbeat"
LAUNCHD_PLIST="$HOME/Library/LaunchAgents/${LAUNCHD_LABEL}.plist"

if [ ! -f "$CONFIG" ]; then
  echo "Config not found at $CONFIG — run setup first" >&2
  exit 1
fi

_ensure_openclaw_path() {
  for _ndir in "$HOME/.nvm/versions/node/"*/bin; do
    [ -d "$_ndir" ] && case ":$PATH:" in *":$_ndir:"*) ;; *) export PATH="$_ndir:$PATH" ;; esac
  done
  [ -d "$HOME/.npm-global/bin" ] && case ":$PATH:" in *":$HOME/.npm-global/bin:"*) ;; *) export PATH="$HOME/.npm-global/bin:$PATH" ;; esac
}

_notify_owner() {
  local _msg="$1"
  _ensure_openclaw_path
  local _oc
  _oc=$(command -v openclaw 2>/dev/null || echo "")
  [ -z "$_oc" ] && return

  "$_oc" cron add \
    --name "notify-$(date +%s)" --at "3s" \
    --message "$_msg" \
    --session isolated --announce --channel last --best-effort-deliver \
    --delete-after-run --timeout-seconds 30 2>/dev/null || true

  "$_oc" system event --text "$_msg" --mode now 2>/dev/null || true
  echo "[HEARTBEAT] notify: announce cron + system event dispatched" >&2
}

API_KEY=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_key'])")
API_BASE=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_base'])")

remove_heartbeat_cron() {
  bash "$SKILL_DIR/scripts/heartbeat-ctl.sh" stop --quiet >/dev/null 2>&1 || true
  echo "[HEARTBEAT] Self-removed from scheduler to stop retry loop." >&2
}

should_stop_cron() {
  echo "$1" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    action = d.get('error', {}).get('action', '') if 'error' in d else d.get('action', '')
    print('yes' if action == 'stop_cron' else 'no')
except Exception:
    print('no')
" 2>/dev/null || echo "no"
}

# --- Identity verification via heartbeat ---
RESP=$(curl -s -w "\n%{http_code}" -X POST "$API_BASE/api/lobster/heartbeat" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}' \
  --max-time 15)

HTTP_CODE=$(echo "$RESP" | tail -1)
# Portable "all but last line" (BSD head does not support head -n -1)
BODY=$(echo "$RESP" | sed '$d')

if [ "$HTTP_CODE" = "401" ]; then
  echo "[HEARTBEAT] AUTH_INVALID: API key rejected (HTTP 401). Need re-registration." >&2
  echo "{\"error\": \"auth_invalid\", \"detail\": \"API key $API_KEY is no longer valid. Run setup again.\"}" > "$AUTH_INVALID_FLAG"
  remove_heartbeat_cron
  echo "AUTH_INVALID"
  exit 1
fi

if [ "$HTTP_CODE" = "403" ]; then
  echo "[HEARTBEAT] SUSPENDED: Agent has been suspended (HTTP 403)." >&2
  echo "{\"error\": \"suspended\", \"detail\": \"$BODY\"}" > "$AUTH_INVALID_FLAG"
  remove_heartbeat_cron
  echo "SUSPENDED"
  exit 1
fi

if [ "$HTTP_CODE" -lt 200 ] || [ "$HTTP_CODE" -ge 300 ]; then
  echo "[HEARTBEAT] Heartbeat failed: HTTP $HTTP_CODE — $BODY" >&2
  if [ "$(should_stop_cron "$BODY")" = "yes" ]; then
    echo "{\"error\": \"stop_cron\", \"detail\": \"Server requested cron stop (HTTP $HTTP_CODE).\"}" > "$AUTH_INVALID_FLAG"
    remove_heartbeat_cron
  fi
  exit 1
fi

# Heartbeat succeeded — clear any previous auth failure flag
if [ -f "$AUTH_INVALID_FLAG" ]; then
  rm -f "$AUTH_INVALID_FLAG"
fi

# --- Auto-update skill via install.sh (before wake dispatch) ---
INSTALL_SCRIPT="$SKILL_DIR/scripts/install.sh"
if [ -x "$INSTALL_SCRIPT" ]; then
  _UPDATE_OUT=$(bash "$INSTALL_SCRIPT" --quiet 2>/dev/null) || true
  if [ -n "$_UPDATE_OUT" ]; then
    echo "[HEARTBEAT] install: $(echo "$_UPDATE_OUT" | head -1)" >&2
  fi
fi

# If skill was just updated, re-run exec approval setup with the new script
_SKILL_UPDATED_FLAG="$SKILL_DIR/.skill_updated"
_EXEC_APPROVAL_DONE="$CLAWGRID_HOME/state/.exec_approval_configured"
if [ -f "$_SKILL_UPDATED_FLAG" ]; then
  rm -f "$_EXEC_APPROVAL_DONE"
  rm -f "$_SKILL_UPDATED_FLAG"
fi

# --- Migration: auto-configure exec approval for automated sessions ---
if [ ! -f "$_EXEC_APPROVAL_DONE" ]; then
  SETUP_EXEC="$SKILL_DIR/scripts/setup-exec-approval.sh"
  if [ -x "$SETUP_EXEC" ]; then
    if bash "$SETUP_EXEC" --quiet 2>/dev/null; then
      mkdir -p "$CLAWGRID_HOME/state"
      touch "$_EXEC_APPROVAL_DONE"
      echo "[HEARTBEAT] exec_approval: configured" >&2
    else
      echo "[HEARTBEAT] exec_approval: setup failed, will retry" >&2
    fi
  else
    mkdir -p "$CLAWGRID_HOME/state"
    touch "$_EXEC_APPROVAL_DONE"
  fi
fi

# --- Retry: nudge AI if a policy task was claimed but not yet executed ---
_APT_FILE="$CLAWGRID_HOME/state/active_policy_task.json"
_APT_STATUS=$(python3 -c "
import json, sys, os
from datetime import datetime, timezone
path = sys.argv[1]
if not os.path.exists(path):
    print('none'); sys.exit(0)
try:
    with open(path) as f:
        d = json.load(f)
    status = d.get('status', '')
    if status != 'claimed':
        print(status); sys.exit(0)
    claimed = d.get('claimed_at', '')
    if claimed:
        age = (datetime.now(timezone.utc) - datetime.fromisoformat(claimed)).total_seconds()
        if age > 120:
            print('retry')
        else:
            print('waiting')
    else:
        print('retry')
except Exception:
    print('none')
" "$_APT_FILE" 2>/dev/null || echo "none")

# Sync: if file says "claimed" but task was already submitted, auto-update the file
if [ "$_APT_STATUS" = "retry" ] || [ "$_APT_STATUS" = "waiting" ]; then
  _SYNC_TID=$(python3 -c "import json; print(json.load(open('$_APT_FILE'))['task_id'])" 2>/dev/null || true)
  _SYNC_TITLE=$(python3 -c "import json; print(json.load(open('$_APT_FILE')).get('title','newcomer task'))" 2>/dev/null || echo "newcomer task")
  if [ -n "$_SYNC_TID" ]; then
    source "$SKILL_DIR/scripts/_clawgrid_env.sh"
    _TASK_STATUS=$(curl -s -H "Authorization: Bearer $(python3 -c "import json; print(json.load(open('$CONFIG'))['api_key'])" 2>/dev/null)" \
      "$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_base'])" 2>/dev/null)/api/lobster/tasks/$_SYNC_TID" \
      --max-time 5 2>/dev/null | python3 -c "import json,sys; print(json.load(sys.stdin).get('status',''))" 2>/dev/null || true)
    if [ "$_TASK_STATUS" = "qa_checking" ] || [ "$_TASK_STATUS" = "completed" ] || [ "$_TASK_STATUS" = "approved" ]; then
      echo "[HEARTBEAT] sync: task $_SYNC_TID already $_TASK_STATUS, updating trigger file" >&2
      python3 -c "
import json
with open('$_APT_FILE') as f:
    d = json.load(f)
d['status'] = 'submitted'
with open('$_APT_FILE', 'w') as f:
    json.dump(d, f, ensure_ascii=False)
" 2>/dev/null || true
      _notify_owner "[ClawGrid.ai] Newcomer task completed: $_SYNC_TITLE ($_TASK_STATUS). Submitted for review!"
      _APT_STATUS="submitted"
    elif [ "$_TASK_STATUS" = "queued" ] || [ "$_TASK_STATUS" = "cancelled" ] || [ -z "$_TASK_STATUS" ]; then
      echo "[HEARTBEAT] sync: task $_SYNC_TID is $_TASK_STATUS (released/gone), removing stale trigger file" >&2
      rm -f "$_APT_FILE"
      _APT_STATUS="none"
    fi
  fi
fi

if [ "$_APT_STATUS" = "retry" ]; then
  _APT_TID=$(python3 -c "import json; print(json.load(open('$_APT_FILE'))['task_id'])" 2>/dev/null || true)
  _APT_TITLE=$(python3 -c "import json; print(json.load(open('$_APT_FILE')).get('title','newcomer task'))" 2>/dev/null || true)
  if [ -n "$_APT_TID" ]; then
    echo "[HEARTBEAT] retry: nudging AI for stale policy_task $_APT_TID" >&2

    _notify_owner "[ClawGrid.ai] Reminder: newcomer task in progress — $_APT_TITLE. Still working on it."

    _ensure_openclaw_path
    _OC=$(command -v openclaw 2>/dev/null || echo "")
    if [ -n "$_OC" ]; then
      "$_OC" cron add \
        --name "retry-exec-$(date +%s)" --at "8s" \
        --message "[ClawGrid.ai] Execute the newcomer task: $_APT_TITLE (ID: $_APT_TID). Submit the result and notify the owner." \
        --session isolated --no-deliver \
        --delete-after-run --timeout-seconds 300 2>/dev/null || true
      echo "[HEARTBEAT] retry: exec cron dispatched (isolated 300s)" >&2
    fi
  fi
fi

WAKE_FLAG=$(echo "$BODY" | python3 -c "import json,sys; print('true' if json.load(sys.stdin).get('wake') else 'false')" 2>/dev/null || echo "false")
echo "[HEARTBEAT] OK wake=$WAKE_FLAG" >&2

# --- Smart wake: parse wake_actions, compute timeout, collect no-ack IDs ---
WAKE_INFO=$(echo "$BODY" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    if not d.get('wake'):
        sys.exit(0)
    actions = d.get('wake_actions', [])
    hints = [a.get('hint','') for a in actions]
    types = [a.get('type','') for a in actions]
    # owner_instruction takes priority over hint-based classification
    mode = None
    for a in actions:
        oi = a.get('payload', {}).get('owner_instruction', {})
        rb = oi.get('required_behavior', '')
        if rb == 'must_ask_owner':
            mode = 'interactive'
            break
        if rb == 'check_condition_first':
            mode = 'interactive'
            break
        if rb == 'inform_and_proceed':
            mode = 'interactive'
            break
    if mode is None:
        if any(h in ('action_required','review_recommended','owner_decision','check_condition','owner_decision_required','inform_and_proceed') for h in hints):
            mode = 'interactive'
        elif any(h == 'auto_claimable' for h in hints):
            mode = 'silent'
        else:
            mode = 'announce'
    timeout = 0
    for a in actions:
        th = a.get('payload', {}).get('timeout_hint', 0)
        if isinstance(th, (int, float)) and th > timeout:
            timeout = int(th)
    if timeout == 0:
        td = {'execute_task': 600, 'handle_revision': 600}
        for t in types:
            if td.get(t, 0) > timeout:
                timeout = td[t]
    if timeout == 0:
        timeout = {'interactive': 180, 'silent': 180, 'announce': 60}.get(mode, 120)
    no_ack = []
    model_hint = ''
    for a in actions:
        if a.get('type') in ('execute_task', 'handle_revision'):
            nid = a.get('payload', {}).get('notification_id')
            if nid:
                no_ack.append(nid)
            mh = a.get('payload', {}).get('model_hint', '')
            if mh and not model_hint:
                model_hint = mh
    msg = d.get('wake_message', '')
    print(json.dumps({'mode': mode, 'message': msg, 'timeout': timeout, 'no_ack_ids': no_ack, 'model_hint': model_hint}))
except Exception:
    pass
" 2>/dev/null || true)

# --- Delivery target resolution ---
# Look up the owner's most-recent DM session from the openclaw session store.
# Channel-agnostic: works with any channel (Discord, Telegram, WhatsApp, Slack, etc.)
# Returns JSON {"channel":"<name>","to":"<target>","accountId":"<id>"} or empty.
_resolve_delivery_target() {
  local sf="$HOME/.openclaw/agents/main/sessions/sessions.json"
  [ ! -f "$sf" ] && return 0
  python3 -c "
import json, sys
try:
    with open(sys.argv[1]) as f:
        data = json.load(f)
    best = None
    for key, val in data.items():
        parts = key.split(':')
        if len(parts) >= 5 and parts[3] in ('direct', 'private'):
            updated = val.get('updatedAt', 0)
            dc = val.get('deliveryContext', {})
            ch = dc.get('channel', '')
            to = dc.get('to', '')
            if not ch or not to or not to.strip():
                continue
            if best is None or updated > best[0]:
                best = (updated, ch, to, dc.get('accountId','default'))
    if best:
        print(json.dumps({'channel': best[1], 'to': best[2], 'accountId': best[3]}))
except Exception:
    pass
" "$sf" 2>/dev/null || true
}

# --- Active session check ---
# Returns "yes" if a clawgrid-initiated openclaw session is currently running.
# Reads sessions.json and filters by label prefix "Cron: clawgrid-" so that
# user conversations and other skills' sessions are not counted.
_has_active_session() {
  local sf="$HOME/.openclaw/agents/main/sessions/sessions.json"
  [ ! -f "$sf" ] && echo "no" && return 0
  python3 -c "
import json, sys, time
try:
    with open(sys.argv[1]) as f:
        data = json.load(f)
    now_ms = time.time() * 1000
    for key, val in data.items():
        label = val.get('label', '')
        if not label.startswith('Cron: clawgrid-'):
            continue
        updated = val.get('updatedAt', 0)
        if now_ms - updated < 150000:
            print('yes'); sys.exit(0)
except Exception:
    pass
print('no')
" "$sf" 2>/dev/null || echo "no"
}

# --- Persist owner delivery target ---
# Write the resolved DM target to a well-known file so the AI agent can
# read it during sessions instead of guessing chat IDs / nicknames.
_OD_FILE="$CLAWGRID_HOME/state/owner_delivery.json"
_OD_RESULT=$(_resolve_delivery_target)
if [ -n "$_OD_RESULT" ]; then
  mkdir -p "$CLAWGRID_HOME/state"
  echo "$_OD_RESULT" > "$_OD_FILE"
fi

# --- Gateway health probe ---
# Quick check: is the gateway reachable and does any channel have a working token?
# Returns: "connected", "configured", or "unreachable"
_probe_gateway_status() {
  local oc="$1"
  "$oc" health --json --timeout 3000 2>/dev/null | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    channels = d.get('channels', {})
    if not isinstance(channels, dict):
        print('unreachable'); sys.exit(0)
    for name, info in channels.items():
        if not isinstance(info, dict):
            continue
        probe = info.get('probe', {})
        if probe.get('ok'):
            print('connected'); sys.exit(0)
        if info.get('configured'):
            print('configured'); sys.exit(0)
    print('unreachable')
except Exception:
    print('unreachable')
" 2>/dev/null || echo "unreachable"
}

if [ -n "$WAKE_INFO" ]; then
  MODE=$(echo "$WAKE_INFO" | python3 -c "import json,sys; print(json.load(sys.stdin).get('mode',''))" 2>/dev/null || true)
  MSG=$(echo "$WAKE_INFO" | python3 -c "import json,sys; print(json.load(sys.stdin).get('message',''))" 2>/dev/null || true)
  _TIMEOUT=$(echo "$WAKE_INFO" | python3 -c "import json,sys; print(json.load(sys.stdin).get('timeout',120))" 2>/dev/null || echo "120")
  _NO_ACK_JSON=$(echo "$WAKE_INFO" | python3 -c "import json,sys; print(json.dumps(json.load(sys.stdin).get('no_ack_ids',[])))" 2>/dev/null || echo "[]")
  _MODEL_HINT=$(echo "$WAKE_INFO" | python3 -c "import json,sys; print(json.load(sys.stdin).get('model_hint',''))" 2>/dev/null || true)

  if [ -n "$MODE" ] && [ -n "$MSG" ]; then
    # --- Persist wake_actions so any session (including main) can read them ---
    _PENDING_FILE="$CLAWGRID_HOME/state/pending_wake_actions.json"
    echo "$BODY" | python3 -c "
import json, sys, os
from datetime import datetime, timezone
try:
    body = json.load(sys.stdin)
    new_actions = body.get('wake_actions', [])
    if not new_actions:
        sys.exit(0)
    now = datetime.now(timezone.utc).isoformat()
    path = sys.argv[1]
    existing = []
    if os.path.exists(path):
        try:
            with open(path) as f:
                data = json.load(f)
            existing = data.get('actions', [])
        except Exception:
            pass
    seen_ids = set()
    merged = []
    for a in new_actions:
        key = a.get('payload', {}).get('task_id') or a.get('payload', {}).get('request_id') or ''
        nid = a.get('payload', {}).get('notification_id', '')
        uid = f'{a.get(\"type\",\"\")}:{key}:{nid}'
        if uid not in seen_ids:
            seen_ids.add(uid)
            a['_written_at'] = now
            merged.append(a)
    for a in existing:
        key = a.get('payload', {}).get('task_id') or a.get('payload', {}).get('request_id') or ''
        nid = a.get('payload', {}).get('notification_id', '')
        uid = f'{a.get(\"type\",\"\")}:{key}:{nid}'
        if uid not in seen_ids:
            written = a.get('_written_at', '')
            if written:
                from datetime import datetime as dt
                try:
                    age = (datetime.now(timezone.utc) - dt.fromisoformat(written)).total_seconds()
                    if age > 1800:
                        continue
                except Exception:
                    pass
            seen_ids.add(uid)
            merged.append(a)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump({'updated_at': now, 'actions': merged}, f, ensure_ascii=False)
except Exception:
    pass
" "$_PENDING_FILE" 2>/dev/null || true

    # --- Cache server owner_instructions to local state for offline fallback ---
    _SERVER_INSTR_FILE="$CLAWGRID_HOME/state/server_instructions.json"
    echo "$BODY" | python3 -c "
import json, sys, os
from datetime import datetime, timezone
try:
    body = json.load(sys.stdin)
    actions = body.get('wake_actions', [])
    instructions = {}
    for a in actions:
        oi = a.get('payload', {}).get('owner_instruction')
        if oi and isinstance(oi, dict):
            atype = a.get('type', '')
            stage_map = {
                'claim_task': 'on_claim', 'bid_on_task': 'on_claim',
                'execute_task': 'on_execute', 'handle_revision': 'on_revision',
                'review_submission': 'on_review', 'review_bid': 'on_bid_review',
                'task_request': 'on_task_request',
            }
            stage = stage_map.get(atype)
            if stage and stage not in instructions:
                instructions[stage] = oi
    if instructions:
        path = sys.argv[1]
        existing = {}
        if os.path.exists(path):
            try:
                with open(path) as f:
                    existing = json.load(f)
            except Exception:
                pass
        existing.update(instructions)
        existing['_cached_at'] = datetime.now(timezone.utc).isoformat()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump(existing, f, ensure_ascii=False)
except Exception:
    pass
" "$_SERVER_INSTR_FILE" 2>/dev/null || true

    # --- Auto-claim policy tasks (deterministic, no AI needed) ---
    _PT_ID=$(echo "$BODY" | python3 -c "
import json, sys
try:
    body = json.load(sys.stdin)
    for a in body.get('wake_actions', []):
        if a.get('hint') == 'policy_task' and a.get('type') == 'claim_task':
            tid = a.get('payload', {}).get('task_id', '')
            if tid:
                print(tid)
                break
except Exception:
    pass
" 2>/dev/null || true)

    _POLICY_CLAIMED=""
    _CLAIM_COOLDOWN_FILE="$CLAWGRID_HOME/state/policy_claim_cooldown"
    if [ -n "$_PT_ID" ]; then
      # Skip if a recent claim failure is still in cooldown (5 min)
      _IN_COOLDOWN=$(python3 -c "
import os, sys
from datetime import datetime, timezone, timedelta
path = sys.argv[1]
if not os.path.exists(path):
    print('no')
else:
    try:
        mtime = os.path.getmtime(path)
        age = datetime.now(timezone.utc).timestamp() - mtime
        print('yes' if age < 300 else 'no')
    except Exception:
        print('no')
" "$_CLAIM_COOLDOWN_FILE" 2>/dev/null || echo "no")

      if [ "$_IN_COOLDOWN" = "yes" ]; then
        echo "[HEARTBEAT] policy_task claim in cooldown, skipping" >&2
      else
      echo "[HEARTBEAT] auto-claim policy_task: $_PT_ID" >&2
      _CLAIM_OUT=$(bash "$SKILL_DIR/scripts/claim.sh" "$_PT_ID" 2>/dev/null || echo '{"action":"error"}')
      _CLAIM_ACT=$(echo "$_CLAIM_OUT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('action',''))" 2>/dev/null || echo "error")
      echo "[HEARTBEAT] policy_task claim result: $_CLAIM_ACT" >&2
      if [ "$_CLAIM_ACT" = "claimed" ]; then
        rm -f "$_CLAIM_COOLDOWN_FILE" 2>/dev/null
        _POLICY_CLAIMED="$_PT_ID"
        _PT_TITLE=$(echo "$_CLAIM_OUT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('title','newcomer task'))" 2>/dev/null || echo "newcomer task")

        # Write trigger file for AI boot check (primary delivery mechanism)
        mkdir -p "$CLAWGRID_HOME/state"
        python3 -c "
import json, sys
from datetime import datetime, timezone
data = {
    'task_id': sys.argv[1],
    'title': sys.argv[2],
    'status': 'claimed',
    'claimed_at': datetime.now(timezone.utc).isoformat(),
    'skill_dir': sys.argv[3],
}
with open(sys.argv[4], 'w') as f:
    json.dump(data, f, ensure_ascii=False)
" "$_PT_ID" "$_PT_TITLE" "$SKILL_DIR" "$_APT_FILE" 2>/dev/null || true
        echo "[HEARTBEAT] wrote active_policy_task.json" >&2

        echo "[HEARTBEAT] policy_task claimed, dispatching notify + execute" >&2
        MSG="[ClawGrid.ai] A newcomer task was auto-claimed for you: \"$_PT_TITLE\" (ID: $_PT_ID). Execute the task, submit the result, and notify the owner about the submission."

        _notify_owner "[ClawGrid.ai] Auto-claimed newcomer task: $_PT_TITLE. Working on it now, will notify when done."
      else
        # Claim failed — enter 5-min cooldown to avoid retrying every heartbeat
        mkdir -p "$CLAWGRID_HOME/state"
        date -u +%s > "$_CLAIM_COOLDOWN_FILE" 2>/dev/null || true
        echo "[HEARTBEAT] policy_task claim failed ($_CLAIM_ACT), cooldown 5min" >&2
      fi
      fi
    fi

    # Append onboarding directives to wake message (only if not a fresh policy claim)
    if [ -z "$_POLICY_CLAIMED" ]; then
      _OB_MSG=$(echo "$BODY" | python3 -c "
import json, sys
try:
    body = json.load(sys.stdin)
    for d in body.get('_directives', []):
        if d.get('type') == 'onboarding':
            cfg = d.get('config', {})
            msg = d.get('message', '')
            hint = cfg.get('hint', '')
            parts = ['\n\n[Onboarding] ' + msg]
            if hint:
                parts.append('Hint: ' + hint)
            print(' '.join(parts))
            break
except:
    pass
" 2>/dev/null || echo "")
      [ -n "$_OB_MSG" ] && MSG="$MSG$_OB_MSG"
    fi

    # Skip dispatch if there is already an active openclaw session running
    # (prevents duplicate wakes when execute_task notifications are not ACK'd)
    # Exception: always dispatch after a fresh policy_task auto-claim
    _ACTIVE=$(_has_active_session)
    if [ "$_ACTIVE" = "yes" ] && [ -z "$_POLICY_CLAIMED" ]; then
      echo "[HEARTBEAT] active session detected, skipping wake dispatch" >&2
    else
      [ -n "$_POLICY_CLAIMED" ] && echo "[HEARTBEAT] forcing dispatch after policy_task auto-claim" >&2
      # Ensure nvm node is in PATH (cron has minimal PATH without nvm)
      for _ndir in "$HOME/.nvm/versions/node/"*/bin; do
        [ -d "$_ndir" ] && case ":$PATH:" in *":$_ndir:"*) ;; *) export PATH="$_ndir:$PATH" ;; esac
      done
      [ -d "$HOME/.npm-global/bin" ] && case ":$PATH:" in *":$HOME/.npm-global/bin:"*) ;; *) export PATH="$HOME/.npm-global/bin:$PATH" ;; esac

      OPENCLAW_BIN=$(command -v openclaw 2>/dev/null || echo "")
      if [ -z "$OPENCLAW_BIN" ]; then
        for _p in /opt/homebrew/bin/openclaw /usr/local/bin/openclaw "$HOME/.local/bin/openclaw"; do
          [ -x "$_p" ] && OPENCLAW_BIN="$_p" && break
        done
      fi
      _WAKE_DISPATCHED=1
      if [ -n "$OPENCLAW_BIN" ]; then
        # --- Layered delivery strategy ---
        _DELIVER_FLAGS="--no-deliver"

        if [ "$MODE" != "silent" ]; then
          _DT=$(_resolve_delivery_target)
          if [ -n "$_DT" ]; then
            _D_CH=$(echo "$_DT" | python3 -c "import json,sys; print(json.load(sys.stdin)['channel'])" 2>/dev/null || true)
            _D_TO=$(echo "$_DT" | python3 -c "import json,sys; print(json.load(sys.stdin)['to'])" 2>/dev/null || true)
            if [ -n "$_D_CH" ] && [ -n "$_D_TO" ]; then
              _DELIVER_FLAGS="--channel $_D_CH --to $_D_TO --best-effort-deliver"
              echo "[HEARTBEAT] delivery=L1 (target: $_D_CH $_D_TO)" >&2
            fi
          else
            _GW=$(_probe_gateway_status "$OPENCLAW_BIN")
            if [ "$_GW" = "connected" ] || [ "$_GW" = "configured" ]; then
              _DELIVER_FLAGS="--best-effort-deliver"
              echo "[HEARTBEAT] delivery=L2 (best-effort, gateway=$_GW)" >&2
            else
              echo "[HEARTBEAT] delivery=L3 (no-deliver, gateway=$_GW)" >&2
            fi
          fi
        else
          echo "[HEARTBEAT] delivery=silent (no-deliver)" >&2
        fi

        _MODEL_FLAGS=""
        if [ -n "$_MODEL_HINT" ]; then
          _MODEL_FLAGS="--model $_MODEL_HINT"
          echo "[HEARTBEAT] model_hint=$_MODEL_HINT" >&2
        fi

        echo "[HEARTBEAT] dispatch: mode=$MODE timeout=${_TIMEOUT}s policy_claimed=${_POLICY_CLAIMED:+yes}" >&2

        # shellcheck disable=SC2086
        "$OPENCLAW_BIN" cron add \
          --name "clawgrid-wake-$(date +%s)" --at "5s" \
          --message "$MSG" \
          --session isolated $_DELIVER_FLAGS $_MODEL_FLAGS \
          --delete-after-run --timeout-seconds "$_TIMEOUT" 2>/dev/null && _WAKE_DISPATCHED=0 || \
        "$OPENCLAW_BIN" system event --text "$MSG" --mode now 2>/dev/null && _WAKE_DISPATCHED=0 || true
      fi

      # --- Selective ACK ---
      # ACK non-execution notifications immediately.  Execution-related
      # notifications (execute_task, handle_revision) are NOT ACK'd so the
      # next heartbeat can re-wake if the cron job timed out.  The server
      # auto-delivers stale ones once the task progresses past the relevant
      # state (see wake_evaluation_service.py stale pruning).
      if [ "$_WAKE_DISPATCHED" -eq 0 ]; then
        _PEND_RESP=$(curl -s "$API_BASE/api/lobster/notifications/pending?limit=20" \
          -H "Authorization: Bearer $API_KEY" \
          --max-time 10 2>/dev/null || echo "{}")
        _ACK_IDS=$(echo "$_PEND_RESP" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    notifs = d.get('notifications', d.get('items', []))
    no_ack = set(json.loads('$_NO_ACK_JSON'))
    ids = [n['id'] for n in notifs if 'id' in n and n['id'] not in no_ack]
    if ids:
        print(json.dumps(ids))
except Exception:
    pass
" 2>/dev/null || true)
        if [ -n "$_ACK_IDS" ] && [ "$_ACK_IDS" != "[]" ]; then
          curl -s -X POST "$API_BASE/api/lobster/notifications/ack" \
            -H "Authorization: Bearer $API_KEY" \
            -H "Content-Type: application/json" \
            -d "{\"ids\":$_ACK_IDS}" \
            --max-time 10 > /dev/null 2>&1 || true
          echo "[HEARTBEAT] ACK'd $(echo "$_ACK_IDS" | python3 -c "import json,sys; print(len(json.load(sys.stdin)))" 2>/dev/null || echo '?') notification(s)" >&2
        fi
        if [ "$_NO_ACK_JSON" != "[]" ]; then
          echo "[HEARTBEAT] deferred $(echo "$_NO_ACK_JSON" | python3 -c "import json,sys; print(len(json.load(sys.stdin)))" 2>/dev/null || echo '?') exec notification(s) for retry" >&2
        fi
      fi
    fi  # end active-session check
  fi
fi

# --- Persist onboarding directive to state (runs regardless of wake) ---
_OB_STATE_FILE="$CLAWGRID_HOME/state/onboarding_status.json"
echo "$BODY" | python3 -c "
import json, sys, os
from datetime import datetime, timezone
try:
    body = json.load(sys.stdin)
    for d in body.get('_directives', []):
        if d.get('type') == 'onboarding':
            cfg = d.get('config', {})
            out = {
                'current_step': cfg.get('current_step', ''),
                'step_title': cfg.get('step_title', ''),
                'progress': cfg.get('progress', ''),
                'journey': cfg.get('journey', ''),
                'is_optional': cfg.get('is_optional', False),
                'policy_task_hint': cfg.get('policy_task_hint', False),
                'policy_task_in_progress': cfg.get('policy_task_in_progress', False),
                'hint': cfg.get('hint', ''),
                'message': d.get('message', ''),
                'updated_at': datetime.now(timezone.utc).isoformat(),
            }
            path = sys.argv[1]
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w') as f:
                json.dump(out, f, ensure_ascii=False)
            break
    else:
        path = sys.argv[1]
        if os.path.exists(path):
            os.remove(path)
except Exception:
    pass
" "$_OB_STATE_FILE" 2>/dev/null || true

# --- Persist tag_proficiency_hint to state ---
echo "$BODY" | python3 -c "
import json, sys, os
try:
    d = json.load(sys.stdin)
    hint = d.get('summary', {}).get('tag_proficiency_hint')
    path = os.path.expanduser('~/.clawgrid/state/.tag_proficiency_hint.json')
    if hint and (hint.get('strong') or hint.get('weak')):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump(hint, f)
    elif os.path.exists(path):
        os.remove(path)
except Exception:
    pass
" 2>/dev/null || true

# --- Cleanup task logs by date (UTC) ---
# Keep logs from today and yesterday to avoid midnight boundary bugs.
if [ -d "$LOG_DIR" ]; then
  CUTOFF_DATE=$(date -u -d "1 day ago" +%F 2>/dev/null || true)
  if [ -n "$CUTOFF_DATE" ]; then
    find "$LOG_DIR" -maxdepth 1 -type f -name "*.log" | while read -r f; do
      FILE_DATE=$(date -u -r "$f" +%F 2>/dev/null || true)
      if [ -n "$FILE_DATE" ] && [ "$FILE_DATE" \< "$CUTOFF_DATE" ]; then
        rm -f "$f"
      fi
    done
  fi
fi

# --- One-time migrations (earner removal + notifier dedup) ---
# Each migration has a persistent marker in ~/.clawgrid/state/ so it runs
# exactly once per node.  openclaw cron remove requires a jobId; we read
# ~/.openclaw/cron/jobs.json to resolve name → jobId.

_cron_ids_for_name() {
  local jobs_file="$HOME/.openclaw/cron/jobs.json"
  [ ! -f "$jobs_file" ] && return 0
  python3 -c "
import json, sys
try:
    with open(sys.argv[1]) as f:
        data = json.load(f)
    jobs = data if isinstance(data, list) else []
    if isinstance(data, dict):
        jobs = data.get('jobs', [])
        if not jobs:
            jobs = [dict(jobId=k, **v) for k, v in data.items() if isinstance(v, dict)]
    for j in jobs:
        if j.get('name') == sys.argv[2]:
            jid = j.get('jobId', j.get('id', ''))
            if jid: print(jid)
except Exception:
    pass
" "$jobs_file" "$1" 2>/dev/null || true
}

_EARNER_DONE="$CLAWGRID_HOME/state/.earner_cleanup_done"
_KEEPALIVE_DONE="$CLAWGRID_HOME/state/.keepalive_rename_done"

if [ ! -f "$_EARNER_DONE" ] || [ ! -f "$_KEEPALIVE_DONE" ]; then
  _OC_BIN=$(command -v openclaw 2>/dev/null || echo "")
  if [ -z "$_OC_BIN" ]; then
    for _p in /opt/homebrew/bin/openclaw /usr/local/bin/openclaw "$HOME/.local/bin/openclaw"; do
      [ -x "$_p" ] && _OC_BIN="$_p" && break
    done
  fi
  if [ -n "$_OC_BIN" ]; then
    # Migration 1: remove legacy earner crons
    if [ ! -f "$_EARNER_DONE" ]; then
      _IDS=$(_cron_ids_for_name "clawgrid-earner")
      if [ -n "$_IDS" ]; then
        while IFS= read -r _jid; do
          [ -n "$_jid" ] && "$_OC_BIN" cron remove "$_jid" 2>/dev/null || true
        done <<< "$_IDS"
      fi
      touch "$_EARNER_DONE"
    fi

    # Migration 2: rename notifier → keepalive
    # Remove old name (clawgrid-notifier) + dedup new name, then re-add one
    if [ ! -f "$_KEEPALIVE_DONE" ]; then
      for _old_name in "clawgrid-notifier" "clawgrid-keepalive"; do
        _IDS=$(_cron_ids_for_name "$_old_name")
        if [ -n "$_IDS" ]; then
          while IFS= read -r _jid; do
            [ -n "$_jid" ] && "$_OC_BIN" cron remove "$_jid" 2>/dev/null || true
          done <<< "$_IDS"
        fi
      done
      _NCRON=$(python3 -c "import json; print(json.load(open('$CONFIG')).get('notifier_cron_expression', '0 9,21 * * *'))" 2>/dev/null || echo "0 9,21 * * *")
      _IS_DUR=$(echo "$_NCRON" | python3 -c "
import sys, re
v = sys.stdin.read().strip()
print('yes' if re.match(r'^\d+[mhd]$', v) else 'no')
" 2>/dev/null || echo "no")
      _NM="Run: bash $SKILL_DIR/scripts/notify.sh — relay output to owner with [ClawGrid.ai] prefix. If HEARTBEAT_OK, just say HEARTBEAT_OK."
      if [ "$_IS_DUR" = "yes" ]; then
        "$_OC_BIN" cron add \
          --name "clawgrid-keepalive" --every "$_NCRON" \
          --session isolated --announce --timeout-seconds 60 \
          --message "$_NM" 2>/dev/null || true
      else
        "$_OC_BIN" cron add \
          --name "clawgrid-keepalive" --cron "$_NCRON" \
          --session isolated --announce --timeout-seconds 60 \
          --message "$_NM" 2>/dev/null || true
      fi
      # Clear old migration marker so this migration runs fresh
      rm -f "$CLAWGRID_HOME/state/.notifier_dedup_done"
      touch "$_KEEPALIVE_DONE"
    fi
  fi
fi
