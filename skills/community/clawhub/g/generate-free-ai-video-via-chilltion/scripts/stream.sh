#!/usr/bin/env bash
# 监听会话 SSE 流。
# 用法：stream.sh <session_id> [from_seq]
# 关键事件：phase_change / progress / preview_ready / video_ready / done / error
set -euo pipefail
source "$(dirname "$0")/_common.sh"

SESSION_ID="${1:?需要 session_id}"
FROM_SEQ="${2:-0}"

curl -sN "${CHILLTION_BASE_URL}/api/chat/${SESSION_ID}/stream?seq=${FROM_SEQ}" \
  -H "${CHILLTION_AUTH}"
