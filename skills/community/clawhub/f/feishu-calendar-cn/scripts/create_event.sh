#!/bin/bash

# 飞书日历创建事件脚本
# 用法：bash create_event.sh "标题" "开始时间" "结束时间" [地点]
# 示例：bash create_event.sh "项目会议" "2026-03-21 14:00" "2026-03-21 15:00" "会议室A"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 获取认证 token
TOKEN=$(bash "$SCRIPT_DIR/auth.sh" 2>/dev/null)

if [ $? -ne 0 ] || [ -z "$TOKEN" ]; then
    echo '{"error": "认证失败"}'
    exit 1
fi

TITLE="$1"
START_TIME_STR="$2"
END_TIME_STR="$3"
LOCATION="${4:-}"

if [ -z "$TITLE" ] || [ -z "$START_TIME_STR" ] || [ -z "$END_TIME_STR" ]; then
    echo '{"error": "用法: bash create_event.sh \"标题\" \"开始时间\" \"结束时间\" [地点]"}'
    echo '{"example": "bash create_event.sh \"会议\" \"2026-03-21 14:00\" \"2026-03-21 15:00\""}'
    exit 1
fi

# 转换时间为 Unix 时间戳
# 兼容 macOS 和 Linux
if date -v0d >/dev/null 2>&1; then
    # macOS
    START_TIME=$(date -j -f "%Y-%m-%d %H:%M" "$START_TIME_STR" +%s 2>/dev/null)
    END_TIME=$(date -j -f "%Y-%m-%d %H:%M" "$END_TIME_STR" +%s 2>/dev/null)
else
    # Linux
    START_TIME=$(date -d "$START_TIME_STR" +%s 2>/dev/null)
    END_TIME=$(date -d "$END_TIME_STR" +%s 2>/dev/null)
fi

if [ -z "$START_TIME" ] || [ -z "$END_TIME" ]; then
    echo '{"error": "时间格式错误，请使用 YYYY-MM-DD HH:MM 格式"}'
    exit 1
fi

# 获取主日历 ID
CALENDAR_RESPONSE=$(curl -s -X POST \
    "https://open.feishu.cn/open-apis/calendar/v4/calendars/primary" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json")

CALENDAR_ID=$(echo "$CALENDAR_RESPONSE" | grep -o '"calendar_id":"[^"]*"' | head -1 | cut -d'"' -f4)

if [ -z "$CALENDAR_ID" ]; then
    echo '{"error": "无法获取日历 ID"}'
    exit 1
fi

# 构建请求体
if [ -n "$LOCATION" ]; then
    LOCATION_JSON=", \"location\": {\"name\": \"$LOCATION\"}"
else
    LOCATION_JSON=""
fi

# 创建事件
RESPONSE=$(curl -s -X POST \
    "https://open.feishu.cn/open-apis/calendar/v4/calendars/$CALENDAR_ID/events" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{
        \"summary\": \"$TITLE\",
        \"start_time\": {
            \"timestamp\": \"$START_TIME\",
            \"timezone\": \"Asia/Shanghai\"
        },
        \"end_time\": {
            \"timestamp\": \"$END_TIME\",
            \"timezone\": \"Asia/Shanghai\"
        }$LOCATION_JSON
    }")

# 输出结果
echo "$RESPONSE"