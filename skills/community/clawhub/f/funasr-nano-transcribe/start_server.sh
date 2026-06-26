#!/bin/bash
# 启动 Fun-ASR-Nano-2512 FastAPI 服务

# 获取脚本所在目录（即技能根目录）
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "$SKILL_DIR"

# 激活虚拟环境
source .venv/bin/activate

echo "🚀 启动 Fun-ASR-Nano-2512 API 服务..."
echo "📍 工作目录: $SKILL_DIR"
echo "🔗 服务地址: http://127.0.0.1:11890"
echo "🔒 安全: 只监听本地地址，不对外暴露"
echo ""

# 启动服务
python scripts/api_server.py
