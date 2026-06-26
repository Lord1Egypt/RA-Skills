#!/usr/bin/env bash
# cap-agent/list.sh - 列出 Agents
# Usage: ./list.sh [--agent-type TYPE] [--limit N]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/../lib/cb-common.sh"

cb_require_cmd "curl"
cb_require_cmd "jq"
cb_load_config
cb_parse_args "$@"

# 构建查询参数
query_parts=()
[[ -n "$CB_AGENT_TYPE" ]] && query_parts+=("agent_type=$CB_AGENT_TYPE")
[[ -n "$CB_LIMIT" ]] && query_parts+=("limit=$CB_LIMIT")

query=$(cb_build_query "${query_parts[@]}")

# 调用 API
output=$(cb_retry 3 cb_http_get "/api/v1/agents" "$query")

# 输出
cb_normalize_json "$output"
