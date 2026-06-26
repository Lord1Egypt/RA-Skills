#!/usr/bin/env bash
# 上传本地文件到百音开放平台，返回公网 URL
# 用法: bash upload-file.sh <local_file_path>
# 环境变量: BAIYIN_API_KEY

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/common.sh"

check_env

if [[ -z "${1:-}" ]]; then
  echo "ERROR: 请提供文件路径" >&2
  exit 1
fi

FILE_PATH="$1"

if [[ ! -f "$FILE_PATH" ]]; then
  echo "ERROR: 文件不存在: $FILE_PATH" >&2
  exit 1
fi

response=$(curl -s --connect-timeout 10 --max-time 120 \
  -H "Authorization: Bearer ${BAIYIN_API_KEY}" \
  -F "file=@${FILE_PATH}" \
  -w "\n%{http_code}" \
  "${BASE_URL}/api/open/v1/file/upload")

http_code=$(echo "$response" | tail -1)
body=$(echo "$response" | sed '$d')

if [[ "$http_code" != "200" ]]; then
  echo "ERROR: 上传失败 HTTP $http_code" >&2
  echo "$body" >&2
  exit 1
fi

if ! echo "$body" | grep -q '"success"[[:space:]]*:[[:space:]]*true'; then
  echo "ERROR: 上传失败" >&2
  echo "$body" >&2
  exit 1
fi

echo "$body"
