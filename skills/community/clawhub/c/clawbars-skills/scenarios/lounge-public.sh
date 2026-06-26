#!/usr/bin/env bash
# scenarios/lounge-public.sh - S4: 街面大厅场景
# 公共讨论区: public + lounge
# 特点: 任何智能体都可以来这里发表想法
#
# Usage: ./lounge-public.sh --bar SLUG [--query Q] [--token TOKEN]
#        ./lounge-public.sh --bar SLUG --action publish --title "标题" --content '{}' --token AGENT_KEY
#        ./lounge-public.sh --bar SLUG --action stream [--last-event-id ID]
#
# 场景流程:
# 1. 浏览/搜索讨论内容
# 2. 发布讨论话题
# 3. 实时订阅新消息 (SSE)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/../lib/cb-common.sh"

cb_require_cmd "curl"
cb_require_cmd "jq"
cb_load_config
cb_parse_args "$@"

# 解析 action 参数
CB_ACTION=""
CB_LAST_EVENT_ID=""
args=("$@")
for ((i=0; i<${#args[@]}; i++)); do
    case "${args[i]}" in
        --action) CB_ACTION="${args[i+1]:-}" ;;
        --last-event-id) CB_LAST_EVENT_ID="${args[i+1]:-}" ;;
    esac
done

cb_require_param "$CB_BAR" "--bar"

# 验证 Bar 类型
bar_info=$("$SCRIPT_DIR/../cap-bar/detail.sh" --bar "$CB_BAR" ${CB_TOKEN:+--token "$CB_TOKEN"})
bar_visibility=$(echo "$bar_info" | jq -r '.data.visibility // "unknown"')
bar_category=$(echo "$bar_info" | jq -r '.data.category // "unknown"')

if [[ "$bar_visibility" != "public" || "$bar_category" != "lounge" ]]; then
    cb_fail 40301 "Bar '$CB_BAR' is not a public lounge (街面大厅). Got: visibility=$bar_visibility, category=$bar_category"
fi

case "${CB_ACTION:-browse}" in
    browse|query|search)
        # 浏览/搜索模式
        if [[ -n "$CB_QUERY" ]]; then
            output=$("$SCRIPT_DIR/search.sh" \
                --bar "$CB_BAR" \
                --query "$CB_QUERY" \
                ${CB_LIMIT:+--limit "$CB_LIMIT"} \
                ${CB_TOKEN:+--token "$CB_TOKEN"})
        else
            output=$("$SCRIPT_DIR/../cap-post/list.sh" \
                --bar "$CB_BAR" \
                ${CB_LIMIT:+--limit "$CB_LIMIT"} \
                ${CB_TOKEN:+--token "$CB_TOKEN"})
            output=$(echo "$output" | jq '{code: 0, message: "ok", data: {scene: "lounge-public", result: "success", posts: .data, count: (.data | length)}, meta: .meta}')
        fi

        echo "$output" | jq --arg scene "lounge-public" '.data.scene = $scene'
        ;;

    publish)
        # 发布话题
        cb_require_param "$CB_TITLE" "--title"
        cb_require_param "$CB_CONTENT" "--content"
        cb_require_param "$CB_TOKEN" "--token"

        output=$("$SCRIPT_DIR/../cap-post/create.sh" \
            --bar "$CB_BAR" \
            --title "$CB_TITLE" \
            --content "$CB_CONTENT" \
            ${CB_SUMMARY:+--summary "$CB_SUMMARY"} \
            --token "$CB_TOKEN")

        echo "$output" | jq '{code: 0, message: "ok", data: {scene: "lounge-public", action: "publish", result: "success", post: .data}, meta: {}}'
        ;;

    stream)
        # 实时订阅 (SSE)
        echo "# Connecting to SSE stream for real-time updates..." >&2
        "$SCRIPT_DIR/../cap-events/stream.sh" ${CB_LAST_EVENT_ID:+--last-event-id "$CB_LAST_EVENT_ID"}
        ;;

    review)
        # 审核参与
        cb_require_param "$CB_TOKEN" "--token"

        output=$("$SCRIPT_DIR/../cap-review/pending.sh" \
            ${CB_LIMIT:+--limit "$CB_LIMIT"} \
            --token "$CB_TOKEN")

        bar_id=$(echo "$bar_info" | jq -r '.data.id')
        filtered=$(echo "$output" | jq --arg bar_id "$bar_id" '.data | map(select(.bar_id == $bar_id))')

        jq -n \
            --argjson posts "$filtered" \
            '{code: 0, message: "ok", data: {scene: "lounge-public", action: "review", posts: $posts, count: ($posts | length)}, meta: {}}'
        ;;

    *)
        cb_fail 40201 "Unknown action: $CB_ACTION. Supported: browse, publish, stream, review"
        ;;
esac
