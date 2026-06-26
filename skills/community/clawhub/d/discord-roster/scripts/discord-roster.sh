#!/usr/bin/env bash
set -euo pipefail

# Discord Roster — query guild members, channels, roles via REST API.
# Reads bot token + proxy from ~/.openclaw/openclaw.json automatically.

DISCORD_API="https://discord.com/api/v10"
CONFIG_FILE="${OPENCLAW_CONFIG:-$HOME/.openclaw/openclaw.json}"

die() { echo "ERROR: $*" >&2; exit 1; }

read_config() {
  [[ -f "$CONFIG_FILE" ]] || die "Config not found: $CONFIG_FILE"
  python3 -c "
import json, sys
with open('$CONFIG_FILE') as f:
    c = json.load(f)
token = c.get('channels',{}).get('discord',{}).get('token','')
proxy = c.get('channels',{}).get('discord',{}).get('proxy','')
print(token)
print(proxy)
"
}

setup() {
  local config
  config=$(read_config)
  BOT_TOKEN=$(echo "$config" | sed -n '1p')
  CONFIG_PROXY=$(echo "$config" | sed -n '2p')
  [[ -n "$BOT_TOKEN" ]] || die "No discord token in $CONFIG_FILE (channels.discord.token)"

  PROXY="${CONFIG_PROXY:-${HTTPS_PROXY:-${https_proxy:-}}}"
  CURL_PROXY=()
  [[ -n "$PROXY" ]] && CURL_PROXY=(--proxy "$PROXY")
}

api() {
  local endpoint="$1"
  shift
  curl -sf "${CURL_PROXY[@]+"${CURL_PROXY[@]}"}" \
    -H "Authorization: Bot $BOT_TOKEN" \
    "$@" \
    "${DISCORD_API}${endpoint}"
}

cmd_members() {
  local guild_id="${1:?Usage: members <guild_id> [--bots|--humans]}"
  local filter="${2:-all}"

  local raw
  raw=$(api "/guilds/${guild_id}/members?limit=1000")

  python3 -c "
import json, sys

data = json.loads('''$( echo "$raw" | python3 -c "import sys; print(sys.stdin.read().replace(\"'\",\"\\\\'\"))" )''')

if isinstance(data, dict) and 'message' in data:
    print(f\"API Error: {data['message']}\", file=sys.stderr)
    sys.exit(1)

filt = '$filter'
print('TYPE\tUSERNAME\tDISPLAY_NAME\tID\tJOINED_AT\tROLES')
for m in sorted(data, key=lambda x: (not x['user'].get('bot', False), x['user']['username'])):
    u = m['user']
    is_bot = u.get('bot', False)
    if filt == '--bots' and not is_bot: continue
    if filt == '--humans' and is_bot: continue
    typ = 'BOT' if is_bot else 'HUMAN'
    uname = u.get('username', '?')
    display = u.get('global_name') or m.get('nick') or '—'
    uid = u['id']
    joined = m.get('joined_at', '?')[:16]
    roles = ','.join(m.get('roles', [])) or '—'
    print(f'{typ}\t{uname}\t{display}\t{uid}\t{joined}\t{roles}')
"
}

cmd_channel() {
  local channel_id="${1:?Usage: channel <channel_id>}"
  local raw
  raw=$(api "/channels/${channel_id}")

  python3 -c "
import json
data = json.loads('''$(echo "$raw" | python3 -c "import sys; print(sys.stdin.read().replace(\"'\",\"\\\\'\"))")''')
if 'message' in data:
    print(f\"API Error: {data['message']}\")
    exit(1)
ch_type = {0:'text',2:'voice',4:'category',5:'announcement',10:'thread',11:'thread',12:'thread',13:'stage',15:'forum'}.get(data.get('type',0),'unknown')
print(f\"Channel: #{data.get('name','?')} ({ch_type})\")
print(f\"ID: {data['id']}\")
print(f\"Guild: {data.get('guild_id','DM')}\")
print(f\"Topic: {data.get('topic') or '—'}\")
print(f\"Position: {data.get('position','?')}\")
overwrites = data.get('permission_overwrites', [])
if overwrites:
    print(f'Permission overwrites: {len(overwrites)}')
    for o in overwrites:
        otype = 'role' if o['type'] == 0 else 'member'
        print(f'  {otype} {o[\"id\"]}: allow={o.get(\"allow\",\"0\")} deny={o.get(\"deny\",\"0\")}')
else:
    print('Permission overwrites: none (inherits guild defaults)')
"
}

cmd_channels() {
  local guild_id="${1:?Usage: channels <guild_id>}"
  local raw
  raw=$(api "/guilds/${guild_id}/channels")

  python3 -c "
import json
data = json.loads('''$(echo "$raw" | python3 -c "import sys; print(sys.stdin.read().replace(\"'\",\"\\\\'\"))")''')
if isinstance(data, dict) and 'message' in data:
    print(f\"API Error: {data['message']}\")
    exit(1)
type_map = {0:'text',2:'voice',4:'category',5:'announce',10:'thread',11:'thread',12:'thread',13:'stage',15:'forum'}
print('TYPE\tNAME\tID\tPARENT_ID')
for ch in sorted(data, key=lambda x: (x.get('position',0))):
    t = type_map.get(ch.get('type',0), 'unknown')
    print(f\"{t}\t#{ch.get('name','?')}\t{ch['id']}\t{ch.get('parent_id') or '—'}\")
"
}

cmd_roles() {
  local guild_id="${1:?Usage: roles <guild_id>}"
  local raw
  raw=$(api "/guilds/${guild_id}/roles")

  python3 -c "
import json
data = json.loads('''$(echo "$raw" | python3 -c "import sys; print(sys.stdin.read().replace(\"'\",\"\\\\'\"))")''')
if isinstance(data, dict) and 'message' in data:
    print(f\"API Error: {data['message']}\")
    exit(1)
print('NAME\tID\tCOLOR\tPOSITION\tMEMBER_COUNT')
for r in sorted(data, key=lambda x: -x.get('position',0)):
    name = r.get('name','?')
    if name == '@everyone': continue
    color = f\"#{r.get('color',0):06x}\" if r.get('color',0) else '—'
    print(f\"{name}\t{r['id']}\t{color}\t{r.get('position',0)}\t—\")
"
}

cmd_guild_of() {
  local channel_id="${1:?Usage: guild-of <channel_id>}"
  local raw
  raw=$(api "/channels/${channel_id}")

  python3 -c "
import json
data = json.loads('''$(echo "$raw" | python3 -c "import sys; print(sys.stdin.read().replace(\"'\",\"\\\\'\"))")''')
gid = data.get('guild_id','')
if gid:
    print(f\"{gid}\")
else:
    print('This is a DM channel (no guild)')
"
}

usage() {
  cat <<'EOF'
discord-roster — Query Discord guild members, channels, roles.

Usage: discord-roster.sh <command> [args...]

Commands:
  members <guild_id> [--bots|--humans]   List guild members
  channel <channel_id>                    Get channel details
  channels <guild_id>                     List guild channels
  roles <guild_id>                        List guild roles
  guild-of <channel_id>                   Find which guild a channel belongs to

Token and proxy are read from ~/.openclaw/openclaw.json automatically.
EOF
}

# --- main ---
setup
cmd="${1:-help}"
shift || true

case "$cmd" in
  members)  cmd_members "$@" ;;
  channel)  cmd_channel "$@" ;;
  channels) cmd_channels "$@" ;;
  roles)    cmd_roles "$@" ;;
  guild-of) cmd_guild_of "$@" ;;
  help|--help|-h) usage ;;
  *) die "Unknown command: $cmd. Run with 'help' for usage." ;;
esac
