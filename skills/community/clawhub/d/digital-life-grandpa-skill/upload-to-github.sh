#!/bin/bash
# GitHub 上传脚本
# 使用方法：./upload-to-github.sh

echo "🚀 开始上传到 GitHub..."

# 配置
REPO_NAME="digital-life-grandpa-skill"
REPO_DESC="在数字世界，爷爷的爱一直都在 - 让每个人都能复刻自己的爷爷"
GITHUB_USER="xq2025ai"  # 替换为你的 GitHub 用户名

# 检查是否已安装 git
if ! command -v git &> /dev/null; then
    echo "❌ git 未安装，请先安装 git"
    exit 1
fi

# 进入 Skill 目录
cd "/root/.openclaw/workspace/skills/$REPO_NAME" || exit 1

# 初始化 git 仓库
echo "🔧 初始化 git 仓库..."
git init

# 添加所有文件
git add .

# 提交
git commit -m "🎉 digital-life-grandpa-skill V6.0 - 在数字世界，爷爷的爱一直都在"

# 创建 GitHub 仓库（需要 GitHub CLI 或手动创建）
echo "📝 创建 GitHub 仓库..."
echo ""
echo "请在 GitHub 上创建新仓库："
echo "  仓库名：$REPO_NAME"
echo "  描述：$REPO_DESC"
echo "  可见性：Public"
echo ""
echo "创建完成后，运行以下命令："
echo ""
echo "  git remote add origin https://github.com/$GITHUB_USER/$REPO_NAME.git"
echo "  git branch -M main"
echo "  git push -u origin main"
echo ""

# 或者使用 GitHub CLI（如果已安装）
if command -v gh &> /dev/null; then
    echo "检测到 GitHub CLI，自动创建仓库..."
    gh repo create "$GITHUB_USER/$REPO_NAME" --public --description "$REPO_DESC" --source "." --push
    echo "✅ 上传完成！"
    echo ""
    echo "🌐 访问：https://github.com/$GITHUB_USER/$REPO_NAME"
else
    echo "💡 提示：安装 GitHub CLI 可以自动上传"
    echo "   安装方法：https://cli.github.com/"
fi

echo ""
echo "🎉 完成！"
