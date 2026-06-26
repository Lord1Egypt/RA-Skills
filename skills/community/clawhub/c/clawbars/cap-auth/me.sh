#!/usr/bin/env bash
# cap-auth/me.sh - 获取当前用户信息
# Usage: ./me.sh --token USER_JWT

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/../lib/cb-common.sh"

cb_require_cmd "curl"
cb_require_cmd "jq"
cb_load_config
cb_parse_args "$@"

cb_require_param "$CB_TOKEN" "--token"

# 调用 API
output=$(cb_http_get "/api/v1/auth/me")

# 输出
cb_normalize_json "$output"
