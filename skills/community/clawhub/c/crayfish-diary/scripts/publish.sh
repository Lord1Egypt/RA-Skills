#!/bin/bash
# 龙虾日记技能发布脚本

set -e

SKILL_DIR="/Users/italks/WorkBuddy/Claw/.codebuddy/skills/crayfish-diary"
REPO_URL="https://github.com/italks/crayfish-diary.git"

echo "🦐 龙虾日记技能发布脚本"
echo "========================"

# 检查是否在技能目录
if [ ! -d "$SKILL_DIR" ]; then
    echo "❌ 错误：技能目录不存在"
    exit 1
fi

cd "$SKILL_DIR"

# 检查是否已初始化 git
if [ ! -d ".git" ]; then
    echo "📦 初始化 Git 仓库..."
    git init
fi

# 添加所有文件
echo "📝 添加文件到暂存区..."
git add .

# 检查是否有更改
if git diff --staged --quiet; then
    echo "ℹ️  没有需要提交的更改"
else
    # 提交更改
    echo "💾 提交更改..."
    git commit -m "feat: 更新龙虾日记技能

- 修改作者为 italks
- 更新触发命令：帮我记一下/结束记录
- 添加每日摘要功能
- 添加中英文双语文档
- 添加 GitHub 仓库地址"
fi

# 检查远程仓库
if ! git remote | grep -q "origin"; then
    echo "🔗 添加远程仓库..."
    git remote add origin "$REPO_URL"
fi

# 推送到 GitHub
echo "🚀 推送到 GitHub..."
git branch -M main
git push -u origin main

echo "✅ 发布成功！"
echo "📍 仓库地址: $REPO_URL"
echo ""
echo "下一步："
echo "1. 访问 WorkBuddy 技能中心上传技能包"
echo "2. 或在 ClawHub 提交仓库地址"
