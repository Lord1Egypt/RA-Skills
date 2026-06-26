#!/usr/bin/env bash
# 提交视频生成任务（失败最多重试 3 次，指数退避，4xx 不重试）
# 用法: bash submit-task.sh '<json_body>'
# 环境变量: BAIYIN_API_KEY

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/common.sh"

check_env

BODY="$1"
MAX_RETRIES=3
attempt=0

while (( attempt < MAX_RETRIES )); do
  attempt=$((attempt + 1))

  response=$(curl_auth -w "\n%{http_code}" \
    -X POST \
    -d "$BODY" \
    "${BASE_URL}/api/open/v1/video/generate")

  http_code=$(echo "$response" | tail -1)
  body=$(echo "$response" | sed '$d')

  # 成功：HTTP 200、success: true、且 data.taskId 存在
  if [[ "$http_code" == "200" ]] \
    && echo "$body" | grep -q '"success"[[:space:]]*:[[:space:]]*true' \
    && echo "$body" | grep -q '"taskId"'; then
    echo "$body"
    exit 0
  fi

  # 4xx 客户端错误不重试
  if [[ "$http_code" == 4* ]]; then
    echo "ERROR: 客户端错误 HTTP $http_code，不重试" >&2
    echo "$body" >&2
    exit 1
  fi

  # 最后一次仍失败
  if (( attempt >= MAX_RETRIES )); then
    echo "ERROR: $MAX_RETRIES 次尝试均失败，最后一次 HTTP $http_code" >&2
    echo "$body" >&2
    exit 1
  fi

  # 指数退避: 1s → 2s → 4s
  sleep $(( 2 ** (attempt - 1) ))
done
