#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$HOME/.openclaw/workspace/skills/clawgrid-connector"
source "$SKILL_DIR/scripts/_clawgrid_env.sh"

if [ ! -f "$CONFIG" ]; then
  echo "HEARTBEAT_OK"
  exit 0
fi

if [ -f "$AUTH_INVALID_FLAG" ]; then
  echo "[ClawGrid.ai] Agent identity is invalid — automation stopped. Check config.json and re-register if needed."
  exit 0
fi

API_KEY=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_key'])")
API_BASE=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_base'])")

# ── Step 1: Pull pending server-side notifications ────────────────────
NOTIF_RESP=$(curl -s -w "\n%{http_code}" "$API_BASE/api/lobster/notifications/pending?limit=10" \
  -H "Authorization: Bearer $API_KEY" \
  --max-time 15 2>/dev/null || echo -e "{}\n000")

NOTIF_CODE=$(echo "$NOTIF_RESP" | tail -1)
NOTIF_BODY=$(echo "$NOTIF_RESP" | sed '$d')

NOTIF_OUTPUT=$(echo "$NOTIF_BODY" | python3 -c "
import json, sys

try:
    data = json.load(sys.stdin)
    items = data.get('notifications', [])
except Exception:
    items = []

if not items:
    print('')
    sys.exit(0)

ids = []
parts = []
for n in items:
    payload = n.get('payload', {})
    msg = payload.get('message', '')
    title = payload.get('title', '')
    if title and msg:
        parts.append(f'{title} {msg}')
    elif msg:
        parts.append(msg)
    elif title:
        parts.append(title)
    nid = n.get('id')
    if nid:
        ids.append(nid)

print(json.dumps({'output': ' | '.join(parts), 'ids': ids}))
" 2>/dev/null || echo "")

if [ -n "$NOTIF_OUTPUT" ] && [ "$NOTIF_OUTPUT" != "" ]; then
  # Parse output and ids
  OUTPUT=$(echo "$NOTIF_OUTPUT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('output',''))" 2>/dev/null || echo "")
  ACK_IDS=$(echo "$NOTIF_OUTPUT" | python3 -c "import json,sys; print(json.dumps(json.load(sys.stdin).get('ids',[])))" 2>/dev/null || echo "[]")

  if [ -n "$OUTPUT" ]; then
    # Ack the notifications we're about to deliver
    if [ "$ACK_IDS" != "[]" ]; then
      curl -s -X POST "$API_BASE/api/lobster/notifications/ack" \
        -H "Authorization: Bearer $API_KEY" \
        -H "Content-Type: application/json" \
        -d "{\"ids\":$ACK_IDS}" \
        --max-time 10 > /dev/null 2>&1 || true
    fi
    echo "$OUTPUT"
    exit 0
  fi
fi

# ── Step 2: Fallback — periodic summary via /me ──────────────────────
ME_RESP=$(curl -s -w "\n%{http_code}" "$API_BASE/api/lobster/me" \
  -H "Authorization: Bearer $API_KEY" \
  --max-time 15)

ME_CODE=$(echo "$ME_RESP" | tail -1)
ME_BODY=$(echo "$ME_RESP" | sed '$d')

if [ "$ME_CODE" -lt 200 ] || [ "$ME_CODE" -ge 300 ]; then
  echo "HEARTBEAT_OK"
  exit 0
fi

python3 -c "
import json, sys, os
from datetime import datetime, timezone

me = json.loads('''$ME_BODY''')
state_path = '$STATE_FILE'
state = {}
if os.path.exists(state_path):
    try:
        state = json.load(open(state_path))
    except Exception:
        state = {}

now = datetime.now(timezone.utc)
now_iso = now.isoformat()
last_notified = state.get('last_notified_at', '')

tasks_today = me.get('tasks_completed_today', state.get('tasks_completed_today', 0))
earned_today = me.get('earned_today_usd', state.get('earned_today_usd', '0'))
earned_total = me.get('total_earned_usd', '0')
status = me.get('status', 'unknown')
health = me.get('health_score', 0)
daily_used = me.get('daily_tasks', {}).get('used', tasks_today)
daily_limit = me.get('daily_tasks', {}).get('limit', state.get('daily_limit', 0))
slots_active = me.get('concurrent_tasks', {}).get('active', 0)
upgrade = state.get('upgrade_progress', '')

has_tasks = tasks_today > 0
has_earnings = float(earned_today) > 0
issues = me.get('issues', [])
has_issues = len(issues) > 0

# Check for pending platform directives
pending_dirs = state.get('pending_directives', [])
me_dirs = me.get('_directives', [])
existing_ids = {d.get('id') for d in pending_dirs}
for d in me_dirs:
    if d.get('notify_owner') and d.get('id') not in existing_ids:
        pending_dirs.append(d)

if not has_tasks and not has_earnings and not has_issues and not pending_dirs:
    if last_notified:
        print('HEARTBEAT_OK')
    else:
        print(f'Status: {status}, health: {health}/100. No tasks completed yet today. Polling continues.')
    state['last_notified_at'] = now_iso
    tmp = state_path + '.tmp'
    with open(tmp, 'w') as f:
        json.dump(state, f, indent=2)
    os.replace(tmp, state_path)
    sys.exit(0)

parts = []
if has_tasks:
    progress = f'{daily_used}/{daily_limit}' if daily_limit else str(daily_used)
    parts.append(f'Today: {progress} tasks, earned \${earned_today}.')

if earned_total and earned_total != '0':
    parts.append(f'Total: \${earned_total}.')

if upgrade:
    parts.append(upgrade)

if has_issues:
    for issue in issues[:2]:
        severity = issue.get('severity', 'info')
        msg = issue.get('message', '')
        if severity in ('warning', 'error'):
            parts.append(f'Issue: {msg}')

if slots_active > 0:
    parts.append(f'{slots_active} task(s) in progress.')

for d in pending_dirs:
    msg = d.get('message', '')
    priority = d.get('priority', 'normal')
    prefix = '[DIRECTIVE]' if priority in ('critical', 'high') else '[Platform]'
    if msg:
        parts.append(f'{prefix} {msg}')

state['pending_directives'] = []

if not parts:
    print('HEARTBEAT_OK')
else:
    print(' '.join(parts))

state['last_notified_at'] = now_iso
tmp = state_path + '.tmp'
with open(tmp, 'w') as f:
    json.dump(state, f, indent=2)
os.replace(tmp, state_path)
"
