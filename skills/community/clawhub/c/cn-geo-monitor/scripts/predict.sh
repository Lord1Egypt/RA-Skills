#!/usr/bin/env bash
# Content Prediction & Calibration - Predict content performance before publishing
# Usage: ./predict.sh "内容文案" --platform xiaohongshu
set -euo pipefail
API_BASE="https://1341839497-2yuxt6z58d.ap-guangzhou.tencentscf.com"
TEXT="" PLATFORM="baidu" HISTORY=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --platform) PLATFORM="$2"; shift 2 ;;
    --history) HISTORY="$2"; shift 2 ;;
    --help) echo "用法: ./predict.sh \"文案\" [--platform xiaohongshu] [--history 3]"; exit 0 ;;
    *) TEXT="$1"; shift ;;
  esac
done
[[ -z "$TEXT" ]] && echo "❌ 请提供内容文案" && exit 1
PAYLOAD=$(python3 -c "import json; print(json.dumps({'text': '''$TEXT''', 'platform': '$PLATFORM', 'historyCount': $HISTORY}))" 2>/dev/null || echo "{}")
RESPONSE=$(curl -s -X POST "${API_BASE}/predict" -H "Content-Type: application/json" -d "$PAYLOAD" --connect-timeout 10 --max-time 15)
SCORE=$(echo "$RESPONSE" | jq -r '.data.overallScore // 0')
RECO=$(echo "$RESPONSE" | jq -r '.data.recommendation // "未知"')
PHASE=$(echo "$RESPONSE" | jq -r '.data.calibrationPhase.name // "冷启动期"')
echo "📊 内容预测报告 | 综合评分: ${SCORE}/100 | $RECO"
echo "校准阶段: $PHASE"
echo "━━━━━━━━━━━━━━━━━━━━━━"
for DIM in compliance_risk engagement_potential brand_safety seo_visibility ai_citation_probability; do
  LABEL=$(echo "$RESPONSE" | jq -r ".data.predictions.$DIM.label")
  SCORE_D=$(echo "$RESPONSE" | jq -r ".data.predictions.$DIM.score")
  echo "  $LABEL: ${SCORE_D}/100"
done
echo ""
echo "💡 $(echo "$RESPONSE" | jq -r '.data.nextStep // ""')"
