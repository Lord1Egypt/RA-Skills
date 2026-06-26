#!/usr/bin/env bash
# cap-post/preview.sh - 获取帖子预览（免费，无需认证）
# Usage: ./preview.sh --post-id POST_ID

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/../lib/cb-common.sh"

cb_require_cmd "curl"
cb_require_cmd "jq"
cb_load_config
cb_parse_args "$@"

cb_require_param "$CB_POST_ID" "--post-id"

# 调用 API
output=$(cb_retry 3 cb_http_get "/api/v1/posts/$CB_POST_ID/preview")

# 输出
cb_normalize_json "$output"
