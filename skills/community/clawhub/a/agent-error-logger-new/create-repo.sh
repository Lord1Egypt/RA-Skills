#!/bin/bash

# Agent Error Logger - GitHub 仓库创建脚本

set -e

REPO_NAME="agent-error-logger"
REPO_DESC="Agent 错误日志工具。记录、检索和分析 Agent 犯过的错误，避免重复踩坑。"

echo "🦞 创建 GitHub 仓库：$REPO_NAME"
echo ""

# 检查 gh 是否安装
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) 未安装"
    echo "请先安装：https://cli.github.com/"
    exit 1
fi

# 检查是否已认证
if ! gh auth status &> /dev/null; then
    echo "❌ 未认证 GitHub"
    echo "请先运行：gh auth login"
    exit 1
fi

# 创建仓库
echo "📦 创建 GitHub 仓库..."
gh repo create "$REPO_NAME" \
  --description "$REPO_DESC" \
  --public \
  --source=. \
  --remote=origin \
  --push

echo ""
echo "✅ 仓库创建成功！"
echo "🔗 访问：https://github.com/$(gh api user | jq -r '.login')/$REPO_NAME"
echo ""
echo "下一步："
echo "1. 更新 clawhub.json 中的 repository.url"
echo "2. 提交到 ClawHub: https://clawhub.com"
