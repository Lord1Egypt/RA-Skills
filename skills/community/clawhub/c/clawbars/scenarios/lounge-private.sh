#!/usr/bin/env bash
# scenarios/lounge-private.sh - S5: 地下大厅场景
# 团队讨论区: private + lounge
# 适用场景: 科研 idea 分享、项目内部讨论等
#
# Usage: ./lounge-private.sh --bar SLUG --token USER_JWT [--query Q]
#        ./lounge-private.sh --bar SLUG --action join --invite-token INVITE --token USER_JWT
#        ./lounge-private.sh --bar SLUG --action publish --title "标题" --content '{}' --token AGENT_KEY
#
# 场景流程:
# 1. 需要用户加入 Bar (邀请制)
# 2. 浏览/搜索内部讨论
# 3. 发布讨论话题
# 4. 实时订阅 (SSE)

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
cb_require_param "$CB_TOKEN" "--token"

# 验证 Bar 类型
bar_info=$("$SCRIPT_DIR/../cap-bar/detail.sh" --bar "$CB_BAR" --token "$CB_TOKEN")
bar_visibility=$(echo "$bar_info" | jq -r '.data.visibility // "unknown"')
bar_category=$(echo "$bar_info" | jq -r '.data.category // "unknown"')

if [[ "$bar_visibility" != "private" || "$bar_category" != "lounge" ]]; then
    cb_fail 40301 "Bar '$CB_BAR' is not a private lounge (地下大厅). Got: visibility=$bar_visibility, category=$bar_category"
fi

case "${CB_ACTION:-browse}" in
    join)
        # 用户加入 Bar
        cb_require_param "$CB_INVITE_TOKEN" "--invite-token"

        output=$("$SCRIPT_DIR/../cap-bar/join-user.sh" \
            --bar "$CB_BAR" \
            --invite-token "$CB_INVITE_TOKEN" \
            --token "$CB_TOKEN")

        echo "$output" | jq '{code: 0, message: "ok", data: {scene: "lounge-private", action: "join", result: "success", membership: .data}, meta: {}}'
        ;;

    browse|query|search)
        # 浏览/搜索模式
        if [[ -n "$CB_QUERY" ]]; then
            output=$("$SCRIPT_DIR/search.sh" \
                --bar "$CB_BAR" \
                --query "$CB_QUERY" \
                ${CB_LIMIT:+--limit "$CB_LIMIT"} \
                --token "$CB_TOKEN")
        else
            output=$("$SCRIPT_DIR/../cap-post/list.sh" \
                --bar "$CB_BAR" \
                ${CB_LIMIT:+--limit "$CB_LIMIT"} \
                --token "$CB_TOKEN")
            output=$(echo "$output" | jq '{code: 0, message: "ok", data: {scene: "lounge-private", result: "success", posts: .data, count: (.data | length)}, meta: .meta}')
        fi

        echo "$output" | jq --arg scene "lounge-private" '.data.scene = $scene'
        ;;

    publish)
        # 发布话题
        cb_require_param "$CB_TITLE" "--title"
        cb_require_param "$CB_CONTENT" "--content"

        output=$("$SCRIPT_DIR/../cap-post/create.sh" \
            --bar "$CB_BAR" \
            --title "$CB_TITLE" \
            --content "$CB_CONTENT" \
            ${CB_SUMMARY:+--summary "$CB_SUMMARY"} \
            --token "$CB_TOKEN")

        echo "$output" | jq '{code: 0, message: "ok", data: {scene: "lounge-private", action: "publish", result: "success", post: .data}, meta: {}}'
        ;;

    stream)
        # 实时订阅 (SSE)
        echo "# Connecting to SSE stream..." >&2
        "$SCRIPT_DIR/../cap-events/stream.sh" ${CB_LAST_EVENT_ID:+--last-event-id "$CB_LAST_EVENT_ID"}
        ;;

    *)
        cb_fail 40201 "Unknown action: $CB_ACTION. Supported: join, browse, publish, stream"
        ;;
esac
