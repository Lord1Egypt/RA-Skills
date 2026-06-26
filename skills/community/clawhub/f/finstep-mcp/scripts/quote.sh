#!/bin/bash
# FinStep MCP - 行情服务
# 用法: quote.sh <type> [params...]

BASE_URL="https://fintool-mcp.finstep.cn/market_quote"
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

# 获取今天日期
TODAY=$(date +%Y-%m-%d)

case "$TYPE" in
    snapshot)
        # 个股实时行情快照
        # 用法: quote.sh snapshot "茅台" 或 quote.sh snapshot "600519"
        call_mcp "get_snapshot" "$(jq -n --arg keyword "$KEYWORD" '{"keyword":$keyword}')"
        ;;
    snapshot_plate)
        # 板块实时行情快照
        call_mcp "get_snapshot" "$(jq -n --arg keyword "$KEYWORD" '{"keyword":$keyword,"is_plate":true}')"
        ;;
    intraday)
        # 分时图数据
        call_mcp "get_intraday" "$(jq -n --arg keyword "$KEYWORD" '{"keyword":$keyword}')"
        ;;
    kline)
        # K线数据
        # 用法: quote.sh kline "600519" [数量] [类型] [复权]
        # 类型: 1=日K, 2=周K, 3=月K (默认1)
        # 复权: 1=不复权, 2=前复权, 3=后复权 (默认2)
        NUM="${3:-30}"
        KTYPE="${4:-1}"
        REINST="${5:-2}"
        call_mcp "get_kline" "$(jq -n \
            --arg keyword "$KEYWORD" --arg end_date "$TODAY" \
            --argjson kline_num "$NUM" --argjson kline_type "$KTYPE" --argjson reinstatement_type "$REINST" \
            '{"keyword":$keyword,"end_date":$end_date,"kline_num":$kline_num,"kline_type":$kline_type,"reinstatement_type":$reinstatement_type}')"
        ;;
    market)
        # 大盘行情快照
        call_mcp "get_market_snapshot" "{}"
        ;;
    leader)
        # 龙虎榜
        # 用法: quote.sh leader [日期] [关键词]
        DATE="${2:-${TODAY}}"
        KW="${3:-}"
        call_mcp "get_leader_board" "$(jq -n --arg trade_date "$DATE" --arg keyword "$KW" \
            '{trade_date:$trade_date} + (if $keyword != "" then {keyword:$keyword} else {} end)')"
        ;;
    flow)
        # 资金流向
        # 用法: quote.sh flow "600519" [结束日期] [开始日期]
        END="${3:-${TODAY}}"
        START="${4:-}"
        call_mcp "get_net_flow_list" "$(jq -n \
            --arg keyword "$KEYWORD" --arg end_date "$END" --arg start_date "$START" \
            '{keyword:$keyword,end_date:$end_date} + (if $start_date != "" then {start_date:$start_date} else {} end)')"
        ;;
    trending)
        # 热门行业
        # 用法: quote.sh trending [日期]
        DATE="${2:-}"
        call_mcp "get_trending_industry" "$(jq -n --arg date "$DATE" \
            'if $date != "" then {date:$date} else {} end')"
        ;;
    calendar)
        # 投资日历
        # 用法: quote.sh calendar [开始日期] [结束日期]
        START="${2:-${TODAY}}"
        END="${3:-${TODAY}}"
        call_mcp "get_invest_calendar" "$(jq -n --arg start_date "$START" --arg end_date "$END" \
            '{"start_date":$start_date,"end_date":$end_date}')"
        ;;
    status)
        # 全市场股票状态
        # 用法: quote.sh status [日期] [页码] [每页数量]
        DATE="${2:-${TODAY}}"
        PAGE="${3:-1}"
        SIZE="${4:-100}"
        call_mcp "get_all_stock_status" "$(jq -n \
            --arg date "$DATE" --argjson page "$PAGE" --argjson page_size "$SIZE" \
            '{"date":$date,"page":$page,"page_size":$page_size}')"
        ;;
    hk_kline)
        # 港股K线
        # 用法: quote.sh hk_kline "00700" [数量]
        NUM="${3:-30}"
        call_mcp "get_hk_stock_kline" "$(jq -n \
            --arg keyword "$KEYWORD" --arg end_date "$TODAY" --argjson kline_num "$NUM" \
            '{"keyword":$keyword,"end_date":$end_date,"kline_num":$kline_num}')"
        ;;
    us_kline)
        # 美股K线
        # 用法: quote.sh us_kline "AAPL" [数量]
        NUM="${3:-30}"
        call_mcp "get_us_stock_kline" "$(jq -n \
            --arg keyword "$KEYWORD" --arg end_date "$TODAY" --argjson kline_num "$NUM" \
            '{"keyword":$keyword,"end_date":$end_date,"kline_num":$kline_num}')"
        ;;
    block_trade)
        # 大宗交易
        # 用法: quote.sh block_trade "600519" [开始日期] [结束日期]
        START="${3:-${TODAY}}"
        END="${4:-${TODAY}}"
        call_mcp "get_block_trade_detail" "$(jq -n \
            --arg keyword "$KEYWORD" --arg start_date "$START" --arg end_date "$END" \
            '{"keyword":$keyword,"start_date":$start_date,"end_date":$end_date}')"
        ;;
    patterns)
        # 股票形态
        # 用法: quote.sh patterns "600519" [开始日期] [结束日期]
        START="${3:-${TODAY}}"
        END="${4:-${TODAY}}"
        call_mcp "get_stock_patterns" "$(jq -n \
            --arg keyword "$KEYWORD" --arg start_date "$START" --arg end_date "$END" \
            '{"keyword":$keyword,"start_date":$start_date,"end_date":$end_date}')"
        ;;
    *)
        echo '{"error": "未知类型，支持: snapshot, snapshot_plate, intraday, kline, market, leader, flow, trending, calendar, status, hk_kline, us_kline, block_trade, patterns"}'
        exit 1
        ;;
esac
