#!/bin/bash
# 216medsearch - 通过 API 查询药品通用名

# 检查参数
if [ $# -eq 0 ]; then
    echo "错误：请提供药品名称"
    echo "用法：$0 <药品名称>"
    exit 1
fi

MED_NAME="$1"

# API 配置
API_URL="http://10.1.23.216:8280/rest/schema/med/query"
API_TOKEN="eyJhbGciOiJIUzUxMiIsInppcCI6IkRFRiJ9.eNqqVipILC4uzy9KUbJSMjQyNjE1cyjKzy9R0lFyDnJ1DHGND_H0dQXKGRkYmekamOgaGCoYGVgZmVuZGOuZmpgB1aVkgvQGGwCZpcWpRXmJualAPtiQWgAAAAD__w.qnT0SfmS79BwoTb7lHJEbJFt1diIb03cTwO5UDuIaUxIHABOy0vfYTRvx4erVFZJHEj8OZ2JeRfCFfq-VS1nlQ"

# 构建查询条件（模糊查询）
CONDITION="name##'${MED_NAME}'"
PROP_NAMES="name"

# 调用 API
RESPONSE=$(curl -s -X 'POST' "${API_URL}" \
    -H 'accept: application/json' \
    -H "token: ${API_TOKEN}" \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -d "condition=${CONDITION}&propNames=${PROP_NAMES}")

# 检查返回结果
if [ -z "$RESPONSE" ]; then
    echo '{"success": false, "error": "API 返回为空"}'
    exit 1
fi

# 检查是否为错误响应
if echo "$RESPONSE" | grep -q "401\|unauthorized\|token"; then
    echo '{"success": false, "error": "API 认证失败，token 可能已过期"}'
    exit 1
fi

# 格式化输出 JSON
echo "$RESPONSE" | python3 -m json.tool
