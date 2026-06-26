#!/bin/bash
# OpenClaw Cron 批量修复脚本
# 用途：自动修复常见的cron配置错误

set -e

COLOR_RED='\033[0;31m'
COLOR_GREEN='\033[0;32m'
COLOR_YELLOW='\033[1;33m'
COLOR_BLUE='\033[0;34m'
COLOR_NC='\033[0m' # No Color

JOBS_FILE="${HOME}/.openclaw/cron/jobs.json"
BACKUP_FILE="${JOBS_FILE}.backup.$(date +%Y%m%d_%H%M%S)"

echo "========================================"
echo "  OpenClaw Cron 批量修复工具 v1.0"
echo "========================================"
echo ""

# 检查文件是否存在
if [ ! -f "$JOBS_FILE" ]; then
  echo -e "${COLOR_RED}❌ 错误: 找不到配置文件 $JOBS_FILE${COLOR_NC}"
  exit 1
fi

# 备份
echo -e "${COLOR_BLUE}📦 创建备份: $BACKUP_FILE${COLOR_NC}"
cp "$JOBS_FILE" "$BACKUP_FILE"
echo -e "${COLOR_GREEN}✅ 备份完成${COLOR_NC}"
echo ""

# 修复计数
FIX_PEER=0
FIX_EXPR=0
FIX_MODE=0

# 修复1: peer对象 → to字符串
echo "========================================"
echo "  修复1: delivery.peer → delivery.to"
echo "========================================"
echo ""

HAS_PEER=$(cat "$JOBS_FILE" | jq '[.jobs[] | select(.delivery.peer != null)] | length')
if [ "$HAS_PEER" -gt 0 ]; then
  echo -e "${COLOR_YELLOW}发现 $HAS_PEER 个任务使用了 peer 对象${COLOR_NC}"
  echo "修复中..."
  
  jq '(.jobs[] | select(.delivery.peer != null)) |=
    .delivery.to = ("chat:" + .delivery.peer.id) |
    del(.delivery.peer)' "$JOBS_FILE" > /tmp/openclaw_cron_fixed.json
  
  # 验证修复结果
  FIXED_PEER=$(cat /tmp/openclaw_cron_fixed.json | jq '[.jobs[] | select(.delivery.peer != null)] | length')
  
  if [ "$FIXED_PEER" -eq 0 ]; then
    mv /tmp/openclaw_cron_fixed.json "$JOBS_FILE"
    FIX_PEER=$HAS_PEER
    echo -e "${COLOR_GREEN}✅ 成功修复 $FIX_PEER 个任务${COLOR_NC}"
  else
    echo -e "${COLOR_RED}❌ 修复失败，请手动检查${COLOR_NC}"
    rm /tmp/openclaw_cron_fixed.json
  fi
else
  echo -e "${COLOR_GREEN}✅ 无需修复${COLOR_NC}"
fi

echo ""

# 修复2: cronExpression → expr
echo "========================================"
echo "  修复2: cronExpression → expr"
echo "========================================"
echo ""

HAS_CRONEXPR=$(cat "$JOBS_FILE" | jq '[.jobs[] | select(.schedule.cronExpression != null)] | length')
if [ "$HAS_CRONEXPR" -gt 0 ]; then
  echo -e "${COLOR_YELLOW}发现 $HAS_CRONEXPR 个任务使用了 cronExpression${COLOR_NC}"
  echo "修复中..."
  
  jq '(.jobs[] | select(.schedule.cronExpression != null)) |=
    .schedule.expr = .schedule.cronExpression |
    del(.schedule.cronExpression)' "$JOBS_FILE" > /tmp/openclaw_cron_fixed2.json
  
  # 验证修复结果
  FIXED_EXPR=$(cat /tmp/openclaw_cron_fixed2.json | jq '[.jobs[] | select(.schedule.cronExpression != null)] | length')
  
  if [ "$FIXED_EXPR" -eq 0 ]; then
    mv /tmp/openclaw_cron_fixed2.json "$JOBS_FILE"
    FIX_EXPR=$HAS_CRONEXPR
    echo -e "${COLOR_GREEN}✅ 成功修复 $FIX_EXPR 个任务${COLOR_NC}"
  else
    echo -e "${COLOR_RED}❌ 修复失败，请手动检查${COLOR_NC}"
    rm /tmp/openclaw_cron_fixed2.json
  fi
else
  echo -e "${COLOR_GREEN}✅ 无需修复${COLOR_NC}"
fi

echo ""

# 修复3: delivery.mode none → announce（询问）
echo "========================================"
echo "  修复3: delivery.mode (可选)"
echo "========================================"
echo ""

HAS_NONE=$(cat "$JOBS_FILE" | jq '[.jobs[] | select(.delivery.mode == "none")] | length')
if [ "$HAS_NONE" -gt 0 ]; then
  echo -e "${COLOR_YELLOW}发现 $HAS_NONE 个任务的 delivery.mode 为 none${COLOR_NC}"
  echo ""
  echo "这些任务不会发送消息到群组。"
  echo "是否将其修改为 announce？(y/n)"
  read -r answer
  
  if [ "$answer" = "y" ] || [ "$answer" = "Y" ]; then
    jq '(.jobs[] | select(.delivery.mode == "none")) |=
      .delivery.mode = "announce"' "$JOBS_FILE" > /tmp/openclaw_cron_fixed3.json
    
    mv /tmp/openclaw_cron_fixed3.json "$JOBS_FILE"
    FIX_MODE=$HAS_NONE
    echo -e "${COLOR_GREEN}✅ 已修复 $FIX_MODE 个任务${COLOR_NC}"
  else
    echo "跳过此项修复"
  fi
else
  echo -e "${COLOR_GREEN}✅ 无需修复${COLOR_NC}"
fi

echo ""
echo "========================================"
echo "  修复总结"
echo "========================================"
echo ""

TOTAL_FIXES=$((FIX_PEER + FIX_EXPR + FIX_MODE))

if [ $TOTAL_FIXES -gt 0 ]; then
  echo -e "${COLOR_GREEN}✅ 总共修复了 $TOTAL_FIXES 个配置错误${COLOR_NC}"
  echo "  - delivery.peer → delivery.to: $FIX_PEER"
  echo "  - cronExpression → expr: $FIX_EXPR"
  echo "  - delivery.mode: $FIX_MODE"
  echo ""
  echo -e "${COLOR_YELLOW}⚠️  下一步：${COLOR_NC}"
  echo "1. 查看修复后的配置："
  echo "   cat ~/.openclaw/cron/jobs.json | jq '.jobs[] | {id, delivery, schedule}'"
  echo ""
  echo "2. 如果确认无误，重启Gateway："
  echo "   openclaw gateway restart"
  echo ""
  echo "3. 如果有问题，恢复备份："
  echo "   cp $BACKUP_FILE ~/.openclaw/cron/jobs.json"
else
  echo -e "${COLOR_GREEN}✅ 配置完美，无需修复！${COLOR_NC}"
fi

echo ""
echo "备份文件: $BACKUP_FILE"
echo "========================================"
