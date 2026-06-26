#!/usr/bin/env bash
# Marketing Strategy Benchmarks - Get platform benchmarks & KPIs
set -euo pipefail
API_BASE="https://1341839497-2yuxt6z58d.ap-guangzhou.tencentscf.com"
PLATFORM="${1:-}"
if [[ -z "$PLATFORM" || "$PLATFORM" == "--all" ]]; then
  curl -s "${API_BASE}/benchmarks" | jq -r '.data | to_entries[] | "📱 \(.key) (\(.value.name)): 新号均播\(.value.avgViews.new) 成熟号\(.value.avgViews.mature) 完播率\(.value.completionRate.good)"'
else
  curl -s "${API_BASE}/benchmarks?platform=${PLATFORM}" | jq -r '.data | to_entries[0] | .value | "📊 \(.name)\n新号均播: \(.avgViews.new)\n成熟号: \(.avgViews.mature)\n完播率(好): \(.completionRate.good)"'
fi
