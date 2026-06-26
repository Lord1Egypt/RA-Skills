#!/usr/bin/env bash
# cap-bar/join-user.sh - User 加入 Bar
# Usage: ./join-user.sh --bar SLUG --token USER_JWT [--invite-token TOKEN]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/../lib/cb-common.sh"

cb_require_cmd "curl"
cb_require_cmd "jq"
cb_load_config
cb_parse_args "$@"

cb_require_param "$CB_BAR" "--bar"
cb_require_param "$CB_TOKEN" "--token"

# 构建请求体
payload=$(jq -n \
    --arg invite_token "${CB_INVITE_TOKEN:-}" \
    '{
        invite_token: (if $invite_token == "" then null else $invite_token end)
    }'
)

# 调用 API
output=$(cb_http_post "/api/v1/bars/$CB_BAR/join/user" "$payload")

# 输出
cb_normalize_json "$output"
