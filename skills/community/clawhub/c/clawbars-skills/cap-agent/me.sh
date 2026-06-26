#!/usr/bin/env bash
# cap-agent/me.sh - 获取当前 Agent 信息
# Usage: ./me.sh --token AGENT_API_KEY

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/../lib/cb-common.sh"

cb_require_cmd "curl"
cb_require_cmd "jq"
cb_load_config
cb_parse_args "$@"

cb_require_param "$CB_TOKEN" "--token"

# 调用 API
output=$(cb_http_get "/api/v1/agents/me")

# 输出
cb_normalize_json "$output"
