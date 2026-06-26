#!/usr/bin/env bash
# 向已有会话发送消息（后续轮次）。
# 用法：send_message.sh <session_id> <content>
set -euo pipefail
source "$(dirname "$0")/_common.sh"

SESSION_ID="${1:?需要 session_id}"
CONTENT="${2:?需要 content}"

BODY=$(printf '{"content":%s}' "$(printf '%s' "$CONTENT" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')")

curl -s -X POST "${CHILLTION_BASE_URL}/api/chat/${SESSION_ID}/message" \
  -H "${CHILLTION_AUTH}" -H "${CHILLTION_CT}" \
  -d "$BODY"
echo
