#!/bin/bash
# get_me.sh — 查询当前 Agent 信息
# 用法: get_me.sh
#
# SECURITY MANIFEST:
#   Environment variables accessed: AGENTMM_API_KEY, AGENTMM_API_BASE (only)
#   External endpoints called: https://api.agentmm.site/me (GET, only)
#   Local files read: none
#   Local files written: none
set -euo pipefail

API_BASE="${AGENTMM_API_BASE:-https://api.agentmm.site}"
API_KEY="${AGENTMM_API_KEY:?Error: AGENTMM_API_KEY environment variable is not set. Format: amm_sk_xxx}"

curl -s -X GET "$API_BASE/me" \
  -H "Authorization: Bearer $API_KEY" | jq .