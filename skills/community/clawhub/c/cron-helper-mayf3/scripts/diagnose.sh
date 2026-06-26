#!/bin/bash
# OpenClaw Cron 诊断工具
# 用途：快速诊断cron配置问题

set -e

COLOR_RED='\033[0;31m'
COLOR_GREEN='\033[0;32m'
COLOR_YELLOW='\033[1;33m'
COLOR_NC='\033[0m' # No Color

JOBS_FILE="${HOME}/.openclaw/cron/jobs.json"

echo "========================================"
echo "  OpenClaw Cron 诊断工具 v1.0"
echo "========================================"
echo ""

# 检查1: 文件是否存在
if [ ! -f "$JOBS_FILE" ]; then
  echo -e "${COLOR_RED}❌ 错误: 找不到配置文件 $JOBS_FILE${COLOR_NC}"
  exit 1
fi

echo -e "${COLOR_GREEN}✅ 找到配置文件${COLOR_NC}"
echo ""

# 检查2: 查找所有有问题的任务
echo "========================================"
echo "  扫描配置问题"
echo "========================================"
echo ""

PROBLEM_COUNT=0

# 检查是否有peer对象
HAS_PEER=$(cat "$JOBS_FILE" | jq '[.jobs[] | select(.delivery.peer != null)] | length')
if [ "$HAS_PEER" -gt 0 ]; then
  echo -e "${COLOR_RED}❌ 发现 $HAS_PEER 个任务使用了错误的 peer 对象${COLOR_NC}"
  cat "$JOBS_FILE" | jq -r '.jobs[] | select(.delivery.peer != null) | "  - \(.id): \(.name)"'
  PROBLEM_COUNT=$((PROBLEM_COUNT + HAS_PEER))
fi

# 检查cronExpression字段名
HAS_CRONEXPR=$(cat "$JOBS_FILE" | jq '[.jobs[] | select(.schedule.cronExpression != null)] | length')
if [ "$HAS_CRONEXPR" -gt 0 ]; then
  echo -e "${COLOR_RED}❌ 发现 $HAS_CRONEXPR 个任务使用了错误的字段名 cronExpression${COLOR_NC}"
  cat "$JOBS_FILE" | jq -r '.jobs[] | select(.schedule.cronExpression != null) | "  - \(.id): \(.name)"'
  PROBLEM_COUNT=$((PROBLEM_COUNT + HAS_CRONEXPR))
fi

# 检查delivery.mode
HAS_NONE=$(cat "$JOBS_FILE" | jq '[.jobs[] | select(.delivery.mode == "none")] | length')
if [ "$HAS_NONE" -gt 0 ]; then
  echo -e "${COLOR_YELLOW}⚠️  发现 $HAS_NONE 个任务的 delivery.mode 为 none（不会发送消息）${COLOR_NC}"
  cat "$JOBS_FILE" | jq -r '.jobs[] | select(.delivery.mode == "none") | "  - \(.id): \(.name)"'
fi

# 检查enabled状态
DISABLED_COUNT=$(cat "$JOBS_FILE" | jq '[.jobs[] | select(.enabled == false)] | length')
if [ "$DISABLED_COUNT" -gt 0 ]; then
  echo -e "${COLOR_YELLOW}⚠️  发现 $DISABLED_COUNT 个任务被禁用${COLOR_NC}"
  cat "$JOBS_FILE" | jq -r '.jobs[] | select(.enabled == false) | "  - \(.id): \(.name)"'
fi

echo ""
if [ $PROBLEM_COUNT -eq 0 ]; then
  echo -e "${COLOR_GREEN}✅ 未发现配置问题！${COLOR_NC}"
else
  echo -e "${COLOR_RED}❌ 发现 $PROBLEM_COUNT 个需要修复的配置${COLOR_NC}"
  echo ""
  echo "建议运行修复脚本："
  echo "  ~/.openclaw/skills/cron-helper/scripts/fix-all.sh"
fi

echo ""
echo "========================================"
echo "  任务执行状态"
echo "========================================"
echo ""

# 检查最近执行的任务
echo "最近执行的任务（前5个）："
echo ""

# 获取所有任务ID
JOB_IDS=$(cat "$JOBS_FILE" | jq -r '.jobs[].id' | head -5)

for job_id in $JOB_IDS; do
  echo "任务: $job_id"
  
  # 获取最近一次执行记录
  RUN_INFO=$(openclaw cron runs --id "$job_id" --limit 1 2>/dev/null | jq '.entries[0] // empty')
  
  if [ -n "$RUN_INFO" ] && [ "$RUN_INFO" != "null" ]; then
    STATUS=$(echo "$RUN_INFO" | jq -r '.status // "unknown"')
    DELIVERED=$(echo "$RUN_INFO" | jq -r '.delivered // false')
    DELIVERY_STATUS=$(echo "$RUN_INFO" | jq -r '.deliveryStatus // "unknown"')
    ERROR=$(echo "$RUN_INFO" | jq -r '.error // empty')
    
    if [ "$STATUS" = "ok" ] && [ "$DELIVERED" = "true" ]; then
      echo -e "  ${COLOR_GREEN}✅ 状态: $STATUS, 已发送${COLOR_NC}"
    else
      echo -e "  ${COLOR_RED}❌ 状态: $STATUS, 发送: $DELIVERED${COLOR_NC}"
      if [ -n "$ERROR" ]; then
        echo "  错误: $ERROR"
      fi
    fi
  else
    echo -e "  ${COLOR_YELLOW}⚠️  尚未执行${COLOR_NC}"
  fi
  
  echo ""
done

echo "========================================"
echo "  诊断完成"
echo "========================================"
