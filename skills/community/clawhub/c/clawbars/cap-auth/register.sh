#!/usr/bin/env bash
# cap-auth/register.sh - 用户注册
# Usage: ./register.sh --name "用户名" --email "xxx@email.com" --password "密码"

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/../lib/cb-common.sh"

cb_require_cmd "curl"
cb_require_cmd "jq"
cb_load_config
cb_parse_args "$@"

cb_require_param "$CB_NAME" "--name"
cb_require_param "$CB_EMAIL" "--email"
cb_require_param "$CB_PASSWORD" "--password"

# 构建请求体
payload=$(jq -n \
    --arg name "$CB_NAME" \
    --arg email "$CB_EMAIL" \
    --arg password "$CB_PASSWORD" \
    '{name: $name, email: $email, password: $password}'
)

# 调用 API
output=$(cb_http_post "/api/v1/auth/register" "$payload")

# 输出
cb_normalize_json "$output"
