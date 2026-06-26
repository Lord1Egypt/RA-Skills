#!/bin/bash
# 完整系统诊断脚本
# 用法: full-diagnose.sh

set -e

# 设置终端变量
export TERM="${TERM:-xterm}"

# 不使用 clear，避免兼容性问题
echo ""

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

clear
echo -e "${CYAN}"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║         🔍 OpenClaw 配置诊断工具 v1.0                  ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# 系统信息
echo -e "${BLUE}📊 系统信息${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "主机名: $(hostname)"
echo "系统: $(cat /etc/os-release | grep PRETTY_NAME | cut -d= -f2)"
echo "内核: $(uname -r)"
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 硬件状态
echo -e "${BLUE}💻 硬件状态${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "CPU: $(nproc) 核"
echo "内存: $(free -h | awk '/^Mem:/ {print $3 "/" $2}')"
echo "磁盘: $(df -h / | awk 'NR==2 {print $3 "/" $2 " (" $5 " 已用)"}')"
echo ""

# OpenClaw 状态
echo -e "${BLUE}🤖 OpenClaw 状态${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Gateway 状态
if pgrep -f "openclaw gateway" >/dev/null; then
    echo -e "Gateway: ${GREEN}✓ 运行中${NC}"
else
    echo -e "Gateway: ${YELLOW}⚠ 未运行${NC}"
fi

# 检查配置文件
if [ -f "/root/.openclaw/openclaw.json" ]; then
    echo -e "配置文件: ${GREEN}✓ 存在${NC}"
else
    echo -e "配置文件: ${RED}✗ 缺失${NC}"
fi

# 检查 workspace
if [ -d "/root/.openclaw/workspace" ]; then
    echo -e "Workspace: ${GREEN}✓ 存在${NC}"
else
    echo -e "Workspace: ${RED}✗ 缺失${NC}"
fi

echo ""

# 环境变量检查
echo -e "${BLUE}🔐 环境变量检查${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

check_env() {
    local name=$1
    if [ -n "${!name}" ]; then
        echo -e "$name: ${GREEN}✓ 已设置${NC}"
    else
        echo -e "$name: ${YELLOW}− 未设置${NC}"
    fi
}

check_env "OPENAI_API_KEY"
check_env "ANTHROPIC_API_KEY"
check_env "BAIDU_API_KEY"
check_env "EMAIL_ADDRESS"
check_env "EMAIL_PASSWORD"

echo ""

# 服务端口检查
echo -e "${BLUE}🌐 服务端口检查${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

check_port() {
    local port=$1
    local name=$2
    if lsof -i:$port >/dev/null 2>&1; then
        echo -e "$name ($port): ${GREEN}✓ 运行中${NC}"
    else
        echo -e "$name ($port): ${YELLOW}− 未启动${NC}"
    fi
}

check_port 3000 "前端服务"
check_port 3001 "后端服务"
check_port 8080 "Web 服务"
check_port 18789 "Gateway"

echo ""

# 网络连接检查
echo -e "${BLUE}🌍 网络连接检查${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

check_connection() {
    local host=$1
    local name=$2
    if ping -c 1 -W 2 $host >/dev/null 2>&1; then
        echo -e "$name: ${GREEN}✓ 可达${NC}"
    else
        echo -e "$name: ${YELLOW}⚠ 不可达${NC}"
    fi
}

check_connection "google.com" "外网"
check_connection "baidu.com" "国内网"

echo ""

# 技能状态
echo -e "${BLUE}🛠️ 技能状态${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

skill_count=$(ls -1 /root/.openclaw/workspace/skills 2>/dev/null | wc -l)
echo "已安装技能: $skill_count 个"

if [ $skill_count -gt 0 ]; then
    echo -e "\n最近更新的技能:"
    ls -lt /root/.openclaw/workspace/skills 2>/dev/null | head -6 | tail -5 | awk '{print "  " $9}'
fi

echo ""

# 记忆文件检查
echo -e "${BLUE}🧠 记忆系统检查${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -f "/root/.openclaw/workspace/MEMORY.md" ]; then
    size=$(wc -c < /root/.openclaw/workspace/MEMORY.md)
    echo -e "MEMORY.md: ${GREEN}✓ 存在 ($size bytes)${NC}"
else
    echo -e "MEMORY.md: ${YELLOW}⚠ 不存在${NC}"
fi

memory_count=$(ls -1 /root/.openclaw/workspace/memory/*.md 2>/dev/null | wc -l)
echo "记忆文件: $memory_count 个"

echo ""

# 问题汇总
echo -e "${BLUE}📋 诊断汇总${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

issues=0

# 检查关键问题
if [ ! -f "/root/.openclaw/openclaw.json" ]; then
    echo -e "${RED}✗ OpenClaw 配置文件缺失${NC}"
    ((issues++))
fi

if ! pgrep -f "openclaw gateway" >/dev/null; then
    echo -e "${YELLOW}⚠ Gateway 未运行${NC}"
fi

if [ $issues -eq 0 ]; then
    echo -e "${GREEN}✓ 系统状态良好${NC}"
else
    echo -e "${YELLOW}发现 $issues 个问题需要关注${NC}"
fi

echo ""
echo -e "${CYAN}诊断完成！$(date '+%Y-%m-%d %H:%M:%S')${NC}"
echo ""
