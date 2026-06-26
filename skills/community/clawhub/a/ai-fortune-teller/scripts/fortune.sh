#!/bin/bash
# AI Fortune Teller - Core Script
# 使用 MiniMax API 进行八字、塔罗、运势分析

set -e

# 加载环境变量
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

if [ -f "$HOME/.clawd/.env" ]; then
    export $(grep -v '^#' "$HOME/.clawd/.env" | xargs)
fi

# 默认 API 配置
MINIMAX_API_HOST="${MINIMAX_API_HOST:-https://api.minimaxi.com}"
MINIMAX_API_KEY="${MINIMAX_API_KEY:-}"

# 帮助信息
show_help() {
    cat << EOF
AI Fortune Teller 🔮

用法: fortune.sh <命令> [参数]

命令:
    bazi <JSON格式用户信息>     八字命理分析
    tarot <问题> [牌阵]        塔罗占卜
    fortune <出生日期> [类型]  运势查询

示例:
    ./fortune.sh bazi '{"name":"张三","gender":"男","birthplace":"山东青岛","solar_date":"1995-07-15","hour":"10"}'
    ./fortune.sh tarot "我最近工作压力大，应该继续坚持还是跳槽？" "三张牌阵"
    ./fortune.sh fortune "1995-07-15" "今日"

EOF
}

# 调用 MiniMax API
call_minimax() {
    local system_prompt="$1"
    local user_message="$2"
    
    if [ -z "$MINIMAX_API_KEY" ]; then
        echo "错误: MINIMAX_API_KEY 未设置"
        return 1
    fi
    
    curl -s --max-time 60 \
        -H "Authorization: Bearer $MINIMAX_API_KEY" \
        -H "Content-Type: application/json" \
        -X POST "$MINIMAX_API_HOST/v1/text/chatcompletion_v2" \
        -d "{
            \"model\": \"MiniMax-Text-01\",
            \"messages\": [
                {\"role\": \"system\", \"content\": \"$system_prompt\"},
                {\"role\": \"user\", \"content\": \"$user_message\"}
            ],
            \"temperature\": 0.7,
            \"max_tokens\": 8192
        }" | jq -r '.choices[0].message.content' 2>/dev/null || echo "API调用失败"
}

# 八字分析
cmd_bazi() {
    local user_info="$1"
    
    # 读取系统提示词
    local system_prompt=$(cat "$SKILL_DIR/references/bazi-prompt.md")
    
    # 提取用户信息
    local name=$(echo "$user_info" | jq -r '.name // "用户"')
    local gender=$(echo "$user_info" | jq -r '.gender // "未指定"}')
    local birthplace=$(echo "$user_info" | jq -r '.birthplace // "未知"}')
    local solar_date=$(echo "$user_info" | jq -r '.solar_date // ""}')
    local hour=$(echo "$user_info" | jq -r '.hour // ""}')
    local year=$(echo "$user_info" | jq -r '.year // "2026"}')
    
    # 构建用户消息
    local user_message=$(cat << EOF
【个人信息】
姓名：$name
性别：$gender
出生地：$birthplace
公历出生日期：$solar_date
出生时间：${hour}时
当前年份：$year

请严格按照八字命理的逻辑进行分析，输出完整的命理报告。
EOF
)
    
    echo "🔮 正在分析八字命盘，请稍候..."
    call_minimax "$system_prompt" "$user_message"
}

# 塔罗占卜
cmd_tarot() {
    local question="$1"
    local cards_type="${2:-单张牌阵}"
    
    # 读取系统提示词
    local system_prompt=$(cat "$SKILL_DIR/references/tarot-prompt.md")
    
    local user_message="【塔罗占卜】
问题：$question
牌阵：$cards_type

请进行塔罗牌解读。"
    
    echo "🔮 正在解读塔罗牌，请稍候..."
    call_minimax "$system_prompt" "$user_message"
}

# 运势查询
cmd_fortune() {
    local birth_date="$1"
    local fortune_type="${2:-今日运势}"
    
    # 读取系统提示词
    local system_prompt=$(cat "$SKILL_DIR/references/daily-fortune-prompt.md")
    
    local user_message="【运势查询】
出生年月日：$birth_date
需要分析的类型：$fortune_type

请进行运势分析。"
    
    echo "🔮 正在分析运势，请稍候..."
    call_minimax "$system_prompt" "$user_message"
}

# 主逻辑
case "${1:-help}" in
    bazi)
        cmd_bazi "$2"
        ;;
    tarot)
        cmd_tarot "$2" "$3"
        ;;
    fortune)
        cmd_fortune "$2" "$3"
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac
