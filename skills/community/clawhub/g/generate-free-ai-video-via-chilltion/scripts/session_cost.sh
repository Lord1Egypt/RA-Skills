#!/usr/bin/env bash
# 会话积分消耗（拆分到 prompt / managed_base / duration / refund）。
# 用法：session_cost.sh <session_id>
set -euo pipefail
source "$(dirname "$0")/_common.sh"

SESSION_ID="${1:?需要 session_id}"

curl -s "${CHILLTION_BASE_URL}/api/credits/session-cost/${SESSION_ID}" \
  -H "${CHILLTION_AUTH}"
echo
