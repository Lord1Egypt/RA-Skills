#!/bin/bash

# 飞书日历忙闲查询脚本
# 用法：bash freebusy.sh "开始日期" "结束日期"
# 示例：bash freebusy.sh "2026-03-21" "2026-03-22"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 获取认证 token
TOKEN=$(bash "$SCRIPT_DIR/auth.sh" 2>/dev/null)

if [ $? -ne 0 ] || [ -z "$TOKEN" ]; then
    echo '{"error": "认证失败"}'
    exit 1
fi

START_DATE="$1"
END_DATE="$2"

if [ -z "$START_DATE" ] || [ -z "$END_DATE" ]; then
    echo '{"error": "用法: bash freebusy.sh \"开始日期\" \"结束日期\""}'
    echo '{"example": "bash freebusy.sh \"2026-03-21\" \"2026-03-22\""}'
    exit 1
fi

# 转换时间为 RFC 3339 格式
TIME_MIN="${START_DATE}T00:00:00+08:00"
TIME_MAX="${END_DATE}T23:59:59+08:00"

# 查询忙闲状态
RESPONSE=$(curl -s -X POST \
    "https://open.feishu.cn/open-apis/calendar/v4/freebusy/list" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{
        \"time_min\": \"$TIME_MIN\",
        \"time_max\": \"$TIME_MAX\"
    }")

# 输出结果
echo "$RESPONSE"