#!/bin/bash
# 查询设备心跳状态
# 用法: check.sh <API_KEY> [CHECK_UUID]
# 需要 healthchecks.io 的 API key（只读即可）

API_KEY="${1:?Usage: check.sh <API_KEY> [CHECK_UUID]}"
CHECK_UUID="$2"

if [ -n "$CHECK_UUID" ]; then
  # 查询单个 check
  curl -fsS --max-time 10 \
    -H "X-Api-Key: $API_KEY" \
    "https://healthchecks.io/api/v3/checks/${CHECK_UUID}" 2>/dev/null
else
  # 列出所有 checks
  curl -fsS --max-time 10 \
    -H "X-Api-Key: $API_KEY" \
    "https://healthchecks.io/api/v3/checks/" 2>/dev/null
fi
