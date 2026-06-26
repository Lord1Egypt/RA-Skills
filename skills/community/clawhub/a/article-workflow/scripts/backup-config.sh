#!/bin/bash
# 配置保护脚本 - 在修改 skill 前备份配置，修改后恢复

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SKILL_DIR/config.json"
CONFIG_BACKUP="$SKILL_DIR/.config.backup.json"
ENV_FILE="$SKILL_DIR/.env"
ENV_BACKUP="$SKILL_DIR/.env.backup"

echo "🔧 Article Workflow 配置保护脚本"
echo "================================"

# 检查是否需要备份
if [ -f "$CONFIG_FILE" ]; then
    echo "✅ 检测到现有配置文件"
    echo "   备份到：$CONFIG_BACKUP"
    cp "$CONFIG_FILE" "$CONFIG_BACKUP"
else
    echo "⚠️  未检测到配置文件"
fi

if [ -f "$ENV_FILE" ]; then
    echo "✅ 检测到环境变量文件"
    echo "   备份到：$ENV_BACKUP"
    cp "$ENV_FILE" "$ENV_BACKUP"
fi

echo ""
echo "📝 使用说明："
echo "1. 在修改 skill 前运行：./scripts/backup-config.sh"
echo "2. 修改完成后运行：./scripts/restore-config.sh"
echo ""
