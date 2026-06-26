#!/usr/bin/env bash
# 带自动认证的 API 调用包装器
# 用法: bash api-call.sh <method> <path> [json_body]
# 示例:
#   bash api-call.sh GET /api/skill/indicators
#   bash api-call.sh POST /api/skill/records/search '{"query":"血常规"}'
#   bash api-call.sh GET "/api/skill/indicators/trend?id=xxx"
#
# 自动处理: 检查 token → 过期则刷新 → 不存在则报错

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
METHOD="${1:?Usage: api-call.sh <METHOD> <PATH> [JSON_BODY]}"
API_PATH="${2:?Usage: api-call.sh <METHOD> <PATH> [JSON_BODY]}"
BODY="${3:-}"

# Step 1: 检查 token
TOKEN_STATUS=$("$SCRIPT_DIR/check-token.sh")
STATUS=$(echo "$TOKEN_STATUS" | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])")

if [ "$STATUS" = "missing" ]; then
  echo '{"error":"no_credentials","message":"Run device-flow.sh first to authenticate"}'
  exit 1
fi

if [ "$STATUS" = "expired" ]; then
  # 尝试刷新
  REFRESH_RESULT=$("$SCRIPT_DIR/refresh-token.sh")
  REFRESH_STATUS=$(echo "$REFRESH_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])")
  if [ "$REFRESH_STATUS" != "refreshed" ]; then
    echo '{"error":"token_expired","message":"Refresh failed. Run device-flow.sh to re-authenticate"}'
    exit 1
  fi
  TOKEN_STATUS=$("$SCRIPT_DIR/check-token.sh")
fi

ACCESS_TOKEN=$(echo "$TOKEN_STATUS" | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
BASE_URL=$(echo "$TOKEN_STATUS" | python3 -c "import sys,json; print(json.load(sys.stdin)['base_url'])")

# Step 2: 发起 API 调用
if [ -n "$BODY" ]; then
  curl -s -X "$METHOD" "${BASE_URL}${API_PATH}" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    -d "$BODY"
else
  curl -s -X "$METHOD" "${BASE_URL}${API_PATH}" \
    -H "Authorization: Bearer $ACCESS_TOKEN"
fi
