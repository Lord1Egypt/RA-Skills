#!/usr/bin/env bash
# cap-post/suggest.sh - 搜索建议
# Usage: ./suggest.sh --query "keyword" [--limit N]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/../lib/cb-common.sh"

cb_require_cmd "curl"
cb_require_cmd "jq"
cb_load_config
cb_parse_args "$@"

cb_require_param "$CB_QUERY" "--query"

# 构建查询参数
query_parts=("q=$(cb_url_encode "$CB_QUERY")")
[[ -n "$CB_LIMIT" ]] && query_parts+=("limit=$CB_LIMIT")

query=$(cb_build_query "${query_parts[@]}")

# 调用 API
output=$(cb_retry 3 cb_http_get "/api/v1/posts/suggest" "$query")

# 输出
cb_normalize_json "$output"
