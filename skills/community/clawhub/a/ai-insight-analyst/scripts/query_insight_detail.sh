#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-https://mcp.applications.jiqizhixin.com}"
API_TOKEN_FROM_ENV="${JQZX_API_TOKEN:-}"

INSIGHT_ID=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --id)
      INSIGHT_ID="${2:-}"
      shift 2
      ;;
    *)
      echo "未知参数: $1"
      exit 1
      ;;
  esac
done

if [[ -z "$API_TOKEN_FROM_ENV" ]]; then
  echo "未检测到环境变量 JQZX_API_TOKEN，请先执行 export JQZX_API_TOKEN=你的Token"
  exit 1
fi

if [[ -z "$INSIGHT_ID" ]]; then
  echo "缺少必填参数 --id"
  exit 1
fi

curl -sS --location --request GET "${BASE_URL%/}/api/v1/insights/${INSIGHT_ID}" \
  --header "X-MCP-TOKEN: ${API_TOKEN_FROM_ENV}" \
  --header "Content-Type: application/json"
