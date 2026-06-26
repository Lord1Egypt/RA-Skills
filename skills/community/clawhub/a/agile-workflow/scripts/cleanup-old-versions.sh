#!/bin/bash
# 工作流老版本清理脚本
# 生成时间：2026-03-15T13:55:00.376Z

set -e

WORKFLOW_DIR="/home/ubutu/.openclaw/workspace/skills/agile-workflow"
BACKUP_DIR="$WORKFLOW_DIR/backups/$(date +%Y%m%d_%H%M%S)"

echo "🔍 开始清理老版本文件..."
echo ""

# 创建备份目录
mkdir -p "$BACKUP_DIR"
echo "✅ 备份目录：$BACKUP_DIR"
echo ""

# 文件列表
FILES_TO_DELETE=(
  "core/agile-workflow-engine-v5.js"
  "core/agile-workflow-engine-v7.js"
  "core/concurrent-executor-v2.js"
  "core/health-check-v2.js"
  "core/stress-test.js"
  "core/test-framework.js"
)

# 删除文件
for file in "${FILES_TO_DELETE[@]}"; do
  src="$WORKFLOW_DIR/$file"
  if [ -f "$src" ]; then
    # 备份
    cp "$src" "$BACKUP_DIR/"
    echo "📦 已备份：$file"
    
    # 删除
    rm "$src"
    echo "❌ 已删除：$file"
  else
    echo "⚠️ 文件不存在：$file"
  fi
done

echo ""
echo "✅ 清理完成！"
echo "📦 备份位置：$BACKUP_DIR"
echo ""
echo "如需恢复，从备份目录复制文件回原位置即可。"
