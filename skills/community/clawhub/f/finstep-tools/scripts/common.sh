#!/bin/bash
# FinStep MCP - 通用工具服务
# 用法: common.sh <type> [params...]

BASE_URL="http://fintool-mcp.finstep.cn/common"
SIGNATURE="${FINSTEP_SIGNATURE:?需要设置环境变量 FINSTEP_SIGNATURE}"

TYPE="$1"

call_mcp() {
    local tool="$1"
    local params="$2"
    
    curl -s -X POST "${BASE_URL}?signature=${SIGNATURE}" \
        -H "Content-Type: application/json" \
        -H "Accept: application/json, text/event-stream" \
        --max-time 30 \
        -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"tools/call\",\"params\":{\"name\":\"${tool}\",\"arguments\":${params}}}"
}

case "$TYPE" in
    time)
        # 获取当前时间
        call_mcp "get_current_time" "{}"
        ;;
    trade_info)
        # 获取今天交易日信息（是否交易日、上一个/下一个交易日）
        call_mcp "get_trade_info" "{}"
        ;;
    trade_date)
        # 获取交易日历，需要参数: start_date end_date market
        # market: 18=北交所, 83=上交所, 90=深交所, 72=港交所, 78=纽交所
        START="${2:-$(date +%Y-%m-%d)}"
        END="${3:-$(date +%Y-%m-%d)}"
        MARKET="${4:-83}"
        call_mcp "get_trade_date" "{\"start_date\":\"${START}\",\"end_date\":\"${END}\",\"security_market\":${MARKET}}"
        ;;
    url)
        # 解析网页内容
        URL="$2"
        call_mcp "url_parse" "{\"url\":\"${URL}\"}"
        ;;
    *)
        echo '{"error": "未知类型，支持: time, trade_info, trade_date <start> <end> <market>, url <url>"}'
        exit 1
        ;;
esac
