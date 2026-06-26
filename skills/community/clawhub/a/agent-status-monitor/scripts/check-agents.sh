#!/bin/bash
# check-agents.sh - 检查所有本地开发 Agent 运行状态
# 用法：./check-agents.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

COLOR_RESET="\033[0m"
COLOR_BLUE="\033[34m"

echo -e "${COLOR_BLUE}========================================${COLOR_RESET}"
echo -e "${COLOR_BLUE}   Agent Status Monitor${COLOR_RESET}"
echo -e "${COLOR_BLUE}========================================${COLOR_RESET}"
echo ""

echo -e "${COLOR_BLUE}--- 进程状态 ---${COLOR_RESET}"

# 调用各个独立检测脚本
"$SCRIPT_DIR/check-claude-code.sh"
echo ""

"$SCRIPT_DIR/check-openclaw.sh"
echo ""

"$SCRIPT_DIR/check-opencode.sh"
echo ""

"$SCRIPT_DIR/check-cursor.sh"
echo ""

echo -e "${COLOR_BLUE}========================================${COLOR_RESET}"
