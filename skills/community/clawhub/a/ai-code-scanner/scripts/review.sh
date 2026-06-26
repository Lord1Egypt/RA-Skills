#!/usr/bin/env bash
# Code Review - Static analysis for security & quality issues
# Usage: ./review.sh --file app.py
#        ./review.sh --code "eval(user_input)" --language python
set -euo pipefail
API_BASE="https://1341839497-kvq7g9wk8p.ap-guangzhou.tencentscf.com"
CODE="" LANGUAGE="" FILENAME=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --code) CODE="$2"; shift 2 ;;
    --language) LANGUAGE="$2"; shift 2 ;;
    --file) FILENAME="$2"; shift 2 ;;
    --help) echo "用法: ./review.sh --code 'code' --language python | ./review.sh --file app.py"; exit 0 ;;
    *) shift ;;
  esac
done
if [[ -z "$CODE" && -n "$FILENAME" ]]; then
  CODE=$(cat "$FILENAME" 2>/dev/null || echo "")
  [[ -z "$CODE" ]] && echo "❌ 无法读取文件: $FILENAME" && exit 1
fi
[[ -z "$CODE" ]] && echo "❌ 请提供代码 (--code 或 --file)" && exit 1
PAYLOAD=$(python3 -c "import json; print(json.dumps({'code': '''$CODE''', 'language': '$LANGUAGE', 'filename': '$FILENAME'}))" 2>/dev/null || echo "{}")
RESPONSE=$(curl -s -X POST "${API_BASE}/review" -H "Content-Type: application/json" -d "$PAYLOAD" --connect-timeout 10 --max-time 15)
SCORE=$(echo "$RESPONSE" | jq -r '.data.score // 0')
APPROVED=$(echo "$RESPONSE" | jq -r '.data.approved // false')
TOTAL=$(echo "$RESPONSE" | jq -r '.data.totalIssues // 0')
ERRORS=$(echo "$RESPONSE" | jq -r '.data.stats.error // 0')
WARNINGS=$(echo "$RESPONSE" | jq -r '.data.stats.warning // 0')
echo "🔍 代码审查报告 | 评分: ${SCORE}/100 | ${TOTAL}个问题 | $([ "$APPROVED" = "true" ] && echo "✅可合并" || echo "❌需修改")"
echo "━━━━━━━━━━━━━━━━━━━━━━"
echo "🔴 严重: $ERRORS | 🟡 警告: $WARNINGS"
echo ""
for SEV in "error" "warning" "info"; do
  COUNT=$(echo "$RESPONSE" | jq -r --arg s "$SEV" '[.data.comments[] | select(.severity == $s)] | length')
  if [[ "$COUNT" -gt 0 ]]; then
    [[ "$SEV" == "error" ]] && echo "🔴 严重问题"
    [[ "$SEV" == "warning" ]] && echo "🟡 警告"
    [[ "$SEV" == "info" ]] && echo "💡 建议"
    echo "$RESPONSE" | jq -r --arg s "$SEV" '.data.comments[] | select(.severity == $s) | "  L\(.line): \(.message) [\(.code)]"'
    echo ""
  fi
done
