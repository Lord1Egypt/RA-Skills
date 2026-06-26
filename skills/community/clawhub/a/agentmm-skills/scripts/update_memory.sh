#!/bin/bash
# update_memory.sh — 更新已有记忆（内部使用 POST /memory 实现 upsert）
# 用法: update_memory.sh --key <key> [--content <new>] [--tags tag1,tag2] [--context <ctx>]
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

while [[ $# -gt 0 ]]; do
  case $1 in
    --key)     KEY="$2";         shift 2 ;;
    --content) CONTENT="$2";     shift 2 ;;
    --tags)    TAGS="$2";        shift 2 ;;
    --context) CONTEXT_VAL="$2"; shift 2 ;;
    *) echo "Error: Unknown parameter: $1" >&2; exit 1 ;;
  esac
done

if [[ -z "${KEY:-}" ]]; then
  echo "Error: --key is required." >&2
  exit 1
fi
if [[ -z "${CONTENT:-}" && -z "${TAGS:-}" && -z "${CONTEXT_VAL:-}" ]]; then
  echo "Error: at least one of --content, --tags, or --context is required." >&2
  exit 1
fi

# API 使用 POST /memory 实现写入和更新（upsert）
PAYLOAD=$(jq -n --arg k "$KEY" '{key: $k}')

[[ -n "${CONTENT:-}" ]] && PAYLOAD=$(echo "$PAYLOAD" | jq --arg c "$CONTENT" '. + {content: $c}')
if [[ -n "${TAGS:-}" ]]; then
  TAGS_ARR=$(echo "$TAGS" | jq -R 'split(",") | map(ltrimstr(" ") | rtrimstr(" "))')
  PAYLOAD=$(echo "$PAYLOAD" | jq --argjson t "$TAGS_ARR" '. + {tags: $t}')
fi
[[ -n "${CONTEXT_VAL:-}" ]] && PAYLOAD=$(echo "$PAYLOAD" | jq --arg ctx "$CONTEXT_VAL" '. + {context: $ctx}')

curl -s -X POST "$API_BASE/memory" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" | jq .