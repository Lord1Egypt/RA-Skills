#!/bin/bash
# forget_memory.sh — 遗忘（软删除）一条记忆
# 用法: forget_memory.sh --key <key>
#
# SECURITY MANIFEST:
#   Environment variables accessed: AGENTMM_API_KEY, AGENTMM_API_BASE (only)
#   External endpoints called: https://api.agentmm.site/memory (DELETE, only)
#   Local files read: none
#   Local files written: none
set -euo pipefail

API_BASE="${AGENTMM_API_BASE:-https://api.agentmm.site}"
API_KEY="${AGENTMM_API_KEY:?Error: AGENTMM_API_KEY environment variable is not set. Format: amm_sk_xxx}"

# Parse arguments
KEY=""
while [[ $# -gt 0 ]]; do
  case $1 in
    --key)
      KEY="$2"
      shift 2
      ;;
    *)
      echo "Unknown parameter: $1"
      exit 1
      ;;
  esac
done

# Validate required parameter
if [[ -z "${KEY:-}" ]]; then
  echo "Error: --key is required."
  exit 1
fi

curl -s -X DELETE "$API_BASE/memory?key=$KEY" \
  -H "Authorization: Bearer $API_KEY" | jq .