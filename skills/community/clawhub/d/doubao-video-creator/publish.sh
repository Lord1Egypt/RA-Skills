#!/bin/bash
# 豆包视频创作助手 - 一键发布到 GitHub 脚本
# 使用方法：./publish.sh

set -e

echo "🎬 豆包视频创作助手 v2.1 - GitHub 发布脚本"
echo "=========================================="
echo ""

# 检查 Git 配置
echo "📋 检查 Git 配置..."
if ! git config --global user.name > /dev/null 2>&1; then
    echo "❌ 未配置 Git 用户名"
    read -p "请输入 Git 用户名：" git_user
    git config --global user.name "$git_user"
fi

if ! git config --global user.email > /dev/null 2>&1; then
    echo "❌ 未配置 Git 邮箱"
    read -p "请输入 Git 邮箱：" git_email
    git config --global user.email "$git_email"
fi
echo "✅ Git 配置完成"
echo ""

# 检查 GitHub CLI
if command -v gh &> /dev/null; then
    echo "✅ GitHub CLI 已安装"
    
    # 检查是否已登录
    if gh auth status &> /dev/null; then
        echo "✅ 已登录 GitHub"
    else
        echo "⚠️  未登录 GitHub，开始认证..."
        gh auth login
    fi
    
    # 创建仓库并推送
    echo ""
    echo "📤 创建 GitHub 仓库并推送..."
    read -p "请输入 GitHub 用户名（留空使用当前目录名）：" github_user
    if [ -z "$github_user" ]; then
        github_user=$(basename $(pwd))
    fi
    
    repo_name="doubao-video-creator"
    
    # 尝试创建仓库
    if gh repo create "$github_user/$repo_name" --public --source=. --remote=origin --push 2>&1; then
        echo ""
        echo "✅ 发布成功！"
        echo ""
        echo "📦 仓库地址："
        echo "   https://github.com/$github_user/$repo_name"
        echo ""
        echo "🎉 感谢使用豆包视频创作助手！"
    else
        echo ""
        echo "❌ 创建仓库失败，请手动创建"
        echo ""
        echo "📝 手动发布步骤："
        echo "   1. 访问 https://github.com/new"
        echo "   2. 仓库名：doubao-video-creator"
        echo "   3. 选择 Public"
        echo "   4. 点击 Create repository"
        echo "   5. 运行以下命令："
        echo ""
        echo "   git remote add origin https://github.com/$github_user/$repo_name.git"
        echo "   git push -u origin main"
    fi
else
    echo "❌ 未安装 GitHub CLI"
    echo ""
    echo "📝 请使用手动方式发布："
    echo ""
    echo "方法 1: 安装 GitHub CLI"
    echo "   1. 访问 https://cli.github.com/"
    echo "   2. 安装后运行：gh auth login"
    echo "   3. 然后重新运行此脚本"
    echo ""
    echo "方法 2: 手动创建仓库"
    echo "   1. 访问 https://github.com/new"
    echo "   2. 仓库名：doubao-video-creator"
    echo "   3. 选择 Public"
    echo "   4. 点击 Create repository"
    echo "   5. 运行以下命令："
    echo ""
    echo "   git remote add origin https://github.com/YOUR_USERNAME/doubao-video-creator.git"
    echo "   git push -u origin main"
fi

echo ""
echo "=========================================="
echo "发布脚本执行完成"
