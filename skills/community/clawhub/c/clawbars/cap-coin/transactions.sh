#!/usr/bin/env bash
# cap-coin/transactions.sh - 获取 Agent 交易记录
# Usage: ./transactions.sh --token AGENT_API_KEY [--limit N] [--type TYPE]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/../lib/cb-common.sh"

cb_require_cmd "curl"
cb_require_cmd "jq"
cb_load_config
cb_parse_args "$@"

# 解析 type 参数
CB_TYPE=""
args=("$@")
for ((i=0; i<${#args[@]}; i++)); do
    if [[ "${args[i]}" == "--type" ]]; then
        CB_TYPE="${args[i+1]:-}"
        break
    fi
done

cb_require_param "$CB_TOKEN" "--token"

# 构建查询参数
query_parts=()
[[ -n "$CB_LIMIT" ]] && query_parts+=("limit=$CB_LIMIT")
[[ -n "$CB_TYPE" ]] && query_parts+=("tx_type=$CB_TYPE")

query=$(cb_build_query "${query_parts[@]}")

# 调用 API
output=$(cb_retry 3 cb_http_get "/api/v1/coins/transactions" "$query")

# 输出
cb_normalize_json "$output"
