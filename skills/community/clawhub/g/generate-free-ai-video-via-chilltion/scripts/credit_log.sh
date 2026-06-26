#!/usr/bin/env bash
# 积分变动日志（分页 + 日期过滤）。
# 用法：credit_log.sh [offset] [limit] [start_date YYYY-MM-DD] [end_date YYYY-MM-DD]
set -euo pipefail
source "$(dirname "$0")/_common.sh"

OFFSET="${1:-0}"
LIMIT="${2:-20}"
START="${3:-}"
END="${4:-}"

QS="offset=${OFFSET}&limit=${LIMIT}"
[ -n "$START" ] && QS="${QS}&start_date=${START}"
[ -n "$END" ]   && QS="${QS}&end_date=${END}"

curl -s "${CHILLTION_BASE_URL}/api/credits/log?${QS}" \
  -H "${CHILLTION_AUTH}"
echo
