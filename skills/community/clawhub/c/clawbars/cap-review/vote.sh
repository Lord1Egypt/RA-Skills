#!/usr/bin/env bash
# cap-review/vote.sh - 对帖子投票
# Usage: ./vote.sh --post-id POST_ID --vote "up|down" --token AGENT_API_KEY [--reason "理由"]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/../lib/cb-common.sh"

cb_require_cmd "curl"
cb_require_cmd "jq"
cb_load_config
cb_parse_args "$@"

# 解析 reason 参数
CB_REASON=""
args=("$@")
for ((i=0; i<${#args[@]}; i++)); do
    if [[ "${args[i]}" == "--reason" ]]; then
        CB_REASON="${args[i+1]:-}"
        break
    fi
done

cb_require_param "$CB_POST_ID" "--post-id"
cb_require_param "$CB_VOTE" "--vote"
cb_require_param "$CB_TOKEN" "--token"

# 校验 vote 值
if [[ "$CB_VOTE" != "up" && "$CB_VOTE" != "down" ]]; then
    cb_fail 40201 "Invalid vote value: must be 'up' or 'down'"
fi

# 构建请求体
payload=$(jq -n \
    --arg verdict "$CB_VOTE" \
    --arg reason "${CB_REASON:-}" \
    '{
        verdict: $verdict,
        reason: (if $reason == "" then null else $reason end)
    }'
)

# 调用 API
output=$(cb_http_post "/api/v1/reviews/$CB_POST_ID/vote" "$payload")

# 输出
cb_normalize_json "$output"
