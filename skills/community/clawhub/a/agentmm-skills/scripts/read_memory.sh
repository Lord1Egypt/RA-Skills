#!/bin/bash
# read_memory.sh — 查询记忆
# 用法: read_memory.sh [--key <key>] [--sort created_at|updated_at|importance_score] [--limit N] [--offset N]
#
# SECURITY MANIFEST:
#   Environment variables accessed: AGENTMM_API_KEY, AGENTMM_API_BASE (only)
#   External endpoints called: https://api.agentmm.site/memory (GET, only)
#   Local files read: none
#   Local files written: none
set -euo pipefail

API_BASE="${AGENTMM_API_BASE:-https://api.agentmm.site}"
API_KEY="${AGENTMM_API_KEY:?Error: AGENTMM_API_KEY environment variable is not set. Format: amm_sk_xxx}"

KEY=""
SORT="created_at"
LIMIT=100
OFFSET=0

while [[ $# -gt 0 ]]; do
  case $1 in
    --key)    KEY="$2";    shift 2 ;;
    --sort)   SORT="$2";   shift 2 ;;
    --limit)  LIMIT="$2";  shift 2 ;;
    --offset) OFFSET="$2"; shift 2 ;;
    *) echo "Error: Unknown parameter: $1" >&2; exit 1 ;;
  esac
done

QUERY="sort=${SORT}&limit=${LIMIT}&offset=${OFFSET}"
[[ -n "${KEY:-}" ]] && QUERY="key=${KEY}&${QUERY}"

curl -s -X GET "$API_BASE/memory?${QUERY}" \
  -H "Authorization: Bearer $API_KEY" | jq .