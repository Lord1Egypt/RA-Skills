#!/usr/bin/env bash
set -euo pipefail

API_BASE="https://discord.com/api/v10"
BOT_TOKEN="${DISCORD_BOT_TOKEN:-}"

usage() {
  cat <<'EOF'
Discord server admin helper

Usage:
  discord-server-admin.sh [--token TOKEN] <command> [args]

Read commands:
  channel-list <guild_id>
  role-list <guild_id>

Channel commands:
  channel-create <guild_id> <name> [--type text|voice|category] [--parent-id ID] [--topic TEXT]
  channel-edit <channel_id> [--name NAME] [--parent-id ID] [--topic TEXT]
  channel-delete <channel_id>

Role commands:
  role-create <guild_id> <name> [--color HEX] [--permissions INT] [--mentionable true|false] [--hoist true|false]
  role-edit <guild_id> <role_id> [--name NAME] [--color HEX] [--permissions INT] [--mentionable true|false] [--hoist true|false]
  role-delete <guild_id> <role_id>
  role-position <guild_id> <role_id> <position>

Member role commands:
  member-role-add <guild_id> <role_id> <user_id>
  member-role-remove <guild_id> <role_id> <user_id>

Notes:
  - Requires DISCORD_BOT_TOKEN or --token.
  - Scope is intentionally limited to channels, roles, and member role assignment.
  - Permissions must be supplied as a Discord integer bitfield string/int.
  - This tool does not do bans, kicks, bulk actions, or guild-wide settings writes.
EOF
}

err() {
  echo "error: $*" >&2
  exit 1
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || err "$1 is required"
}

require_token() {
  [[ -n "$BOT_TOKEN" ]] || err "DISCORD_BOT_TOKEN not set; pass --token or export it"
}

json_bool() {
  case "$1" in
    true|false) printf '%s' "$1" ;;
    *) err "expected true|false, got: $1" ;;
  esac
}

normalize_color() {
  local raw="$1"
  raw="${raw#\#}"
  raw="${raw#0x}"
  [[ "$raw" =~ ^[0-9A-Fa-f]{6}$ ]] || err "color must be 6-digit hex, e.g. 111111 or #111111"
  printf '%d' "$((16#$raw))"
}

channel_type_id() {
  case "$1" in
    text) printf '0' ;;
    voice) printf '2' ;;
    category) printf '4' ;;
    *) err "unsupported channel type: $1 (use text|voice|category)" ;;
  esac
}

json_retry_after() {
  local body="$1"
  python3 - "$body" <<'PY'
import json, sys
body = sys.argv[1]
try:
    data = json.loads(body)
    val = data.get("retry_after", 1)
except Exception:
    val = 1
print(val)
PY
}

api() {
  local method="$1"
  local endpoint="$2"
  local data="${3:-}"
  local tmp body code
  tmp=$(mktemp)
  trap 'rm -f "$tmp"' RETURN

  if [[ -n "$data" ]]; then
    code=$(curl -sS -o "$tmp" -w '%{http_code}' -X "$method" \
      "$API_BASE$endpoint" \
      -H "Authorization: Bot $BOT_TOKEN" \
      -H 'Content-Type: application/json' \
      --data "$data")
  else
    code=$(curl -sS -o "$tmp" -w '%{http_code}' -X "$method" \
      "$API_BASE$endpoint" \
      -H "Authorization: Bot $BOT_TOKEN" \
      -H 'Content-Type: application/json')
  fi

  body=$(cat "$tmp")
  case "$code" in
    200|201) printf '%s\n' "$body" ;;
    204) ;;
    401) err "Discord API 401 Unauthorized (bad token?)" ;;
    403) err "Discord API 403 Forbidden (missing permissions or blocked by role hierarchy?)" ;;
    404) err "Discord API 404 Not Found (bad guild/channel/role/user id?)" ;;
    429)
      local retry
      retry=$(json_retry_after "$body")
      sleep "$retry"
      api "$method" "$endpoint" "$data"
      ;;
    *)
      if [[ -n "$body" ]]; then
        err "Discord API $code: $body"
      else
        err "Discord API $code"
      fi
      ;;
  esac
}

build_role_json() {
  local name="" color="" permissions="" mentionable="" hoist=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --name)
        name="$2"; shift 2 ;;
      --color)
        color=$(normalize_color "$2"); shift 2 ;;
      --permissions)
        permissions="$2"; shift 2 ;;
      --mentionable)
        mentionable=$(json_bool "$2"); shift 2 ;;
      --hoist)
        hoist=$(json_bool "$2"); shift 2 ;;
      *) err "unknown role option: $1" ;;
    esac
  done

  ROLE_NAME="$name" ROLE_COLOR="$color" ROLE_PERMISSIONS="$permissions" ROLE_MENTIONABLE="$mentionable" ROLE_HOIST="$hoist" \
  python3 <<'PY'
import json, os
payload = {}
if os.environ.get('ROLE_NAME'):
    payload['name'] = os.environ['ROLE_NAME']
if os.environ.get('ROLE_COLOR'):
    payload['color'] = int(os.environ['ROLE_COLOR'])
if os.environ.get('ROLE_PERMISSIONS'):
    payload['permissions'] = os.environ['ROLE_PERMISSIONS']
if os.environ.get('ROLE_MENTIONABLE'):
    payload['mentionable'] = os.environ['ROLE_MENTIONABLE'] == 'true'
if os.environ.get('ROLE_HOIST'):
    payload['hoist'] = os.environ['ROLE_HOIST'] == 'true'
print(json.dumps(payload, separators=(',', ':')))
PY
}

build_channel_json() {
  local name="" type="" parent_id="" topic=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --name)
        name="$2"; shift 2 ;;
      --type)
        type=$(channel_type_id "$2"); shift 2 ;;
      --parent-id)
        parent_id="$2"; shift 2 ;;
      --topic)
        topic="$2"; shift 2 ;;
      *) err "unknown channel option: $1" ;;
    esac
  done

  CHANNEL_NAME="$name" CHANNEL_TYPE="$type" CHANNEL_PARENT_ID="$parent_id" CHANNEL_TOPIC="$topic" \
  python3 <<'PY'
import json, os
payload = {}
if os.environ.get('CHANNEL_NAME'):
    payload['name'] = os.environ['CHANNEL_NAME']
if os.environ.get('CHANNEL_TYPE'):
    payload['type'] = int(os.environ['CHANNEL_TYPE'])
if os.environ.get('CHANNEL_PARENT_ID'):
    payload['parent_id'] = os.environ['CHANNEL_PARENT_ID']
if os.environ.get('CHANNEL_TOPIC'):
    payload['topic'] = os.environ['CHANNEL_TOPIC']
print(json.dumps(payload, separators=(',', ':')))
PY
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --token)
      BOT_TOKEN="$2"
      shift 2
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      break
      ;;
  esac
done

require_cmd curl
require_cmd python3

cmd="${1:-}"
[[ -n "$cmd" ]] || { usage; exit 1; }
shift || true
require_token

case "$cmd" in
  channel-list)
    [[ $# -eq 1 ]] || err "usage: channel-list <guild_id>"
    api GET "/guilds/$1/channels"
    ;;
  role-list)
    [[ $# -eq 1 ]] || err "usage: role-list <guild_id>"
    api GET "/guilds/$1/roles"
    ;;
  channel-create)
    [[ $# -ge 2 ]] || err "usage: channel-create <guild_id> <name> [options]"
    guild_id="$1"; name="$2"; shift 2
    payload=$(build_channel_json --name "$name" "$@")
    api POST "/guilds/$guild_id/channels" "$payload"
    ;;
  channel-edit)
    [[ $# -ge 1 ]] || err "usage: channel-edit <channel_id> [options]"
    channel_id="$1"; shift
    payload=$(build_channel_json "$@")
    [[ "$payload" != '{}' ]] || err "channel-edit requires at least one field"
    api PATCH "/channels/$channel_id" "$payload"
    ;;
  channel-delete)
    [[ $# -eq 1 ]] || err "usage: channel-delete <channel_id>"
    api DELETE "/channels/$1"
    ;;
  role-create)
    [[ $# -ge 2 ]] || err "usage: role-create <guild_id> <name> [options]"
    guild_id="$1"; name="$2"; shift 2
    payload=$(build_role_json --name "$name" "$@")
    api POST "/guilds/$guild_id/roles" "$payload"
    ;;
  role-edit)
    [[ $# -ge 2 ]] || err "usage: role-edit <guild_id> <role_id> [options]"
    guild_id="$1"; role_id="$2"; shift 2
    payload=$(build_role_json "$@")
    [[ "$payload" != '{}' ]] || err "role-edit requires at least one field"
    api PATCH "/guilds/$guild_id/roles/$role_id" "$payload"
    ;;
  role-delete)
    [[ $# -eq 2 ]] || err "usage: role-delete <guild_id> <role_id>"
    api DELETE "/guilds/$1/roles/$2"
    ;;
  role-position)
    [[ $# -eq 3 ]] || err "usage: role-position <guild_id> <role_id> <position>"
    [[ "$3" =~ ^-?[0-9]+$ ]] || err "position must be an integer"
    payload=$(python3 - "$2" "$3" <<'PY'
import json, sys
print(json.dumps([{'id': sys.argv[1], 'position': int(sys.argv[2])}], separators=(',', ':')))
PY
)
    api PATCH "/guilds/$1/roles" "$payload"
    ;;
  member-role-add)
    [[ $# -eq 3 ]] || err "usage: member-role-add <guild_id> <role_id> <user_id>"
    api PUT "/guilds/$1/members/$3/roles/$2"
    ;;
  member-role-remove)
    [[ $# -eq 3 ]] || err "usage: member-role-remove <guild_id> <role_id> <user_id>"
    api DELETE "/guilds/$1/members/$3/roles/$2"
    ;;
  *)
    usage
    err "unknown command: $cmd"
    ;;
esac
