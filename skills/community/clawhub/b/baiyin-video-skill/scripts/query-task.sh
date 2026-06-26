#!/usr/bin/env bash
# 查询视频任务状态
# 用法: bash query-task.sh <taskId>
# 环境变量: BAIYIN_API_KEY

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/common.sh"

check_env

if [[ -z "${1:-}" ]]; then
  echo "ERROR: 请提供 taskId 参数" >&2
  exit 1
fi

TASK_ID="$1"

response=$(curl_auth -w "\n%{http_code}" \
  "${BASE_URL}/api/open/v1/tasks/${TASK_ID}")

http_code=$(echo "$response" | tail -1)
body=$(echo "$response" | sed '$d')

if [[ "$http_code" != "200" ]]; then
  echo "ERROR: 查询任务返回 HTTP $http_code" >&2
  echo "$body" >&2
  exit 1
fi

echo "$body"
