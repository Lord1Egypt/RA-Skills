#!/bin/bash
# =============================================
# Codex Agent 自动配置脚本
# =============================================

set -e

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
MODE="${1:-simple}"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo_info() { echo -e "${GREEN}ℹ️  $1${NC}"; }
echo_warn() { echo -e "${YELLOW}⚠️  $1${NC}"; }
echo_error() { echo -e "${RED}❌ $1${NC}"; }

check_dependencies() {
    echo_info "检查依赖..."
    if ! command -v codex &>/dev/null; then
        echo_error "Codex CLI 未安装"
        exit 1
    fi
    if ! command -v openclaw &>/dev/null; then
        echo_error "OpenClaw 未安装"
        exit 1
    fi
    echo_info "✓ 依赖检查通过"
}

get_user_config() {
    echo ""
    echo_info "请配置以下参数："
    read -p "Agent 名称 (main/kimi-agent/gpt-agent/glm-agent, 默认 main): " agent_name
    AGENT_NAME="${agent_name:-main}"
    read -p "Telegram Chat ID (默认 7936836901): " chat_id
    CHAT_ID="${chat_id:-7936836901}"
    if [ "$MODE" = "cron" ]; then
        read -p "项目目录路径 (默认当前目录): " project_dir
        PROJECT_DIR="${project_dir:-$(pwd)}"
        read -p "任务 ID (默认 TASK-001): " task_id
        TASK_ID="${task_id:-TASK-001}"
    fi
}

create_env_file() {
    local env_file="$SKILL_DIR/.env"
    cat > "$env_file" << EOF
OPENCLAW_AGENT_NAME="$AGENT_NAME"
OPENCLAW_AGENT_CHAT_ID="$CHAT_ID"
OPENCLAW_AGENT_CHANNEL="telegram"
EOF
    if [ "$MODE" = "cron" ]; then
        cat >> "$env_file" << EOF
OPENCLAW_PROJECT_STATE_FILE="$PROJECT_DIR/.codex-task-state.json"
OPENCLAW_PROJECT_TASK_ID="$TASK_ID"
OPENCLAW_PROJECT_TASK_DIR="$PROJECT_DIR/tasks/$TASK_ID"
EOF
    fi
    echo_info "✓ .env 文件已创建"
}

configure_codex() {
    local config_file="$HOME/.codex/config.toml"
    local hook_path="$SKILL_DIR/hooks/on_complete.py"
    if [ ! -f "$config_file" ]; then
        mkdir -p "$(dirname "$config_file")"
        cat > "$config_file" << EOF
model = "gpt-5.3-codex"
notify = ["python3", "$hook_path"]
[features]
fast_mode = true
EOF
    elif ! grep -q "^notify" "$config_file"; then
        echo "" >> "$config_file"
        echo "notify = [\"python3\", \"$hook_path\"]" >> "$config_file"
    fi
    echo_info "✓ Codex 配置已更新"
}

configure_cron() {
    local cron_dir="$SKILL_DIR/cron"
    local cron_file="$cron_dir/codex-task-waker.json"
    mkdir -p "$cron_dir"
    cat > "$cron_file" << EOF
{
  "name": "codex-task-waker",
  "agentId": "$AGENT_NAME",
  "schedule": {
    "kind": "every",
    "everyMs": 600000,
    "anchorMs": $(date +%s)000
  },
  "sessionTarget": "main",
  "wakeMode": "now",
  "payload": {
    "kind": "systemEvent",
    "text": "请读取 $SKILL_DIR/tasks/codex-task-waker.prompt.md 并严格执行。"
  },
  "delivery": { "mode": "none" },
  "deleteAfterRun": false
}
EOF
    echo_info "✓ Cron Job 配置已创建"
    echo_warn "手动执行：openclaw cron add $cron_file"
}

main() {
    echo "============================================="
    echo "  Codex Agent 自动配置 [模式：$MODE]"
    echo "============================================="
    check_dependencies
    get_user_config
    create_env_file
    configure_codex
    [ "$MODE" = "cron" ] && configure_cron
    echo "============================================="
    echo "  ✅ 配置完成！"
    echo "============================================="
    echo "下一步："
    echo "  source $SKILL_DIR/.env"
    [ "$MODE" = "cron" ] && echo "  openclaw cron add $SKILL_DIR/cron/codex-task-waker.json"
    echo "  codex exec --full-auto \"你的任务\""
}

main
