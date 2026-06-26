#!/bin/bash
# write_memory.sh — 写入或更新一条记忆
# 用法: write_memory.sh --key <key> --content <content> [--tags tag1,tag2] [--context <ctx>] [--related key1,key2]
#
# SECURITY MANIFEST:
#   Environment variables accessed: AGENTMM_API_KEY, AGENTMM_API_BASE (only)
#   External endpoints called: https://api.agentmm.site/memory (POST, only)
#   Local files read: none
#   Local files written: none
set -euo pipefail

API_BASE="${AGENTMM_API_BASE:-https://api.agentmm.site}"
API_KEY="${AGENTMM_API_KEY:?Error: AGENTMM_API_KEY environment variable is not set. Format: amm_sk_xxx}"

KEY=""
CONTENT=""
TAGS=""
CONTEXT_VAL=""
RELATED=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --key)     KEY="$2";         shift 2 ;;
    --content) CONTENT="$2";     shift 2 ;;
    --tags)    TAGS="$2";        shift 2 ;;
    --context) CONTEXT_VAL="$2"; shift 2 ;;
    --related) RELATED="$2";     shift 2 ;;
    *) echo "Error: Unknown parameter: $1" >&2; exit 1 ;;
  esac
done

if [[ -z "${KEY:-}" || -z "${CONTENT:-}" ]]; then
  echo "Error: --key and --content are required." >&2
  exit 1
fi

# Build payload with jq to handle special characters safely
PAYLOAD=$(jq -n --arg k "$KEY" --arg c "$CONTENT" '{key: $k, content: $c}')

if [[ -n "${TAGS:-}" ]]; then
  TAGS_ARR=$(echo "$TAGS" | jq -R 'split(",") | map(ltrimstr(" ") | rtrimstr(" "))')
  PAYLOAD=$(echo "$PAYLOAD" | jq --argjson t "$TAGS_ARR" '. + {tags: $t}')
fi
if [[ -n "${CONTEXT_VAL:-}" ]]; then
  PAYLOAD=$(echo "$PAYLOAD" | jq --arg ctx "$CONTEXT_VAL" '. + {context: $ctx}')
fi
if [[ -n "${RELATED:-}" ]]; then
  RELATED_ARR=$(echo "$RELATED" | jq -R 'split(",") | map(ltrimstr(" ") | rtrimstr(" "))')
  PAYLOAD=$(echo "$PAYLOAD" | jq --argjson r "$RELATED_ARR" '. + {related: $r}')
fi

curl -s -X POST "$API_BASE/memory" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" | jq .