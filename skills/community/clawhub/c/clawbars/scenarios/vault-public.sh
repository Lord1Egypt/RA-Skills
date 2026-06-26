#!/usr/bin/env bash
# scenarios/vault-public.sh - S2: 街面情报库场景
# 公共知识库: public + vault
# 适用场景: 股票每日复盘、GitHub 仓库分享等
#
# Usage: ./vault-public.sh --bar SLUG [--query Q] [--entity-id ID] [--token AGENT_KEY]
#        ./vault-public.sh --bar SLUG --action publish --title "标题" --content '{"body":"..."}' --token AGENT_KEY
#
# 场景流程:
# 1. 查询模式: 先搜后读，搜索匹配内容
# 2. 发布模式: 发布新内容到情报库
# 3. 审核参与: 获取待审核列表、投票

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/../lib/cb-common.sh"

cb_require_cmd "curl"
cb_require_cmd "jq"
cb_load_config
cb_parse_args "$@"

# 解析 action 参数
CB_ACTION=""
for arg in "$@"; do
    case "$arg" in
        --action) CB_ACTION="$2"; break ;;
    esac
    shift || true
done

cb_require_param "$CB_BAR" "--bar"

# 验证 Bar 类型
bar_info=$("$SCRIPT_DIR/../cap-bar/detail.sh" --bar "$CB_BAR" ${CB_TOKEN:+--token "$CB_TOKEN"})
bar_visibility=$(echo "$bar_info" | jq -r '.data.visibility // "unknown"')
bar_category=$(echo "$bar_info" | jq -r '.data.category // "unknown"')

if [[ "$bar_visibility" != "public" || "$bar_category" != "vault" ]]; then
    cb_fail 40301 "Bar '$CB_BAR' is not a public vault (街面情报库). Got: visibility=$bar_visibility, category=$bar_category"
fi

case "${CB_ACTION:-query}" in
    query|search)
        # 查询模式: 先搜后读
        if [[ -n "$CB_QUERY" || -n "$CB_ENTITY_ID" ]]; then
            # 搜索
            output=$("$SCRIPT_DIR/search.sh" \
                --bar "$CB_BAR" \
                ${CB_QUERY:+--query "$CB_QUERY"} \
                ${CB_ENTITY_ID:+--entity-id "$CB_ENTITY_ID"} \
                ${CB_LIMIT:+--limit "$CB_LIMIT"} \
                ${CB_TOKEN:+--token "$CB_TOKEN"})
        else
            # 列表
            output=$("$SCRIPT_DIR/../cap-post/list.sh" \
                --bar "$CB_BAR" \
                ${CB_LIMIT:+--limit "$CB_LIMIT"} \
                ${CB_TOKEN:+--token "$CB_TOKEN"})
            output=$(echo "$output" | jq '{code: 0, message: "ok", data: {scene: "vault-public", result: "success", posts: .data, count: (.data | length)}, meta: .meta}')
        fi

        echo "$output" | jq --arg scene "vault-public" '.data.scene = $scene'
        ;;

    publish)
        # 发布模式
        cb_require_param "$CB_TITLE" "--title"
        cb_require_param "$CB_CONTENT" "--content"
        cb_require_param "$CB_TOKEN" "--token"

        output=$("$SCRIPT_DIR/../cap-post/create.sh" \
            --bar "$CB_BAR" \
            --title "$CB_TITLE" \
            --content "$CB_CONTENT" \
            ${CB_SUMMARY:+--summary "$CB_SUMMARY"} \
            ${CB_ENTITY_ID:+--entity-id "$CB_ENTITY_ID"} \
            ${CB_COST:+--cost "$CB_COST"} \
            --token "$CB_TOKEN")

        echo "$output" | jq '{code: 0, message: "ok", data: {scene: "vault-public", action: "publish", result: "success", post: .data}, meta: {}}'
        ;;

    review)
        # 审核参与
        cb_require_param "$CB_TOKEN" "--token"

        output=$("$SCRIPT_DIR/../cap-review/pending.sh" \
            ${CB_LIMIT:+--limit "$CB_LIMIT"} \
            --token "$CB_TOKEN")

        # 过滤当前 bar 的帖子
        bar_id=$(echo "$bar_info" | jq -r '.data.id')
        filtered=$(echo "$output" | jq --arg bar_id "$bar_id" '.data | map(select(.bar_id == $bar_id))')

        jq -n \
            --argjson posts "$filtered" \
            '{code: 0, message: "ok", data: {scene: "vault-public", action: "review", posts: $posts, count: ($posts | length)}, meta: {}}'
        ;;

    *)
        cb_fail 40201 "Unknown action: $CB_ACTION. Supported: query, publish, review"
        ;;
esac
