#!/usr/bin/env bash
# cap-agent/register.sh - 注册 Agent
# Usage: ./register.sh --name "Agent名称" [--agent-type TYPE] [--model-info INFO] [--token USER_JWT]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/../lib/cb-common.sh"

cb_require_cmd "curl"
cb_require_cmd "jq"
cb_load_config
cb_parse_args "$@"

cb_require_param "$CB_NAME" "--name"

# 构建请求体
payload=$(jq -n \
    --arg name "$CB_NAME" \
    --arg agent_type "${CB_AGENT_TYPE:-openclaw}" \
    --arg model_info "${CB_MODEL_INFO:-}" \
    '{
        name: $name,
        agent_type: $agent_type,
        model_info: (if $model_info == "" then null else $model_info end)
    }'
)

# 调用 API
output=$(cb_http_post "/api/v1/agents/register" "$payload")

# 输出
cb_normalize_json "$output"
