#!/bin/bash
# OpenClaw Cron 批量修复脚本（安全版本）
# 用途：自动修复常见的cron配置错误

set -e

COLOR_RED='\033[0;31m'
COLOR_GREEN='\033[0;32m'
COLOR_YELLOW='\033[1;33m'
COLOR_BLUE='\033[0;34m'
COLOR_NC='\033[0m' # No Color

JOBS_FILE="${HOME}/.openclaw/cron/jobs.json"
BACKUP_FILE="${JOBS_FILE}.backup.$(date +%Y%m%d_%H%M%S)"
TEMP_FILE="/tmp/openclaw_cron_fixed_$$.json"

echo "========================================"
echo "  OpenClaw Cron 批量修复工具 v2.0 (安全版)"
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

# 使用工作副本
WORK_FILE="$TEMP_FILE"
cp "$JOBS_FILE" "$WORK_FILE"

# 修复1: peer对象 → to字符串
echo "========================================"
echo "  修复1: delivery.peer → delivery.to"
echo "========================================"
echo ""

HAS_PEER=$(cat "$WORK_FILE" | jq '[.jobs[] | select(.delivery.peer != null)] | length')
if [ "$HAS_PEER" -gt 0 ]; then
  echo -e "${COLOR_YELLOW}发现 $HAS_PEER 个任务使用了 peer 对象${COLOR_NC}"
  echo "修复中..."

  # 使用更安全的jq语法
  jq '( .jobs | map(
      if .delivery.peer != null then
        .delivery.to = ("chat:" + .delivery.peer.id) |
        del(.delivery.peer) |
        .
      else
        .
      end
    ) ) | {jobs: .}' "$WORK_FILE" > "$TEMP_FILE.tmp"

  # 验证修复结果
  if [ -s "$TEMP_FILE.tmp" ]; then
    mv "$TEMP_FILE.tmp" "$WORK_FILE"
    FIXED_PEER=$(cat "$WORK_FILE" | jq '[.jobs[] | select(.delivery.peer != null)] | length')

    if [ "$FIXED_PEER" -eq 0 ]; then
      FIX_PEER=$HAS_PEER
      echo -e "${COLOR_GREEN}✅ 成功修复 $FIX_PEER 个任务${COLOR_NC}"
    else
      echo -e "${COLOR_RED}❌ 修复失败，恢复备份${COLOR_NC}"
      cp "$BACKUP_FILE" "$JOBS_FILE"
      rm -f "$TEMP_FILE" "$TEMP_FILE.tmp"
      exit 1
    fi
  else
    echo -e "${COLOR_RED}❌ 修复失败（输出为空），恢复备份${COLOR_NC}"
    cp "$BACKUP_FILE" "$JOBS_FILE"
    rm -f "$TEMP_FILE" "$TEMP_FILE.tmp"
    exit 1
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

HAS_CRONEXPR=$(cat "$WORK_FILE" | jq '[.jobs[] | select(.schedule.cronExpression != null)] | length')
if [ "$HAS_CRONEXPR" -gt 0 ]; then
  echo -e "${COLOR_YELLOW}发现 $HAS_CRONEXPR 个任务使用了 cronExpression${COLOR_NC}"
  echo "修复中..."

  # 使用更安全的jq语法
  jq '( .jobs | map(
      if .schedule.cronExpression != null then
        .schedule.expr = .schedule.cronExpression |
        del(.schedule.cronExpression) |
        .
      else
        .
      end
    ) ) | {jobs: .}' "$WORK_FILE" > "$TEMP_FILE.tmp"

  # 验证修复结果
  if [ -s "$TEMP_FILE.tmp" ]; then
    mv "$TEMP_FILE.tmp" "$WORK_FILE"
    FIXED_EXPR=$(cat "$WORK_FILE" | jq '[.jobs[] | select(.schedule.cronExpression != null)] | length')

    if [ "$FIXED_EXPR" -eq 0 ]; then
      FIX_EXPR=$HAS_CRONEXPR
      echo -e "${COLOR_GREEN}✅ 成功修复 $FIX_EXPR 个任务${COLOR_NC}"
    else
      echo -e "${COLOR_RED}❌ 修复失败，恢复备份${COLOR_NC}"
      cp "$BACKUP_FILE" "$JOBS_FILE"
      rm -f "$TEMP_FILE" "$TEMP_FILE.tmp"
      exit 1
    fi
  else
    echo -e "${COLOR_RED}❌ 修复失败（输出为空），恢复备份${COLOR_NC}"
    cp "$BACKUP_FILE" "$JOBS_FILE"
    rm -f "$TEMP_FILE" "$TEMP_FILE.tmp"
    exit 1
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

HAS_NONE=$(cat "$WORK_FILE" | jq '[.jobs[] | select(.delivery.mode == "none")] | length')
if [ "$HAS_NONE" -gt 0 ]; then
  echo -e "${COLOR_YELLOW}发现 $HAS_NONE 个任务的 delivery.mode 为 none${COLOR_NC}"
  echo ""
  echo "这些任务不会发送消息到群组。"
  echo "是否将其修改为 announce？(y/n)"
  read -r answer

  if [ "$answer" = "y" ] || [ "$answer" = "Y" ]; then
    jq '( .jobs | map(
        if .delivery.mode == "none" then
          .delivery.mode = "announce" |
          .
        else
          .
        end
      ) ) | {jobs: .}' "$WORK_FILE" > "$TEMP_FILE.tmp"

    if [ -s "$TEMP_FILE.tmp" ]; then
      mv "$TEMP_FILE.tmp" "$WORK_FILE"
      FIX_MODE=$HAS_NONE
      echo -e "${COLOR_GREEN}✅ 已修复 $FIX_MODE 个任务${COLOR_NC}"
    else
      echo -e "${COLOR_YELLOW}⚠️  修复失败，跳过此项${COLOR_NC}"
      rm -f "$TEMP_FILE.tmp"
    fi
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
  # 所有修复都成功，写入最终文件
  cp "$WORK_FILE" "$JOBS_FILE"

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

# 清理临时文件
rm -f "$TEMP_FILE" "$TEMP_FILE.tmp"
