#!/usr/bin/env bash
# 创建会话。可选附带首条消息，后端会立即开始处理。
# 用法：
#   create_session.sh [mode] [message]
#     mode    autonomous | interactive（默认 autonomous）
#     message 首条消息（可选）；省略则只创建会话
set -euo pipefail
source "$(dirname "$0")/_common.sh"

MODE="${1:-autonomous}"
MESSAGE="${2:-}"

if [ -n "$MESSAGE" ]; then
  BODY=$(printf '{"mode":"%s","message":%s}' "$MODE" "$(printf '%s' "$MESSAGE" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')")
else
  BODY=$(printf '{"mode":"%s"}' "$MODE")
fi

curl -s -X POST "${CHILLTION_BASE_URL}/api/sessions" \
  -H "${CHILLTION_AUTH}" -H "${CHILLTION_CT}" \
  -d "$BODY"
echo
