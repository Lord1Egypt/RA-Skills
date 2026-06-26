# Backup Scripts Reference

## Core Backup Script

### `backup-now.sh` - 立即备份
```bash
#!/usr/bin/env bash
# 立即创建备份

set -euo pipefail

# 配置
BACKUP_ROOT="$HOME/.openclaw/backups"
YEAR="$(date +%Y)"
MONTH="$(date +%m)"
DAY="$(date +%d)"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP_PATH="$BACKUP_ROOT/daily/$YEAR/$MONTH/$DAY"
BACKUP_FILE="$BACKUP_PATH/config_$TIMESTAMP.tar.gz"
LOG_FILE="$HOME/.openclaw/workspace/memory/backup-log.md"

# 创建备份目录
mkdir -p "$BACKUP_PATH"

echo "🦞 开始压缩备份 OpenClaw 配置..."

# 创建临时目录
TEMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TEMP_DIR"' EXIT

# 收集要备份的文件到临时目录
collect_backup_files() {
    echo "📦 收集备份文件..."
    
    # OpenClaw配置
    cp "$HOME/.openclaw/openclaw.json" "$TEMP_DIR/" 2>/dev/null || true
    cp "$HOME/.openclaw/agents/main/agent/models.json" "$TEMP_DIR/" 2>/dev/null || true
    cp "$HOME/.openclaw/agents/main/agent/agent.json" "$TEMP_DIR/" 2>/dev/null || true
    
    # 工作空间重要文件
    cp "$HOME/.openclaw/workspace/MEMORY.md" "$TEMP_DIR/" 2>/dev/null || true
    cp "$HOME/.openclaw/workspace/USER.md" "$TEMP_DIR/" 2>/dev/null || true
    cp "$HOME/.openclaw/workspace/SOUL.md" "$TEMP_DIR/" 2>/dev/null || true
    cp "$HOME/.openclaw/workspace/IDENTITY.md" "$TEMP_DIR/" 2>/dev/null || true
    cp "$HOME/.openclaw/workspace/LAOCHEN_TODOLIST.md" "$TEMP_DIR/" 2>/dev/null || true
    cp "$HOME/.openclaw/workspace/XIACHEN_TODOLIST.md" "$TEMP_DIR/" 2>/dev/null || true
    cp "$HOME/.openclaw/workspace/OUR_TODOLIST.md" "$TEMP_DIR/" 2>/dev/null || true
    cp "$HOME/.openclaw/workspace/HEARTBEAT.md" "$TEMP_DIR/" 2>/dev/null || true
    cp "$HOME/.openclaw/workspace/TOOLS.md" "$TEMP_DIR/" 2>/dev/null || true
    
    # 统计文件
    FILE_COUNT=$(find "$TEMP_DIR" -type f | wc -l)
    TOTAL_SIZE=$(du -sk "$TEMP_DIR" | cut -f1)
    
    echo "  收集完成: $FILE_COUNT 个文件, ${TOTAL_SIZE}KB"
}

# 创建压缩备份
create_compressed_backup() {
    echo "🗜️ 创建压缩备份..."
    
    # 切换到临时目录上级，确保相对路径正确
    cd "$(dirname "$TEMP_DIR")"
    
    # 创建tar.gz压缩包
    tar -czf "$BACKUP_FILE" -C "$(basename "$TEMP_DIR")" .
    
    # 检查压缩包
    if [[ -f "$BACKUP_FILE" ]]; then
        BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
        echo "  ✅ 压缩备份创建成功: $BACKUP_FILE ($BACKUP_SIZE)"
    else
        echo "  ❌ 压缩备份创建失败"
        exit 1
    fi
}

# 创建软链接到最新备份
create_latest_link() {
    echo "🔗 更新最新备份链接..."
    
    # 删除旧的daily/latest软链接
    rm -f "$BACKUP_ROOT/daily/latest"
    
    # 创建新的软链接
    ln -sf "$BACKUP_PATH" "$BACKUP_ROOT/daily/latest"
    
    echo "  ✅ 最新备份链接: $BACKUP_ROOT/daily/latest -> $BACKUP_PATH"
}

# 执行备份流程
collect_backup_files
create_compressed_backup
create_latest_link

# 记录备份日志
{
    echo "## 📅 每日配置备份 - $(date '+%Y-%m-%d %H:%M:%S')"
    echo "- **备份文件**: $(basename "$BACKUP_FILE")"
    echo "- **备份路径**: $BACKUP_PATH"
    echo "- **压缩大小**: $BACKUP_SIZE"
    echo "- **包含文件**: $(find "$TEMP_DIR" -type f | wc -l) 个"
    echo ""
} >> "$LOG_FILE"

echo "✅ 压缩备份完成: $BACKUP_FILE"
```

## Weekly Skills Backup Script

### `backup-weekly-skills.sh` - 自开发Skills备份
```bash
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
```

## Cleanup Script

### `cleanup-expired.sh` - 清理过期备份
```bash
#!/usr/bin/env bash
# 清理过期备份

set -euo pipefail

BACKUP_ROOT="$HOME/.openclaw/backups"
LOG_FILE="$HOME/.openclaw/workspace/memory/backup-log.md"

echo "🧹 开始清理过期备份..."

# 清理超过7天的每日备份 (按时间分层结构)
echo "🧹 清理过期每日备份 (超过7天)..."
find "$BACKUP_ROOT/daily" -type f -name "*.tar.gz" -mtime +7 2>/dev/null | while read file; do
    echo "  删除: $file"
    rm -f "$file"
done

# 清理空目录
find "$BACKUP_ROOT/daily" -type d -empty 2>/dev/null | while read dir; do
    # 保留年份和月份目录，只删除空的日期目录
    if [[ "$dir" =~ /[0-9]{4}/[0-9]{2}/[0-9]{2}$ ]]; then
        echo "  删除空目录: $dir"
        rmdir "$dir" 2>/dev/null || true
    fi
done

# 清理超过4周的每周备份
echo "🧹 清理过期每周备份 (超过4周)..."
find "$BACKUP_ROOT/weekly" -type f -name "*.tar.gz" -mtime +28 2>/dev/null | while read file; do
    echo "  删除: $file"
    rm -f "$file"
done

# 清理超过12个月的每月备份
echo "🧹 清理过期每月备份 (超过12个月)..."
find "$BACKUP_ROOT/monthly" -type f -name "*.tar.gz" -mtime +365 2>/dev/null | while read file; do
    echo "  删除: $file"
    rm -f "$file"
done

# 记录清理日志
{
    echo "## 🧹 清理记录 - $(date '+%Y-%m-%d %H:%M:%S')"
    echo "- **清理类型**: 过期备份"
    echo "- **清理时间**: $(date)"
    echo ""
} >> "$LOG_FILE"

echo "✅ 清理完成"
```

## Pre-modification Backup

### `backup-before-change.sh` - 修改前备份
```bash
#!/usr/bin/env bash
# 重大修改前备份

set -euo pipefail

BACKUP_ROOT="$HOME/.openclaw/backups"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
REASON="$1"
BACKUP_FILE="$BACKUP_ROOT/critical/before-$REASON-$TIMESTAMP.tar.gz"
LOG_FILE="$HOME/.openclaw/workspace/memory/backup-log.md"

echo "⚠️ 创建重大修改前压缩备份: $REASON"

# 创建临时目录
TEMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TEMP_DIR"' EXIT

# 收集关键文件
echo "📦 收集关键文件..."
cp "$HOME/.openclaw/openclaw.json" "$TEMP_DIR/" 2>/dev/null || true
cp "$HOME/.openclaw/agents/main/agent/models.json" "$TEMP_DIR/" 2>/dev/null || true
cp "$HOME/.openclaw/agents/main/agent/agent.json" "$TEMP_DIR/" 2>/dev/null || true
cp "$HOME/.openclaw/workspace/MEMORY.md" "$TEMP_DIR/" 2>/dev/null || true
cp "$HOME/.openclaw/workspace/USER.md" "$TEMP_DIR/" 2>/dev/null || true
cp "$HOME/.openclaw/workspace/SOUL.md" "$TEMP_DIR/" 2>/dev/null || true
cp "$HOME/.openclaw/workspace/IDENTITY.md" "$TEMP_DIR/" 2>/dev/null || true

# 创建压缩备份
cd "$(dirname "$TEMP_DIR")"
tar -czf "$BACKUP_FILE" -C "$(basename "$TEMP_DIR")" .

if [[ -f "$BACKUP_FILE" ]]; then
    BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    echo "  ✅ 关键备份创建成功: $BACKUP_FILE ($BACKUP_SIZE)"
    
    # 记录原因
    {
        echo "## ⚠️ 重大修改前备份 - $(date '+%Y-%m-%d %H:%M:%S')"
        echo "- **修改原因**: $REASON"
        echo "- **备份文件**: $(basename "$BACKUP_FILE")"
        echo "- **压缩大小**: $BACKUP_SIZE"
        echo "- **提醒**: 此备份为重大修改前创建，建议永久保留或手动清理"
        echo ""
    } >> "$LOG_FILE"
    
    echo "✅ 修改前备份完成: $BACKUP_FILE"
else
    echo "❌ 关键备份创建失败"
    exit 1
fi
```

## Restoration Script

### `restore-from-backup.sh` - 从备份恢复
```bash
#!/usr/bin/env bash
# 从备份恢复

set -euo pipefail

BACKUP_FILE="$1"
LOG_FILE="$HOME/.openclaw/workspace/memory/backup-log.md"

if [[ ! -f "$BACKUP_FILE" ]]; then
    echo "❌ 备份文件不存在: $BACKUP_FILE"
    echo "💡 提示: 备份文件应该是 .tar.gz 格式"
    exit 1
fi

# 检查文件类型
if [[ ! "$BACKUP_FILE" =~ \.tar\.gz$ ]]; then
    echo "❌ 不支持的备份格式: $BACKUP_FILE"
    echo "💡 提示: 只支持 .tar.gz 格式的压缩备份"
    exit 1
fi

echo "🔄 从压缩备份恢复: $BACKUP_FILE"

# 先创建当前状态备份
echo "⚠️ 先创建当前状态备份..."
"$(dirname "$0")/backup-before-change.sh" "restore-from-$(basename "$BACKUP_FILE")"

# 创建临时解压目录
TEMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TEMP_DIR"' EXIT

echo "📦 解压备份文件..."
tar -xzf "$BACKUP_FILE" -C "$TEMP_DIR"

if [[ $? -ne 0 ]]; then
    echo "❌ 解压备份文件失败"
    exit 1
fi

echo "✅ 解压完成，开始恢复文件..."

# 恢复文件
restore_file() {
    local src="$1"
    local dest="$2"
    
    if [[ -f "$src" ]]; then
        # 确保目标目录存在
        mkdir -p "$(dirname "$dest")"
        cp "$src" "$dest"
        echo "  ✅ 恢复: $(basename "$src")"
    else
        echo "  ⚠️  源文件不存在: $(basename "$src")"
    fi
}

# 恢复OpenClaw配置
restore_file "$TEMP_DIR/openclaw.json" "$HOME/.openclaw/openclaw.json"
restore_file "$TEMP_DIR/models.json" "$HOME/.openclaw/agents/main/agent/models.json"
restore_file "$TEMP_DIR/agent.json" "$HOME/.openclaw/agents/main/agent/agent.json"

# 恢复工作空间文件
restore_file "$TEMP_DIR/MEMORY.md" "$HOME/.openclaw/workspace/MEMORY.md"
restore_file "$TEMP_DIR/USER.md" "$HOME/.openclaw/workspace/USER.md"
restore_file "$TEMP_DIR/SOUL.md" "$HOME/.openclaw/workspace/SOUL.md"
restore_file "$TEMP_DIR/IDENTITY.md" "$HOME/.openclaw/workspace/IDENTITY.md"
restore_file "$TEMP_DIR/LAOCHEN_TODOLIST.md" "$HOME/.openclaw/workspace/LAOCHEN_TODOLIST.md"
restore_file "$TEMP_DIR/XIACHEN_TODOLIST.md" "$HOME/.openclaw/workspace/XIACHEN_TODOLIST.md"
restore_file "$TEMP_DIR/OUR_TODOLIST.md" "$HOME/.openclaw/workspace/OUR_TODOLIST.md"
restore_file "$TEMP_DIR/HEARTBEAT.md" "$HOME/.openclaw/workspace/HEARTBEAT.md"
restore_file "$TEMP_DIR/TOOLS.md" "$HOME/.openclaw/workspace/TOOLS.md"

# 记录恢复日志
{
    echo "## 🔄 恢复记录 - $(date '+%Y-%m-%d %H:%M:%S')"
    echo "- **恢复来源**: $BACKUP_DIR"
    echo "- **恢复时间**: $(date)"
    echo "- **警告**: 恢复操作已覆盖当前文件"
    echo ""
} >> "$LOG_FILE"

echo "✅ 恢复完成，需要重启OpenClaw网关应用新配置"
```

## Setup Script

### `setup-backup-manager.sh` - 初始化备份管理器
```bash
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
```

## Usage Examples

### 日常使用
```bash
# 初始化备份管理器
./setup-backup-manager.sh

# 每日配置备份
./backup-now.sh

# 每周完整备份
./backup-full.sh

# 月度完整备份（每月1日自动执行）
./backup-monthly.sh

# 清理过期备份
./cleanup-expired.sh

# 重大修改前备份
./backup-before-change.sh "glm-config-change"

# 从备份恢复
./restore-from-backup.sh ~/.openclaw/backups/daily/2026/03/08/config_20260308_020000.tar.gz
```

### 计划任务（Cron）
```bash
# 每日凌晨2点配置备份
0 2 * * * /path/to/backup-manager/backup-now.sh

# 每周一凌晨3点完整备份
0 3 * * 1 /path/to/backup-manager/backup-full.sh

# 每月1日凌晨4点月度备份
0 4 1 * * /path/to/backup-manager/backup-monthly.sh

# 每周一凌晨5点清理过期备份
0 5 * * 1 /path/to/backup-manager/cleanup-expired.sh
```

### 集成到OpenClaw
```bash
# 在HEARTBEAT.md中添加备份检查
# 备份检查：每周运行一次备份和清理
```

## Security Notes

1. **权限管理**：备份目录权限700，防止未授权访问
2. **日志记录**：所有操作记录到备份日志
3. **确认机制**：高风险操作需要用户确认
4. **恢复保护**：恢复前自动创建当前状态备份
