#!/bin/bash

# Crypto Funding Monitor - 快速启动脚本

echo "🚀 Crypto Funding Monitor - Quick Start"
echo "========================================"
echo ""

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js first."
    exit 1
fi

echo "✅ Node.js version: $(node --version)"
echo ""

# 检查 npm
if ! command -v npm &> /dev/null; then
    echo "❌ npm not found. Please install npm first."
    exit 1
fi

echo "✅ npm version: $(npm --version)"
echo ""

# 安装依赖
echo "📦 Installing dependencies..."
npm install

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed"
echo ""

# 检查 .env 文件
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "📝 Please edit .env file with your configuration"
    echo ""
fi

# 显示配置提示
echo "📋 Configuration Checklist:"
echo "  - SkillPay API Key: ✅ (already configured)"
echo "  - Telegram Bot Token: ⚠️  (optional, edit .env)"
echo "  - Discord Webhook: ⚠️  (optional, edit .env)"
echo "  - Email SMTP: ⚠️  (optional, edit .env)"
echo ""

# 询问是否启动
read -p "🎯 Start the server now? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🚀 Starting server..."
    echo ""
    npm start
else
    echo ""
    echo "📚 Next steps:"
    echo "  1. Edit .env file: nano .env"
    echo "  2. Start server: npm start"
    echo "  3. Run tests: node test.js"
    echo "  4. Deploy to Clawhub: clawhub publish"
    echo ""
    echo "📖 Read USAGE.md for detailed instructions"
    echo ""
fi
