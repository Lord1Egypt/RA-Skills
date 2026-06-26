#!/usr/bin/env bash
# 上传文件到 CareMax — 创建 session + 上传文件
# 用法: bash upload.sh <file1> [file2] [file3] ...
# 输出: JSON { "session_id": "...", "member_id": "...", "files": [...] }
#
# 示例:
#   bash upload.sh /path/to/report.jpg
#   bash upload.sh /path/to/img1.jpg /path/to/img2.png /path/to/report.pdf

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if [ $# -eq 0 ]; then
  echo '{"error":"usage","message":"Usage: upload.sh <file1> [file2] ..."}'
  exit 1
fi

# 检查 token
TOKEN_STATUS=$("$SCRIPT_DIR/check-token.sh")
STATUS=$(echo "$TOKEN_STATUS" | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])")

if [ "$STATUS" = "missing" ]; then
  echo '{"error":"no_credentials","message":"Run auth-flow.sh first to authenticate"}'
  exit 1
fi

if [ "$STATUS" = "expired" ]; then
  REFRESH_RESULT=$("$SCRIPT_DIR/refresh-token.sh")
  REFRESH_STATUS=$(echo "$REFRESH_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])")
  if [ "$REFRESH_STATUS" != "refreshed" ]; then
    echo '{"error":"token_expired","message":"Refresh failed. Run auth-flow.sh to re-authenticate"}'
    exit 1
  fi
  TOKEN_STATUS=$("$SCRIPT_DIR/check-token.sh")
fi

ACCESS_TOKEN=$(echo "$TOKEN_STATUS" | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
BASE_URL=$(echo "$TOKEN_STATUS" | python3 -c "import sys,json; print(json.load(sys.stdin)['base_url'])")

# 构建 curl -F 参数
FILE_ARGS=()
for filepath in "$@"; do
  if [ ! -f "$filepath" ]; then
    echo "{\"error\":\"file_not_found\",\"message\":\"File not found: $filepath\"}"
    exit 1
  fi
  FILE_ARGS+=(-F "files=@$filepath")
done

curl -s -X POST "${BASE_URL}/api/sessions/upload" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  "${FILE_ARGS[@]}"
