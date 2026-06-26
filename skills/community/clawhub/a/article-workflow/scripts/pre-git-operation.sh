#!/bin/bash
# Git 钩子脚本 - 在 git pull/checkout 前自动备份配置

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SKILL_DIR/config.json"
CONFIG_BACKUP="$SKILL_DIR/.config.backup.json"

# 检查是否是 article-workflow 目录
if [ ! -f "$SKILL_DIR/SKILL.md" ]; then
    echo "❌ 不在 article-workflow 目录"
    exit 1
fi

# 备份配置（如果存在）
if [ -f "$CONFIG_FILE" ]; then
    echo "🔧 检测到配置文件，自动备份..."
    cp "$CONFIG_FILE" "$CONFIG_BACKUP"
    echo "✅ 配置已备份到：$CONFIG_BACKUP"
else
    echo "ℹ️  无现有配置文件，跳过备份"
fi

echo ""
echo "✨ 现在可以安全执行 Git 操作"
echo "   操作完成后运行：./scripts/restore-config.sh"
echo ""
