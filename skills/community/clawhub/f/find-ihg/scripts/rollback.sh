#!/bin/bash
# IHG技能回滚脚本
# 用法: ./rollback.sh [版本号]
#   v2.1 - 回滚到v2.1版本
#   v2.0 - 回滚到v2.0版本

set -e

VERSION=${1:-"v2.1"}
BACKUP_ROOT="/home/node/.openclaw/backups"
SKILLS_DIR="/home/node/.openclaw/skills/find-ihg"
SCRIPTS_DIR="/home/node/.openclaw/scripts/ihg-monitor-python"
BACKUP_DIR="$BACKUP_ROOT/find-ihg-$VERSION"

echo "🔄 开始回滚到 $VERSION 版本..."

# 检查备份是否存在
if [ ! -d "$BACKUP_DIR" ]; then
    echo "❌ 备份目录不存在: $BACKUP_DIR"
    exit 1
fi

echo "📦 备份目录内容:"
ls -la "$BACKUP_DIR"

# 询问确认
read -p "⚠️  确认要回滚到 $VERSION 版本吗？(y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ 用户取消回滚"
    exit 0
fi

# 执行回滚
echo "📤 回滚技能文件..."
cp -r "$BACKUP_DIR/skills/"* "$SKILLS_DIR/" 2>/dev/null || true

echo "📤 回滚脚本文件..."
cp -r "$BACKUP_DIR/scripts/"* "$SCRIPTS_DIR/" 2>/dev/null || true

echo "✅ 回滚完成！"
echo "📝 版本信息:"
echo "   - 技能目录: $SKILLS_DIR"
echo "   - 脚本目录: $SCRIPTS_DIR"
echo "   - 回滚版本: $VERSION"

# 验证回滚
echo "🔍 验证回滚..."
if [ -f "$SKILLS_DIR/skills.json" ]; then
    echo "✅ 技能配置已恢复"
else
    echo "❌ 技能配置恢复失败"
fi