#!/bin/bash
# 飞书 Token 管理脚本
# 自动获取和缓存 tenant_access_token

set -e

# 配置
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/../config/feishu.env"
CACHE_FILE="/tmp/feishu_token_cache.json"

# 加载配置
load_config() {
  if [[ -f "$CONFIG_FILE" ]]; then
    source "$CONFIG_FILE"
  else
    echo "Error: Config file not found: $CONFIG_FILE" >&2
    echo "Please create it from feishu.env.example" >&2
    exit 1
  fi

  if [[ -z "$FEISHU_APP_ID" || -z "$FEISHU_APP_SECRET" ]]; then
    echo "Error: FEISHU_APP_ID or FEISHU_APP_SECRET not set" >&2
    exit 1
  fi
}

# 获取新 token
fetch_new_token() {
  local response
  response=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
    -H "Content-Type: application/json" \
    -d "{
      \"app_id\": \"${FEISHU_APP_ID}\",
      \"app_secret\": \"${FEISHU_APP_SECRET}\"
    }")

  local code=$(echo "$response" | grep -o '"code":[0-9]*' | cut -d: -f2)
  
  if [[ "$code" != "0" ]]; then
    echo "Error: Failed to get token. Response: $response" >&2
    exit 1
  fi

  # 缓存 token 和过期时间
  local token=$(echo "$response" | grep -o '"tenant_access_token":"[^"]*"' | cut -d'"' -f4)
  local expire=$(echo "$response" | grep -o '"expire":[0-9]*' | cut -d: -f2)
  local expiry_time=$(($(date +%s) + expire - 60))  # 提前60秒过期

  cat > "$CACHE_FILE" << EOF
{
  "token": "${token}",
  "expiry_time": ${expiry_time}
}
EOF

  echo "$token"
}

# 获取有效 token（带缓存）
get_feishu_token() {
  # 检查缓存
  if [[ -f "$CACHE_FILE" ]]; then
    local expiry_time=$(grep -o '"expiry_time":[0-9]*' "$CACHE_FILE" | cut -d: -f2)
    local current_time=$(date +%s)
    
    if [[ $current_time -lt $expiry_time ]]; then
      grep -o '"token":"[^"]*"' "$CACHE_FILE" | cut -d'"' -f4
      return 0
    fi
  fi

  # 缓存过期或不存在，获取新 token
  load_config
  fetch_new_token
}

# 强制刷新 token
refresh_feishu_token() {
  load_config
  rm -f "$CACHE_FILE"
  fetch_new_token
}

# 主入口
case "${1:-}" in
  "get")
    get_feishu_token
    ;;
  "refresh")
    refresh_feishu_token
    ;;
  *)
    echo "Usage: $0 {get|refresh}"
    echo "  get     - Get valid token (from cache or fetch new)"
    echo "  refresh - Force refresh token"
    exit 1
    ;;
esac
