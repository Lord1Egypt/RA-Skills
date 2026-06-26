#!/bin/bash
# OpenClaw Cron Jobs 语法校验工具 (支持两种格式)
# 用途：在写入 jobs.json 之前验证语法是否正确
# 支持格式：
#   - 新格式: [{ ... }] (直接数组)
#   - 旧格式: { "jobs": [{ ... }] } (包含jobs字段的对象)

JOBS_FILE="${HOME}/.openclaw/cron/jobs.json"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "========================================"
echo "  OpenClaw Cron 语法校验工具 v3.0"
echo "========================================"
echo ""

# 参数检查
if [ $# -eq 0 ]; then
  echo "用法："
  echo "  $0 <json文件路径>                    # 校验指定文件"
  echo "  $0 --current                        # 校验当前的jobs.json"
  echo ""
  exit 1
fi

# 确定要校验的文件
if [ "$1" = "--current" ]; then
  if [ ! -f "$JOBS_FILE" ]; then
    echo -e "${RED}❌ 错误: 找不到配置文件 $JOBS_FILE${NC}"
    exit 1
  fi
  TARGET_FILE="$JOBS_FILE"
else
  if [ ! -f "$1" ]; then
    echo -e "${RED}❌ 错误: 找不到文件 $1${NC}"
    exit 1
  fi
  TARGET_FILE="$1"
fi

ERRORS=0
WARNINGS=0

# 检测格式
echo "📋 检测文件格式..."
echo "----------------------------------------"
FILE_TYPE=$(jq -r 'if type == "array" then "array" elif .jobs != null then "object" else "unknown" end' "$TARGET_FILE" 2>/dev/null)

if [ "$FILE_TYPE" = "array" ]; then
  echo -e "${GREEN}✅ 新格式: 直接数组 [...]{NC}"
  JOBS_QUERY="."
elif [ "$FILE_TYPE" = "object" ]; then
  echo -e "${GREEN}✅ 旧格式: 包含jobs字段的对象{NC}"
  JOBS_QUERY=".jobs"
else
  echo -e "${RED}❌ 错误: 无法识别文件格式${NC}"
  exit 1
fi
echo ""

# 检查1: 基础JSON语法
echo "📋 检查1: JSON基础语法"
echo "----------------------------------------"
if ! jq empty "$TARGET_FILE" 2>/dev/null; then
  echo -e "${RED}❌ JSON语法错误！${NC}"
  jq empty "$TARGET_FILE" 2>&1 | head -5
  exit 1
fi
echo -e "${GREEN}✅ JSON语法正确${NC}"
echo ""

# 检查2: 任务数量
echo "📋 检查2: 任务列表"
echo "----------------------------------------"
JOBS_COUNT=$(jq "$JOBS_QUERY | length" "$TARGET_FILE")
echo -e "${GREEN}✅ 包含 $JOBS_COUNT 个任务${NC}"
echo ""

# 检查3: 必填字段
echo "📋 检查3: 必填字段"
echo "----------------------------------------"

check_field() {
  local field=$1
  local count=$(jq "[$JOBS_QUERY[] | select(.${field} == null)] | length" "$TARGET_FILE" 2>/dev/null || echo "0")
  if [ "$count" -gt 0 ]; then
    echo -e "${YELLOW}⚠️  $count 个任务缺少 '${field}'${NC}"
    WARNINGS=$((WARNINGS + 1))
  fi
}

check_field "id"
check_field "name"
check_field "enabled"
check_field "schedule"
check_field "payload"

if [ $WARNINGS -eq 0 ]; then
  echo -e "${GREEN}✅ 必填字段完整${NC}"
fi
echo ""

# 检查4: schedule 结构
echo "📋 检查4: schedule 结构"
echo "----------------------------------------"

INVALID_KIND=$(jq "[$JOBS_QUERY[] | select(.schedule.kind != \"at\" and .schedule.kind != \"every\" and .schedule.kind != \"cron\" and .schedule.kind != null)] | length" "$TARGET_FILE" 2>/dev/null || echo "0")
if [ "$INVALID_KIND" -gt 0 ]; then
  echo -e "${RED}❌ $INVALID_KIND 个任务的 schedule.kind 值无效${NC}"
  ERRORS=$((ERRORS + 1))
else
  echo -e "${GREEN}✅ schedule.kind 正确${NC}"
fi

MISSING_EXPR=$(jq "[$JOBS_QUERY[] | select(.schedule.kind == \"cron\" and (.schedule.expr == null or .schedule.expr == \"\"))] | length" "$TARGET_FILE" 2>/dev/null || echo "0")
if [ "$MISSING_EXPR" -gt 0 ]; then
  echo -e "${YELLOW}⚠️  $MISSING_EXPR 个cron任务缺少 expr${NC}"
  WARNINGS=$((WARNINGS + 1))
fi
echo ""

# 检查5: payload 结构
echo "📋 检查5: payload 结构"
echo "----------------------------------------"

INVALID_KIND=$(jq "[$JOBS_QUERY[] | select(.payload.kind != \"systemEvent\" and .payload.kind != \"agentTurn\" and .payload.kind != null)] | length" "$TARGET_FILE" 2>/dev/null || echo "0")
if [ "$INVALID_KIND" -gt 0 ]; then
  echo -e "${RED}❌ $INVALID_KIND 个任务的 payload.kind 值无效${NC}"
  ERRORS=$((ERRORS + 1))
else
  echo -e "${GREEN}✅ payload.kind 正确${NC}"
fi

MISSING_MSG=$(jq "[$JOBS_QUERY[] | select(.payload.kind == \"agentTurn\" and (.payload.message == null or .payload.message == \"\"))] | length" "$TARGET_FILE" 2>/dev/null || echo "0")
if [ "$MISSING_MSG" -gt 0 ]; then
  echo -e "${YELLOW}⚠️  $MISSING_MSG 个agentTurn任务缺少 message${NC}"
  WARNINGS=$((WARNINGS + 1))
fi
echo ""

# 检查6: delivery 结构（关键！）
echo "📋 检查6: delivery 结构 (关键)"
echo "----------------------------------------"

HAS_PEER=$(jq "[$JOBS_QUERY[] | select(.delivery.peer != null)] | length" "$TARGET_FILE" 2>/dev/null || echo "0")
if [ "$HAS_PEER" -gt 0 ]; then
  echo -e "${RED}❌ $HAS_PEER 个任务使用了废弃的 'delivery.peer' 对象${NC}"
  echo "   应该使用 'delivery.to' 字符串，格式: \"chat:oc_xxx\""
  ERRORS=$((ERRORS + 1))
else
  echo -e "${GREEN}✅ 没有使用废弃的 peer 对象${NC}"
fi

INVALID_MODE=$(jq "[$JOBS_QUERY[] | select(.delivery.mode != null and .delivery.mode != \"announce\" and .delivery.mode != \"webhook\" and .delivery.mode != \"none\")] | length" "$TARGET_FILE" 2>/dev/null || echo "0")
if [ "$INVALID_MODE" -gt 0 ]; then
  echo -e "${RED}❌ $INVALID_MODE 个任务的 delivery.mode 值无效${NC}"
  ERRORS=$((ERRORS + 1))
else
  echo -e "${GREEN}✅ delivery.mode 正确${NC}"
fi
echo ""

# 检查7: 其他常见问题
echo "📋 检查7: 其他常见问题"
echo "----------------------------------------"

INVALID_ENABLED=$(jq "[$JOBS_QUERY[] | select(.enabled != null and (.enabled | type) != \"boolean\")] | length" "$TARGET_FILE" 2>/dev/null || echo "0")
if [ "$INVALID_ENABLED" -gt 0 ]; then
  echo -e "${RED}❌ $INVALID_ENABLED 个任务的 enabled 不是布尔值${NC}"
  ERRORS=$((ERRORS + 1))
else
  echo -e "${GREEN}✅ enabled 字段正确${NC}"
fi

# 检查重复ID
DUPLICATE_IDS=$(jq "[$JOBS_QUERY[].id] | group_by(.) | map(select(length > 1)) | map(.[0]) | length" "$TARGET_FILE" 2>/dev/null || echo "0")
if [ "$DUPLICATE_IDS" -gt 0 ]; then
  echo -e "${RED}❌ 发现重复的任务ID${NC}"
  ERRORS=$((ERRORS + 1))
else
  echo -e "${GREEN}✅ 没有重复的任务ID${NC}"
fi
echo ""

# 总结
echo "========================================"
echo "  总结"
echo "========================================"
echo ""

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
  echo -e "${GREEN}✅ 完美！没有发现任何问题${NC}"
  echo ""
  echo "这个 jobs.json 文件符合 OpenClaw 官方规范。"
  exit 0
elif [ $ERRORS -eq 0 ]; then
  echo -e "${YELLOW}⚠️  发现 $WARNINGS 个警告（非致命）${NC}"
  echo ""
  echo "文件语法正确，但有一些需要注意的地方。"
  exit 0
else
  echo -e "${RED}❌ 发现 $ERRORS 个错误, $WARNINGS 个警告${NC}"
  echo ""
  echo "❌ 文件不符合规范，请修复错误后再使用。"
  exit 1
fi
