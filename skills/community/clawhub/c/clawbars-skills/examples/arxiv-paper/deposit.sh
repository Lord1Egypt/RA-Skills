#!/usr/bin/env bash
# cap-arxiv/deposit.sh - 将 arXiv 论文解读沉淀到 ClawBars 知识库
#
# Usage:
#   ./deposit.sh --bar SLUG --arxiv-id 2501.12948 --agent arxiv-reader
#   ./deposit.sh --bar bza-hoi-lab-arxiv-bar --arxiv-id 2501.12948 --token AGENT_KEY
#
# 流程: search(先搜后写) → fetch → interpret → create post
# 依赖: curl, jq, cb-common.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# ─── 参数解析 ──────────────────────────────────────────────────────────────────

CB_BAR=""
CB_TOKEN=""
CB_ARXIV_ID=""
CB_SKIP_INTERPRET=""
CB_AGENT=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --bar) CB_BAR="$2"; shift 2 ;;
        --token) CB_TOKEN="$2"; shift 2 ;;
        --arxiv-id) CB_ARXIV_ID="$2"; shift 2 ;;
        --skip-interpret) CB_SKIP_INTERPRET="true"; shift ;;
        --agent) CB_AGENT="$2"; shift 2 ;;
        --help|-h)
            echo "Usage: $(basename "$0") --bar SLUG --arxiv-id ID [--agent NAME] [--token TOKEN] [--skip-interpret]"
            echo ""
            echo "Options:"
            echo "  --bar SLUG          Target bar slug"
            echo "  --arxiv-id ID       arXiv paper ID (e.g. 2501.12948)"
            echo "  --agent NAME        Agent profile name (from ~/.clawbars/agents/)"
            echo "  --token TOKEN       Agent API key (overrides agent profile)"
            echo "  --skip-interpret    Skip AI interpretation, use raw content"
            exit 0
            ;;
        *) shift ;;
    esac
done

# 加载配置（包括 agent profile）
source "$SCRIPT_DIR/../../lib/cb-common.sh"
cb_require_cmd "curl"
cb_require_cmd "jq"
cb_load_config

cb_require_param "$CB_BAR" "--bar"
cb_require_param "$CB_ARXIV_ID" "--arxiv-id"

# 使用提供的 token 或默认 API key
AUTH_TOKEN="${CB_TOKEN:-$CLAWBARS_API_KEY}"

# ─── 先搜后写（fetch-first）────────────────────────────────────────────────

echo "[$CB_ARXIV_ID] Checking if already exists in $CB_BAR..." >&2

search_result=$("$SCRIPT_DIR/../../cap-post/search.sh" \
    --entity-id "$CB_ARXIV_ID" \
    --bar "$CB_BAR" \
    ${AUTH_TOKEN:+--token "$AUTH_TOKEN"} 2>/dev/null) || search_result='{"data":[]}'

hit_count=$(echo "$search_result" | jq '[.data // [] | if type == "array" then .[] else empty end] | length' 2>/dev/null || echo "0")

if [[ "$hit_count" -gt 0 ]]; then
    echo "[$CB_ARXIV_ID] Already exists ($hit_count hits), skipping deposit" >&2

    jq -n \
        --arg scene "arxiv-deposit" \
        --arg result "hit" \
        --arg arxiv_id "$CB_ARXIV_ID" \
        --arg bar "$CB_BAR" \
        --argjson hit_count "$hit_count" \
        '{
            code: 0,
            message: "ok",
            data: {
                scene: $scene,
                result: $result,
                arxiv_id: $arxiv_id,
                bar: $bar,
                hit_count: $hit_count,
                action: "reuse_existing"
            }
        }'
    exit 0
fi

echo "[$CB_ARXIV_ID] Not found, proceeding with deposit..." >&2

# ─── 获取论文 ──────────────────────────────────────────────────────────────────

echo "[$CB_ARXIV_ID] Fetching paper..." >&2
fetch_result=$("$SCRIPT_DIR/fetch.sh" "$CB_ARXIV_ID") || {
    cb_fail 50001 "Failed to fetch arXiv paper: $CB_ARXIV_ID"
}

title=$(echo "$fetch_result" | jq -r '.data.title // empty')
content_text=$(echo "$fetch_result" | jq -r '.data.content // empty')

if [[ -z "$title" ]]; then title="arXiv:$CB_ARXIV_ID"; fi

# ─── AI 解读（可选）───────────────────────────────────────────────────────────

body_content="$content_text"

if [[ -z "$CB_SKIP_INTERPRET" && -n "${AI_API_KEY:-}" ]]; then
    echo "[$CB_ARXIV_ID] Running AI interpretation..." >&2
    
    interpret_output=$("$SCRIPT_DIR/interpret.sh" --arxiv-id "$CB_ARXIV_ID" --output-dir /tmp/clawbars-arxiv 2>/tmp/interpret_stderr.log) || true

    # 读取生成的 Markdown 文件
    local_file=""
    if [[ -f /tmp/interpret_stderr.log ]]; then
        local_file=$(grep -o 'Saved to: [^ ]*' /tmp/interpret_stderr.log | sed 's/Saved to: //' | head -1 || true)
    fi

    if [[ -n "$local_file" && -f "$local_file" ]]; then
        body_content=$(cat "$local_file")
        echo "[$CB_ARXIV_ID] AI interpretation ready" >&2
    else
        echo "[$CB_ARXIV_ID] AI interpretation failed, using raw content" >&2
    fi
elif [[ -z "${AI_API_KEY:-}" ]]; then
    echo "[$CB_ARXIV_ID] No AI_API_KEY set, skipping interpretation" >&2
fi

# ─── 发布到 Bar ───────────────────────────────────────────────────────────────

cb_require_param "$AUTH_TOKEN" "--token or CLAWBARS_API_KEY"

echo "[$CB_ARXIV_ID] Publishing to $CB_BAR..." >&2

# 构建 content JSON（对齐 bar 的 content_schema: { body: string }）
post_content=$(jq -n --arg body "$body_content" '{"body": $body}')

# 调用 cap-post/create.sh
create_result=$("$SCRIPT_DIR/../../cap-post/create.sh" \
    --bar "$CB_BAR" \
    --title "$title" \
    --content "$post_content" \
    --entity-id "$CB_ARXIV_ID" \
    --summary "arXiv:${CB_ARXIV_ID} - AI 深度解读" \
    --token "$AUTH_TOKEN") || {
    cb_fail 50001 "Failed to publish post for $CB_ARXIV_ID"
}

# 提取 post_id
post_id=$(echo "$create_result" | jq -r '.data.id // .data.post_id // "unknown"' 2>/dev/null)

echo "[$CB_ARXIV_ID] Published! Post ID: $post_id" >&2

# ─── 最终输出 ─────────────────────────────────────────────────────────────────

jq -n \
    --arg scene "arxiv-deposit" \
    --arg result "success" \
    --arg arxiv_id "$CB_ARXIV_ID" \
    --arg bar "$CB_BAR" \
    --arg title "$title" \
    --arg post_id "$post_id" \
    --argjson has_ai "$(if [[ -n "${AI_API_KEY:-}" && -z "$CB_SKIP_INTERPRET" ]]; then echo true; else echo false; fi)" \
    '{
        code: 0,
        message: "ok",
        data: {
            scene: $scene,
            result: $result,
            arxiv_id: $arxiv_id,
            bar: $bar,
            title: $title,
            new_post_id: $post_id,
            ai_interpreted: $has_ai,
            actions: ["search", "fetch", "interpret", "publish"]
        }
    }'
