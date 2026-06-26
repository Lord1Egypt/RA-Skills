#!/bin/bash
# feishu-meeting/scripts/create.sh (v4.1 - publishable)
# Creates a Feishu meeting via Calendar API with VC integration.
#
# Usage:
#   ./create.sh "Topic"                                    # Instant meeting
#   ./create.sh "Topic" --invitee "138..." --invitee "a@b" # With invitees
#   ./create.sh "Topic" --rrule "FREQ=WEEKLY;BYDAY=WE"    # Recurring
#   ./create.sh "Topic" --start "2026-03-05 14:00" --duration 60

set -euo pipefail

# ============================================================
# CONFIGURATION — Edit these before first use
# ============================================================
# Default meeting owner's Open ID (required)
DEFAULT_OWNER_OPEN_ID="${FEISHU_MEETING_OWNER_ID:-}"
# Bot's primary calendar ID (required — see SKILL.md for discovery)
CALENDAR_ID="${FEISHU_MEETING_CALENDAR_ID:-}"
# OpenClaw config file path
CONFIG_FILE="${OPENCLAW_CONFIG:-/root/.openclaw/openclaw.json}"
# ============================================================

# --- Parse Arguments ---
MEETING_TOPIC="${1:-Quick Meeting}"
shift 2>/dev/null || true

INVITEES=()
RRULE=""
START_TIME=""
DURATION=60

while [[ $# -gt 0 ]]; do
  case "$1" in
    --invitee)  INVITEES+=("$2"); shift 2 ;;
    --rrule)    RRULE="$2"; shift 2 ;;
    --start)    START_TIME="$2"; shift 2 ;;
    --duration) DURATION="$2"; shift 2 ;;
    *)          INVITEES+=("$1"); shift ;;
  esac
done

# --- Validate Config ---
if [ -z "$DEFAULT_OWNER_OPEN_ID" ] || [ -z "$CALENDAR_ID" ]; then
  echo "Error: Set FEISHU_MEETING_OWNER_ID and FEISHU_MEETING_CALENDAR_ID" >&2
  echo "  export FEISHU_MEETING_OWNER_ID='ou_xxx'" >&2
  echo "  export FEISHU_MEETING_CALENDAR_ID='feishu.cn_xxx@group.calendar.feishu.cn'" >&2
  echo "Or edit the CONFIGURATION section in this script." >&2
  exit 1
fi

# --- Read Feishu Credentials ---
APP_ID=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['channels']['feishu']['appId'])")
APP_SECRET=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['channels']['feishu']['appSecret'])")

# --- Get Tenant Access Token ---
ACCESS_TOKEN=$(curl -s -X POST \
  "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}" \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['tenant_access_token'])")

# --- Calculate Timestamps ---
if [ -n "$START_TIME" ]; then
  START_TS=$(date -d "$START_TIME" +%s 2>/dev/null || python3 -c "
from datetime import datetime
print(int(datetime.strptime('$START_TIME', '%Y-%m-%d %H:%M').timestamp()))
")
else
  START_TS=$(($(date +%s) + 300))
fi
END_TS=$((START_TS + DURATION * 60))

# --- Build Event Payload ---
EVENT_JSON=$(python3 -c "
import json
event = {
    'summary': '''$MEETING_TOPIC''',
    'start_time': {'timestamp': '$START_TS', 'timezone': 'Asia/Shanghai'},
    'end_time':   {'timestamp': '$END_TS',   'timezone': 'Asia/Shanghai'},
    'vchat': {'vc_type': 'vc'},
    'attendee_ability': 'can_see_others'
}
rrule = '''$RRULE'''
if rrule:
    r = rrule.replace('RRULE:', '')
    if 'COUNT' not in r and 'UNTIL' not in r:
        r += ';COUNT=52'
    event['recurrence'] = r
print(json.dumps(event, ensure_ascii=False))
")

# --- Step 1: Create Calendar Event ---
CREATE_RESP=$(curl -s -X POST \
  "https://open.feishu.cn/open-apis/calendar/v4/calendars/${CALENDAR_ID}/events?user_id_type=open_id" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d "$EVENT_JSON")

EVENT_ID=$(echo "$CREATE_RESP" | python3 -c "
import json,sys; d=json.load(sys.stdin)
if d.get('code')!=0: print('ERROR:'+d.get('msg','')); exit()
print(d['data']['event']['event_id'])
")

if [[ "$EVENT_ID" == ERROR* ]]; then
  echo "Error: Failed to create event. ${EVENT_ID#ERROR:}" >&2
  exit 1
fi

MEETING_URL=$(echo "$CREATE_RESP" | python3 -c "
import json,sys; print(json.load(sys.stdin)['data']['event'].get('vchat',{}).get('meeting_url',''))
")

# --- Step 2: Resolve Invitees ---
EXTRA_OPEN_IDS=""
NOT_FOUND=""
if [ ${#INVITEES[@]} -gt 0 ]; then
  RESOLVE=$(python3 -c "
import json,sys,urllib.request
contacts = sys.argv[1:]
mobiles = [c for c in contacts if '@' not in c]
emails  = [c for c in contacts if '@' in c]
body = {}
if mobiles: body['mobiles'] = mobiles
if emails:  body['emails'] = emails
req = urllib.request.Request(
    'https://open.feishu.cn/open-apis/contact/v3/users/batch_get_id?user_id_type=open_id',
    data=json.dumps(body).encode(),
    headers={'Authorization':'Bearer $ACCESS_TOKEN','Content-Type':'application/json; charset=utf-8'})
resp = json.loads(urllib.request.urlopen(req).read())
found, nf = [], []
for u in resp.get('data',{}).get('user_list',[]):
    oid = u.get('open_id')
    ident = u.get('mobile') or u.get('email') or '?'
    (found if oid else nf).append(oid or ident)
print(','.join(found))
print(','.join(nf))
" "${INVITEES[@]}")
  EXTRA_OPEN_IDS=$(echo "$RESOLVE" | head -1)
  NOT_FOUND=$(echo "$RESOLVE" | tail -1)
fi

# --- Step 3: Add Attendees ---
ATTENDEES_JSON=$(python3 -c "
import json
owner = '$DEFAULT_OWNER_OPEN_ID'
extras = [x for x in '$EXTRA_OPEN_IDS'.split(',') if x]
all_ids = list(dict.fromkeys([owner] + extras))
print(json.dumps({'attendees': [{'type':'user','user_id':uid} for uid in all_ids]}))
")

ATT_RESP=$(curl -s -X POST \
  "https://open.feishu.cn/open-apis/calendar/v4/calendars/${CALENDAR_ID}/events/${EVENT_ID}/attendees?user_id_type=open_id" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d "$ATTENDEES_JSON")

NAMES=$(echo "$ATT_RESP" | python3 -c "
import json,sys; d=json.load(sys.stdin)
print(', '.join(a.get('display_name','?') for a in d.get('data',{}).get('attendees',[])))
")

# --- Output ---
echo "✅ 会议创建成功！"
echo "主题: $MEETING_TOPIC"
echo "链接: $MEETING_URL"
echo "参与人: $NAMES"
[ -n "$RRULE" ] && echo "重复规则: $RRULE"
[ -n "$NOT_FOUND" ] && echo "⚠️ 未找到飞书账号: $NOT_FOUND"
echo ""
echo "📅 日程已添加到参与人的飞书日历中"
