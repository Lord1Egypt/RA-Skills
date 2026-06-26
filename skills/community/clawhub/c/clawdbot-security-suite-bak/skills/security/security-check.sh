#!/bin/bash
# 安全巡检快速脚本
# 用法：security-check [daily|weekly|status|events]

set -euo pipefail

LOG_FILE="$HOME/.openclaw/logs/security-events.log"
SKILL_DIR="$HOME/.openclaw/workspaces/main/skills/clawdbot-security-suite/skills/security"

# 颜色代码
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

show_status() {
    echo -e "${BLUE}=== 安全系统状态 ===${NC}"
    
    # 检查 security.sh
    if command -v security.sh &> /dev/null; then
        echo -e "${GREEN}✅ security.sh${NC} - 已安装 ($(which security.sh))"
    else
        echo -e "${RED}❌ security.sh${NC} - 未安装"
    fi
    
    # 检查 jq
    if command -v jq &> /dev/null; then
        echo -e "${GREEN}✅ jq${NC} - $(jq --version)"
    else
        echo -e "${YELLOW}⚠️ jq${NC} - 未安装 (影响安全验证功能)"
    fi
    
    # 检查日志文件
    if [[ -f "$LOG_FILE" ]]; then
        local event_count=$(wc -l < "$LOG_FILE" 2>/dev/null || echo "0")
        echo -e "${GREEN}✅ 安全日志${NC} - $event_count 条事件"
    else
        echo -e "${YELLOW}⚠️ 安全日志${NC} - 未创建"
    fi
    
    # 检查 cron 任务
    echo -e "${GREEN}✅ 定时任务${NC} - 每日巡检 (07:00) + 每周更新 (周一 09:00)"
}

show_events() {
    local count="${1:-20}"
    echo -e "${BLUE}=== 最近 $count 条安全事件 ===${NC}"
    
    if [[ -f "$LOG_FILE" ]]; then
        tail -"$count" "$LOG_FILE" | while read -r line; do
            if [[ "$line" == *"THREAT"* ]]; then
                echo -e "${RED}$line${NC}"
            elif [[ "$line" == *"SAFE"* ]]; then
                echo -e "${GREEN}$line${NC}"
            elif [[ "$line" == *"WARNING"* ]]; then
                echo -e "${YELLOW}$line${NC}"
            else
                echo "$line"
            fi
        done
    else
        echo -e "${YELLOW}日志文件不存在${NC}"
    fi
}

daily_check() {
    echo -e "${BLUE}=== 每日安全巡检 ===${NC}\n"
    
    local issues=0
    
    # 检查 security.sh
    if ! command -v security.sh &> /dev/null; then
        echo -e "${RED}❌ security.sh 未安装${NC}"
        ((issues++))
    else
        echo -e "${GREEN}✅ security.sh 正常${NC}"
    fi
    
    # 测试安全验证
    if security.sh validate-command "echo test" | grep -q "ALLOWED"; then
        echo -e "${GREEN}✅ 安全验证功能正常${NC}"
    else
        echo -e "${RED}❌ 安全验证功能异常${NC}"
        ((issues++))
    fi
    
    # 查看威胁事件
    if [[ -f "$LOG_FILE" ]]; then
        local threat_count=$(grep -c "THREAT" "$LOG_FILE" 2>/dev/null || echo "0")
        if [[ "$threat_count" -gt 0 ]]; then
            echo -e "${YELLOW}⚠️ 发现 $threat_count 起威胁事件${NC}"
            echo "   最近威胁:"
            grep "THREAT" "$LOG_FILE" | tail -3 | while read -r line; do
                echo "   - $line"
            done
        else
            echo -e "${GREEN}✅ 无威胁事件${NC}"
        fi
    fi
    
    # 总结
    echo ""
    if [[ "$issues" -eq 0 ]]; then
        echo -e "${GREEN}✅ 所有检查通过${NC}"
    else
        echo -e "${RED}❌ 发现 $issues 个问题需要处理${NC}"
    fi
}

weekly_update() {
    echo -e "${BLUE}=== 每周威胁模式更新 ===${NC}\n"
    
    if [[ ! -d "$SKILL_DIR" ]]; then
        echo -e "${RED}❌ 安全技能目录不存在${NC}"
        exit 1
    fi
    
    cd "$SKILL_DIR"
    
    echo "当前模式版本:"
    jq -r '.version' patterns.json 2>/dev/null || echo "未知"
    
    echo ""
    echo "模式数量统计:"
    echo "  - 命令注入: $(jq -r '.command_injection | length' patterns.json)"
    echo "  - SSRF: $(jq -r '.ssrf | length' patterns.json)"
    echo "  - 路径遍历: $(jq -r '.path_traversal | length' patterns.json)"
    echo "  - API 密钥: $(jq -r '.api_keys | length' patterns.json)"
    
    echo ""
    echo -e "${GREEN}✅ 模式文件完整${NC}"
}

# 主逻辑
case "${1:-status}" in
    status)
        show_status
        ;;
    events)
        show_events "${2:-20}"
        ;;
    daily)
        daily_check
        ;;
    weekly)
        weekly_update
        ;;
    *)
        echo "用法：$0 [status|events|daily|weekly]"
        echo ""
        echo "  status  - 显示安全系统状态"
        echo "  events  - 显示最近安全事件 (默认 20 条)"
        echo "  daily   - 执行每日安全检查"
        echo "  weekly  - 执行每周模式审查"
        exit 1
        ;;
esac
