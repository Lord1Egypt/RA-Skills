#!/usr/bin/env bash
# cap-auth/refresh.sh - 刷新 token
# Usage: ./refresh.sh --refresh-token "REFRESH_TOKEN"

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/../lib/cb-common.sh"

cb_require_cmd "curl"
cb_require_cmd "jq"
cb_load_config
cb_parse_args "$@"

cb_require_param "$CB_REFRESH_TOKEN" "--refresh-token"

# 构建请求体
payload=$(jq -cn \
    --arg refresh_token "$CB_REFRESH_TOKEN" \
    '{refresh_token: $refresh_token}'
)

# 调用 API
output=$(cb_http_post "/api/v1/auth/refresh" "$payload")

# 输出
cb_normalize_json "$output"
