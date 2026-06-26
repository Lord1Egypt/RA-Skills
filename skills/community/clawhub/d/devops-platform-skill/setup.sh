#!/bin/bash

# DevOps Platform Skill 安装脚本

set -e

echo "🔧 DevOps Platform Skill 安装脚本"
echo "=================================="

# 检查Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 未找到Node.js，请先安装Node.js"
    exit 1
fi

NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 14 ]; then
    echo "⚠️  Node.js版本过低 (需要14+，当前: $(node --version))"
    read -p "是否继续？[y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "✅ Node.js $(node --version)"

# 检查npm
if ! command -v npm &> /dev/null; then
    echo "❌ 未找到npm"
    exit 1
fi

echo "✅ npm $(npm --version)"

# 安装依赖
echo ""
echo "📦 安装依赖..."
npm install

if [ $? -eq 0 ]; then
    echo "✅ 依赖安装成功"
else
    echo "❌ 依赖安装失败"
    exit 1
fi

# 全局安装
echo ""
echo "🌍 全局安装CLI工具..."
npm install -g .

if [ $? -eq 0 ]; then
    echo "✅ 全局安装成功"
else
    echo "❌ 全局安装失败，尝试使用sudo？"
    read -p "使用sudo安装？[y/N] " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        sudo npm install -g .
        if [ $? -eq 0 ]; then
            echo "✅ sudo安装成功"
        else
            echo "❌ 安装失败"
            exit 1
        fi
    fi
fi

# 验证安装
echo ""
echo "🔍 验证安装..."
if command -v devops-platform &> /dev/null; then
    echo "✅ CLI工具已安装: $(which devops-platform)"
    
    echo ""
    echo "📋 显示帮助信息:"
    devops-platform --help
    
    echo ""
    echo "🎉 安装完成！"
    echo ""
    echo "下一步："
    echo "1. 配置API: devops-platform config"
    echo "2. 查看状态: devops-platform status"
    echo "3. 获取迭代列表: devops-platform iterations"
    echo "4. 获取应用列表: devops-platform apps"
else
    echo "❌ CLI工具未找到，请检查安装"
    exit 1
fi

# 作为OpenClaw skill安装的可选步骤
echo ""
read -p "是否安装为OpenClaw skill？[y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    OPENCLAW_SKILLS_DIR="/opt/homebrew/lib/node_modules/openclaw/skills"
    
    if [ -d "$OPENCLAW_SKILLS_DIR" ]; then
        echo "📁 复制到OpenClaw skills目录..."
        sudo cp -r "$(pwd)" "$OPENCLAW_SKILLS_DIR/devops-platform-skill"
        
        if [ $? -eq 0 ]; then
            echo "✅ 已安装为OpenClaw skill"
            echo "   位置: $OPENCLAW_SKILLS_DIR/devops-platform-skill"
        else
            echo "❌ 复制失败，可能需要sudo权限"
        fi
    else
        echo "⚠️  未找到OpenClaw skills目录: $OPENCLAW_SKILLS_DIR"
        echo "   请手动复制: sudo cp -r $(pwd) /path/to/openclaw/skills/"
    fi
fi

echo ""
echo "📚 文档："
echo "   - README.md: 基本使用"
echo "   - INSTALL.md: 安装指南"
echo "   - SKILL.md: OpenClaw skill文档"
echo "   - SUMMARY.md: 功能总结"
echo ""
echo "🚀 开始使用吧！"