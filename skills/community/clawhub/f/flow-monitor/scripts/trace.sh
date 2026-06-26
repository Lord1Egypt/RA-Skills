#!/bin/bash

LOG_FILE="claw_execution.log"

if [ ! -f "$LOG_FILE" ]; then
    echo "{\"status\": \"error\", \"message\": \"Log file not found at $LOG_FILE\"}"
    exit 0
fi

# 跨平台时间转 Unix 时间戳函数
get_unix_time() {
    local raw_time="$1"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS (BSD Date)
        date -j -f "%Y-%m-%d %H:%M:%S" "$raw_time" "+%s" 2>/dev/null
    else
        # Linux (GNU Date)
        date -d "$raw_time" "+%s" 2>/dev/null
    fi
}

echo "["
# 提取日志中 Calling tool 的行
grep "Calling tool" "$LOG_FILE" | tail -n 15 | while read -r line; do
    # 提取时间戳 [YYYY-MM-DD HH:MM:SS]
    RAW_TIME=$(echo "$line" | grep -oE "[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}")
    UNIX_TIME=$(get_unix_time "$RAW_TIME")
    
    # 提取 Skill 名称
    SKILL_NAME=$(echo "$line" | sed -n 's/.*Calling tool: \([^ ]*\).*/\1/p')
    
    # 提取内容并估算 Token
    # 逻辑：中文字符数*1.5 + 英文字符数*0.3 (综合估算)
    PAYLOAD=$(echo "$line" | sed -n 's/.*with input: \(.*\)/\1/p')
    CHAR_COUNT=${#PAYLOAD}
    EST_TOKENS=$(( CHAR_COUNT / 2 + 1 )) # 简易中英折中算法

    echo "  {"
    echo "    \"timestamp\": \"$RAW_TIME\","
    echo "    \"unix_time\": \"${UNIX_TIME:-0}\","
    echo "    \"skill\": \"$SKILL_NAME\","
    echo "    \"estimated_tokens\": $EST_TOKENS,"
    echo "    \"raw_size\": $CHAR_COUNT"
    echo "  },"
done | sed '$ s/,$//'
echo "]"

