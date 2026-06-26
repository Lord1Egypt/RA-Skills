#!/usr/bin/env bash
# cap-bar/joined.sh - 列出用户已加入的 Bars
# Usage: ./joined.sh --token USER_JWT

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/../lib/cb-common.sh"

cb_require_cmd "curl"
cb_require_cmd "jq"
cb_load_config
cb_parse_args "$@"

cb_require_param "$CB_TOKEN" "--token"

# 调用 API
output=$(cb_retry 3 cb_http_get "/api/v1/bars/joined")

# 输出
cb_normalize_json "$output"
