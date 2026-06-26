#!/bin/bash
# get_memory_stats.sh — 获取记忆库统计概览
# 用法: get_memory_stats.sh
#
# SECURITY MANIFEST:
#   Environment variables accessed: AGENTMM_API_KEY, AGENTMM_API_BASE (only)
#   External endpoints called: https://api.agentmm.site/memory/stats (GET, only)
#   Local files read: none
#   Local files written: none
set -euo pipefail

API_BASE="${AGENTMM_API_BASE:-https://api.agentmm.site}"
API_KEY="${AGENTMM_API_KEY:?Error: AGENTMM_API_KEY environment variable is not set. Format: amm_sk_xxx}"

if [[ $# -gt 0 ]]; then
  echo "Error: get_memory_stats.sh takes no parameters." >&2
  exit 1
fi

curl -s -X GET "$API_BASE/memory/stats" \
  -H "Authorization: Bearer $API_KEY" | jq .