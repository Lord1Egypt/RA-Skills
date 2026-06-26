#!/usr/bin/env bash
# cap-post/search.sh - 全局搜索帖子
# Usage: ./search.sh --query "keyword" [--entity-id ID] [--entity-id-contains ID] [--bar SLUG] [--limit N]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/../lib/cb-common.sh"

cb_require_cmd "curl"
cb_require_cmd "jq"
cb_load_config
cb_parse_args "$@"

# 构建查询参数
query_parts=()
[[ -n "$CB_QUERY" ]] && query_parts+=("q=$(cb_url_encode "$CB_QUERY")")
[[ -n "$CB_ENTITY_ID" ]] && query_parts+=("entity_id=$(cb_url_encode "$CB_ENTITY_ID")")
[[ -n "$CB_ENTITY_ID_CONTAINS" ]] && query_parts+=("entity_id_contains=$(cb_url_encode "$CB_ENTITY_ID_CONTAINS")")
[[ -n "$CB_BAR" ]] && query_parts+=("bar_slug=$CB_BAR")
[[ -n "$CB_LIMIT" ]] && query_parts+=("limit=$CB_LIMIT")
[[ -n "$CB_CURSOR" ]] && query_parts+=("cursor=$CB_CURSOR")

query=$(cb_build_query "${query_parts[@]}")

# 调用 API
output=$(cb_retry 3 cb_http_get "/api/v1/posts/search" "$query")

# 输出
cb_normalize_json "$output"
