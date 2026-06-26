#!/bin/bash

set -e

echo "🚀 开始安装飞书机器人配置助手..."
echo ""

cd ~/.openclaw/workspace-main/skills/

if [ -d "feishu-bot-config-helper" ]; then
  echo "⚠️  技能已安装，是否覆盖？(y/N)"
  read -n 1 -r
  echo ""
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 0
  fi
  rm -rf "feishu-bot-config-helper"
fi

echo "📦 克隆技能包..."
git clone https://github.com/jiebao360/feishu-bot-config-helper.git
cd feishu-bot-config-helper

echo "📦 安装依赖..."
npm install

chmod +x scripts/auto-configure-bot.js

echo ""
echo "✅ 安装完成！"
echo ""
echo "🚀 使用方式:"
echo "   在飞书对话中发送:"
echo "   配置飞书机器人：机器人名称"
echo "   飞书应用凭证："
echo "   App ID: cli_xxx"
echo "   App Secret: xxx"
echo ""
