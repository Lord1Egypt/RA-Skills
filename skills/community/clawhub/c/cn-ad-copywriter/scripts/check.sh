#!/usr/bin/env bash
# Ad Copy Compliance Check - Scan ad copy for banned words + SEO issues
# Usage: ./check.sh "广告文案" --platform douyin --keywords "护肤,面膜"
set -euo pipefail
API_BASE="https://1341839497-2yuxt6z58d.ap-guangzhou.tencentscf.com"
TEXT="" PLATFORM="baidu" KEYWORDS="" TITLE=""
while [[ $# -gt 0 ]]; do
  case "$1" in --platform) PLATFORM="$2"; shift 2 ;; --keywords) KEYWORDS="$2"; shift 2 ;; --title) TITLE="$2"; shift 2 ;; --help) echo "用法: ./check.sh \"文案\" [--platform douyin] [--keywords 护肤]"; exit 0 ;; *) TEXT="$1"; shift ;; esac
done
[[ -z "$TEXT" ]] && echo "❌ 请提供文案内容" && exit 1
PAYLOAD=$(printf '{"text":"%s","platform":"%s","keywords":"%s","title":"%s"}' "$TEXT" "$PLATFORM" "$KEYWORDS" "$TITLE")
RESPONSE=$(curl -s -X POST "${API_BASE}/check" -H "Content-Type: application/json" -d "$PAYLOAD" --connect-timeout 10 --max-time 15)
TOTAL=$(echo "$RESPONSE" | jq -r '.data.totalIssues // 0')
HIGH=$(echo "$RESPONSE" | jq -r '.data.stats["高"] // 0')
MID=$(echo "$RESPONSE" | jq -r '.data.stats["中"] // 0')
LOW=$(echo "$RESPONSE" | jq -r '.data.stats["低"] // 0')
echo "📋 合规检测: ${TOTAL}个问题 | 🔴${HIGH} 🟡${MID} 🔵${LOW}"
echo ""
for LEVEL in "高" "中" "低"; do
  WORDS=$(echo "$RESPONSE" | jq -r --arg l "$LEVEL" '[.data.bannedWords[] | select(.level == $l)] | length')
  [[ "$WORDS" -gt 0 ]] && { echo "$RESPONSE" | jq -r --arg l "$LEVEL" '.data.bannedWords[] | select(.level == $l) | "  ⚡ \"" + .keyword + "\" → " + (.suggestion // [] | join(", ")) + " [" + .category + "]"'; echo ""; }
done
