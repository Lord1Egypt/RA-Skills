# autothread-telegram.sh — Create a Telegram forum topic from a /topic
# command and post the original message as a quote inside it.
#
# DISCLOSURE: this script reads the local OpenClaw config (Telegram bot
# token only) and sends message content, sender attribution and the
# target chat to api.telegram.org. Nothing is sent anywhere else.
# See SKILL.md "Privacy & data handling".
#
# Usage:
#   ./autothread-telegram.sh <chat_id> <message_id> <sender> [title] [text]
#
# Args:
#   chat_id    (required) — target supergroup chat ID (negative number)
#   message_id (required) — original message to quote/forward
#   sender     (required) — display name of the original sender
#   title      (optional) — topic title. If empty, auto-generates from
#                           first ~50 chars of text at a word boundary.
#   text       (optional) — message body (everything after "/topic").
#                           If empty, the message is forwarded as media.
#
# Prerequisites:
#   - Forum/topics enabled on the group.
#   - Bot is an admin with the "Manage Topics" permission.
#   - Bot token in OpenClaw config (.channels.telegram.botToken).
#
# Output: JSON — {"topic_id": <id>, "title": "<title>", "link": "<url>"}
# Exit codes: 0 = success, 1 = error (details on stderr)

set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/common.sh
source "$SCRIPT_DIR/lib/common.sh"

autothread_require curl jq
autothread_config_path >/dev/null

# ── config ──────────────────────────────────────────────────────────
# AUTOTHREAD_OVERRIDE_TOKEN lets wrapper adapters (e.g. Nicegram) inject
# a platform-specific token instead of the default Telegram one.
BOT_TOKEN="${AUTOTHREAD_OVERRIDE_TOKEN:-}"
if [ -z "$BOT_TOKEN" ]; then
  BOT_TOKEN=$(autothread_config_get '.channels.telegram.botToken // empty')
fi
# AUTOTHREAD_API_BASE is overridable for offline testing with a mock API.
API="${AUTOTHREAD_API_BASE:-https://api.telegram.org}"

# ── arguments ───────────────────────────────────────────────────────
CHAT_ID="${1:-}"
MESSAGE_ID="${2:-}"
SENDER="${3:-}"
TITLE_ARG="${4:-}"
RAW_TEXT="${5:-}"

if [ -z "$CHAT_ID" ] || [ -z "$MESSAGE_ID" ] || [ -z "$SENDER" ]; then
  echo "Usage: $0 <chat_id> <message_id> <sender> [title] [text]" >&2
  exit 1
fi

# ── validate numeric arguments ──────────────────────────────────────
if ! printf '%s' "$CHAT_ID" | grep -qE '^-?[0-9]+$'; then
  echo "ERROR: chat_id must be an integer, got: '$CHAT_ID'" >&2
  exit 1
fi
if ! printf '%s' "$MESSAGE_ID" | grep -qE '^[0-9]+$'; then
  echo "ERROR: message_id must be a positive integer, got: '$MESSAGE_ID'" >&2
  exit 1
fi

MSG=$(autothread_trim "$RAW_TEXT")

# ── determine title (Telegram caps topic names at 128 chars) ────────
if [ -n "$TITLE_ARG" ]; then
  TITLE="$TITLE_ARG"
else
  TITLE=$(autothread_fallback_title "$MSG")
fi
TITLE=$(printf '%s' "$TITLE" | cut -c1-128)

# ── create forum topic ──────────────────────────────────────────────
CREATE_RESULT=$(curl -s "$API/bot${BOT_TOKEN}/createForumTopic" \
  -d "chat_id=${CHAT_ID}" \
  --data-urlencode "name=${TITLE}")

TOPIC_ID=$(echo "$CREATE_RESULT" | jq -r '.result.message_thread_id // empty')

if [ -z "$TOPIC_ID" ]; then
  ERR_DESC=$(echo "$CREATE_RESULT" | jq -r '.description // "unknown error"')
  echo "ERROR: Failed to create topic: $ERR_DESC" >&2
  exit 1
fi

# ── post quote into the new topic ───────────────────────────────────
if [ -n "$MSG" ]; then
  ESC_MSG=$(autothread_html_escape "$MSG")
  ESC_SENDER=$(autothread_html_escape "$SENDER")

  QUOTED="<blockquote>${ESC_MSG}</blockquote>
— <b>${ESC_SENDER}</b>"

  SEND_RESULT=$(curl -s "$API/bot${BOT_TOKEN}/sendMessage" \
    -d "chat_id=${CHAT_ID}" \
    -d "message_thread_id=${TOPIC_ID}" \
    --data-urlencode "text=${QUOTED}" \
    -d "parse_mode=HTML")

  SEND_OK=$(echo "$SEND_RESULT" | jq -r '.ok // "false"')
  if [ "$SEND_OK" != "true" ]; then
    echo "WARNING: sendMessage failed: $(echo "$SEND_RESULT" | jq -r '.description // "unknown"')" >&2
  fi
else
  # Media — forward to preserve attachments
  FWD_RESULT=$(curl -s "$API/bot${BOT_TOKEN}/forwardMessage" \
    -d "chat_id=${CHAT_ID}" \
    -d "from_chat_id=${CHAT_ID}" \
    -d "message_id=${MESSAGE_ID}" \
    -d "message_thread_id=${TOPIC_ID}")

  FWD_OK=$(echo "$FWD_RESULT" | jq -r '.ok // "false"')
  if [ "$FWD_OK" != "true" ]; then
    echo "WARNING: forwardMessage failed: $(echo "$FWD_RESULT" | jq -r '.description // "unknown"')" >&2
  fi
fi

# ── build topic link ────────────────────────────────────────────────
# Strip the -100 prefix from chat_id for the t.me/c/ link format
STRIPPED_ID=$(printf '%s' "$CHAT_ID" | sed 's/^-100//')
LINK="https://t.me/c/${STRIPPED_ID}/${TOPIC_ID}"

autothread_emit_result "$TOPIC_ID" "$TITLE" "$LINK"
