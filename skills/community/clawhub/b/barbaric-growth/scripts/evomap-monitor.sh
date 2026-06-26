#!/bin/bash
# EvoMap 高价值任务监控器
# 每60秒检查一次，发现$50+任务立即通知
# 依赖: curl, python3, message tool (via Nova session)

NODE_ID="node_2bd13d1a7e1558fd"
NODE_SECRET="fb61d04fef52f7c32c41938f38bc8d32b00056d1608c4dc2447afd53f5457995"
EVO_API="https://evomap.ai/a2a/heartbeat"
STATE_DIR="${HOME}/.openclaw/evomap-monitor"
NOTIFIED_FILE="${STATE_DIR}/last_notified.txt"
LOG_FILE="${STATE_DIR}/monitor.log"
MIN_AMOUNT=50
POLL_INTERVAL=60

mkdir -p "$STATE_DIR"

log() {
    echo "[$(date '+%H:%M:%S')] $1" >> "$LOG_FILE"
}

check_tasks() {
    local result
    result=$(curl -s -X POST "$EVO_API" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $NODE_SECRET" \
        -d "{\"node_id\": \"$NODE_ID\"}" 2>/dev/null)
    
    if [ $? -ne 0 ] || [ -z "$result" ]; then
        log "API请求失败"
        return
    fi
    
    # 解析任务
    local task_count
    task_count=$(echo "$result" | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d.get('available_tasks',[])))" 2>/dev/null)
    
    if [ "$task_count" = "0" ] || [ -z "$task_count" ]; then
        return
    fi
    
    # 找最高价值任务
    local top_task top_amount top_title
    top_task=$(echo "$result" | python3 -c "
import sys,json
tasks = d.get('available_tasks',[])
if not tasks: exit()
best = max(tasks, key=lambda t: float(t.get('bounty_amount',0)))
print(best.get('task_id','') + '|' + best.get('bounty_amount','') + '|' + best.get('title','')[:80])
" 2>/dev/null)
    
    if [ -z "$top_task" ]; then
        return
    fi
    
    IFS='|' read -r task_id amount title <<< "$top_task"
    
    # 检查是否超过阈值
    amount_val=$(echo "$amount" | python3 -c "print(float(open('/dev/stdin').read().strip()) if open('/dev/stdin').read().strip() else 0" 2>/dev/null)
    amount_val=$(python3 -c "print($amount)")
    
    if [ $(echo "$amount_val >= $MIN_AMOUNT" | python3) -eq 0 ]; then
        return
    fi
    
    # 检查是否已经通知过
    if [ -f "$NOTIFIED_FILE" ]; then
        last_notified=$(cat "$NOTIFIED_FILE")
        if [ "$last_notified" = "$task_id" ]; then
            log "任务已通知过，跳过: $task_id $amount"
            return
        fi
    fi
    
    # 发现高价值任务 → 记录并通知
    log "🚨 发现高价值任务: $task_id $amount $title"
    echo "$task_id" > "$NOTIFIED_FILE"
    
    # 写入通知文件（Nova 的主会话可以看到）
    notify_file="${STATE_DIR}/ALERT.txt"
    cat > "$notify_file" << EOF
🚨 【EvoMap 高价值任务】
金额: \$$amount
标题: $title
任务ID: $task_id
发现时间: $(date '+%Y-%m-%d %H:%M:%S')
EOF
    log "已写入ALERT: $amount $title"
}

log "=== 监控启动 ==="
log "每${POLL_INTERVAL}秒检查一次，阈值 \$${MIN_AMOUNT}"

while true; do
    check_tasks
    sleep $POLL_INTERVAL
done
