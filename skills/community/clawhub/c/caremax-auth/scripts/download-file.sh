#!/usr/bin/env bash
# 下载 session 文件到本地
# 用法: bash download-file.sh <file_id> [output_path]
# 示例:
#   bash download-file.sh abc-123                      → 保存为 abc-123 (自动检测扩展名)
#   bash download-file.sh abc-123 ~/Downloads/report.jpg → 保存到指定路径

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
FILE_ID="${1:?Usage: download-file.sh <file_id> [output_path]}"
OUTPUT="${2:-}"

# 检查 token
TOKEN_STATUS=$("$SCRIPT_DIR/check-token.sh")
STATUS=$(echo "$TOKEN_STATUS" | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])")

if [ "$STATUS" = "missing" ]; then
  echo '{"error":"no_credentials","message":"Run auth-flow.sh first"}'
  exit 1
fi

if [ "$STATUS" = "expired" ]; then
  REFRESH_RESULT=$("$SCRIPT_DIR/refresh-token.sh")
  REFRESH_STATUS=$(echo "$REFRESH_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])")
  if [ "$REFRESH_STATUS" != "refreshed" ]; then
    echo '{"error":"token_expired","message":"Refresh failed"}'
    exit 1
  fi
  TOKEN_STATUS=$("$SCRIPT_DIR/check-token.sh")
fi

ACCESS_TOKEN=$(echo "$TOKEN_STATUS" | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
BASE_URL=$(echo "$TOKEN_STATUS" | python3 -c "import sys,json; print(json.load(sys.stdin)['base_url'])")

# 如果没指定输出路径，用 file_id 作为文件名
if [ -z "$OUTPUT" ]; then
  OUTPUT="$FILE_ID"
fi

# 下载
HTTP_CODE=$(curl -s -o "$OUTPUT" -w "%{http_code}" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  "${BASE_URL}/api/sessions/file-content/${FILE_ID}")

if [ "$HTTP_CODE" = "200" ]; then
  SIZE=$(wc -c < "$OUTPUT" | tr -d ' ')
  echo "{\"status\":\"ok\",\"path\":\"$OUTPUT\",\"size\":$SIZE}"
else
  rm -f "$OUTPUT" 2>/dev/null
  echo "{\"error\":\"download_failed\",\"http_code\":$HTTP_CODE}"
  exit 1
fi
