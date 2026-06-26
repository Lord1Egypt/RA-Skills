#!/bin/bash
# notify.sh - 灵活的通知系统
# 支持 Telegram、Discord、Webhook 等

set -euo pipefail

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

print_msg() { echo -e "${1}${2}${NC}"; }

# ========== 配置 ==========

# 从环境变量读取配置
TELEGRAM_BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-}"
TELEGRAM_CHAT_ID="${TELEGRAM_CHAT_ID:-}"
TELEGRAM_TOPIC_ID="${TELEGRAM_TOPIC_ID:-}"  # Forum group topic ID
DISCORD_WEBHOOK="${DISCORD_WEBHOOK:-}"
WEBHOOK_URL="${WEBHOOK_URL:-}"
DEFAULT_CHANNEL="${DEFAULT_CHANNEL:-telegram}"

# ========== Telegram ==========

send_telegram() {
    local message="$1"
    local chat_id="${2:-$TELEGRAM_CHAT_ID}"
    local topic_id="${3:-$TELEGRAM_TOPIC_ID}"
    local parse_mode="${4:-Markdown}"
    
    if [[ -z "$TELEGRAM_BOT_TOKEN" || -z "$chat_id" ]]; then
        print_msg "$YELLOW" "⚠️ 未配置 Telegram"
        return 1
    fi
    
    # 构建请求
    local url="https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage"
    local data="chat_id=$chat_id&text=$message&parse_mode=$parse_mode"
    
    # 如果是 forum group 的 topic
    if [[ -n "$topic_id" ]]; then
        data="$data&message_thread_id=$topic_id"
    fi
    
    local response
    response=$(curl -s -X POST "$url" \
        -d "$data" 2>&1)
    
    if echo "$response" | jq -e '.ok' &>/dev/null; then
        print_msg "$GREEN" "✅ Telegram 发送成功"
        return 0
    else
        print_msg "$RED" "❌ Telegram 发送失败: $response"
        return 1
    fi
}

# ========== Discord ==========

send_discord() {
    local message="$1"
    local webhook="${2:-$DISCORD_WEBHOOK}"
    
    if [[ -z "$webhook" ]]; then
        print_msg "$YELLOW" "⚠️ 未配置 Discord"
        return 1
    fi
    
    local payload
    payload=$(cat <<EOF
{
    "content": "$message",
    "username": "Codex Tasks",
    "avatar_url": "https://i.imgur.com/AfFp7pu.png"
}
EOF
)
    
    local response
    response=$(curl -s -X POST "$webhook" \
        -H "Content-Type: application/json" \
        -d "$payload" 2>&1)
    
    if [[ "$response" == "null" || -z "$response" ]]; then
        print_msg "$GREEN" "✅ Discord 发送成功"
        return 0
    else
        print_msg "$RED" "❌ Discord 发送失败: $response"
        return 1
    fi
}

# ========== Webhook ==========

send_webhook() {
    local message="$1"
    local url="${2:-$WEBHOOK_URL}"
    
    if [[ -z "$url" ]]; then
        print_msg "$YELLOW" "⚠️ 未配置 Webhook"
        return 1
    fi
    
    local payload
    payload=$(cat <<EOF
{
    "text": "$message",
    "timestamp": "$(date -Iseconds)"
}
EOF
)
    
    local response
    response=$(curl -s -X POST "$url" \
        -H "Content-Type: application/json" \
        -d "$payload" 2>&1)
    
    print_msg "$GREEN" "✅ Webhook 发送成功"
}

# ========== 统一发送接口 ==========

send() {
    local channel="${1:-telegram}"
    local message="${2:-}"
    shift 2
    
    case "$channel" in
        telegram)
            send_telegram "$message" "$@"
            ;;
        discord)
            send_discord "$message" "$@"
            ;;
        webhook)
            send_webhook "$message" "$@"
            ;;
        all)
            # 发送到所有配置的平台
            send_telegram "$message" "$@"
            send_discord "$message" "$@"
            send_webhook "$message" "$@"
            ;;
        *)
            print_msg "$RED" "❌ 未知渠道: $channel"
            return 1
            ;;
    esac
}

# ========== 进度汇报 ==========

report_progress() {
    local task_id="$1"
    local progress="$2"      # 0-100
    local message="$3"
    local channel="${4:-$DEFAULT_CHANNEL}"
    
    # 进度条
    local bar_length=20
    local filled=$((progress * bar_length / 100))
    local empty=$((bar_length - filled))
    
    local bar="["
    for ((i=0; i<filled; i++)); do bar+="▓"; done
    for ((i=0; i<empty; i++)); do bar+="░"; done
    bar+="]"
    
    local status_msg="📊 进度: $progress% $bar\n📝 $message\n🆔 $task_id"
    
    send "$channel" "$status_msg"
}

report_start() {
    local task_id="$1"
    local task_name="$2"
    local channel="${3:-$DEFAULT_CHANNEL}"
    
    local message="🚀 任务开始

🆔 ID: $task_id
📋 名称: $task_name
⏰ 时间: $(date '+%H:%M:%S')"
    
    send "$channel" "$message"
}

report_complete() {
    local task_id="$1"
    local task_name="$2"
    local pr="${3:-无PR}"
    local outputs="${4:-}"
    local channel="${5:-$DEFAULT_CHANNEL}"
    
    local message="✅ 任务完成

🆔 ID: $task_id
📋 名称: $task_name
🔗 PR: #$pr
⏰ 完成时间: $(date '+%H:%M:%S')"
    
    if [[ -n "$outputs" ]]; then
        message+="\n\n$outputs"
    fi
    
    send "$channel" "$message"
}

report_error() {
    local task_id="$1"
    local task_name="$2"
    local error="$3"
    local channel="${4:-$DEFAULT_CHANNEL}"
    
    local message="❌ 任务失败

🆔 ID: $task_id
📋 名称: $task_name
💥 错误: $error
⏰ 时间: $(date '+%H:%M:%S')"
    
    send "$channel" "$message"
}

report_intervene() {
    local task_id="$1"
    local message="${2:-}"
    local channel="${3:-$DEFAULT_CHANNEL}"
    
    local msg="✏️ 人工干预

🆔 ID: $task_id
💬 消息: $message
⏰ 时间: $(date '+%H:%M:%S')"
    
    send "$channel" "$msg"
}

# ========== 实时进度条 ==========

# 用于在终端显示实时进度（不发送通知）
show_progress_bar() {
    local progress="$1"
    local message="${2:-}"
    
    local bar_length=30
    local filled=$((progress * bar_length / 100))
    local empty=$((bar_length - filled))
    
    local bar=""
    for ((i=0; i<filled; i++)); do bar+="▓"; done
    for ((i=0; i<empty; i++)); do bar+="░"; done
    
    printf "\r📊 [%s] %d%% - %s" "$bar" "$progress" "$message"
    
    if [[ $progress -eq 100 ]]; then
        echo ""
    fi
}

# ========== 帮助 ==========

help() {
    cat <<EOF
notify.sh - 灵活的通知系统

用法: notify.sh <command> [options]

环境变量:
  TELEGRAM_BOT_TOKEN   Telegram Bot Token
  TELEGRAM_CHAT_ID     Telegram Chat ID
  TELEGRAM_TOPIC_ID    Telegram Forum Topic ID
  DISCORD_WEBHOOK     Discord Webhook URL
  WEBHOOK_URL         通用 Webhook URL
  DEFAULT_CHANNEL     默认通知渠道

命令:
  send <channel> <message>
    发送消息 (channel: telegram/discord/webhook/all)
  
  progress <task_id> <progress> <message> [channel]
    汇报进度
  
  start <task_id> <name> [channel]
    汇报任务开始
  
  complete <task_id> <name> [pr] [channel]
    汇报任务完成
  
  error <task_id> <name> <error> [channel]
    汇报任务失败
  
  intervene <task_id> <message> [channel]
    汇报人工干预
  
  bar <progress> <message>
    终端进度条（不发送通知）

示例:
  # 配置
  export TELEGRAM_BOT_TOKEN="xxx"
  export TELEGRAM_CHAT_ID="xxx"
  export TELEGRAM_TOPIC_ID="xxx"  # 可选
  
  # 发送消息
  notify.sh send telegram "Hello"
  
  # 汇报进度
  notify.sh progress task-123 50 "正在开发..."
  
  # 任务开始
  notify.sh start task-123 "用户登录功能"
  
  # 任务完成
  notify.sh complete task-123 "用户登录功能" 341
EOF
}

# 主命令
main() {
    local command="${1:-}"
    shift || true
    
    case "$command" in
        send)
            send "$@"
            ;;
        progress)
            report_progress "$@"
            ;;
        start)
            report_start "$@"
            ;;
        complete)
            report_complete "$@"
            ;;
        error)
            report_error "$@"
            ;;
        intervene)
            report_intervene "$@"
            ;;
        bar)
            show_progress_bar "$@"
            ;;
        help|--help|-h|"")
            help
            ;;
        *)
            echo "未知命令: $command"
            help
            ;;
    esac
}

main "$@"
