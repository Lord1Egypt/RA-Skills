#!/bin/bash
# ============================================================
# OpenClaw Skill 运行入口
# 功能：接收 OpenClaw 传入的消息参数，调用 Python 脚本处理
# 用法：./run.sh '<JSON消息体>'
# ============================================================

set -euo pipefail

# 获取脚本所在目录（Skill 安装目录）
SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"

# Python 解释器路径（优先使用 Skill 虚拟环境）
if [ -f "${SKILL_DIR}/venv/bin/python3" ]; then
    PYTHON="${SKILL_DIR}/venv/bin/python3"
elif command -v python3 &>/dev/null; then
    PYTHON="python3"
else
    echo "❌ 未找到 Python3 解释器" >&2
    exit 1
fi

# 检查配置是否存在（加密配置文件 + 加密密钥文件缺一不可）
if [ ! -f "${SKILL_DIR}/scripts/conf/cos_secret.enc" ] || [ ! -f "${SKILL_DIR}/scripts/conf/.encryption_key" ]; then
    echo "⚠️ COS 配置未完成或密钥文件缺失，请先运行: ${PYTHON} ${SKILL_DIR}/scripts/setup_config.py"
    exit 1
fi

# 调用 Python Skill 处理脚本，传入所有命令行参数
exec "${PYTHON}" "${SKILL_DIR}/scripts/skill_handler.py" "$@"
