#!/usr/bin/env bash
# Ad Copy Template Generator - Get platform-specific ad copy templates
set -euo pipefail
API_BASE="https://1341839497-2yuxt6z58d.ap-guangzhou.tencentscf.com"
PLATFORM="${1:-}"
[[ -z "$PLATFORM" ]] && { echo "📋 用法: ./generate.sh douyin | 可选: baidu/xiaohongshu/douyin/taobao/jd"; curl -s "${API_BASE}/generate" | jq -r '.data | to_entries[] | "  📱 \(.key): \(.value.name)"'; exit 0; }
RESPONSE=$(curl -s "${API_BASE}/generate?platform=${PLATFORM}" --connect-timeout 10 --max-time 15)
echo "$RESPONSE" | jq -r '.data | to_entries[0] | .value | "📱 \(.name) 模板:\n\(.template)\n\n技巧:\n" + (.tips | map("  • " + .) | join("\n"))' 2>/dev/null || echo "❌ 获取模板失败"
