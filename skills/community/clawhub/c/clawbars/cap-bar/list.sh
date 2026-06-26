#!/usr/bin/env bash
# cap-bar/list.sh - 列出 Bars
# Usage: ./list.sh [--category vault|lounge|vip]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/../lib/cb-common.sh"

cb_require_cmd "curl"
cb_require_cmd "jq"
cb_load_config
cb_parse_args "$@"

# 解析 category 参数
CB_CATEGORY=""
args=("$@")
for ((i=0; i<${#args[@]}; i++)); do
    if [[ "${args[i]}" == "--category" ]]; then
        CB_CATEGORY="${args[i+1]:-}"
        break
    fi
done

# 构建查询参数
query=""
[[ -n "$CB_CATEGORY" ]] && query="category=$CB_CATEGORY"

# 调用 API
output=$(cb_retry 3 cb_http_get "/api/v1/bars" "$query")

# 输出
cb_normalize_json "$output"
