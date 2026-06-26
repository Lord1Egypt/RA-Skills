#!/bin/bash
# DM 轮询脚本 - 状态变化时通过 sessions_send 通知主会话
# 
# 用法: dm-poll-notify.sh <thread_id> [parent_session_key] [max_timeout_minutes]
#
# 参数:
#   thread_id          - DM 会话 ID（必填）
#   parent_session_key - 主会话标识（默认: main）
#   max_timeout        - 最大轮询时间（分钟，默认: 60）
#
# 输出:
#   状态变化时通过 sessions_send 发送通知
#   通知格式: DM_POLL_NOTIFY:<thread_id>:<state>:<base64编码的result>
#
# 退出码:
#   0 - 正常退出（终止状态）
#   1 - 失败状态
#   2 - 超时
#   3 - 参数错误

set -e

THREAD_ID="$1"
PARENT_SESSION="${2:-main}"
MAX_TIMEOUT="${3:-60}"

# 参数检查
if [ -z "$THREAD_ID" ]; then
    echo "用法: $0 <thread_id> [parent_session_key] [max_timeout_minutes]"
    exit 3
fi

# 轮询间隔（秒）：递增策略
INTERVALS=(5 10 20 40 60)
interval_idx=0
total_seconds=0
max_seconds=$((MAX_TIMEOUT * 60))
last_state=""

# 发送通知给主会话
send_notification() {
    local state="$1"
    local result="$2"
    
    # Base64 编码结果（避免特殊字符问题）
    local encoded=""
    if command -v base64 &> /dev/null; then
        encoded=$(echo -n "$result" | base64 | tr -d '\n' 2>/dev/null || echo "")
    fi
    
    # 如果 base64 编码失败，使用原始结果（URL编码特殊字符）
    if [ -z "$encoded" ]; then
        encoded="$result"
    fi
    
    # 发送通知
    local message="DM_POLL_NOTIFY:${THREAD_ID}:${state}:${encoded}"
    
    echo "[NOTIFY] 发送通知: state=$state"
    
    # 使用 sessions_send 发送消息
    # 注意：这需要在 OpenClaw 环境中运行
    if command -v sessions_send &> /dev/null; then
        sessions_send --sessionKey "$PARENT_SESSION" --message "$message" 2>/dev/null || true
    else
        # 如果 sessions_send 不可用，输出到标准输出
        echo "$message"
    fi
}

# 提取关键信息
extract_info() {
    local result="$1"
    local state="$2"
    local info=""
    
    case "$state" in
        "ask_human")
            # 提取问题
            info=$(echo "$result" | jq -r '.data.message_display_to_human // ""' 2>/dev/null || echo "")
            ;;
        "async_tag_task")
            # 提取任务名称
            info=$(echo "$result" | jq -r '.data.status_info.task_name // ""' 2>/dev/null || echo "")
            ;;
        "completed"|"failed")
            # 提取最后消息
            info=$(echo "$result" | jq -r '.data.last_messages[0].content // ""' 2>/dev/null | head -c 200 || echo "")
            ;;
    esac
    
    echo "$info"
}

echo "[START] 开始轮询 thread_id=$THREAD_ID, parent_session=$PARENT_SESSION"

# 主轮询循环
while true; do
    # 检查超时
    if [ $total_seconds -ge $max_seconds ]; then
        echo "[TIMEOUT] 轮询超时 (${MAX_TIMEOUT}分钟)"
        send_notification "timeout" "{\"error\": \"轮询超时\", \"thread_id\": \"$THREAD_ID\"}"
        exit 2
    fi
    
    # 执行轮询
    echo "[POLL] 查询状态..."
    result=$(dm-cli thread result --thread-id "$THREAD_ID" --json 2>&1)
    exit_code=$?
    
    if [ $exit_code -ne 0 ]; then
        echo "[ERROR] dm-cli 执行失败: exit_code=$exit_code"
        sleep 10
        total_seconds=$((total_seconds + 10))
        continue
    fi
    
    # 解析状态
    state=$(echo "$result" | jq -r '.data.state // "unknown"' 2>/dev/null || echo "unknown")
    
    if [ "$state" = "unknown" ] || [ -z "$state" ]; then
        echo "[WARN] 无法解析状态，原始响应: ${result:0:200}..."
        sleep 10
        total_seconds=$((total_seconds + 10))
        continue
    fi
    
    echo "[STATE] 当前状态: $state"
    
    # 检测状态变化
    if [ "$state" != "$last_state" ]; then
        echo "[STATE_CHANGE] $last_state -> $state"
        
        # 发送通知
        send_notification "$state" "$result"
        
        last_state="$state"
    fi
    
    # 处理终止状态
    case "$state" in
        "completed")
            echo "[EXIT] 任务完成"
            exit 0
            ;;
        "ask_human")
            question=$(extract_info "$result" "$state")
            echo "[EXIT] 需要用户输入: ${question:0:100}..."
            exit 0
            ;;
        "failed")
            echo "[EXIT] 任务失败"
            exit 1
            ;;
    esac
    
    # 计算等待时间
    interval=${INTERVALS[$interval_idx]:-60}
    echo "[WAIT] 等待 ${interval}s 后继续轮询..."
    sleep $interval
    
    # 递增间隔
    if [ $interval_idx -lt $((${#INTERVALS[@]} - 1)) ]; then
        interval_idx=$((interval_idx + 1))
    fi
    
    total_seconds=$((total_seconds + interval))
done