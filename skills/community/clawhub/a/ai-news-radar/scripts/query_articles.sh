#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-https://mcp.applications.jiqizhixin.com}"
API_TOKEN_FROM_ENV="${JQZX_API_TOKEN:-}"

KEYWORD=""
PAGE=""
PER_PAGE=""
START_AT=""
END_AT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --keyword)
      KEYWORD="${2:-}"
      shift 2
      ;;
    --page)
      PAGE="${2:-}"
      shift 2
      ;;
    --per-page)
      PER_PAGE="${2:-}"
      shift 2
      ;;
    --start-at)
      START_AT="${2:-}"
      shift 2
      ;;
    --end-at)
      END_AT="${2:-}"
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

if [[ -z "$KEYWORD" ]]; then
  echo "缺少必填参数 --keyword"
  exit 1
fi

curl -sS --location --request GET "${BASE_URL%/}/api/v1/articles" \
  --header "X-MCP-TOKEN: ${API_TOKEN_FROM_ENV}" \
  --header "Content-Type: application/json" \
  --get \
  --data-urlencode "keyword=${KEYWORD}" \
  ${PAGE:+--data-urlencode "page=${PAGE}"} \
  ${PER_PAGE:+--data-urlencode "per_page=${PER_PAGE}"} \
  ${START_AT:+--data-urlencode "start_at=${START_AT}"} \
  ${END_AT:+--data-urlencode "end_at=${END_AT}"}
