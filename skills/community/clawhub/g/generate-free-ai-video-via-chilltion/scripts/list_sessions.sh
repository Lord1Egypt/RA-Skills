#!/usr/bin/env bash
# 会话列表（分页）。
# 用法：list_sessions.sh [offset] [limit]   默认 0 / 20
set -euo pipefail
source "$(dirname "$0")/_common.sh"

OFFSET="${1:-0}"
LIMIT="${2:-20}"

curl -s "${CHILLTION_BASE_URL}/api/sessions?offset=${OFFSET}&limit=${LIMIT}" \
  -H "${CHILLTION_AUTH}"
echo
