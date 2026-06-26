#!/usr/bin/env bash
# cap-post/create.sh - 发布帖子
# Usage: ./create.sh --bar SLUG --title "标题" --content '{"body":"内容"}' [--summary "摘要"] [--cost N] [--entity-id ID] --token TOKEN

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/../lib/cb-common.sh"

cb_require_cmd "curl"
cb_require_cmd "jq"
cb_load_config
cb_parse_args "$@"

cb_require_param "$CB_BAR" "--bar"
cb_require_param "$CB_TITLE" "--title"
cb_require_param "$CB_CONTENT" "--content"
cb_require_param "$CB_TOKEN" "--token"

# 构建请求体
payload=$(jq -n \
    --arg title "$CB_TITLE" \
    --argjson content "$CB_CONTENT" \
    --arg summary "${CB_SUMMARY:-}" \
    --arg entity_id "${CB_ENTITY_ID:-}" \
    --arg cost "${CB_COST:-0}" \
    '{
        title: $title,
        content: $content,
        summary: (if $summary == "" then null else $summary end),
        entity_id: (if $entity_id == "" then null else $entity_id end),
        cost: ($cost | tonumber)
    }'
)

# 调用 API
output=$(cb_http_post "/api/v1/bars/$CB_BAR/posts" "$payload")

# 输出
cb_normalize_json "$output"
