#!/usr/bin/env bash
# 每日配置备份（压缩版）

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

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 创建备份目录
mkdir -p "$BACKUP_PATH"

echo -e "${BLUE}🦞 开始压缩备份 OpenClaw 配置...${NC}"

# 创建临时目录
TEMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TEMP_DIR"' EXIT

# 收集要备份的文件到临时目录
collect_backup_files() {
    echo -e "${BLUE}📦 收集备份文件...${NC}"
    
    local file_count=0
    
    # OpenClaw配置
    if [[ -f "$HOME/.openclaw/openclaw.json" ]]; then
        cp "$HOME/.openclaw/openclaw.json" "$TEMP_DIR/"
        echo -e "  ${GREEN}✅ openclaw.json${NC}"
        ((file_count++))
    else
        echo -e "  ${YELLOW}⚠️  openclaw.json 不存在${NC}"
    fi
    
    if [[ -f "$HOME/.openclaw/agents/main/agent/models.json" ]]; then
        cp "$HOME/.openclaw/agents/main/agent/models.json" "$TEMP_DIR/"
        echo -e "  ${GREEN}✅ models.json${NC}"
        ((file_count++))
    else
        echo -e "  ${YELLOW}⚠️  models.json 不存在${NC}"
    fi
    
    if [[ -f "$HOME/.openclaw/agents/main/agent/agent.json" ]]; then
        cp "$HOME/.openclaw/agents/main/agent/agent.json" "$TEMP_DIR/"
        echo -e "  ${GREEN}✅ agent.json${NC}"
        ((file_count++))
    else
        echo -e "  ${YELLOW}⚠️  agent.json 不存在${NC}"
    fi
    
    # 工作空间重要文件
    echo -e "${BLUE}📁 收集工作空间文件...${NC}"
    
    local workspace_files=(
        "MEMORY.md" "USER.md" "SOUL.md" "IDENTITY.md"
        "LAOCHEN_TODOLIST.md" "XIACHEN_TODOLIST.md" "OUR_TODOLIST.md"
        "HEARTBEAT.md" "TOOLS.md"
    )
    
    for file in "${workspace_files[@]}"; do
        if [[ -f "$HOME/.openclaw/workspace/$file" ]]; then
            cp "$HOME/.openclaw/workspace/$file" "$TEMP_DIR/"
            echo -e "  ${GREEN}✅ $file${NC}"
            ((file_count++))
        else
            echo -e "  ${YELLOW}⚠️  $file 不存在${NC}"
        fi
    done
    
    # 统计文件
    local total_size=$(du -sk "$TEMP_DIR" 2>/dev/null | cut -f1 || echo "0")
    
    echo -e "${GREEN}📊 收集完成: $file_count 个文件, ${total_size}KB${NC}"
    echo "$file_count" > "$TEMP_DIR/.file_count"
    echo "$total_size" > "$TEMP_DIR/.total_size"
}

# 创建压缩备份
create_compressed_backup() {
    echo -e "${BLUE}🗜️ 创建压缩备份...${NC}"
    
    # 切换到临时目录上级，确保相对路径正确
    cd "$(dirname "$TEMP_DIR")"
    
    # 创建tar.gz压缩包
    tar -czf "$BACKUP_FILE" -C "$(basename "$TEMP_DIR")" .
    
    # 检查压缩包
    if [[ -f "$BACKUP_FILE" ]]; then
        local backup_size=$(du -h "$BACKUP_FILE" | cut -f1)
        echo -e "  ${GREEN}✅ 压缩备份创建成功: $(basename "$BACKUP_FILE") ($backup_size)${NC}"
        echo "$backup_size" > "$TEMP_DIR/.backup_size"
    else
        echo -e "  ${RED}❌ 压缩备份创建失败${NC}"
        exit 1
    fi
}

# 创建软链接到最新备份
create_latest_link() {
    echo -e "${BLUE}🔗 更新最新备份链接...${NC}"
    
    # 删除旧的daily/latest软链接
    rm -f "$BACKUP_ROOT/daily/latest"
    
    # 创建新的软链接
    ln -sf "$BACKUP_PATH" "$BACKUP_ROOT/daily/latest"
    
    echo -e "  ${GREEN}✅ 最新备份链接: daily/latest -> $BACKUP_PATH${NC}"
}

# 执行备份流程
collect_backup_files
create_compressed_backup
create_latest_link

# 读取统计信息
FILE_COUNT=$(cat "$TEMP_DIR/.file_count" 2>/dev/null || echo "0")
TOTAL_SIZE=$(cat "$TEMP_DIR/.total_size" 2>/dev/null || echo "0")
BACKUP_SIZE=$(cat "$TEMP_DIR/.backup_size" 2>/dev/null || echo "0KB")

# 计算压缩率（如果可能）
COMPRESSION_RATIO="N/A"
if [[ "$TOTAL_SIZE" -gt 0 ]] && [[ "$BACKUP_SIZE" =~ [0-9]+[KMG]?B? ]]; then
    # 简化计算：假设备份大小显示为"12K"格式
    backup_size_num=$(echo "$BACKUP_SIZE" | sed 's/[^0-9]//g')
    if [[ -n "$backup_size_num" ]]; then
        ratio=$((100 - (backup_size_num * 1024 * 100 / TOTAL_SIZE)))
        if [[ $ratio -lt 0 ]]; then
            ratio=0
        fi
        COMPRESSION_RATIO="${ratio}%"
    fi
fi

# 记录备份日志
{
    echo ""
    echo "## 📅 每日配置备份 - $(date '+%Y-%m-%d %H:%M:%S')"
    echo "- **备份文件**: \`$(basename "$BACKUP_FILE")\`"
    echo "- **备份路径**: \`$BACKUP_PATH\`"
    echo "- **压缩大小**: $BACKUP_SIZE"
    echo "- **包含文件**: $FILE_COUNT 个"
    echo "- **原始大小**: ${TOTAL_SIZE}KB"
    echo "- **压缩率**: $COMPRESSION_RATIO"
    echo "- **类型**: 每日配置备份"
    echo "- **保留期限**: 7天"
    echo ""
} >> "$LOG_FILE"

echo -e "${GREEN}✅ 压缩备份完成${NC}"
echo -e "  📁 路径: $BACKUP_PATH"
echo -e "  📦 文件: $(basename "$BACKUP_FILE")"
echo -e "  📊 大小: $BACKUP_SIZE ($FILE_COUNT 个文件)"
echo -e "  📝 日志: $LOG_FILE"
echo -e "  🔗 最新: $BACKUP_ROOT/daily/latest"

# 设置备份文件权限
chmod 600 "$BACKUP_FILE"
echo -e "${BLUE}🔒 备份文件权限已设置${NC}"