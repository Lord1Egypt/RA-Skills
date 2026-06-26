#!/usr/bin/env bash
# cap-bar/detail.sh - 获取 Bar 详情
# Usage: ./detail.sh --bar SLUG [--token TOKEN]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/../lib/cb-common.sh"

cb_require_cmd "curl"
cb_require_cmd "jq"
cb_load_config
cb_parse_args "$@"

cb_require_param "$CB_BAR" "--bar"

# 调用 API
output=$(cb_retry 3 cb_http_get "/api/v1/bars/$CB_BAR")

# 输出
cb_normalize_json "$output"
