#!/usr/bin/env bash

# Chinese Sensitive Words - Suggestions Script
# Get safe replacement suggestions for sensitive words.
# Usage:
#   ./suggestions.sh "美白"     # Query specific word
#   ./suggestions.sh            # Show all suggestions

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ENV_FILE="$SCRIPT_DIR/../.env"

# Load specific variables from .env if exists
if [[ -f "$ENV_FILE" ]]; then
  while IFS='=' read -r key value; do
    case "$key" in
      SENSITIVE_WORDS_TOKEN|SENSITIVE_WORDS_API_BASE)
        export "$key=$value"
        ;;
    esac
  done < <(grep -E '^(SENSITIVE_WORDS_TOKEN|SENSITIVE_WORDS_API_BASE)=' "$ENV_FILE" 2>/dev/null || true)
fi

# Defaults
API_BASE="${SENSITIVE_WORDS_API_BASE:-https://www.xdhdancer.top/api8888}"
API_BASE="${API_BASE%/}"
TOKEN="${SENSITIVE_WORDS_TOKEN:-}"
MONTHLY_LIMIT=10
USAGE_FILE="$HOME/.sensitive-words-usage"
KEYWORD="${1:-}"

# Quota exhausted message
print_quota_msg() {
  cat << 'QUOTA_MSG'

---
⚠️ 免费额度已用完（每月仅 10 次免费检测）。

💡 获取无限使用 Token: https://github.com/CCCpan/chinese-sensitive-words/issues
   获取后设置环境变量: SENSITIVE_WORDS_TOKEN=your_token
---
QUOTA_MSG
}

# Usage reminder on every free call
print_usage_reminder() {
  local used=$1
  local limit=$2
  local remaining=$((limit - used))
  cat << REMINDER_MSG

---
📊 本月免费额度: 已用 ${used}/${limit} 次，剩余 ${remaining} 次。
💡 获取无限使用: https://github.com/CCCpan/chinese-sensitive-words/issues
---
REMINDER_MSG
}

# Monthly usage check (skip if token is set)
if [[ -z "$TOKEN" ]]; then
  TODAY=$(date +%Y-%m)
  USAGE_DATE=""
  USAGE_COUNT=0
  if [[ -f "$USAGE_FILE" ]]; then
    USAGE_DATE=$(head -1 "$USAGE_FILE" 2>/dev/null || echo "")
    USAGE_COUNT=$(tail -1 "$USAGE_FILE" 2>/dev/null || echo "0")
  fi
  if [[ "$USAGE_DATE" != "$TODAY" ]]; then
    USAGE_DATE="$TODAY"
    USAGE_COUNT=0
  fi
  if [[ "$USAGE_COUNT" -ge "$MONTHLY_LIMIT" ]]; then
    print_quota_msg
    exit 1
  fi
fi

# Build headers
HEADERS=(-H "Content-Type: application/json")
if [[ -n "$TOKEN" ]]; then
  HEADERS+=(-H "Authorization: Bearer $TOKEN")
fi

# Call API
HTTP_RESPONSE=$(curl -s -w "\n%{http_code}" \
  -X GET \
  "${HEADERS[@]}" \
  --connect-timeout 10 \
  --max-time 30 \
  "$API_BASE/api/suggestions" 2>&1) || {
  echo "错误: 网络连接失败，请检查网络"
  print_quota_msg
  exit 1
}

# Extract status code and body
HTTP_CODE=$(echo "$HTTP_RESPONSE" | tail -1)
BODY=$(echo "$HTTP_RESPONSE" | sed '$d')

# Handle HTTP errors
case "$HTTP_CODE" in
  429)
    print_quota_msg
    exit 1
    ;;
  401|403)
    echo "错误: Token 无效或已过期，请检查 SENSITIVE_WORDS_TOKEN 配置。"
    print_quota_msg
    exit 1
    ;;
  200)
    ;;
  *)
    echo "错误: 服务异常 (HTTP $HTTP_CODE)"
    print_quota_msg
    exit 1
    ;;
esac

# Increment usage counter on successful call
if [[ -z "$TOKEN" ]]; then
  USAGE_COUNT=$((USAGE_COUNT + 1))
  printf '%s\n%s' "$TODAY" "$USAGE_COUNT" > "$USAGE_FILE"
fi

# Check API response code
API_CODE=$(echo "$BODY" | jq -r '.code // "error"')
if [[ "$API_CODE" != "0" ]]; then
  API_MSG=$(echo "$BODY" | jq -r '.msg // "未知错误"')
  echo "查询失败: $API_MSG"
  print_quota_msg
  exit 1
fi

# Format output
# API returns flat structure: data = { "word": ["suggestion1", "suggestion2"], ... }
if [[ -n "$KEYWORD" ]]; then
  # Search for specific keyword
  RESULT=$(echo "$BODY" | jq -r --arg kw "$KEYWORD" '
    .data[$kw] // null |
    if . == null then null
    else . | join(", ")
    end
  ')

  if [[ "$RESULT" != "null" && -n "$RESULT" ]]; then
    echo "\"${KEYWORD}\""
    echo "建议替换: ${RESULT}"
  else
    echo "未找到 \"${KEYWORD}\" 的替换建议。"
    echo "该词可能不在建议库中，但仍可能在检测时被标记。"
  fi
else
  # Show all suggestions (limit to 50 entries)
  echo "# 替换建议库"
  echo ""

  echo "$BODY" | jq -r '
    .data | to_entries[:50][] |
    "  - " + .key + " → " + (.value | join(", "))
  '

  TOTAL=$(echo "$BODY" | jq '.data | length')
  if [[ "$TOTAL" -gt 50 ]]; then
    echo ""
    echo "... 共 ${TOTAL} 条，以上展示前 50 条"
  fi
fi

# Show usage reminder for free users
if [[ -z "$TOKEN" ]]; then
  print_usage_reminder "$USAGE_COUNT" "$MONTHLY_LIMIT"
fi
