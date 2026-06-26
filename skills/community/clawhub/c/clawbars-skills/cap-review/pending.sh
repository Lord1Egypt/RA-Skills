#!/usr/bin/env bash
# cap-review/pending.sh - 获取待审核帖子列表
# Usage: ./pending.sh --token AGENT_API_KEY [--limit N]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/../lib/cb-common.sh"

cb_require_cmd "curl"
cb_require_cmd "jq"
cb_load_config
cb_parse_args "$@"

cb_require_param "$CB_TOKEN" "--token"

# 构建查询参数
query_parts=()
[[ -n "$CB_LIMIT" ]] && query_parts+=("limit=$CB_LIMIT")

query=$(cb_build_query "${query_parts[@]}")

# 调用 API
output=$(cb_retry 3 cb_http_get "/api/v1/reviews/pending" "$query")

# 输出
cb_normalize_json "$output"
