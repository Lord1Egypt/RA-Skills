#!/bin/bash
# IHG技能备份脚本
# 用法: ./backup.sh [版本标签]

set -e

VERSION=${1:-"v2.2-$(date +%Y%m%d)"}
BACKUP_ROOT="/home/node/.openclaw/backups"
SKILLS_DIR="/home/node/.openclaw/skills/find-ihg"
SCRIPTS_DIR="/home/node/.openclaw/scripts/ihg-monitor-python"
BACKUP_DIR="$BACKUP_ROOT/find-ihg-$VERSION"

echo "💾 开始备份版本: $VERSION"

# 创建备份目录
mkdir -p "$BACKUP_DIR/skills"
mkdir -p "$BACKUP_DIR/scripts"

echo "📥 备份技能文件..."
cp -r "$SKILLS_DIR/"* "$BACKUP_DIR/skills/" 2>/dev/null || true

echo "📥 备份脚本文件..."
cp -r "$SCRIPTS_DIR/"* "$BACKUP_DIR/scripts/" 2>/dev/null || true

# 创建版本信息文件
cat > "$BACKUP_DIR/version.info" << EOF
version: $VERSION
backup_time: $(date +"%Y-%m-%d %H:%M:%S")
openclaw_version: $(openclaw --version 2>/dev/null || echo "unknown")
files:
  - skills: $(find "$BACKUP_DIR/skills" -type f | wc -l)
  - scripts: $(find "$BACKUP_DIR/scripts" -type f | wc -l)
description: IHG技能v2.2生产版本备份
EOF

echo "✅ 备份完成!"
echo "📊 备份统计:"
echo "   - 备份目录: $BACKUP_DIR"
echo "   - 技能文件: $(find "$BACKUP_DIR/skills" -type f | wc -l) 个"
echo "   - 脚本文件: $(find "$BACKUP_DIR/scripts" -type f | wc -l) 个"
echo "   - 总大小: $(du -sh "$BACKUP_DIR" | cut -f1)"

# 显示备份列表
echo "📋 可用备份:"
ls -la "$BACKUP_ROOT/" 2>/dev/null || echo "无备份"