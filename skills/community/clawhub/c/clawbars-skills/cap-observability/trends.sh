#!/usr/bin/env bash
# cap-observability/trends.sh - 获取趋势数据
# Usage: ./trends.sh [--period 24h|7d] [--top N]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/../lib/cb-common.sh"

cb_require_cmd "curl"
cb_require_cmd "jq"
cb_load_config

# 解析参数
period=""
top=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --period) period="$2"; shift 2 ;;
        --top) top="$2"; shift 2 ;;
        *) shift ;;
    esac
done

# 构建查询参数
query_parts=()
[[ -n "$period" ]] && query_parts+=("period=$period")
[[ -n "$top" ]] && query_parts+=("top=$top")

query=$(cb_build_query "${query_parts[@]}")

# 调用 API
output=$(cb_retry 3 cb_http_get "/api/v1/trends" "$query")

# 输出
cb_normalize_json "$output"
