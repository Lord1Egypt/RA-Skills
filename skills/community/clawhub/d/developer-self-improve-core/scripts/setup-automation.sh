#!/bin/bash

# 自动化功能配置脚本
# 提供定时提醒配置说明

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_FILE="$SKILL_DIR/config/config.yaml"
DAILY_CHECK_SCRIPT="$SKILL_DIR/scripts/daily-check.sh"

echo "🔧 配置自动化功能..."
echo ""

# 1. 检查配置文件
if [ ! -f "$CONFIG_FILE" ]; then
    echo "⚠️  配置文件不存在：$CONFIG_FILE"
    exit 1
fi

# 2. 读取配置并提示修改
DINGTALK_TARGET=$(awk -F': ' '/^dingtalk_target:/{print $2}' "$CONFIG_FILE" | tr -d '"')
REMINDER_TIME=$(awk -F': ' '/^reminder_time:/{print $2}' "$CONFIG_FILE" | tr -d '"')

# 检查钉钉 ID 是否已配置
if [ -z "$DINGTALK_TARGET" ]; then
    echo "❌ dingtalk_target 为空"
    echo "   请修改 config/config.yaml"
    echo "   设置 dingtalk_target: \"你的钉钉 ID\""
    exit 1
fi

# 检查是否为占位符
if echo "$DINGTALK_TARGET" | grep -qiE "^YOUR_|^your_|^你的|^placeholder"; then
    echo "❌ dingtalk_target 为占位符，未配置实际值"
    echo "   当前值：$DINGTALK_TARGET"
    echo ""
    echo "   请修改 config/config.yaml"
    echo "   设置 dingtalk_target: \"你的钉钉 ID（18 位数字）\""
    exit 1
fi

# 3. 提供配置指导
echo "📋 配置定时任务："
echo ""
echo "1. 编辑 crontab："
echo "   crontab -e"
echo ""
echo "2. 添加以下行："
echo "   $REMINDER_TIME cd $SKILL_DIR && ./scripts/daily-check.sh"
echo ""
echo "3. 保存并退出"
echo ""
echo "✅ 配置完成！"
