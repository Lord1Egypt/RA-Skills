#!/bin/bash
# FinStep MCP - 板块服务
# 用法: plates.sh <type> [params...]

BASE_URL="https://fintool-mcp.finstep.cn/plates"
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

TODAY=$(date +%Y-%m-%d)

case "$TYPE" in
    list)
        # 板块列表
        # 用法: plates.sh list [关键词] [类型]
        # 类型: concept=概念板块, industry=行业板块
        SECTOR="${3:-}"
        call_mcp "get_plate_list" "$(jq -n --arg keyword "$KEYWORD" --arg sector_type "$SECTOR" \
            '(if $keyword != "" then {keyword:$keyword} else {} end) +
             (if $sector_type != "" then {sector_type:$sector_type} else {} end)')"
        ;;
    ranking)
        # 板块涨跌排名
        # 用法: plates.sh ranking [日期] [数量]
        DATE="${2:-}"
        NUM="${3:-20}"
        call_mcp "get_plate_rate_ranking" "$(jq -n --arg trade_date "$DATE" --argjson num "$NUM" \
            '{num:$num} + (if $trade_date != "" then {trade_date:$trade_date} else {} end)')"
        ;;
    stock)
        # 查询股票所属板块
        # 用法: plates.sh stock "茅台" 或 plates.sh stock "600519"
        call_mcp "get_stock_plate" "$(jq -n --arg keyword "$KEYWORD" '{"keyword":$keyword}')"
        ;;
    stocks)
        # 板块成分股
        # 用法: plates.sh stocks "白酒" [页码] [每页数量]
        PAGE="${3:-1}"
        SIZE="${4:-50}"
        call_mcp "get_plate_stocks" "$(jq -n \
            --arg keyword "$KEYWORD" --argjson page "$PAGE" --argjson page_size "$SIZE" \
            '{"keyword":$keyword,"page":$page,"page_size":$page_size}')"
        ;;
    *)
        echo '{"error": "未知类型，支持: list [关键词] [类型], ranking [日期] [数量], stock <关键词>, stocks <关键词> [页码] [每页数量]"}'
        exit 1
        ;;
esac
