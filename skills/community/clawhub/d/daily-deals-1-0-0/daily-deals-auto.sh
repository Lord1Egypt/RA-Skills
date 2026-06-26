#!/bin/bash
# 每日神价推送 - 自动化脚本
# 用法：./daily-deals-auto.sh

set -e

SKILL_DIR="$HOME/.openclaw/skills/daily-deals-1.0.0"
ASSETS_DIR="$SKILL_DIR/assets"
WORKSPACE="$HOME/.openclaw/workspace"

echo "🚀 每日神价推送 - 自动化流程"
echo ""

# 1. 抓取什么值得买
echo "📡 抓取什么值得买..."
# 这里需要通过 OpenClaw browser 工具抓取
# 手动步骤：
# browser(action="open", targetUrl="https://faxian.smzdm.com/h3s183t0f0c0p1/")
# browser(action="snapshot", refs="aria")
# 保存 snapshot 到 $ASSETS_DIR/smzdm-snapshot.txt

# 2. 抓取识货网
echo "📡 抓取识货网..."
# browser(action="open", targetUrl="https://www.shihuo.cn/")
# browser(action="snapshot", refs="aria")
# 保存 snapshot 到 $ASSETS_DIR/shihuo-snapshot.txt

# 3. 生成并推送
echo "📝 生成报告并推送..."
cd "$SKILL_DIR" && node scripts/daily-push.js

echo ""
echo "✅ 完成！"
