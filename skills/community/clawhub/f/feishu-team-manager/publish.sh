#!/bin/bash
# 飞书团队管理器发布脚本
# 使用方法：./publish.sh YOUR_API_TOKEN

set -e

TOKEN="$1"
if [ -z "$TOKEN" ]; then
    echo "❌ 错误：请提供 ClawHub API Token"
    echo "使用方法：./publish.sh YOUR_API_TOKEN"
    echo ""
    echo "如何获取 Token："
    echo "1. 访问 https://clawhub.com"
    echo "2. 登录后进入 Settings → API Tokens"
    echo "3. 生成新令牌并复制"
    exit 1
fi

echo "🚀 开始发布飞书团队管理器 v2.4.0..."
echo ""

# 1. 登录
echo "步骤 1/3: 登录 ClawHub..."
clawhub login --token "$TOKEN"

# 2. 验证
echo "步骤 2/3: 验证登录状态..."
clawhub whoami

# 3. 发布
echo "步骤 3/3: 发布技能..."
clawhub publish . \
  --slug "feishu-team-manager" \
  --name "飞书团队管理器 (HR 大姐头)" \
  --version "2.4.0" \
  --changelog "v2.4: 安全增强: 用户确认提示、依赖检查、配置备份、SKILL.md 清理优化" \
  --description "自动化招聘新 Agent，配置独立飞书机器人并重构多账号路由" \
  --tags "feishu,lark,hr,recruitment,agent-management,team"

echo ""
echo "✅ 发布完成！"
echo "技能链接：https://clawhub.com/skills/feishu-team-manager"
echo ""
echo "📢 下一步："
echo "1. 替换 SKILL.md 中的赞赏码图片 URL"
echo "2. 在 OpenClaw Discord #skills-showcase 分享"
echo "3. 监控安装量和用户反馈"