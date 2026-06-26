#!/bin/bash
# 豆包视频创作助手 - 快速发布到 GitHub
# 使用方法：./quick_push_github.sh

set -e

echo "🎬 豆包视频创作助手 - GitHub 发布"
echo "=================================="
echo ""

cd /root/.openclaw/workspace/skills/doubao-video-creator

# 设置远程仓库
echo "📍 设置远程仓库..."
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/465367/doubao-video-creator.git
echo "✅ 远程仓库已设置"
echo ""

# 确保分支名为 main
echo "🔄 设置分支名..."
git branch -M main 2>/dev/null || true
echo "✅ 分支已设置为 main"
echo ""

# 推送代码
echo "📤 推送代码到 GitHub..."
echo "💡 提示：首次推送需要输入 GitHub 凭证"
echo "   用户名：465367@qq.com"
echo "   密码/令牌：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"
echo ""

# 使用 GIT_ASKPASS 自动提供凭证
export GIT_ASKPASS=/bin/echo
export GIT_USERNAME="465367@qq.com"
export GIT_PASSWORD="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"

git push -u origin main --force 2>&1 || {
    echo ""
    echo "⚠️  自动推送失败，请手动输入凭证"
    echo ""
    echo "📝 请运行以下命令："
    echo "   cd /root/.openclaw/workspace/skills/doubao-video-creator"
    echo "   git push -u origin main"
    echo ""
    echo "然后输入："
    echo "   Username: 465367@qq.com"
    echo "   Password: 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"
    exit 1
}

echo ""
echo "✅ 发布成功！"
echo ""
echo "📦 仓库地址："
echo "   https://github.com/465367/doubao-video-creator"
echo ""
echo "🎉 感谢使用豆包视频创作助手！"
