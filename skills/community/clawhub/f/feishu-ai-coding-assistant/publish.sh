#!/bin/bash

# 飞书 AI 编程助手 - 发布脚本
# 用法：./publish.sh

set -e

SKILL_NAME="feishu-ai-coding-assistant"
SKILL_DIR="/home/node/openclaw-skills/$SKILL_NAME"
CLAW_TOKEN="clh_wfoNYpWcWq0gNC7X0DfsbL2cW3Ayba7jxmGaNf_3IU0"
GITHUB_TOKEN="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"

echo "🚀 开始发布 Skill: $SKILL_NAME"
echo ""

# 步骤 1: 检查 Claw-CLI 是否安装
if ! command -v claw &> /dev/null; then
    echo "⚠️  Claw-CLI 未安装，请先安装:"
    echo "   npm install -g @openclaw/claw-cli"
    echo "   或从 https://clawhub.ai 下载安装"
    echo ""
    exit 1
fi

# 步骤 2: 登录 ClawHub
echo "🔐 登录 ClawHub..."
claw login --token $CLAW_TOKEN

# 步骤 3: 验证登录
echo "✅ 验证登录状态..."
claw whoami

# 步骤 4: 进入 Skill 目录
echo "📂 进入 Skill 目录：$SKILL_DIR"
cd $SKILL_DIR

# 步骤 5: 更新版本号（可选）
echo "📝 当前版本：$(cat skill.json | grep '"version"' | head -1)"

# 步骤 6: Git 推送
echo "📤 推送到 GitHub..."
git remote -v | grep origin || git remote add origin https://$GITHUB_TOKEN@github.com/openclaw-skills/$SKILL_NAME.git
git push -u origin main 2>/dev/null || echo "⚠️  GitHub 推送失败，请手动创建仓库后重试"

# 步骤 7: 发布到 ClawHub
echo "📦 发布到 ClawHub..."
claw skill publish

# 步骤 8: 验证发布
echo "✅ 验证发布..."
claw skill my

echo ""
echo "🎉 发布完成！"
echo ""
echo "📱 查看 Skill:"
echo "   https://clawhub.ai/skills/$SKILL_NAME"
echo ""
echo "🔧 安装命令:"
echo "   claw skill install $SKILL_NAME"
