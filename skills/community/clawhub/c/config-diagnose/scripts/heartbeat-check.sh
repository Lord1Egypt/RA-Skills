#!/bin/bash
# 配置诊断 - Heartbeat 集成脚本
# 用于定时检查关键问题并主动提醒

SKILL_DIR="/root/.openclaw/workspace/skills/config-diagnose"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 问题收集
ISSUES=""
ISSUE_COUNT=0

# 检查函数
check_and_report() {
    local level=$1
    local name=$2
    local condition=$3
    local message=$4
    
    if eval "$condition"; then
        if [ "$level" = "critical" ]; then
            ISSUES="${ISSUES}🔴 ${name}: ${message}\n"
            ((ISSUE_COUNT++))
        elif [ "$level" = "warning" ]; then
            ISSUES="${ISSUES}🟡 ${name}: ${message}\n"
            ((ISSUE_COUNT++))
        fi
    fi
}

# ========== 关键检查 ==========

# 1. Gateway 服务
check_and_report "critical" "Gateway服务" \
    "! pgrep -f 'openclaw gateway' >/dev/null 2>&1" \
    "已停止运行"

# 2. 配置文件
check_and_report "critical" "配置文件" \
    "[ ! -f /root/.openclaw/openclaw.json ]" \
    "openclaw.json 丢失"

# 3. Workspace 目录
check_and_report "critical" "Workspace" \
    "[ ! -d /root/.openclaw/workspace ]" \
    "workspace 目录丢失"

# 4. 磁盘空间
DISK_USAGE=$(df / | awk 'NR==2 {print $5}' | tr -d '%')
if [ "$DISK_USAGE" -gt 90 ]; then
    ISSUES="${ISSUES}🔴 磁盘空间: 已使用 ${DISK_USAGE}%\n"
    ((ISSUE_COUNT++))
elif [ "$DISK_USAGE" -gt 80 ]; then
    ISSUES="${ISSUES}🟡 磁盘空间: 已使用 ${DISK_USAGE}%\n"
    ((ISSUE_COUNT++))
fi

# ========== 警告检查 ==========

# 5. 内存使用
MEM_USAGE=$(free | awk '/^Mem:/ {printf "%.0f", $3/$2 * 100}')
if [ "$MEM_USAGE" -gt 90 ]; then
    ISSUES="${ISSUES}🟡 内存使用: ${MEM_USAGE}%\n"
    ((ISSUE_COUNT++))
fi

# 6. 后端服务（如果项目存在）
if [ -d "/root/.openclaw/workspace/projects/china-travel-ai/backend" ]; then
    check_and_report "warning" "后端API" \
        "! lsof -i:3001 >/dev/null 2>&1" \
        "未运行 (端口 3001)"
fi

# ========== 输出结果 ==========

if [ $ISSUE_COUNT -gt 0 ]; then
    echo ""
    echo -e "${YELLOW}⚠️ 发现 $ISSUE_COUNT 个问题：${NC}"
    echo ""
    echo -e "$ISSUES"
    echo ""
    echo "建议运行完整诊断："
    echo "  bash $SKILL_DIR/scripts/full-diagnose.sh"
    echo ""
    # 返回非0表示有问题
    exit 1
else
    echo "✅ 系统状态正常"
    exit 0
fi
