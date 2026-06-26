#!/bin/bash

# Agent P2P 启动脚本

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$SKILL_DIR"

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 安装依赖
echo "安装依赖..."
venv/bin/pip install -q -r requirements.txt

# 创建数据目录
mkdir -p data

# 启动服务
echo "启动 Agent P2P Portal..."
venv/bin/python src/main.py
