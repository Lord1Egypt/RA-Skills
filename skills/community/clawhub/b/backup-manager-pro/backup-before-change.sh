#!/usr/bin/env bash
# 重大修改前关键备份（压缩版）

set -euo pipefail

# 配置
BACKUP_ROOT="$HOME/.openclaw/backups"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
REASON="$1"
BACKUP_FILE="$BACKUP_ROOT/critical/before-$REASON-$TIMESTAMP.tar.gz"
LOG_FILE="$HOME/.openclaw/workspace/memory/backup-log.md"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${RED}⚠️ 创建重大修改前压缩备份: $REASON${NC}"

# 创建临时目录
TEMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TEMP_DIR"' EXIT

# 收集关键文件
echo -e "${BLUE}📦 收集关键文件...${NC}"

file_count=0

# OpenClaw配置
if [[ -f "$HOME/.openclaw/openclaw.json" ]]; then
    cp "$HOME/.openclaw/openclaw.json" "$TEMP_DIR/"
    echo -e "  ${GREEN}✅ openclaw.json${NC}"
    ((file_count++))
fi

if [[ -f "$HOME/.openclaw/agents/main/agent/models.json" ]]; then
    cp "$HOME/.openclaw/agents/main/agent/models.json" "$TEMP_DIR/"
    echo -e "  ${GREEN}✅ models.json${NC}"
    ((file_count++))
fi

if [[ -f "$HOME/.openclaw/agents/main/agent/agent.json" ]]; then
    cp "$HOME/.openclaw/agents/main/agent/agent.json" "$TEMP_DIR/"
    echo -e "  ${GREEN}✅ agent.json${NC}"
    ((file_count++))
fi

# API认证配置（最关键）
if [[ -f "$HOME/.openclaw/agents/main/agent/auth-profiles.json" ]]; then
    cp "$HOME/.openclaw/agents/main/agent/auth-profiles.json" "$TEMP_DIR/"
    echo -e "  ${GREEN}✅ auth-profiles.json (API密钥)${NC}"
    ((file_count++))
fi

# 身份文件（最重要的）
echo -e "${BLUE}🔐 收集身份文件...${NC}"

identity_files=(
    "MEMORY.md" "USER.md" "SOUL.md" "IDENTITY.md"
    "LAOCHEN_TODOLIST.md" "XIACHEN_TODOLIST.md"
)

for file in "${identity_files[@]}"; do
    if [[ -f "$HOME/.openclaw/workspace/$file" ]]; then
        cp "$HOME/.openclaw/workspace/$file" "$TEMP_DIR/"
        echo -e "  ${GREEN}✅ $file${NC}"
        ((file_count++))
    else
        echo -e "  ${YELLOW}⚠️  $file 不存在${NC}"
    fi
done

# 创建压缩备份
echo -e "${BLUE}🗜️ 创建关键压缩备份...${NC}"
cd "$(dirname "$TEMP_DIR")"
tar -czf "$BACKUP_FILE" -C "$(basename "$TEMP_DIR")" .

if [[ -f "$BACKUP_FILE" ]]; then
    BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    echo -e "  ${GREEN}✅ 关键备份创建成功: $(basename "$BACKUP_FILE") ($BACKUP_SIZE)${NC}"
    
    # 设置文件权限
    chmod 600 "$BACKUP_FILE"
    
    # 记录原因
    {
        echo ""
        echo "## ⚠️ 重大修改前备份 - $(date '+%Y-%m-%d %H:%M:%S')"
        echo "- **修改原因**: $REASON"
        echo "- **备份文件**: \`$(basename "$BACKUP_FILE")\`"
        echo "- **压缩大小**: $BACKUP_SIZE"
        echo "- **包含文件**: $file_count 个"
        echo "- **提醒**: 此备份为重大修改前创建，建议永久保留或手动清理"
        echo ""
    } >> "$LOG_FILE"
    
    echo -e "${GREEN}✅ 修改前备份完成${NC}"
    echo -e "  📦 文件: $BACKUP_FILE"
    echo -e "  📊 大小: $BACKUP_SIZE ($file_count 个文件)"
    echo -e "  📝 日志: $LOG_FILE"
    echo -e "  ⚠️  注意: 此备份包含关键身份文件，建议妥善保存"
else
    echo -e "${RED}❌ 关键备份创建失败${NC}"
    exit 1
fi