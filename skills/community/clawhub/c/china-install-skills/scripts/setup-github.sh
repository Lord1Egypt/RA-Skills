#!/bin/bash
# GitHub 仓库设置脚本
# 用法：./setup-github.sh <GitHub 用户名>

set -e

GITHUB_USER="${1:-5145852587}"
REPO_NAME="china-install-skills"
REMOTE_URL="https://github.com/${GITHUB_USER}/${REPO_NAME}.git"

echo "🚀 设置 GitHub 仓库：${GITHUB_USER}/${REPO_NAME}"
echo ""

# 检查 gh CLI 是否安装
if ! command -v gh &> /dev/null; then
  echo "❌ GitHub CLI (gh) 未安装"
  echo "   安装：brew install gh"
  exit 1
fi

# 检查是否已登录 GitHub
if ! gh auth status &> /dev/null; then
  echo "🔐 需要登录 GitHub..."
  gh auth login
fi

# 检查远程仓库是否已存在
if gh repo view "${GITHUB_USER}/${REPO_NAME}" &> /dev/null; then
  echo "⚠️  仓库已存在：${GITHUB_USER}/${REPO_NAME}"
  read -p "是否继续？(y/N) " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
  fi
else
  echo "📦 创建 GitHub 仓库..."
  gh repo create "${GITHUB_USER}/${REPO_NAME}" --public
fi

# 添加远程仓库
if ! git remote get-url origin &> /dev/null; then
  echo "🔗 添加远程仓库..."
  git remote add origin "$REMOTE_URL"
else
  echo "🔗 更新远程仓库..."
  git remote set-url origin "$REMOTE_URL"
fi

# 重命名分支为 main
echo "🌿 重命名分支为 main..."
git branch -M main

# 推送代码
echo "📤 推送代码到 GitHub..."
git push -u origin main

# 提示配置 Secret
echo ""
echo "✅ 代码已推送到 GitHub！"
echo ""
echo "🔐 下一步：配置 ClawHub Token"
echo "   1. 获取 token: clawhub login"
echo "   2. 访问：https://github.com/${GITHUB_USER}/${REPO_NAME}/settings/secrets/actions"
echo "   3. 添加 Secret: CLAWHUB_TOKEN"
echo ""
echo "📦 发布第一个版本:"
echo "   git tag v1.0.0"
echo "   git push origin v1.0.0"
echo ""
echo "🔗 仓库地址：${REMOTE_URL}"
echo "🔗 Actions:   https://github.com/${GITHUB_USER}/${REPO_NAME}/actions"
