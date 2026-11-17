# autothread-discord.sh — Create a Discord thread from a /topic command
# and post the original message as a quote inside it.
#
# DISCLOSURE: this script reads the local OpenClaw config (Discord bot
# token only) and sends the thread title, message content and sender
# attribution to discord.com. Nothing is sent anywhere else.
# See SKILL.md "Privacy & data handling".
#
# Usage:
#   ./autothread-discord.sh <channel_id> <message_id> <sender> [title] [text]
#
# Args:
#   channel_id (required) — ID of the text channel containing the message
#   message_id (required) — ID of the original message to thread from
#   sender     (required) — display name of the original sender
#   title      (optional) — thread title. If empty, auto-generates from
#                           first ~50 chars of text at a word boundary.
#   text       (optional) — message body (everything after "/topic").
#
# Prerequisites:
#   - Bot token in OpenClaw config (.channels.discord.token).
#   - Bot has "Create Public Threads" + "Send Messages in Threads".
#   - The channel is a guild text channel (thread-from-message).
#
# Output: JSON — {"topic_id": "<thread_id>", "title": "<title>", "link": "<url>"}
# Exit codes: 0 = success, 1 = error (details on stderr)

set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/common.sh
source "$SCRIPT_DIR/lib/common.sh"

autothread_require curl jq
autothread_config_path >/dev/null

API_BASE="${AUTOTHREAD_API_BASE:-https://discord.com/api/v10}"

# ── config ──────────────────────────────────────────────────────────
BOT_TOKEN=$(autothread_config_get '.channels.discord.token // empty')

# ── arguments ───────────────────────────────────────────────────────
CHANNEL_ID="${1:-}"
MESSAGE_ID="${2:-}"
SENDER="${3:-}"
TITLE_ARG="${4:-}"
RAW_TEXT="${5:-}"

if [ -z "$CHANNEL_ID" ] || [ -z "$MESSAGE_ID" ] || [ -z "$SENDER" ]; then
  echo "Usage: $0 <channel_id> <message_id> <sender> [title] [text]" >&2
  exit 1
fi

# ── validate numeric arguments ──────────────────────────────────────
if ! printf '%s' "$CHANNEL_ID" | grep -qE '^[0-9]+$'; then
  echo "ERROR: channel_id must be a snowflake ID (digits), got: '$CHANNEL_ID'" >&2
  exit 1
fi
if ! printf '%s' "$MESSAGE_ID" | grep -qE '^[0-9]+$'; then
  echo "ERROR: message_id must be a snowflake ID (digits), got: '$MESSAGE_ID'" >&2
  exit 1
fi

MSG=$(autothread_trim "$RAW_TEXT")

# ── determine title (Discord caps thread names at 100 chars) ────────
if [ -n "$TITLE_ARG" ]; then
  TITLE="$TITLE_ARG"
else
  TITLE=$(autothread_fallback_title "$MSG")
fi
TITLE=$(printf '%s' "$TITLE" | cut -c1-100)

# ── resolve guild_id for the shareable link ─────────────────────────
CHANNEL_INFO=$(curl -s -H "Authorization: Bot ${BOT_TOKEN}" "$API_BASE/channels/${CHANNEL_ID}")
GUILD_ID=$(echo "$CHANNEL_INFO" | jq -r '.guild_id // empty')
if [ -z "$GUILD_ID" ]; then
  ERR_MSG=$(echo "$CHANNEL_INFO" | jq -r '.message // "unknown error"')
  echo "ERROR: Cannot resolve channel ${CHANNEL_ID}: $ERR_MSG" >&2
  exit 1
fi

# ── create the thread from the original message ─────────────────────
PAYLOAD=$(jq -n --arg name "$TITLE" '{"name": $name}')
CREATE_RESULT=$(curl -s -X POST \
  -H "Authorization: Bot ${BOT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" \
  "$API_BASE/channels/${CHANNEL_ID}/messages/${MESSAGE_ID}/threads")

THREAD_ID=$(echo "$CREATE_RESULT" | jq -r '.id // empty')

if [ -z "$THREAD_ID" ]; then
  ERR_MSG=$(echo "$CREATE_RESULT" | jq -r '.message // "unknown error"')
  echo "ERROR: Failed to create thread: $ERR_MSG" >&2
  exit 1
fi

# ── post quote into the new thread ──────────────────────────────────
if [ -n "$MSG" ]; then
  PAYLOAD=$(jq -n --arg msg "$MSG" --arg sender "$SENDER" \
    '{content: ("> " + $msg + "\n— **" + $sender + "**")}')

  SEND_RESULT=$(curl -s -X POST \
    -H "Authorization: Bot ${BOT_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD" \
    "$API_BASE/channels/${THREAD_ID}/messages")

  SEND_ID=$(echo "$SEND_RESULT" | jq -r '.id // empty')
  if [ -z "$SEND_ID" ]; then
    echo "WARNING: Failed to post quote: $(echo "$SEND_RESULT" | jq -r '.message // "unknown"')" >&2
  fi
fi

LINK="https://discord.com/channels/${GUILD_ID}/${THREAD_ID}"

autothread_emit_result "$THREAD_ID" "$TITLE" "$LINK"
