#!/usr/bin/env bash
# OCR V2 流式调用 — 读取 SSE 进度并输出最终结果
# 用法: bash ocr-stream.sh <session_id>
# 输出: 每行一个 SSE 事件 JSON，最后一行 step=done 包含完整 reports
#
# 错误处理:
# - 409: session 正在被处理，返回 {"step":"error","code":"processing_in_progress",...}
# - 403: OCR 配额用完，返回 {"step":"error","code":"ocr_limit_exceeded",...}
# - 非 SSE 响应: 自动检测并转换为 error JSON

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SESSION_ID="${1:?Usage: ocr-stream.sh <session_id>}"

# 检查 token
TOKEN_STATUS=$("$SCRIPT_DIR/check-token.sh")
STATUS=$(echo "$TOKEN_STATUS" | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])")

if [ "$STATUS" = "missing" ]; then
  echo '{"step":"error","progress":-1,"message":"No credentials. Run auth-flow.sh first"}'
  exit 1
fi

if [ "$STATUS" = "expired" ]; then
  REFRESH_RESULT=$("$SCRIPT_DIR/refresh-token.sh")
  REFRESH_STATUS=$(echo "$REFRESH_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])")
  if [ "$REFRESH_STATUS" != "refreshed" ]; then
    echo '{"step":"error","progress":-1,"message":"Token expired and refresh failed"}'
    exit 1
  fi
  TOKEN_STATUS=$("$SCRIPT_DIR/check-token.sh")
fi

ACCESS_TOKEN=$(echo "$TOKEN_STATUS" | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
BASE_URL=$(echo "$TOKEN_STATUS" | python3 -c "import sys,json; print(json.load(sys.stdin)['base_url'])")

# 捕获 HTTP 响应头到临时文件，用于检测 content-type 和 status code
HEADER_FILE=$(mktemp)
trap 'rm -f "$HEADER_FILE"' EXIT

# SSE 流式请求 — 用 -D 写响应头, -N 禁止缓冲
# 注意: 如果后端返回非 SSE (409/403/500), curl 会输出 JSON 正文
curl -s -N -X POST "${BASE_URL}/api/sessions/${SESSION_ID}/ocr" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -D "$HEADER_FILE" \
  -d '{}' |
{
  GOT_SSE=false
  while IFS= read -r line; do
    if [[ "$line" == data:* ]]; then
      GOT_SSE=true
      echo "${line#data: }"
    elif [ "$GOT_SSE" = false ] && [[ "$line" == "{"* ]]; then
      # 非 SSE 响应: 直接输出为 JSON (可能是 409/403/500 错误)
      # 从响应头提取 HTTP 状态码
      HTTP_CODE=$(grep -oE 'HTTP/[0-9.]+ ([0-9]+)' "$HEADER_FILE" | tail -1 | grep -oE '[0-9]+$' || echo "0")
      ERROR_MSG=$(echo "$line" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('error','Unknown error'))" 2>/dev/null || echo "Unknown error")
      ERROR_CODE=$(echo "$line" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('code',''))" 2>/dev/null || echo "")
      if [ -n "$ERROR_CODE" ]; then
        echo "{\"step\":\"error\",\"progress\":-1,\"message\":\"$ERROR_MSG\",\"code\":\"$ERROR_CODE\",\"http_status\":$HTTP_CODE}"
      else
        echo "{\"step\":\"error\",\"progress\":-1,\"message\":\"$ERROR_MSG\",\"http_status\":$HTTP_CODE}"
      fi
      exit 1
    fi
  done
}
