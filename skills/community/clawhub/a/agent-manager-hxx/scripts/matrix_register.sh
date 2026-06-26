#!/bin/bash

# 配置：如果有环境变量则使用，否则默认本地
HOMESERVER_URL="${HOMESERVER_URL:-http://localhost:8008}"

# 简易 JSON 提取函数（只提取双引号内的值）
extract_val() {
    local key="$1"
    local json="$2"
    echo "$json" | sed -n "s/.*\"$key\":\"\([^\"]*\)\".*/\1/p" | head -n 1
}

# 1. 注册账号
register_user() {
    local user="$1"
    local pass="$2"
    
    echo "--- 正在尝试注册: $user ---"
    # 直接使用你提供的 v3 接口和 payload
    local resp=$(curl -s -X POST "${HOMESERVER_URL}/_matrix/client/v3/register" \
        -H "Content-Type: application/json" \
        -d "{
            \"username\": \"$user\",
            \"password\": \"$pass\",
            \"auth\": {\"type\": \"m.login.dummy\"}
        }")
    
    local err=$(extract_val "errcode" "$resp")
    if [ -z "$err" ]; then
        echo "注册成功！"
    else
        echo "注册反馈: $err (可能账号已存在，将尝试直接登录)"
    fi
}

# 2. 获取 Access Token
get_token() {
    local user="$1"
    local pass="$2"
    
    echo "--- 正在获取 Access Token ---"
    # 使用你提供的登录接口
    local resp=$(curl -s -X POST "${HOMESERVER_URL}/_matrix/client/v3/login" \
        -H "Content-Type: application/json" \
        -d "{
            \"type\": \"m.login.password\",
            \"identifier\": {\"type\": \"m.id.user\", \"user\": \"$user\"},
            \"password\": \"$pass\"
        }")

    local token=$(extract_val "access_token" "$resp")
    local full_uid=$(extract_val "user_id" "$resp")

    if [ -n "$token" ]; then
        # 建议这里只打印结果，不要有其他干扰字符，或者用特定格式
        echo "RESULT_USER_ID: $full_uid"
        echo "RESULT_ACCESS_TOKEN: $token"
    else
        echo "错误：无法获取 Token" >&2 # 输出到错误流
        exit 1
    fi
}

# 执行逻辑
if [ -z "$2" ]; then
    echo "用法: $0 <用户id> <密码>"
    exit 1
fi

register_user "$1" "$2"
get_token "$1" "$2"