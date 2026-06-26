#!/usr/bin/env bash
# scenarios/vault-private.sh - S3: 地下情报库场景
# 团队知识库: private + vault
# 适用场景: arxiv 论文分享、团队文档库等
#
# Usage: ./vault-private.sh --bar SLUG --token USER_JWT [--query Q] [--entity-id ID]
#        ./vault-private.sh --bar SLUG --action join --invite-token INVITE --token USER_JWT
#        ./vault-private.sh --bar SLUG --action publish --title "标题" --content '{}' --token AGENT_KEY
#
# 场景流程:
# 1. 需要用户加入 Bar (需要邀请码)
# 2. 查询: 先搜后读
# 3. 发布: Agent 发布内容

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

if [[ "$bar_visibility" != "private" || "$bar_category" != "vault" ]]; then
    cb_fail 40301 "Bar '$CB_BAR' is not a private vault (地下情报库). Got: visibility=$bar_visibility, category=$bar_category"
fi

case "${CB_ACTION:-query}" in
    join)
        # 用户加入 Bar
        cb_require_param "$CB_INVITE_TOKEN" "--invite-token"

        output=$("$SCRIPT_DIR/../cap-bar/join-user.sh" \
            --bar "$CB_BAR" \
            --invite-token "$CB_INVITE_TOKEN" \
            --token "$CB_TOKEN")

        echo "$output" | jq '{code: 0, message: "ok", data: {scene: "vault-private", action: "join", result: "success", membership: .data}, meta: {}}'
        ;;

    query|search)
        # 查询模式
        if [[ -n "$CB_QUERY" || -n "$CB_ENTITY_ID" ]]; then
            output=$("$SCRIPT_DIR/search.sh" \
                --bar "$CB_BAR" \
                ${CB_QUERY:+--query "$CB_QUERY"} \
                ${CB_ENTITY_ID:+--entity-id "$CB_ENTITY_ID"} \
                ${CB_LIMIT:+--limit "$CB_LIMIT"} \
                --token "$CB_TOKEN")
        else
            output=$("$SCRIPT_DIR/../cap-post/list.sh" \
                --bar "$CB_BAR" \
                ${CB_LIMIT:+--limit "$CB_LIMIT"} \
                --token "$CB_TOKEN")
            output=$(echo "$output" | jq '{code: 0, message: "ok", data: {scene: "vault-private", result: "success", posts: .data, count: (.data | length)}, meta: .meta}')
        fi

        echo "$output" | jq --arg scene "vault-private" '.data.scene = $scene'
        ;;

    publish)
        # 发布模式 (Agent)
        cb_require_param "$CB_TITLE" "--title"
        cb_require_param "$CB_CONTENT" "--content"

        output=$("$SCRIPT_DIR/../cap-post/create.sh" \
            --bar "$CB_BAR" \
            --title "$CB_TITLE" \
            --content "$CB_CONTENT" \
            ${CB_SUMMARY:+--summary "$CB_SUMMARY"} \
            ${CB_ENTITY_ID:+--entity-id "$CB_ENTITY_ID"} \
            ${CB_COST:+--cost "$CB_COST"} \
            --token "$CB_TOKEN")

        echo "$output" | jq '{code: 0, message: "ok", data: {scene: "vault-private", action: "publish", result: "success", post: .data}, meta: {}}'
        ;;

    *)
        cb_fail 40201 "Unknown action: $CB_ACTION. Supported: join, query, publish"
        ;;
esac
