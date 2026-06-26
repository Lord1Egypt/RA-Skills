#!/usr/bin/env bash
# 共享：校验环境变量；source 到其他脚本里使用。
# 用法（在其他 .sh 头部）：source "$(dirname "$0")/_common.sh"
set -euo pipefail

: "${CHILLTION_BASE_URL:=https://chilltion.com}"

if [ -z "${CHILLTION_API_KEY:-}" ]; then
  echo "缺少 CHILLTION_API_KEY（ct_ 开头）" >&2
  exit 2
fi

CHILLTION_AUTH="Authorization: Bearer ${CHILLTION_API_KEY}"
CHILLTION_CT="Content-Type: application/json"
