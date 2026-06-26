#!/usr/bin/env bash
# GEO Engine Monitor - List AI search engines & audit framework
set -euo pipefail
API_BASE="https://1341839497-2yuxt6z58d.ap-guangzhou.tencentscf.com"
CATEGORY="${1:-}"
if [[ -z "$CATEGORY" || "$CATEGORY" == "--all" ]]; then
  curl -s "${API_BASE}/geo-engines" | jq -r '.data | to_entries[] | "🔍 \(.key): " + (if (.value | type) == "array" then (.value | map("\(.name) \(.marketShare)") | join(", ")) else .value end)'
else
  curl -s "${API_BASE}/geo-engines?category=${CATEGORY}" | jq -r '.data | to_entries[0] | .value | if type == "array" then map("📊 \(.name) — 份额: \(.marketShare)") | join("\n") else . end'
fi
