#!/bin/bash
# DM 任务轮询脚本
# 用法: ./dm-poll.sh <thread_id> <status_file> [max_timeout_minutes]
# 
# 输出：
#   - 状态变化时写入 status_file
#   - 终止状态时退出并返回最终结果
#
# 状态文件格式：
#   STATE=<state>
#   THREAD_ID=<thread_id>
#   MESSAGE=<message_display_to_human 或 task_name>
#   RESULT_JSON=<完整的 result JSON>

set -e

THREAD_ID="$1"
STATUS_FILE="$2"
MAX_TIMEOUT="${3:-60}"  # 默认 60 分钟

if [ -z "$THREAD_ID" ] || [ -z "$STATUS_FILE" ]; then
    echo "用法: $0 <thread_id> <status_file> [max_timeout_minutes]"
    exit 1
fi

# 轮询间隔（秒）：递增策略
INTERVALS=(5 10 20 40 60)
interval_index=0
total_seconds=0
max_seconds=$((MAX_TIMEOUT * 60))

last_state=""

write_status() {
    local state="$1"
    local message="$2"
    local result_json="$3"
    
    cat > "$STATUS_FILE" << EOF
STATE=$state
THREAD_ID=$THREAD_ID
MESSAGE=$message
RESULT_JSON=$result_json
TIMESTAMP=$(date -Iseconds)
EOF
}

# 主轮询循环
while true; do
    # 检查超时
    if [ $total_seconds -ge $max_seconds ]; then
        write_status "timeout" "轮询超时（${MAX_TIMEOUT}分钟）" ""
        echo "[TIMEOUT] 轮询超时，thread_id=$THREAD_ID"
        exit 2
    fi
    
    # 执行轮询
    result=$(dm-cli thread result --thread-id "$THREAD_ID" --json 2>&1)
    exit_code=$?
    
    if [ $exit_code -ne 0 ]; then
        # 网络错误或其他错误，记录但继续重试
        echo "[ERROR] dm-cli 返回错误: $result"
        sleep 10
        total_seconds=$((total_seconds + 10))
        continue
    fi
    
    # 解析状态
    state=$(echo "$result" | jq -r '.data.state // empty')
    
    if [ -z "$state" ]; then
        echo "[ERROR] 无法解析状态: $result"
        sleep 10
        total_seconds=$((total_seconds + 10))
        continue
    fi
    
    # 检测状态变化
    if [ "$state" != "$last_state" ]; then
        echo "[STATE_CHANGE] $last_state -> $state"
        last_state="$state"
        
        # 根据状态处理
        case "$state" in
            "running")
                # running 状态变化，只记录，不退出
                write_status "running" "任务执行中..." "$result"
                ;;
            
            "async_tag_task")
                # 需要 GUI 确认，提取 task_name
                task_name=$(echo "$result" | jq -r '.data.status_info.task_name // "未知任务"')
                write_status "async_tag_task" "$task_name" "$result"
                # 继续轮询，不退出
                ;;
            
            "ask_human")
                # 需要用户输入，提取问题
                question=$(echo "$result" | jq -r '.data.message_display_to_human // ""')
                write_status "ask_human" "$question" "$result"
                echo "[ASK_HUMAN] $question"
                exit 0
                ;;
            
            "completed")
                # 成功完成
                write_status "completed" "任务完成" "$result"
                echo "[COMPLETED] 任务完成，thread_id=$THREAD_ID"
                exit 0
                ;;
            
            "failed")
                # 失败
                write_status "failed" "任务失败" "$result"
                echo "[FAILED] 任务失败，thread_id=$THREAD_ID"
                exit 1
                ;;
            
            *)
                # 未知状态
                write_status "$state" "未知状态: $state" "$result"
                echo "[UNKNOWN] 未知状态: $state"
                ;;
        esac
    fi
    
    # 如果是终止状态，退出
    case "$state" in
        "ask_human"|"completed"|"failed")
            exit 0
            ;;
    esac
    
    # 计算下一次轮询间隔
    interval=${INTERVALS[$interval_index]:-60}
    echo "[POLL] 状态=$state, 等待 ${interval}s..."
    sleep $interval
    
    # 递增间隔
    if [ $interval_index -lt $((${#INTERVALS[@]} - 1)) ]; then
        interval_index=$((interval_index + 1))
    fi
    
    total_seconds=$((total_seconds + interval))
done