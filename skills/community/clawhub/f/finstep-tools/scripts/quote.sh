#!/bin/bash
# FinStep MCP - 行情服务
# 用法: quote.sh <type> [params...]

BASE_URL="http://fintool-mcp.finstep.cn/market_quote"
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
        -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"tools/call\",\"params\":{\"name\":\"${tool}\",\"arguments\":${params}}}"
}

# 获取今天日期
TODAY=$(date +%Y-%m-%d)

case "$TYPE" in
    snapshot)
        # 个股实时行情快照
        # 用法: quote.sh snapshot "茅台" 或 quote.sh snapshot "600519"
        call_mcp "get_snapshot" "{\"keyword\":\"${KEYWORD}\"}"
        ;;
    snapshot_plate)
        # 板块实时行情快照
        call_mcp "get_snapshot" "{\"keyword\":\"${KEYWORD}\",\"is_plate\":true}"
        ;;
    intraday)
        # 分时图数据
        call_mcp "get_intraday" "{\"keyword\":\"${KEYWORD}\"}"
        ;;
    kline)
        # K线数据
        # 用法: quote.sh kline "600519" [数量] [类型] [复权]
        # 类型: 1=日K, 2=周K, 3=月K (默认1)
        # 复权: 1=不复权, 2=前复权, 3=后复权 (默认2)
        NUM="${3:-30}"
        KTYPE="${4:-1}"
        REINST="${5:-2}"
        call_mcp "get_kline" "{\"keyword\":\"${KEYWORD}\",\"end_date\":\"${TODAY}\",\"kline_num\":${NUM},\"kline_type\":${KTYPE},\"reinstatement_type\":${REINST}}"
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
        if [ -n "$KW" ]; then
            call_mcp "get_leader_board" "{\"trade_date\":\"${DATE}\",\"keyword\":\"${KW}\"}"
        else
            call_mcp "get_leader_board" "{\"trade_date\":\"${DATE}\"}"
        fi
        ;;
    flow)
        # 资金流向
        # 用法: quote.sh flow "600519" [结束日期] [开始日期]
        END="${3:-${TODAY}}"
        START="${4:-}"
        if [ -n "$START" ]; then
            call_mcp "get_net_flow_list" "{\"keyword\":\"${KEYWORD}\",\"end_date\":\"${END}\",\"start_date\":\"${START}\"}"
        else
            call_mcp "get_net_flow_list" "{\"keyword\":\"${KEYWORD}\",\"end_date\":\"${END}\"}"
        fi
        ;;
    trending)
        # 热门行业
        # 用法: quote.sh trending [日期]
        DATE="${2:-}"
        if [ -n "$DATE" ]; then
            call_mcp "get_trending_industry" "{\"date\":\"${DATE}\"}"
        else
            call_mcp "get_trending_industry" "{}"
        fi
        ;;
    calendar)
        # 投资日历
        # 用法: quote.sh calendar [开始日期] [结束日期]
        START="${2:-${TODAY}}"
        END="${3:-${TODAY}}"
        call_mcp "get_invest_calendar" "{\"start_date\":\"${START}\",\"end_date\":\"${END}\"}"
        ;;
    status)
        # 全市场股票状态
        # 用法: quote.sh status [日期] [页码] [每页数量]
        DATE="${2:-${TODAY}}"
        PAGE="${3:-1}"
        SIZE="${4:-100}"
        call_mcp "get_all_stock_status" "{\"date\":\"${DATE}\",\"page\":${PAGE},\"page_size\":${SIZE}}"
        ;;
    hk_kline)
        # 港股K线
        # 用法: quote.sh hk_kline "00700" [数量]
        NUM="${3:-30}"
        call_mcp "get_hk_stock_kline" "{\"keyword\":\"${KEYWORD}\",\"end_date\":\"${TODAY}\",\"kline_num\":${NUM}}"
        ;;
    us_kline)
        # 美股K线
        # 用法: quote.sh us_kline "AAPL" [数量]
        NUM="${3:-30}"
        call_mcp "get_us_stock_kline" "{\"keyword\":\"${KEYWORD}\",\"end_date\":\"${TODAY}\",\"kline_num\":${NUM}}"
        ;;
    block_trade)
        # 大宗交易
        # 用法: quote.sh block_trade "600519" [开始日期] [结束日期]
        START="${3:-${TODAY}}"
        END="${4:-${TODAY}}"
        call_mcp "get_block_trade_detail" "{\"keyword\":\"${KEYWORD}\",\"start_date\":\"${START}\",\"end_date\":\"${END}\"}"
        ;;
    patterns)
        # 股票形态
        # 用法: quote.sh patterns "600519" [开始日期] [结束日期]
        START="${3:-${TODAY}}"
        END="${4:-${TODAY}}"
        call_mcp "get_stock_patterns" "{\"keyword\":\"${KEYWORD}\",\"start_date\":\"${START}\",\"end_date\":\"${END}\"}"
        ;;
    *)
        echo '{"error": "未知类型，支持: snapshot, snapshot_plate, intraday, kline, market, leader, flow, trending, calendar, status, hk_kline, us_kline, block_trade, patterns"}'
        exit 1
        ;;
esac
