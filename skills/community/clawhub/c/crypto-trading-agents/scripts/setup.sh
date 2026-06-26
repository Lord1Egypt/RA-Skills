#!/usr/bin/env bash
# ─────────────────────────────────────────────
# Crypto Trading Agents - 一键安装脚本
# 运行方式：bash setup.sh
# ─────────────────────────────────────────────

set -e

echo "🚀 Crypto Trading Agents 安装脚本"
echo "=================================="

# 检测 uv 是否安装
if ! command -v uv &> /dev/null; then
    echo "📦 安装 uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source "$HOME/.local/bin/env" 2>/dev/null || true
    export PATH="$HOME/.local/bin:$PATH"
fi

echo "✅ uv 已就绪: $(uv --version)"

# Python 版本检查
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "🐍 Python 版本: $PYTHON_VERSION"

# 创建虚拟环境
if [ ! -d ".venv" ]; then
    echo "📦 创建虚拟环境..."
    uv venv .venv --python 3.12
fi

echo "✅ 虚拟环境已创建"

# 激活虚拟环境
source .venv/bin/activate

# 安装核心依赖
echo "📦 安装 TradingAgents 核心依赖..."
pip install .

# 安装 CCXT（Binance 对接）
echo "📦 安装 CCXT..."
uv pip install ccxt

echo ""
echo "=================================="
echo "✅ 安装完成！"
echo ""
echo "下一步："
echo "1. 复制环境配置文件："
echo "   cp .env.example .env"
echo ""
echo "2. 编辑 .env，填入你的 API Key："
echo "   nano .env"
echo ""
echo "3. 开始分析："
echo "   python -m tradingagents.crypto_trading --symbol BTC/USDT --action analyze"
echo ""
echo "=================================="
