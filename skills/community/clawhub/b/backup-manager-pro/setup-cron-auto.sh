#!/usr/bin/env bash
# 自动设置备份Cron任务（无需交互）

set -euo pipefail

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

BACKUP_MANAGER_DIR="$HOME/.openclaw/workspace/skills/backup-manager"
CRON_FILE="/tmp/openclaw-backup-cron-auto"

echo -e "${BLUE}🦞 自动设置备份Cron任务...${NC}"

# 检查备份管理器目录
if [[ ! -d "$BACKUP_MANAGER_DIR" ]]; then
    echo -e "${RED}❌ 备份管理器目录不存在: $BACKUP_MANAGER_DIR${NC}"
    exit 1
fi

# 检查脚本是否存在
REQUIRED_SCRIPTS=("backup-now.sh" "backup-full.sh" "backup-monthly.sh" "cleanup-expired.sh")
for script in "${REQUIRED_SCRIPTS[@]}"; do
    if [[ ! -f "$BACKUP_MANAGER_DIR/$script" ]]; then
        echo -e "${RED}❌ 缺少脚本: $script${NC}"
        exit 1
    fi
done

echo -e "${GREEN}✅ 备份脚本检查通过${NC}"

# 创建Cron配置
cat > "$CRON_FILE" << EOF
# ============================================
# OpenClaw 备份系统 - 自动调度任务
# 生成时间: $(date '+%Y-%m-%d %H:%M:%S')
# 备份管理器: $BACKUP_MANAGER_DIR
# ============================================

# 🕐 每日备份任务
# 每日凌晨2:00 - 配置备份（快速，保留7天）
0 2 * * * "$BACKUP_MANAGER_DIR/backup-now.sh" >> "$HOME/.openclaw/workspace/memory/backup-cron.log" 2>&1

# 🗓️ 每周备份任务  
# 每周一凌晨3:00 - 完整备份（较大，保留4周）
0 3 * * 1 "$BACKUP_MANAGER_DIR/backup-full.sh" >> "$HOME/.openclaw/workspace/memory/backup-cron.log" 2>&1

# 📅 月度备份任务
# 每月1日凌晨4:00 - 月度完整备份（保留12个月）
0 4 1 * * "$BACKUP_MANAGER_DIR/backup-monthly.sh" >> "$HOME/.openclaw/workspace/memory/backup-cron.log" 2>&1

# 🧹 清理任务
# 每周一凌晨5:00 - 清理过期备份
0 5 * * 1 "$BACKUP_MANAGER_DIR/cleanup-expired.sh" >> "$HOME/.openclaw/workspace/memory/backup-cron.log" 2>&1

# 🔍 健康检查
# 每天中午12:00 - 检查备份系统状态
0 12 * * * echo "[备份健康检查] \$(date)" >> "$HOME/.openclaw/workspace/memory/backup-cron.log"
EOF

echo -e "${BLUE}📋 Cron配置详情:${NC}"
echo "============================================"
echo -e "${YELLOW}📅 执行时间:${NC}"
echo -e "  • 每日配置备份: 02:00 (凌晨2点)"
echo -e "  • 每周完整备份: 03:00 每周一 (凌晨3点)"  
echo -e "  • 月度完整备份: 04:00 每月1日 (凌晨4点)"
echo -e "  • 清理过期备份: 05:00 每周一 (凌晨5点)"
echo -e "  • 健康检查: 12:00 (中午12点)"
echo ""
echo -e "${YELLOW}📝 日志文件: $HOME/.openclaw/workspace/memory/backup-cron.log${NC}"
echo "============================================"

# 备份现有crontab
EXISTING_CRON=$(crontab -l 2>/dev/null || true)
if [[ -n "$EXISTING_CRON" ]]; then
    BACKUP_FILE="$HOME/.openclaw/workspace/memory/crontab-backup-$(date +%Y%m%d_%H%M%S).txt"
    echo "$EXISTING_CRON" > "$BACKUP_FILE"
    echo -e "${GREEN}📦 已备份现有crontab到: $BACKUP_FILE${NC}"
fi

# 合并现有cron和新cron（避免重复）
{
    # 先输出现有cron（排除OpenClaw备份相关行）
    if [[ -n "$EXISTING_CRON" ]]; then
        echo "$EXISTING_CRON" | grep -v "OpenClaw 备份系统" | grep -v "backup-now.sh" | grep -v "backup-full.sh" | grep -v "backup-monthly.sh" | grep -v "cleanup-expired.sh"
    fi
    # 添加新的备份cron
    cat "$CRON_FILE"
} | crontab -

# 验证cron设置
NEW_CRON=$(crontab -l 2>/dev/null || true)
if echo "$NEW_CRON" | grep -q "backup-now.sh"; then
    echo -e "${GREEN}✅ Cron任务添加成功！${NC}"
else
    echo -e "${RED}❌ Cron任务添加失败${NC}"
    exit 1
fi

# 创建日志文件
if [[ ! -f "$HOME/.openclaw/workspace/memory/backup-cron.log" ]]; then
    echo "# OpenClaw备份Cron日志" > "$HOME/.openclaw/workspace/memory/backup-cron.log"
    echo "# 开始时间: $(date '+%Y-%m-%d %H:%M:%S')" >> "$HOME/.openclaw/workspace/memory/backup-cron.log"
    echo "# ===========================================" >> "$HOME/.openclaw/workspace/memory/backup-cron.log"
    echo "" >> "$HOME/.openclaw/workspace/memory/backup-cron.log"
    echo -e "${GREEN}📝 已创建日志文件: $HOME/.openclaw/workspace/memory/backup-cron.log${NC}"
fi

# 显示当前cron状态
echo ""
echo -e "${BLUE}📊 当前Cron任务列表:${NC}"
echo "============================================"
crontab -l
echo "============================================"

# 立即测试一个备份任务
echo ""
echo -e "${BLUE}🧪 立即测试每日备份任务...${NC}"
"$BACKUP_MANAGER_DIR/backup-now.sh"
echo -e "${GREEN}✅ 测试完成${NC}"

echo ""
echo -e "${GREEN}🎉 Cron自动备份配置完成！${NC}"
echo ""
echo -e "${BLUE}📋 使用说明:${NC}"
echo "1. 查看Cron任务: crontab -l"
echo "2. 编辑Cron任务: crontab -e"
echo "3. 查看备份日志: tail -f ~/.openclaw/workspace/memory/backup-cron.log"
echo "4. 查看备份详情: tail -f ~/.openclaw/workspace/memory/backup-log.md"
echo "5. 手动运行备份: cd $BACKUP_MANAGER_DIR && ./backup-now.sh"
echo ""
echo -e "${YELLOW}⚠️  注意: Cron任务将在设定的时间自动执行${NC}"
echo -e "${YELLOW}💡 建议: 明天检查日志确认任务正常执行${NC}"

# 清理临时文件
rm -f "$CRON_FILE"