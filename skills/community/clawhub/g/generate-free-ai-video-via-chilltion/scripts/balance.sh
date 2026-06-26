#!/usr/bin/env bash
# 账户余额。
# 用法：balance.sh
set -euo pipefail
source "$(dirname "$0")/_common.sh"

curl -s "${CHILLTION_BASE_URL}/api/credits/balance" \
  -H "${CHILLTION_AUTH}"
echo
