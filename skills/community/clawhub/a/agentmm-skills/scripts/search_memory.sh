#!/bin/bash
# search_memory.sh — 关键词搜索记忆
# 用法: search_memory.sh --query <搜索词> [--limit N]
#
# SECURITY MANIFEST:
#   Environment variables accessed: AGENTMM_API_KEY, AGENTMM_API_BASE (only)
#   External endpoints called: https://api.agentmm.site/memory/search (POST, only)
#   Local files read: none
#   Local files written: none
set -euo pipefail

API_BASE="${AGENTMM_API_BASE:-https://api.agentmm.site}"
API_KEY="${AGENTMM_API_KEY:?Error: AGENTMM_API_KEY environment variable is not set. Format: amm_sk_xxx}"

# Parse arguments
QUERY=""
TAGS=""
LIMIT=50
FUZZY=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --query)
      QUERY="$2"
      shift 2
      ;;
    --tags)
      TAGS="$2"
      shift 2
      ;;
    --limit)
      LIMIT="$2"
      shift 2
      ;;
    --fuzzy)
      FUZZY=true
      shift
      ;;
    *)
      echo "Unknown parameter: $1"
      exit 1
      ;;
  esac
done

# Validate required parameters
if [[ -z "${QUERY:-}" ]]; then
  echo "Error: --query is required."
  exit 1
fi

# Build JSON payload safely via jq (no shell interpolation)
PAYLOAD=$(jq -n --arg q "$QUERY" --argjson l "$LIMIT" '{query: $q, limit: $l}')
if [[ -n "${TAGS:-}" ]]; then
  TAGS_ARR=$(echo "$TAGS" | jq -R 'split(",") | map(ltrimstr(" ") | rtrimstr(" "))')
  PAYLOAD=$(echo "$PAYLOAD" | jq --argjson t "$TAGS_ARR" '. + {tags: $t}')
fi
if [[ "$FUZZY" == true ]]; then
  PAYLOAD=$(echo "$PAYLOAD" | jq '. + {fuzzy: true}')
fi

curl -s -X POST "$API_BASE/memory/search" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" | jq .