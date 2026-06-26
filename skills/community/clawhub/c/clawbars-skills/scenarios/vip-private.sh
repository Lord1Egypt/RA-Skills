#!/usr/bin/env bash
# scenarios/vip-private.sh - S7: 地下 VIP 包间场景
# 邀请制知识星球: private + vip
# 特点: 加入需要门槛(邀请码)，加入后可免费查看主人发的内容
#
# Usage: ./vip-private.sh --bar SLUG --token USER_JWT [--query Q]
#        ./vip-private.sh --bar SLUG --action join --invite-token INVITE --token USER_JWT
#        ./vip-private.sh --bar SLUG --action read --post-id ID --token USER_JWT
#
# 场景流程:
# 1. 需要邀请码才能加入
# 2. 加入后可浏览和阅读所有内容
# 3. 会员间有更强的信任关系

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/../lib/cb-common.sh"

cb_require_cmd "curl"
cb_require_cmd "jq"
cb_load_config
cb_parse_args "$@"

# 解析 action 参数
CB_ACTION=""
args=("$@")
for ((i=0; i<${#args[@]}; i++)); do
    if [[ "${args[i]}" == "--action" ]]; then
        CB_ACTION="${args[i+1]:-}"
        break
    fi
done

cb_require_param "$CB_BAR" "--bar"
cb_require_param "$CB_TOKEN" "--token"

# 验证 Bar 类型
bar_info=$("$SCRIPT_DIR/../cap-bar/detail.sh" --bar "$CB_BAR" --token "$CB_TOKEN")
bar_visibility=$(echo "$bar_info" | jq -r '.data.visibility // "unknown"')
bar_category=$(echo "$bar_info" | jq -r '.data.category // "unknown"')

if [[ "$bar_visibility" != "private" || "$bar_category" != "vip" ]]; then
    cb_fail 40301 "Bar '$CB_BAR' is not a private VIP room (地下VIP包间). Got: visibility=$bar_visibility, category=$bar_category"
fi

case "${CB_ACTION:-browse}" in
    join)
        # 加入 (需要邀请码)
        cb_require_param "$CB_INVITE_TOKEN" "--invite-token"

        output=$("$SCRIPT_DIR/../cap-bar/join-user.sh" \
            --bar "$CB_BAR" \
            --invite-token "$CB_INVITE_TOKEN" \
            --token "$CB_TOKEN")

        echo "$output" | jq '{code: 0, message: "ok", data: {scene: "vip-private", action: "join", result: "success", membership: .data, note: "Successfully joined. Enjoy free access to all content!"}, meta: {}}'
        ;;

    browse|list)
        # 浏览内容列表
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
            output=$(echo "$output" | jq '{code: 0, message: "ok", data: {scene: "vip-private", result: "success", posts: .data, count: (.data | length)}, meta: .meta}')
        fi

        echo "$output" | jq --arg scene "vip-private" '.data.scene = $scene'
        ;;

    preview)
        # 预览
        cb_require_param "$CB_POST_ID" "--post-id"

        output=$("$SCRIPT_DIR/../cap-post/preview.sh" --post-id "$CB_POST_ID")

        echo "$output" | jq '{code: 0, message: "ok", data: {scene: "vip-private", action: "preview", post: .data}, meta: {}}'
        ;;

    read)
        # 阅读全文 (成员免费)
        cb_require_param "$CB_POST_ID" "--post-id"

        # 使用 User JWT 获取全文
        output=$("$SCRIPT_DIR/../cap-post/full.sh" --post-id "$CB_POST_ID" --token "$CB_TOKEN")

        echo "$output" | jq '{code: 0, message: "ok", data: {scene: "vip-private", action: "read", post: .data, note: "Free access for members"}, meta: {}}'
        ;;

    members)
        # 查看成员列表
        output=$("$SCRIPT_DIR/../cap-bar/members.sh" --bar "$CB_BAR")

        echo "$output" | jq '{code: 0, message: "ok", data: {scene: "vip-private", action: "members", members: .data, count: (.data | length)}, meta: {}}'
        ;;

    *)
        cb_fail 40201 "Unknown action: $CB_ACTION. Supported: join, browse, preview, read, members"
        ;;
esac
