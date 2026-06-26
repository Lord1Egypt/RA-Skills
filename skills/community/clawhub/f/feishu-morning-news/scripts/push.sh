#!/bin/bash
set -e

# 配置
CONFIG_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_FILE="/var/log/feishu-morning-news.log"
DATA_URL="https://60s.viki.moe/v2/60s"
MAX_RETRIES=3
RETRY_DELAY=60

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# 发送飞书消息
send_message() {
    local content="$1"
    log "正在发送早报消息..."
    
    # 保存内容到临时文件
    tmp_file=$(mktemp)
    echo "$content" > "$tmp_file"
    
    # 使用openclaw message工具发送
    openclaw message send --to "user:ou_b8bd6c6f4b69a9dda0dd16c2788c32ca" --file "$tmp_file" >> "$LOG_FILE" 2>&1
    
    local exit_code=$?
    rm -f "$tmp_file"
    
    if [ $exit_code -eq 0 ]; then
        log "早报发送成功"
        return 0
    else
        log "早报发送失败"
        return 1
    fi
}

# 主逻辑
main() {
    log "=== 开始执行早报推送 ==="
    
    # 重试逻辑
    for ((retry=1; retry<=MAX_RETRIES; retry++)); do
        log "尝试第 $retry 次拉取数据..."
        
        # 拉取数据
        response=$(curl -s -w "\n%{http_code}" "$DATA_URL")
        http_code=$(echo "$response" | tail -n1)
        data=$(echo "$response" | head -n -1)
        
        if [ "$http_code" != "200" ]; then
            log "数据拉取失败，HTTP状态码: $http_code"
            if [ $retry -lt $MAX_RETRIES ]; then
                log "等待 $RETRY_DELAY 秒后重试..."
                sleep $RETRY_DELAY
            fi
            continue
        fi
        
        log "数据拉取成功，开始解析..."
        
        # 解析数据
        date=$(echo "$data" | python3 -c "import json, sys; print(json.load(sys.stdin)['data']['date'])")
        week=$(echo "$data" | python3 -c "import json, sys; print(json.load(sys.stdin)['data']['day_of_week'].replace('星期', ''))")
        tip=$(echo "$data" | python3 -c "import json, sys; print(json.load(sys.stdin)['data']['tip'])")
        news=$(echo "$data" | python3 -c "
import json, sys
news_list = json.load(sys.stdin)['data']['news']
for i, item in enumerate(news_list, 1):
    print(f'{i}. {item}')
")
        
        # 格式化消息
        content="## ☀️ 今日早报 | $date 星期$week

### 📰 60秒读懂世界
$news

### 💡 每日箴言
$tip"
        
        # 发送消息
        if send_message "$content"; then
            log "=== 早报推送完成 ==="
            exit 0
        else
            if [ $retry -lt $MAX_RETRIES ]; then
                log "等待 $RETRY_DELAY 秒后重试..."
                sleep $RETRY_DELAY
            fi
        fi
    done
    
    log "=== 所有重试都失败，早报推送失败 ==="
    exit 1
}

# 执行主函数
main "$@"
