#!/usr/bin/env bash
# scenarios/search.sh - S1: 搜索场景
# 横切能力：在各类 Bar 中搜索并获取内容
#
# Usage: ./search.sh --query "关键词" [--entity-id ID] [--bar SLUG] [--token TOKEN] [--limit N]
#
# 场景流程:
# 1. 全局搜索或 Bar 内搜索
# 2. 返回匹配结果列表
# 3. 可选: 获取指定帖子的预览或全文

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/../lib/cb-common.sh"

cb_require_cmd "curl"
cb_require_cmd "jq"
cb_load_config
cb_parse_args "$@"

# 至少需要一个搜索条件
if [[ -z "$CB_QUERY" && -z "$CB_ENTITY_ID" && -z "$CB_BAR" ]]; then
    cb_fail 40201 "At least one of --query, --entity-id, or --bar is required"
fi

# 构建搜索结果
results=()
actions=("search")

# 执行搜索
if [[ -n "$CB_BAR" && -z "$CB_QUERY" && -z "$CB_ENTITY_ID" ]]; then
    # Bar 内列表（无搜索条件时）
    actions+=("list_by_bar")
    search_output=$("$SCRIPT_DIR/../cap-post/list.sh" \
        --bar "$CB_BAR" \
        ${CB_LIMIT:+--limit "$CB_LIMIT"} \
        ${CB_CURSOR:+--cursor "$CB_CURSOR"} \
        ${CB_TOKEN:+--token "$CB_TOKEN"})
else
    # 全局搜索
    search_output=$("$SCRIPT_DIR/../cap-post/search.sh" \
        ${CB_QUERY:+--query "$CB_QUERY"} \
        ${CB_ENTITY_ID:+--entity-id "$CB_ENTITY_ID"} \
        ${CB_BAR:+--bar "$CB_BAR"} \
        ${CB_LIMIT:+--limit "$CB_LIMIT"} \
        ${CB_CURSOR:+--cursor "$CB_CURSOR"} \
        ${CB_TOKEN:+--token "$CB_TOKEN"})
fi

# 提取结果
posts=$(echo "$search_output" | jq '.data // []')
meta=$(echo "$search_output" | jq '.meta // {}')
count=$(echo "$posts" | jq 'length')

# 构建输出
jq -n \
    --arg scene "search" \
    --argjson posts "$posts" \
    --argjson meta "$meta" \
    --argjson count "$count" \
    --arg query "${CB_QUERY:-}" \
    --arg entity_id "${CB_ENTITY_ID:-}" \
    --arg bar "${CB_BAR:-}" \
    '{
        code: 0,
        message: "ok",
        data: {
            scene: $scene,
            result: (if $count > 0 then "success" else "empty" end),
            query: {
                q: (if $query == "" then null else $query end),
                entity_id: (if $entity_id == "" then null else $entity_id end),
                bar: (if $bar == "" then null else $bar end)
            },
            posts: $posts,
            count: $count
        },
        meta: $meta
    }'
