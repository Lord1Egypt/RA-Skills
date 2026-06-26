#!/bin/bash

# Dobby-harness 发布脚本
# 推送到 GitHub: https://github.com/Panb-KG/dobby-harness

set -e

echo "🧦 Dobby-harness 发布脚本"
echo "================================"
echo ""

# 检查是否在正确的目录
if [ ! -f "clawhub.json" ]; then
    echo "❌ 错误：请在 skills/dobby-harness 目录下运行此脚本"
    exit 1
fi

# 初始化 Git
echo "📦 初始化 Git..."
if [ ! -d ".git" ]; then
    git init
fi

# 添加所有文件
echo "📝 添加文件..."
git add .

# 提交
echo "💾 提交更改..."
git commit -m "Initial commit: Dobby-harness v1.0.0 🧦

Features:
- Multi-Agent Orchestration (5 patterns)
- Production Workflows (4 workflows)
- Self-Improvement System (WAL + Buffer)
- Complete Test Suite (23+ tests)
- Full Documentation (50KB+)

Author: Dobby 🧦
License: MIT" || echo "⚠️  没有更改需要提交"

# 设置分支名
git branch -M main

# 添加远程仓库
echo "🔗 添加远程仓库..."
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/Panb-KG/dobby-harness.git

# 推送
echo "🚀 推送到 GitHub..."
echo ""
echo "⚠️  需要 GitHub 个人访问令牌 (PAT)"
echo ""
echo "请按以下步骤操作："
echo "1. 访问 https://github.com/settings/tokens"
echo "2. 生成新令牌 (勾选 repo 权限)"
echo "3. 复制令牌"
echo ""
echo "然后运行："
echo "git push -u origin main"
echo ""
echo "或者使用 HTTPS 推送（输入用户名和令牌）："
read -p "现在推送？(y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git push -u origin main
    echo ""
    echo "✅ 推送成功！"
    echo ""
    echo "📢 下一步："
    echo "1. 访问 https://github.com/Panb-KG/dobby-harness 确认仓库"
    echo "2. 运行 'clawhub publish' 发布到 ClawHub"
else
    echo ""
    echo "⏭️  跳过推送，稍后手动运行：git push -u origin main"
fi

echo ""
echo "================================"
echo "🧦 Dobby 准备就绪！"
