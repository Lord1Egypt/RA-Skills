#!/usr/bin/env bash

# Chinese Sensitive Words - Check Script
# Detects sensitive/prohibited words in Chinese text.
# Usage:
#   ./check.sh "要检测的文案"
#   ./check.sh "要检测的文案" --no-ner
#   ./check.sh --file input.txt

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
NER=true
TEXT=""
FILE=""

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

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --no-ner)
      NER=false
      shift
      ;;
    --file)
      FILE="$2"
      shift 2
      ;;
    *)
      if [[ -z "$TEXT" ]]; then
        TEXT="$1"
      fi
      shift
      ;;
  esac
done

# Read from file if specified
if [[ -n "$FILE" ]]; then
  if [[ ! -f "$FILE" ]]; then
    echo "错误: 文件不存在 - $FILE" >&2
    exit 1
  fi
  TEXT=$(cat "$FILE")
fi

# Validate input
if [[ -z "$TEXT" ]]; then
  echo "用法: ./check.sh \"要检测的文案\"" >&2
  echo "      ./check.sh --file input.txt" >&2
  exit 1
fi

# Check text length
CHAR_COUNT=${#TEXT}
if [[ $CHAR_COUNT -gt 3000 ]]; then
  echo "错误: 文本长度 ${CHAR_COUNT} 超过上限 3000 字符" >&2
  exit 1
fi

# Build request
PAYLOAD=$(jq -n --arg text "$TEXT" --argjson ner "$NER" '{text: $text, ner: $ner}')

# Build headers
HEADERS=(-H "Content-Type: application/json")
if [[ -n "$TOKEN" ]]; then
  HEADERS+=(-H "Authorization: Bearer $TOKEN")
fi

# Call API
HTTP_RESPONSE=$(curl -s -w "\n%{http_code}" \
  -X POST \
  "${HEADERS[@]}" \
  -d "$PAYLOAD" \
  --connect-timeout 10 \
  --max-time 30 \
  "$API_BASE/check" 2>&1) || {
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
  echo "检测失败: $API_MSG"
  print_quota_msg
  exit 1
fi

# Parse and format output
HAS_SENSITIVE=$(echo "$BODY" | jq -r '.data.hasSensitive')

if [[ "$HAS_SENSITIVE" == "false" ]]; then
  echo "✅ 未检测到敏感词，文案可以安全发布。"
  echo ""
  echo "检测摘要: 0 个问题，已扫描政治、色情、暴力、赌博、毒品、广告法、医疗功效等全部类别。"
  # Show usage reminder for free users
  if [[ -z "$TOKEN" ]]; then
    print_usage_reminder "$USAGE_COUNT" "$MONTHLY_LIMIT"
  fi
  exit 0
fi

WORD_COUNT=$(echo "$BODY" | jq -r '.data.wordCount')
STAT_HIGH=$(echo "$BODY" | jq -r '.data.stats.high')
STAT_MID=$(echo "$BODY" | jq -r '.data.stats.mid')
STAT_LOW=$(echo "$BODY" | jq -r '.data.stats.low')
STAT_TIP=$(echo "$BODY" | jq -r '.data.stats.tip')
HAS_HIGH=$(echo "$BODY" | jq -r '.data.hasHighRisk')

echo "⚠️ 检测到 ${WORD_COUNT} 个敏感词"
echo ""
echo "风险概览: 🔴 高危=${STAT_HIGH} | 🟡 中危=${STAT_MID} | 🔵 低危=${STAT_LOW} | 💡 提示=${STAT_TIP}"
echo ""

if [[ "$HAS_HIGH" == "true" ]]; then
  echo "🚨 警告: 文本包含高危词汇，可能导致封号或内容删除！"
  echo ""
fi

# Output by risk level
for LEVEL in "高" "中" "低" "提示"; do
  WORDS=$(echo "$BODY" | jq -r --arg level "$LEVEL" '[.data.wordList[] | select(.level == $level)] | length')
  if [[ "$WORDS" -gt 0 ]]; then
    case "$LEVEL" in
      高)    echo "🔴 高危（可能导致封号/删帖）" ;;
      中)    echo "🟡 中危（可能导致限流/降权）" ;;
      低)    echo "🔵 低危（建议修改）" ;;
      提示)  echo "💡 提示（注意措辞）" ;;
    esac

    echo "$BODY" | jq -r --arg level "$LEVEL" '
      .data.wordList[] | select(.level == $level) |
      "  - \"" + .keyword + "\" — 分类: " + .category +
      (if .suggestion and (.suggestion | length) > 0
       then " → 建议替换: " + (.suggestion | join(", "))
       else "" end)
    '
    echo ""
  fi
done

# Show usage reminder for free users
if [[ -z "$TOKEN" ]]; then
  print_usage_reminder "$USAGE_COUNT" "$MONTHLY_LIMIT"
fi
