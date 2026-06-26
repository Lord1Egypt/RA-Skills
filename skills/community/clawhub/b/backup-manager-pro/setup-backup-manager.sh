#!/usr/bin/env bash
# 初始化备份管理器

set -euo pipefail

echo "🦞 初始化备份管理器..."

# 创建备份目录结构（时间分层）
mkdir -p "$HOME/.openclaw/backups"/{daily,weekly,monthly,critical}

# 创建当前年份和月份的目录结构（便于测试）
CURRENT_YEAR="$(date +%Y)"
CURRENT_MONTH="$(date +%m)"
CURRENT_DAY="$(date +%d)"
CURRENT_WEEK="w$(date +%V)"

mkdir -p "$HOME/.openclaw/backups/daily/$CURRENT_YEAR/$CURRENT_MONTH/$CURRENT_DAY"
mkdir -p "$HOME/.openclaw/backups/weekly/$CURRENT_YEAR/$CURRENT_WEEK"
mkdir -p "$HOME/.openclaw/backups/monthly/$CURRENT_YEAR/$CURRENT_MONTH"

# 设置目录权限
chmod 700 "$HOME/.openclaw/backups"
find "$HOME/.openclaw/backups" -type d -exec chmod 700 {} \;

# 创建备份日志文件
if [[ ! -f "$HOME/.openclaw/workspace/memory/backup-log.md" ]]; then
    echo "# 备份日志" > "$HOME/.openclaw/workspace/memory/backup-log.md"
    echo "" >> "$HOME/.openclaw/workspace/memory/backup-log.md"
    echo "## 初始化 - $(date '+%Y-%m-%d %H:%M:%S')" >> "$HOME/.openclaw/workspace/memory/backup-log.md"
    echo "- **备份根目录**: $HOME/.openclaw/backups" >> "$HOME/.openclaw/workspace/memory/backup-log.md"
    echo "- **目录结构**: 时间分层 (年/月/日)" >> "$HOME/.openclaw/workspace/memory/backup-log.md"
    echo "- **压缩格式**: .tar.gz" >> "$HOME/.openclaw/workspace/memory/backup-log.md"
    echo "- **保留策略**: 每日7天，每周4周，每月12个月" >> "$HOME/.openclaw/workspace/memory/backup-log.md"
    echo "" >> "$HOME/.openclaw/workspace/memory/backup-log.md"
fi

# 设置脚本权限
chmod +x "$(dirname "$0")"/*.sh

echo "✅ 备份管理器初始化完成"
echo ""
echo "📋 可用命令:"
echo "  ./backup-now.sh           # 每日配置备份"
echo "  ./backup-full.sh          # 每周完整备份"
echo "  ./backup-monthly.sh       # 月度完整备份"
echo "  ./backup-before-change.sh # 修改前关键备份"
echo "  ./cleanup-expired.sh      # 清理过期备份"
echo "  ./restore-from-backup.sh  # 从备份恢复"
echo "  ./setup-backup-manager.sh # 初始化"
echo ""
echo "📁 目录结构:"
echo "  ~/.openclaw/backups/daily/YYYY/MM/DD/config_*.tar.gz"
echo "  ~/.openclaw/backups/weekly/YYYY/wW/full_*.tar.gz"
echo "  ~/.openclaw/backups/monthly/YYYY/MM/full_*.tar.gz"
echo "  ~/.openclaw/backups/critical/before-*.tar.gz"