#!/usr/bin/env bash
# Cron Auditor - 检查 cron job 质量
# 用法: bash audit-cron.sh

set -euo pipefail

G=$'\033[0;32m' Y=$'\033[1;33m' R=$'\033[0;31m' B=$'\033[1m' C=$'\033[0;36m' N=$'\033[0m'

echo -e "${B}⏰ Cron Job 审计${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 通过 openclaw cron list 获取
cron_output=$(openclaw cron list 2>/dev/null || echo "")

if [[ -z "$cron_output" ]] || echo "$cron_output" | grep -qi "no jobs\|empty"; then
    echo -e "${G}✓ 没有 cron job${NC}"
    exit 0
fi

echo "$cron_output"
echo ""

# 分析
echo -e "${B}分析:${NC}"
echo ""

issues=0

# 检查是否有高频任务
echo "$cron_output" | grep -iE "every.*min|every.*hour|cron.*\*/[0-9]" | while read -r line; do
    echo -e "  ${Y}⚠️  高频任务:${NC} $line"
    echo "     → 检查是否真的需要这么频繁"
    ((issues++))
done || true

# 检查重复任务
echo "$cron_output" | awk '{print $NF}' | sort | uniq -d | while read -r dup; do
    echo -e "  ${Y}⚠️  可能重复:${NC} $dup"
    ((issues++))
done || true

echo ""
echo -e "${B}优化建议:${NC}"
echo "  1. 删除不再需要的任务"
echo "  2. 降低频率（能每天一次的别每小时一次）"
echo "  3. 合并相似任务（比如检查邮件+检查日历可以合并到一个 job）"
echo "  4. 用 agentTurn 替代 systemEvent（更高效）"
echo ""
echo "管理命令:"
echo "  openclaw cron list          # 查看所有"
echo "  openclaw cron remove <id>   # 删除"
