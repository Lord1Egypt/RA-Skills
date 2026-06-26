#!/usr/bin/env bash
# 自开发Skills备份（每周执行）

set -euo pipefail

# 配置
BACKUP_ROOT="$HOME/.openclaw/backups"
YEAR="$(date +%Y)"
WEEK="w$(date +%V)"  # ISO周数
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP_DIR="$BACKUP_ROOT/weekly/skills"
BACKUP_FILE="$BACKUP_DIR/skills-custom_${YEAR}${WEEK}_$TIMESTAMP.tar.gz"
LOG_FILE="$HOME/.openclaw/workspace/memory/backup-log.md"

# 自开发Skills列表（需要备份的skills）
CUSTOM_SKILLS=(
    "arxiv-paper-collector"
    "backup-manager"
    "pdf-processor"
)

# 创建备份目录
mkdir -p "$BACKUP_DIR"

echo "🦞 开始自开发Skills备份..."

# 创建临时目录
TEMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TEMP_DIR"' EXIT

# 收集自开发Skills
echo "📦 收集自开发Skills..."
for skill in "${CUSTOM_SKILLS[@]}"; do
    SKILL_PATH="$HOME/.openclaw/workspace/skills/$skill"
    if [[ -d "$SKILL_PATH" ]]; then
        echo "  ✓ $skill"
        cp -r "$SKILL_PATH" "$TEMP_DIR/" 2>/dev/null || true
    else
        echo "  ⚠️  $skill (不存在，跳过)"
    fi
done

# 统计文件
FILE_COUNT=$(find "$TEMP_DIR" -type f | wc -l)
TOTAL_SIZE=$(du -sk "$TEMP_DIR" | cut -f1)
echo "  收集完成: $FILE_COUNT 个文件, ${TOTAL_SIZE}KB"

# 创建压缩备份
echo "🗜️ 创建压缩备份..."
cd "$(dirname "$TEMP_DIR")"
tar -czf "$BACKUP_FILE" -C "$(basename "$TEMP_DIR")" .

# 检查压缩包
if [[ -f "$BACKUP_FILE" ]]; then
    BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    echo "  ✅ Skills备份创建成功: $BACKUP_FILE ($BACKUP_SIZE)"
else
    echo "  ❌ Skills备份创建失败"
    exit 1
fi

# 创建软链接到最新Skills备份
echo "🔗 更新最新Skills备份链接..."
rm -f "$BACKUP_DIR/latest"
ln -sf "$BACKUP_FILE" "$BACKUP_DIR/latest"
echo "  ✅ 最新Skills备份链接: $BACKUP_DIR/latest -> $BACKUP_FILE"

# 记录备份日志
{
    echo "## 🎯 自开发Skills备份 - $(date '+%Y-%m-%d %H:%M:%S')"
    echo "- **备份文件**: $(basename "$BACKUP_FILE")"
    echo "- **备份路径**: $BACKUP_DIR"
    echo "- **压缩大小**: $BACKUP_SIZE"
    echo "- **包含Skills**: ${#CUSTOM_SKILLS[@]} 个"
    echo "- **文件数量**: $FILE_COUNT 个"
    echo "- **原始大小**: ${TOTAL_SIZE}KB"
    echo "- **压缩率**: $((100 - (${BACKUP_SIZE%?} * 1024 * 100 / TOTAL_SIZE)))%"
    echo "- **Skills列表**:"
    for skill in "${CUSTOM_SKILLS[@]}"; do
        echo "  - $skill"
    done
    echo ""
} >> "$LOG_FILE"

echo "✅ 自开发Skills备份完成: $BACKUP_FILE"
echo "💡 建议: Skills备份较小，建议每周执行一次"
