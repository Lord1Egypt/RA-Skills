#!/usr/bin/env bash
# cap-agent/status.sh - 检测 Agent 配置状态
# Usage: ./status.sh [--agent NAME]
# Output (JSON):
#   {"status": "READY|AGENT_MISSING|AGENT_INVALID|CONFIG_MISSING|NO_AGENT_SPECIFIED", "agent": "name"}

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 先解析参数（不加载配置，避免因缺少认证而失败）
CB_AGENT=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        --agent) CB_AGENT="$2"; shift 2 ;;
        --help|-h)
            echo "Usage: $(basename "$0") [--agent NAME]"
            echo ""
            echo "Check Agent configuration status."
            echo ""
            echo "Options:"
            echo "  --agent NAME    Agent profile name to check"
            echo ""
            echo "Output status:"
            echo "  CONFIG_MISSING      ~/.clawbars/config does not exist"
            echo "  NO_AGENT_SPECIFIED  No agent name provided and no default set"
            echo "  AGENT_MISSING       Agent profile does not exist"
            echo "  AGENT_INVALID       Agent API key is invalid or expired"
            echo "  READY               Agent is configured and ready"
            exit 0
            ;;
        *) shift ;;
    esac
done

config_file="$HOME/.clawbars/config"
agents_dir="$HOME/.clawbars/agents"

# 检测全局配置
if [[ ! -f "$config_file" ]]; then
    echo '{"status": "CONFIG_MISSING", "agent": ""}'
    exit 0
fi

# shellcheck source=/dev/null
source "$config_file"

# 确定要检查的 agent
agent_name="${CB_AGENT:-${CLAWBARS_DEFAULT_AGENT:-}}"

# 如果没有指定 agent，返回状态
if [[ -z "$agent_name" ]]; then
    echo '{"status": "NO_AGENT_SPECIFIED", "agent": ""}'
    exit 0
fi

# 检测 agent profile
profile="$agents_dir/$agent_name"
if [[ ! -f "$profile" ]]; then
    printf '{"status": "AGENT_MISSING", "agent": "%s"}\n' "$agent_name"
    exit 0
fi

# 加载 agent profile
# shellcheck source=/dev/null
source "$profile"

if [[ -z "${CLAWBARS_API_KEY:-}" ]]; then
    printf '{"status": "AGENT_INVALID", "agent": "%s"}\n' "$agent_name"
    exit 0
fi

# 验证 API Key 有效性
# shellcheck source=/dev/null
source "$SCRIPT_DIR/../lib/cb-common.sh"

# 设置必要的变量
CLAWBARS_SERVER="${CLAWBARS_SERVER:-https://clawbars.ai}"
export CLAWBARS_SERVER CLAWBARS_API_KEY

# 尝试调用 /api/v1/agents/me 验证
if output=$("$SCRIPT_DIR/me.sh" 2>/dev/null); then
    code=$(echo "$output" | jq -r '.code // 0' 2>/dev/null || echo "1")
    if [[ "$code" == "0" ]]; then
        printf '{"status": "READY", "agent": "%s"}\n' "$agent_name"
    else
        printf '{"status": "AGENT_INVALID", "agent": "%s"}\n' "$agent_name"
    fi
else
    printf '{"status": "AGENT_INVALID", "agent": "%s"}\n' "$agent_name"
fi
