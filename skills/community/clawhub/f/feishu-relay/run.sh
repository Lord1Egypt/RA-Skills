#!/bin/bash
#
# Feishu Notifier v2.0 - Entry Point
# 飞书通知技能入口脚本
#
# 这个脚本作为 OpenClaw skill 的入口，调用 Python 核心模块

set -e

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIB_DIR="${SCRIPT_DIR}/lib"

# 设置 skill 目录环境变量（用于配置查找）
export FEISHU_SKILL_DIR="${SCRIPT_DIR}"

# 检查 Python 是否可用
if ! command -v python3 &> /dev/null; then
    echo '{"success":false,"error":"PYTHON_NOT_FOUND","message":"Python 3 is required but not installed"}' >&2
    exit 1
fi

# 执行 Python 核心模块
exec python3 "${LIB_DIR}/send.py" "$@"
