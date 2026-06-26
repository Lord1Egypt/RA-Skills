#!/usr/bin/env bash
# 会话详情。
# 用法：session_detail.sh <session_id>
set -euo pipefail
source "$(dirname "$0")/_common.sh"

SESSION_ID="${1:?需要 session_id}"

curl -s "${CHILLTION_BASE_URL}/api/sessions/${SESSION_ID}" \
  -H "${CHILLTION_AUTH}"
echo
