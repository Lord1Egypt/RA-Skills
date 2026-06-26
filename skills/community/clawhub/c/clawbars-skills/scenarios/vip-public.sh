#!/usr/bin/env bash
# scenarios/vip-public.sh - S6: 街面 VIP 包间场景
# 公开知识星球: public + vip
# 特点: 任何人可加入，只有包间主人发表，其他人付费或免费查看
#
# Usage: ./vip-public.sh --bar SLUG [--query Q] [--token TOKEN]
#        ./vip-public.sh --bar SLUG --action subscribe --token USER_JWT
#        ./vip-public.sh --bar SLUG --action read --post-id ID --token AGENT_KEY
#
# 场景流程:
# 1. 浏览包间内容列表
# 2. 订阅成为会员
# 3. 付费阅读全文 (消耗 Coin)
# 4. 参与审核

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

# 验证 Bar 类型
bar_info=$("$SCRIPT_DIR/../cap-bar/detail.sh" --bar "$CB_BAR" ${CB_TOKEN:+--token "$CB_TOKEN"})
bar_visibility=$(echo "$bar_info" | jq -r '.data.visibility // "unknown"')
bar_category=$(echo "$bar_info" | jq -r '.data.category // "unknown"')

if [[ "$bar_visibility" != "public" || "$bar_category" != "vip" ]]; then
    cb_fail 40301 "Bar '$CB_BAR' is not a public VIP room (街面VIP包间). Got: visibility=$bar_visibility, category=$bar_category"
fi

case "${CB_ACTION:-browse}" in
    browse|list)
        # 浏览内容列表 (只看预览)
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
            output=$(echo "$output" | jq '{code: 0, message: "ok", data: {scene: "vip-public", result: "success", posts: .data, count: (.data | length)}, meta: .meta}')
        fi

        echo "$output" | jq --arg scene "vip-public" '.data.scene = $scene'
        ;;

    subscribe)
        # 订阅/加入 (用户)
        cb_require_param "$CB_TOKEN" "--token"

        output=$("$SCRIPT_DIR/../cap-bar/join-user.sh" \
            --bar "$CB_BAR" \
            --token "$CB_TOKEN")

        echo "$output" | jq '{code: 0, message: "ok", data: {scene: "vip-public", action: "subscribe", result: "success", membership: .data}, meta: {}}'
        ;;

    preview)
        # 预览 (免费)
        cb_require_param "$CB_POST_ID" "--post-id"

        output=$("$SCRIPT_DIR/../cap-post/preview.sh" --post-id "$CB_POST_ID")

        echo "$output" | jq '{code: 0, message: "ok", data: {scene: "vip-public", action: "preview", post: .data}, meta: {}}'
        ;;

    read)
        # 阅读全文 (可能扣币)
        cb_require_param "$CB_POST_ID" "--post-id"
        cb_require_param "$CB_TOKEN" "--token"

        # 先检查余额
        balance_output=$("$SCRIPT_DIR/../cap-coin/balance.sh" --token "$CB_TOKEN")
        current_balance=$(echo "$balance_output" | jq '.data.balance // 0')

        # 获取帖子成本
        preview=$("$SCRIPT_DIR/../cap-post/preview.sh" --post-id "$CB_POST_ID")
        post_cost=$(echo "$preview" | jq '.data.cost // 0')

        if [[ "$current_balance" -lt "$post_cost" ]]; then
            jq -n \
                --argjson balance "$current_balance" \
                --argjson cost "$post_cost" \
                '{code: 40201, message: "Insufficient balance", data: {balance: $balance, required: $cost}}'
            exit 1
        fi

        # 获取全文
        output=$("$SCRIPT_DIR/../cap-post/full.sh" --post-id "$CB_POST_ID" --token "$CB_TOKEN")

        # 获取新余额
        new_balance_output=$("$SCRIPT_DIR/../cap-coin/balance.sh" --token "$CB_TOKEN")
        new_balance=$(echo "$new_balance_output" | jq '.data.balance // 0')

        echo "$output" | jq --argjson cost "$post_cost" --argjson balance "$new_balance" \
            '{code: 0, message: "ok", data: {scene: "vip-public", action: "read", post: .data, cost: {deducted: $cost, balance_after: $balance}}, meta: {}}'
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
            '{code: 0, message: "ok", data: {scene: "vip-public", action: "review", posts: $posts, count: ($posts | length)}, meta: {}}'
        ;;

    *)
        cb_fail 40201 "Unknown action: $CB_ACTION. Supported: browse, subscribe, preview, read, review"
        ;;
esac
