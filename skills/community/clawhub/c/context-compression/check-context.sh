#!/bin/bash
# 检查 OpenClaw 会话上下文使用情况

set -e

# 颜色定义
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 默认值
OPENCLAW_DIR="${OPENCLAW_DIR:-$HOME/.openclaw}"
SESSIONS_DIR="$OPENCLAW_DIR/agents/main/sessions"

# 打印帮助
print_help() {
    echo "OpenClaw 上下文检查工具"
    echo ""
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -s, --session <id>  指定会话ID"
    echo "  -a, --all           显示所有会话"
    echo "  -j, --json          JSON 格式输出"
    echo "  -h, --help          显示帮助"
    echo ""
    echo "示例:"
    echo "  $0                  # 检查当前会话"
    echo "  $0 -a               # 显示所有会话"
    echo "  $0 -s <session-id>  # 检查指定会话"
}

# 解析参数
SESSION_ID=""
SHOW_ALL=false
JSON_OUTPUT=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -s|--session)
            SESSION_ID="$2"
            shift 2
            ;;
        -a|--all)
            SHOW_ALL=true
            shift
            ;;
        -j|--json)
            JSON_OUTPUT=true
            shift
            ;;
        -h|--help)
            print_help
            exit 0
            ;;
        *)
            echo "未知参数: $1"
            print_help
            exit 1
            ;;
    esac
done

# 检查 OpenClaw 是否运行
check_gateway() {
    if pgrep -f "openclaw-gateway" > /dev/null; then
        return 0
    else
        return 1
    fi
}

# 获取会话大小
get_session_size() {
    local session_file="$1"
    if [[ -f "$session_file" ]]; then
        wc -c < "$session_file"
    else
        echo "0"
    fi
}

# 估算 char 数（粗略：每4字符≈1unit）
estimate_units() {
    local size="$1"
    echo $((size / 4))
}

# 格式化输出
format_output() {
    local session_id="$1"
    local size="$2"
    local chars="$3"
    local config_limit="$4"
    
    if $JSON_OUTPUT; then
        echo "{\"session_id\":\"$session_id\",\"size_bytes\":$size,\"estimated_units\":$chars,\"limit\":$config_limit}"
    else
        local percent=0
        if [[ $config_limit -gt 0 ]]; then
            percent=$((chars * 100 / config_limit))
        fi
        
        local status_icon
        local status_color
        if [[ $percent -lt 50 ]]; then
            status_icon="✅"
            status_color="$GREEN"
        elif [[ $percent -lt 80 ]]; then
            status_icon="⚠️"
            status_color="$YELLOW"
        else
            status_icon="🔴"
            status_color="$RED"
        fi
        
        echo -e "${status_color}${status_icon} Session: ${session_id}${NC}"
        echo "   Size: $(numfmt --to=iec $size)"
        echo "   Est. Chars: ${chars}"
        echo "   Usage: ${percent}%"
        echo ""
    fi
}

# 读取配置中的 char 限制
get_config_limit() {
    local config_file="$OPENCLAW_DIR/openclaw.json"
    if [[ -f "$config_file" ]]; then
        local limit=$(grep -o '"contextChars"[[:space:]]*:[[:space:]]*[0-9]*' "$config_file" | grep -o '[0-9]*$')
        if [[ -n "$limit" ]]; then
            echo "$limit"
            return
        fi
    fi
    echo "100000"  # 默认值
}

# 主逻辑
main() {
    echo -e "${BLUE}OpenClaw 上下文检查${NC}"
    echo ""
    
    # 检查 gateway
    if ! check_gateway; then
        echo -e "${YELLOW}⚠️ OpenClaw Gateway 未运行${NC}"
    fi
    
    # 获取配置限制
    local config_limit=$(get_config_limit)
    
    if ! $JSON_OUTPUT; then
        echo "Char 限制: ${config_limit}"
        echo ""
    fi
    
    # 检查会话目录
    if [[ ! -d "$SESSIONS_DIR" ]]; then
        echo -e "${RED}❌ 会话目录不存在: $SESSIONS_DIR${NC}"
        exit 1
    fi
    
    # 列出会话
    local sessions
    if [[ -n "$SESSION_ID" ]]; then
        sessions=$(find "$SESSIONS_DIR" -name "${SESSION_ID}.jsonl" 2>/dev/null)
    elif $SHOW_ALL; then
        sessions=$(find "$SESSIONS_DIR" -name "*.jsonl" -type f 2>/dev/null | sort -r | head -10)
    else
        sessions=$(find "$SESSIONS_DIR" -name "*.jsonl" -type f -mmin -60 2>/dev/null | head -5)
    fi
    
    if [[ -z "$sessions" ]]; then
        echo "没有找到会话文件"
        exit 0
    fi
    
    # 遍历会话
    for session_file in $sessions; do
        local session_name=$(basename "$session_file" .jsonl)
        local size=$(get_session_size "$session_file")
        local chars=$(estimate_units "$size")
        format_output "$session_name" "$size" "$chars" "$config_limit"
    done
    
    # 压缩建议
    if ! $JSON_OUTPUT; then
        echo -e "${BLUE}建议:${NC}"
        echo "  - 上下文 <50%: 正常"
        echo "  - 上下文 50-80%: 考虑压缩"
        echo "  - 上下文 >80%: 执行压缩"
        echo ""
        echo "压缩命令: /compact 或编辑 openclaw.json"
    fi
}

main
