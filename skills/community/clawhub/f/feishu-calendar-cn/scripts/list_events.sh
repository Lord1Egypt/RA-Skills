#!/bin/bash

# 飞书日历事件查询脚本（使用用户身份）
# 用法：bash list_events.sh [日期|today]
# 示例：bash list_events.sh today
#       bash list_events.sh 2026-03-21

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TOKEN_FILE="$SCRIPT_DIR/.user_token.json"

# 检查是否有保存的用户 token
if [ ! -f "$TOKEN_FILE" ]; then
    echo '{"error": "未找到用户授权 token，请先运行: bash oauth_token.sh <授权码>"}'
    exit 1
fi

# 读取 user_access_token
USER_TOKEN=$(cat "$TOKEN_FILE" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)

if [ -z "$USER_TOKEN" ]; then
    echo '{"error": "无效的用户 token，请重新授权"}'
    exit 1
fi

# 解析日期参数
if [ "$1" = "today" ] || [ -z "$1" ]; then
    DATE=$(date +%Y-%m-%d)
else
    DATE="$1"
fi

# 计算时间范围
if date -v0d >/dev/null 2>&1; then
    START_TIME=$(date -j -f "%Y-%m-%d %H:%M:%S" "$DATE 00:00:00" +%s)
else
    START_TIME=$(date -d "$DATE 00:00:00" +%s)
fi
END_TIME=$((START_TIME + 86400))

# 获取主日历 ID
CALENDAR_RESPONSE=$(curl -s -X POST \
    "https://open.feishu.cn/open-apis/calendar/v4/calendars/primary" \
    -H "Authorization: Bearer $USER_TOKEN" \
    -H "Content-Type: application/json")

CALENDAR_ID=$(echo "$CALENDAR_RESPONSE" | grep -o '"calendar_id":"[^"]*"' | head -1 | cut -d'"' -f4)

if [ -z "$CALENDAR_ID" ]; then
    echo "{\"error\": \"无法获取日历 ID\", \"response\": $CALENDAR_RESPONSE}"
    exit 1
fi

# 查询事件
EVENTS_RESPONSE=$(curl -s -X GET \
    "https://open.feishu.cn/open-apis/calendar/v4/calendars/$CALENDAR_ID/events?start_time=$START_TIME&end_time=$END_TIME&user_id_type=open_id" \
    -H "Authorization: Bearer $USER_TOKEN" \
    -H "Content-Type: application/json")

echo "$EVENTS_RESPONSE"