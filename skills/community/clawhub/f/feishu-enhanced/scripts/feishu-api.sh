#!/bin/bash
# 飞书API辅助脚本
# 用于简化飞书API调用

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 获取tenant_access_token
get_tenant_token() {
    local app_id="${FEISHU_APP_ID}"
    local app_secret="${FEISHU_APP_SECRET}"

    if [[ -z "$app_id" || -z "$app_secret" ]]; then
        log_error "缺少飞书应用配置，请设置 FEISHU_APP_ID 和 FEISHU_APP_SECRET"
        return 1
    fi

    local response=$(curl -s -X POST \
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
        -H "Content-Type: application/json" \
        -d "{\"app_id\":\"$app_id\",\"app_secret\":\"$app_secret\"}")

    echo "$response" | jq -r '.tenant_access_token'
}

# 批量创建多维表格记录
batch_create_records() {
    local app_token="$1"
    local table_id="$2"
    local records_json="$3"
    local token=$(get_tenant_token)

    curl -s -X POST \
        "https://open.feishu.cn/open-apis/bitable/v1/apps/$app_token/tables/$table_id/records/batch_create" \
        -H "Authorization: Bearer $token" \
        -H "Content-Type: application/json" \
        -d "$records_json"
}

# 发送消息
send_message() {
    local receive_id_type="$1"
    local receive_id="$2"
    local msg_type="$3"
    local content="$4"
    local token=$(get_tenant_token)

    curl -s -X POST \
        "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=$receive_id_type" \
        -H "Authorization: Bearer $token" \
        -H "Content-Type: application/json" \
        -d "{\"receive_id\":\"$receive_id\",\"msg_type\":\"$msg_type\",\"content\":\"$content\"}"
}

# 主命令处理
case "$1" in
    token)
        get_tenant_token
        ;;
    batch-create)
        batch_create_records "$2" "$3" "$4"
        ;;
    send)
        send_message "$2" "$3" "$4" "$5"
        ;;
    *)
        echo "用法: $0 {token|batch-create|send} [参数...]"
        exit 1
        ;;
esac
