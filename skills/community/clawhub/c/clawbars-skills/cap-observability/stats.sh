#!/usr/bin/env bash
# cap-observability/stats.sh - 获取平台统计数据
# Usage: ./stats.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/../lib/cb-common.sh"

cb_require_cmd "curl"
cb_require_cmd "jq"
cb_load_config

# 调用 API
output=$(cb_retry 3 cb_http_get "/api/v1/stats")

# 输出
cb_normalize_json "$output"
