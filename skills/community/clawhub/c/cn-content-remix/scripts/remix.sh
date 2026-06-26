#!/usr/bin/env bash
# Content Remix - Get platform-specific content adaptation rules
set -euo pipefail
API_BASE="https://1341839497-2yuxt6z58d.ap-guangzhou.tencentscf.com"
PLATFORM="${1:-}"
if [[ -z "$PLATFORM" || "$PLATFORM" == "--all" ]]; then
  curl -s "${API_BASE}/remix" | jq -r '.data | to_entries[] | "📱 \(.key) (\(.value.name)): 标题\(.value.titleLength.min)-\(.value.titleLength.max)字 正文\(.value.contentLength.min)-\(.value.contentLength.max)字"'
else
  curl -s "${API_BASE}/remix?platform=${PLATFORM}" | jq -r '.data | to_entries[0] | .value | "📱 \(.name)\n标题: \(.titleLength.min)-\(.titleLength.max)字\n正文: \(.contentLength.min)-\(.contentLength.max)字\n标签: \(.hashtags.min)-\(.hashtags.max)个\n语气: \(.tone)"'
fi
