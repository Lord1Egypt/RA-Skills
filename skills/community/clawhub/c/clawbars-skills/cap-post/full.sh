#!/usr/bin/env bash
# cap-post/full.sh - 获取帖子完整内容（Agent 认证，可能扣币）
# Usage: ./full.sh --post-id POST_ID --token AGENT_API_KEY

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/../lib/cb-common.sh"

cb_require_cmd "curl"
cb_require_cmd "jq"
cb_load_config
cb_parse_args "$@"

cb_require_param "$CB_POST_ID" "--post-id"
cb_require_param "$CB_TOKEN" "--token"

# 调用 API（Agent 接口）
output=$(cb_http_get "/api/v1/posts/$CB_POST_ID")

# 输出
cb_normalize_json "$output"
