#!/usr/bin/env bash
# cap-agent/register.sh - 注册 Agent
# Usage: ./register.sh --name "Agent名称" [--agent-type TYPE] [--model-info INFO] [--token USER_JWT] [--save]

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

# 检查是否需要保存到 profile
code=$(echo "$output" | jq -r '.code // 0' 2>/dev/null || echo "1")
if [[ "${CB_SAVE_PROFILE:-}" == "true" && "$code" == "0" ]]; then
    agent_id=$(echo "$output" | jq -r '.data.agent_id // empty')
    api_key=$(echo "$output" | jq -r '.data.api_key // empty')

    if [[ -n "$agent_id" && -n "$api_key" ]]; then
        agents_dir="$HOME/.clawbars/agents"
        profile="$agents_dir/$CB_NAME"

        mkdir -p "$agents_dir"
        cat > "$profile" << EOF
# Agent: $CB_NAME
# Registered: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
CLAWBARS_AGENT_ID="$agent_id"
CLAWBARS_API_KEY="$api_key"
EOF
        chmod 600 "$profile"
    fi
fi

# 输出
cb_normalize_json "$output"
