#!/bin/bash
# OpenClaw 安装后钩子 - 自动运行初始化
# OpenClaw 会自动执行此脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$(dirname "$SCRIPT_DIR")"

echo "🔔 运行安装后初始化..."

# 运行初始化脚本（非交互模式）
export NONINTERACTIVE=1
"${SKILLS_DIR}/scripts/init-noninteractive.sh"

echo "✅ 初始化完成"
