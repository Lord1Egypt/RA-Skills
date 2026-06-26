#!/bin/bash
# FinStep MCP - 搜索服务
# 用法: search.sh <type> [keyword]
# type: news, report, announcement, morning, opinion, weixin, community

BASE_URL="https://fintool-mcp.finstep.cn/news"
SIGNATURE="${FINSTEP_SIGNATURE:?需要设置环境变量 FINSTEP_SIGNATURE}"

TYPE="$1"
KEYWORD="$2"

call_mcp() {
    local tool="$1"
    local params="$2"

    curl -s -X POST "${BASE_URL}?signature=${SIGNATURE}" \
        -H "Content-Type: application/json" \
        -H "Accept: application/json, text/event-stream" \
        --max-time 30 \
        -d "$(jq -n --arg name "$tool" --argjson arguments "$params" \
            '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":$name,"arguments":$arguments}}')"
}

case "$TYPE" in
    news)
        call_mcp "search_news" "$(jq -n --arg query "$KEYWORD" '{"query":$query,"limit":10}')"
        ;;
    report)
        call_mcp "search_report" "$(jq -n --arg query "$KEYWORD" '{"query":$query,"limit":10}')"
        ;;
    announcement)
        call_mcp "search_announcement" "$(jq -n --arg query "$KEYWORD" '{"query":$query,"limit":10}')"
        ;;
    morning)
        call_mcp "get_alpha_morning" "{}"
        ;;
    opinion)
        call_mcp "search_opinion" "$(jq -n --arg query "$KEYWORD" '{"query":$query,"limit":10}')"
        ;;
    weixin)
        call_mcp "search_mp_weixin" "$(jq -n --arg query "$KEYWORD" '{"query":$query,"limit":10}')"
        ;;
    community)
        call_mcp "search_community_forum" "$(jq -n --arg query "$KEYWORD" '{"query":$query,"limit":10}')"
        ;;
    web)
        call_mcp "web_search" "$(jq -n --arg query "$KEYWORD" '{"query":$query,"limit":10}')"
        ;;
    *)
        echo '{"error": "未知类型，支持: news, report, announcement, morning, opinion, weixin, community, web"}'
        exit 1
        ;;
esac
