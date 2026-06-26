#!/usr/bin/env bash
# 完整工作空间备份（每周执行）

set -euo pipefail

# 配置
BACKUP_ROOT="$HOME/.openclaw/backups"
YEAR="$(date +%Y)"
WEEK="w$(date +%V)"  # ISO周数
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP_PATH="$BACKUP_ROOT/weekly/$YEAR/$WEEK"
BACKUP_FILE="$BACKUP_PATH/full_$TIMESTAMP.tar.gz"
LOG_FILE="$HOME/.openclaw/workspace/memory/backup-log.md"

# 创建备份目录
mkdir -p "$BACKUP_PATH"

echo "🦞 开始完整工作空间压缩备份..."

# 创建临时目录
TEMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TEMP_DIR"' EXIT

# 收集完整工作空间
echo "📦 收集完整工作空间..."
echo "  1. 复制工作空间目录..."
cp -r "$HOME/.openclaw/workspace" "$TEMP_DIR/" 2>/dev/null || true

echo "  2. 复制配置文件..."
cp "$HOME/.openclaw/openclaw.json" "$TEMP_DIR/" 2>/dev/null || true
cp -r "$HOME/.openclaw/agents" "$TEMP_DIR/" 2>/dev/null || true

# 排除不需要备份的大文件
echo "  3. 清理临时文件..."
find "$TEMP_DIR" -name "*.log" -type f -delete 2>/dev/null || true
find "$TEMP_DIR" -name "*.tmp" -type f -delete 2>/dev/null || true
find "$TEMP_DIR" -name "*.cache" -type f -delete 2>/dev/null || true

# 统计文件
FILE_COUNT=$(find "$TEMP_DIR" -type f | wc -l)
TOTAL_SIZE=$(du -sk "$TEMP_DIR" | cut -f1)
echo "  收集完成: $FILE_COUNT 个文件, ${TOTAL_SIZE}KB"

# 创建压缩备份
echo "🗜️ 创建完整压缩备份..."
cd "$(dirname "$TEMP_DIR")"
tar -czf "$BACKUP_FILE" -C "$(basename "$TEMP_DIR")" .

# 检查压缩包
if [[ -f "$BACKUP_FILE" ]]; then
    BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    echo "  ✅ 完整压缩备份创建成功: $BACKUP_FILE ($BACKUP_SIZE)"
else
    echo "  ❌ 完整压缩备份创建失败"
    exit 1
fi

# 创建软链接到最新完整备份
echo "🔗 更新最新完整备份链接..."
rm -f "$BACKUP_ROOT/weekly/latest"
ln -sf "$BACKUP_PATH" "$BACKUP_ROOT/weekly/latest"
echo "  ✅ 最新完整备份链接: $BACKUP_ROOT/weekly/latest -> $BACKUP_PATH"

# 记录备份日志
{
    echo "## 📦 每周完整备份 - $(date '+%Y-%m-%d %H:%M:%S')"
    echo "- **备份文件**: $(basename "$BACKUP_FILE")"
    echo "- **备份路径**: $BACKUP_PATH"
    echo "- **压缩大小**: $BACKUP_SIZE"
    echo "- **包含文件**: $FILE_COUNT 个"
    echo "- **原始大小**: ${TOTAL_SIZE}KB"
    echo "- **压缩率**: $((100 - (${BACKUP_SIZE%?} * 1024 * 100 / TOTAL_SIZE)))%"
    echo ""
} >> "$LOG_FILE"

echo "✅ 完整工作空间备份完成: $BACKUP_FILE"
echo "💡 建议: 完整备份较大，建议每周执行一次"