#!/bin/bash
#
# 输出格式化工具函数库
# 提供 JSON 输出、错误处理等功能
#

# 输出成功结果（JSON 格式）
# 参数:
#   $1 - 数据（JSON 格式）
#   $2 - 消息（可选）
# 输出到: STDOUT
output_success() {
    local data="$1"
    local message="${2:-操作成功}"
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    cat <<EOF
{
  "success": true,
  "data": $data,
  "message": "$message",
  "timestamp": "$timestamp"
}
EOF
}

# 输出错误信息（JSON 格式）
# 参数:
#   $1 - 错误类型
#   $2 - 错误消息
#   $3 - 建议数组（可选，JSON 数组格式）
# 输出到: STDERR
output_error() {
    local error_type="$1"
    local error_message="$2"
    local suggestions="${3:-[]}"
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    cat >&2 <<EOF
{
  "success": false,
  "error": "$error_type",
  "message": "$error_message",
  "suggestions": $suggestions,
  "timestamp": "$timestamp"
}
EOF
}

# 解析 JSON 输入（简化版）
# 注意：这是一个简化的 JSON 解析器，不支持复杂嵌套
# 参数: $1 - JSON 字符串
# 参数: $2 - 键名
# 返回值: 对应的值
parse_json() {
    local json="$1"
    local key="$2"

    # 使用 grep 和 sed 提取值
    # 支持：字符串、数字、布尔值
    local value=$(echo "$json" | sed -n "s/.*\"$key\"\s*:\s*\(\"\([^\"]*\)\"\|\\([0-9]*\\)\\|\\(true\\|false\\|null\)\\).*/\\2\\3\\4/p" | head -1)

    echo "$value"
}

# 从 JSON 中获取字符串值
# 参数: $1 - JSON 字符串
# 参数: $2 - 键名
# 返回值: 对应的字符串值
get_json_string() {
    local json="$1"
    local key="$2"

    echo "$json" | grep -o "\"$key\"[[:space:]]*:[[:space:]]*\"[^\"]*\"" | sed 's/.*: *"\([^"]*\)".*/\1/'
}

# 从 JSON 中获取数字值
# 参数: $1 - JSON 字符串
# 参数: $2 - 键名
# 返回值: 对应的数字值
get_json_number() {
    local json="$1"
    local key="$2"

    echo "$json" | grep -o "\"$key\"[[:space:]]*:[[:space:]]*[0-9]*" | sed 's/.*: *\([0-9]*\).*/\1/'
}

# 从 JSON 中获取布尔值
# 参数: $1 - JSON 字符串
# 参数: $2 - 键名
# 返回值: 对应的布尔值（true|false）
get_json_bool() {
    local json="$1"
    local key="$2"

    echo "$json" | grep -o "\"$key\"[[:space:]]*:[[:space:]]*\(true\|false\)" | sed 's/.*: *\(true\|false\).*/\1/'
}

# 验证 JSON 格式
# 参数: $1 - JSON 字符串
# 返回值: 0=有效, 1=无效
validate_json() {
    local json="$1"

    # 尝试解析 JSON（如果 Python 可用）
    if command -v python3 &> /dev/null; then
        echo "$json" | python3 -m json.tool >/dev/null 2>&1
        return $?
    elif command -v python &> /dev/null; then
        echo "$json" | python -m json.tool >/dev/null 2>&1
        return $?
    elif command -v jq &> /dev/null; then
        echo "$json" | jq . >/dev/null 2>&1
        return $?
    else
        # 简单验证：检查是否以 { 开头，以 } 结尾
        if [[ "$json" =~ ^\{.*\}$ ]]; then
            return 0
        else
            return 1
        fi
    fi
}

# 转义 JSON 字符串
# 参数: $1 - 原始字符串
# 返回值: 转义后的字符串
escape_json_string() {
    local str="$1"

    # 转义特殊字符
    str="${str//\\/\\\\}"  # 反斜杠
    str="${str//\"/\\\"}"  # 双引号
    str="${str//$'\n'/\\n}"  # 换行
    str="${str//$'\r'/\\r}"  # 回车
    str="${str//$'\t'/\\t}"  # 制表符

    echo "$str"
}

# 构建键值对 JSON
# 参数: 奇数个参数，格式：key1 value1 key2 value2 ...
# 返回值: JSON 对象字符串
build_json() {
    local json=""
    local count=$#

    if [ $((count % 2)) -ne 0 ]; then
        echo "{}"
        return 1
    fi

    local i=1
    while [ $i -le $count ]; do
        local key="${!i}"
        local i=$((i + 1))
        local value="${!i}"

        if [ $i -eq 2 ]; then
            json="{\"$key\": \"$value\""
        else
            json="$json, \"$key\": \"$value\""
        fi

        i=$((i + 1))
    done

    json="$json}"
    echo "$json"
}

# 输出日志（调试用）
# 参数: $1 - 日志级别（INFO|WARN|ERROR）
# 参数: $2 - 日志消息
# 输出到: STDERR
log() {
    local level="$1"
    local message="$2"
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    echo "[$timestamp] [$level] $message" >&2
}

# 输出进度信息
# 参数: $1 - 进度消息
# 输出到: STDERR
output_progress() {
    local message="$1"
    echo "[INFO] $message" >&2
}

# 输出警告信息
# 参数: $1 - 警告消息
# 输出到: STDERR
output_warning() {
    local message="$1"
    echo "[WARN] $message" >&2
}
