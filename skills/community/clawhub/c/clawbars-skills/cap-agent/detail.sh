#!/usr/bin/env bash
# cap-agent/detail.sh - 获取 Agent 详情
# Usage: ./detail.sh --agent-id AGENT_ID

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/../lib/cb-common.sh"

cb_require_cmd "curl"
cb_require_cmd "jq"
cb_load_config
cb_parse_args "$@"

cb_require_param "$CB_AGENT_ID" "--agent-id"

# 调用 API
output=$(cb_retry 3 cb_http_get "/api/v1/agents/$CB_AGENT_ID")

# 输出
cb_normalize_json "$output"
