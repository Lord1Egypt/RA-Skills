#!/bin/bash
# DM 轮询脚本 - 状态变化时通过 message 工具直接通知用户
#
# 用法: dm-poll-once.sh <thread_id> <status_file> [max_timeout_minutes]
#
# 功能：
#   - 状态变化时调用 message 工具通知用户
#   - 用户直接收到结果，无需主代理介入
#
# 输出格式（单行，供 Exec completed 日志）：
#   DM_POLL_RESULT:<state>:<thread_id>

set -e

THREAD_ID="$1"
STATUS_FILE="$2"
MAX_TIMEOUT="${3:-60}"

if [ -z "$THREAD_ID" ] || [ -z "$STATUS_FILE" ]; then
    echo "DM_POLL_ERROR:参数错误"
    exit 3
fi

INTERVALS=(5 10 20 40 60)
interval_idx=0
total_seconds=0
max_seconds=$((MAX_TIMEOUT * 60))
last_state=""

write_status() {
    local state="$1"
    local prev_state="$2"
    local result="$3"
    mkdir -p "$(dirname "$STATUS_FILE")" 2>/dev/null || true
    echo "STATE=$state" > "$STATUS_FILE"
    echo "THREAD_ID=$THREAD_ID" >> "$STATUS_FILE"
    echo "PREV_STATE=$prev_state" >> "$STATUS_FILE"
    echo "TIMESTAMP=$(date -Iseconds)" >> "$STATUS_FILE"
    echo "$result" > "${STATUS_FILE}.json"
}

# 通知用户（通过 OpenClaw message 工具）
notify_user() {
    local state="$1"
    local thread_id="$2"
    local message="$3"
    
    # 构建通知内容
    local notification=""
    case "$state" in
        "completed")
            notification="✅ **DM 任务完成**\n\nthread_id: \`$thread_id\`\n\n$message"
            ;;
        "ask_human")
            notification="⏸️ **DM 需要您的回复**\n\n$message\n\n请回复后继续。"
            ;;
        "failed")
            notification="❌ **DM 任务失败**\n\nthread_id: \`$thread_id\`\n\n$message"
            ;;
        "async_tag_task")
            notification="⚠️ **DM 异步任务待确认**\n\n任务: $message\n\n请前往 DM 平台 GUI 确认。"
            ;;
    esac
    
    # 使用 message 工具发送通知
    if command -v message &> /dev/null; then
        message --action send --message "$notification" 2>/dev/null || true
    elif command -v sessions_send &> /dev/null; then
        sessions_send --sessionKey main --message "$notification" 2>/dev/null || true
    fi
}

# 提取结果摘要
extract_summary() {
    local result="$1"
    local state="$2"
    
    case "$state" in
        "completed")
            # 提取文件链接
            local file_url=$(echo "$result" | jq -r '.data.last_messages[-1].content' 2>/dev/null | jq -r '.artifact.attachments[0].data // empty' 2>/dev/null || echo "")
            local text=$(echo "$result" | jq -r '.data.last_messages[0].content' 2>/dev/null | jq -r '.content // empty' 2>/dev/null | head -c 300 || echo "")
            if [ -n "$file_url" ]; then
                echo "📄 文件: $file_url\n\n$text"
            else
                echo "$text"
            fi
            ;;
        "ask_human")
            echo "$result" | jq -r '.data.message_display_to_human // ""' 2>/dev/null || echo ""
            ;;
        "failed")
            echo "$result" | jq -r '.error.message // "任务失败"' 2>/dev/null || echo "任务失败"
            ;;
        "async_tag_task")
            echo "$result" | jq -r '.data.status_info.task_name // ""' 2>/dev/null || echo ""
            ;;
        *)
            echo ""
            ;;
    esac
}

while true; do
    if [ $total_seconds -ge $max_seconds ]; then
        write_status "timeout" "$last_state" ""
        echo "DM_POLL_RESULT:timeout:$THREAD_ID"
        exit 2
    fi
    
    result=$(dm-cli thread result --thread-id "$THREAD_ID" --json 2>&1) || {
        sleep 10
        total_seconds=$((total_seconds + 10))
        continue
    }
    
    state=$(echo "$result" | jq -r '.data.state // "unknown"' 2>/dev/null || echo "unknown")
    
    [ "$state" = "unknown" ] && { sleep 10; total_seconds=$((total_seconds + 10)); continue; }
    
    # 状态变化
    if [ -n "$last_state" ] && [ "$state" != "$last_state" ]; then
        write_status "$state" "$last_state" "$result"
        
        # 中间状态变化也通知用户
        case "$state" in
            "async_tag_task")
                local task_name=$(echo "$result" | jq -r '.data.status_info.task_name // ""' 2>/dev/null)
                notify_user "$state" "$THREAD_ID" "$task_name"
                echo "DM_POLL_RESULT:$state:$THREAD_ID"
                exit 0
                ;;
        esac
    fi
    
    # 终止状态
    case "$state" in
        "completed")
            write_status "completed" "$last_state" "$result"
            local summary=$(extract_summary "$result" "completed")
            notify_user "completed" "$THREAD_ID" "$summary"
            echo "DM_POLL_RESULT:completed:$THREAD_ID"
            exit 0
            ;;
        "ask_human")
            write_status "ask_human" "$last_state" "$result"
            local question=$(extract_summary "$result" "ask_human")
            notify_user "ask_human" "$THREAD_ID" "$question"
            echo "DM_POLL_RESULT:ask_human:$THREAD_ID"
            exit 0
            ;;
        "failed")
            write_status "failed" "$last_state" "$result"
            local error=$(extract_summary "$result" "failed")
            notify_user "failed" "$THREAD_ID" "$error"
            echo "DM_POLL_RESULT:failed:$THREAD_ID"
            exit 1
            ;;
    esac
    
    last_state="$state"
    sleep ${INTERVALS[$interval_idx]:-60}
    [ $interval_idx -lt 4 ] && interval_idx=$((interval_idx + 1))
    total_seconds=$((total_seconds + ${INTERVALS[$interval_idx]:-60}))
done