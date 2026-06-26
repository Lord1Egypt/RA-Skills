#!/usr/bin/env bash
# Chinese AI Search Engine Deep Data - Query per-engine optimization data
# Usage: ./cn-ai-engines.sh deepseek
#        ./cn-ai-engines.sh --all
set -euo pipefail
API_BASE="https://1341839497-2yuxt6z58d.ap-guangzhou.tencentscf.com"
ENGINE="${1:-}"
[[ "$ENGINE" == "--all" ]] && ENGINE=""
if [[ -z "$ENGINE" ]]; then
  echo "🔍 中国AI搜索引擎深度数据"
  echo "━━━━━━━━━━━━━━━━━━━━━━"
  RESPONSE=$(curl -s "${API_BASE}/cn-ai-engines" --connect-timeout 10 --max-time 15)
  for e in deepseek kimi doubao tongyi ernie; do
    echo "$RESPONSE" | jq -r --arg e "$e" '.data[$e] | "🔍 \(.name)(\(.company)) — 份额:\(.marketShare) 月活:\(.monthlyActiveUsers)\n   引用:\(.citationStyle) | 偏好:\(.preferredSources | join(","))\n   最佳格式:\(.contentPreferences.bestFormat)\n"'
  done
  echo "$RESPONSE" | jq -r '.data.optimizationFramework | "📋 优化框架: \(.name)\n" + (.steps | map("  Step \(.step): \(.action) — \(.detail)") | join("\n"))'
else
  RESPONSE=$(curl -s "${API_BASE}/cn-ai-engines?engine=$ENGINE" --connect-timeout 10 --max-time 15)
  echo "$RESPONSE" | jq -r '.data | to_entries[0] | .value |
    "🔍 \(.name)(\(.company))\n" +
    "份额: \(.marketShare) | 月活: \(.monthlyActiveUsers) | API: \(if .apiAvailable then "✅" else "❌" end)\n" +
    "引用风格: \(.citationStyle) | 优先级: \(.priority)\n" +
    "偏好来源: \(.preferredSources | join(" > "))\n" +
    "最佳格式: \(.contentPreferences.bestFormat)\n" +
    "引用长度: \(.contentPreferences.avgCitationLength)\n" +
    "触发条件: \(.contentPreferences.citationTrigger)\n" +
    "避免: \(.contentPreferences.avoidPatterns | join(", "))\n" +
    "优化技巧:\n" + (.optimizationTips | map("  • " + .) | join("\n"))'
fi
