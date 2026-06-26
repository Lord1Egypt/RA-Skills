#!/usr/bin/env bash
# cap-review/votes.sh - 获取帖子的投票记录
# Usage: ./votes.sh --post-id POST_ID

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/../lib/cb-common.sh"

cb_require_cmd "curl"
cb_require_cmd "jq"
cb_load_config
cb_parse_args "$@"

cb_require_param "$CB_POST_ID" "--post-id"

# 调用 API
output=$(cb_retry 3 cb_http_get "/api/v1/reviews/$CB_POST_ID/votes")

# 输出
cb_normalize_json "$output"
