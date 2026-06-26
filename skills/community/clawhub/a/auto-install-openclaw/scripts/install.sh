#!/bin/bash
# OpenClaw 全自动安装脚本
# 用法：./install.sh

set -e

echo "🦞 OpenClaw 全自动安装脚本"
echo "=========================="

# 检查 Node.js
echo "📦 检查 Node.js..."
if ! command -v node &> /dev/null; then
    echo "❌ 未找到 Node.js，请先安装 Node.js 18+"
    exit 1
fi
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js 版本过低 ($NODE_VERSION)，需要 18+"
    exit 1
fi
echo "✅ Node.js $(node -v)"

# 检查 pnpm
echo "📦 检查 pnpm..."
if ! command -v pnpm &> /dev/null; then
    echo "⚠️ 未找到 pnpm，正在安装..."
    npm install -g pnpm
fi
echo "✅ pnpm $(pnpm -v)"

# 检查 Python
echo "🐍 检查 Python..."
if ! command -v python3 &> /dev/null; then
    echo "⚠️ 未找到 Python3"
fi

# 安装 OpenClaw
echo "🦞 安装 OpenClaw..."
if command -v openclaw &> /dev/null; then
    CURRENT_VERSION=$(openclaw --version)
    echo "ℹ️  当前已安装 OpenClaw $CURRENT_VERSION"
    read -p "是否重新安装？(y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "✅ 跳过安装"
        exit 0
    fi
fi

pnpm add -g openclaw

# 验证安装
echo "✅ 验证安装..."
openclaw --version

# 初始化配置
echo "⚙️  初始化配置..."
if [ ! -d ~/.openclaw ]; then
    mkdir -p ~/.openclaw
fi

# 创建必要的目录
mkdir -p ~/.openclaw/logs
mkdir -p ~/.openclaw/plugins
mkdir -p ~/.openclaw/skills

echo "✅ OpenClaw 安装完成！"
echo ""
echo "下一步："
echo "1. 运行 'openclaw onboard' 完成向导设置"
echo "2. 运行 './scripts/configure-claude.sh' 配置 Claude API"
echo "3. 运行 './scripts/install-feishu.sh' 安装飞书插件"
