#!/bin/bash
# 配置恢复脚本 - 修改 skill 后恢复配置

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SKILL_DIR/../config.json"
CONFIG_BACKUP="$SKILL_DIR/../.config.backup.json"
ENV_FILE="$SKILL_DIR/../.env"
ENV_BACKUP="$SKILL_DIR/../.env.backup"

echo "🔄 Article Workflow 配置恢复脚本"
echo "================================"

# 恢复配置文件
if [ -f "$CONFIG_BACKUP" ]; then
    echo "✅ 恢复配置文件"
    cp "$CONFIG_BACKUP" "$CONFIG_FILE"
    echo "   从：$CONFIG_BACKUP"
    echo "   到：$CONFIG_FILE"
else
    echo "⚠️  未找到配置备份"
fi

# 恢复环境变量文件
if [ -f "$ENV_BACKUP" ]; then
    echo "✅ 恢复环境变量文件"
    cp "$ENV_BACKUP" "$ENV_FILE"
    echo "   从：$ENV_BACKUP"
    echo "   到：$ENV_FILE"
else
    echo "⚠️  未找到环境变量备份"
fi

echo ""
echo "✨ 配置恢复完成！"
echo ""
