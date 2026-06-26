#!/bin/bash
# FinStep MCP - 宏观数据服务
# 用法: macro.sh <type> [params...]

BASE_URL="https://fintool-mcp.finstep.cn/macro"
SIGNATURE="${FINSTEP_SIGNATURE:?需要设置环境变量 FINSTEP_SIGNATURE}"

TYPE="$1"

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
# 默认查近一年
YEAR_AGO=$(date -d "-1 year" +%Y-%m-%d 2>/dev/null || date +%Y-%m-%d)

case "$TYPE" in
    lpr)
        # LPR利率
        # 用法: macro.sh lpr [开始日期] [结束日期]
        START="${2:-${YEAR_AGO}}"
        END="${3:-${TODAY}}"
        call_mcp "get_china_lpr" "$(jq -n --arg begin_date "$START" --arg end_date "$END" \
            '{"begin_date":$begin_date,"end_date":$end_date}')"
        ;;
    bond)
        # 中美国债收益率
        START="${2:-${YEAR_AGO}}"
        END="${3:-${TODAY}}"
        call_mcp "get_bond_cn_us_rate" "$(jq -n --arg begin_date "$START" --arg end_date "$END" \
            '{"begin_date":$begin_date,"end_date":$end_date}')"
        ;;
    pboc)
        # 央行公开市场操作
        # 用法: macro.sh pboc [日期]
        DATE="${2:-${TODAY}}"
        call_mcp "get_central_bank_operation" "$(jq -n --arg trading_date "$DATE" \
            '{"trading_date":$trading_date}')"
        ;;
    pboc_week)
        # 央行一周操作汇总
        # 用法: macro.sh pboc_week [周末日期]
        DATE="${2:-${TODAY}}"
        call_mcp "get_central_bank_operation_week" "$(jq -n --arg week_end_date "$DATE" \
            '{"week_end_date":$week_end_date}')"
        ;;
    rrr)
        # 存款准备金率
        START="${2:-${YEAR_AGO}}"
        END="${3:-${TODAY}}"
        call_mcp "get_china_reserve_requirement_ratio" "$(jq -n --arg begin_date "$START" --arg end_date "$END" \
            '{"begin_date":$begin_date,"end_date":$end_date}')"
        ;;
    rmb_rate)
        # 人民币利率
        DATE="${2:-${TODAY}}"
        call_mcp "get_rmb_interest_rate" "$(jq -n --arg query_date "$DATE" \
            '{"query_date":$query_date}')"
        ;;
    interbank)
        # 银行间利率
        # 用法: macro.sh interbank <品种> <指标> [开始] [结束]
        # 品种: Shibor, LPR, DR等
        # 指标: 1W, 1M, 3M等
        SYMBOL="${2:-Shibor}"
        INDICATOR="${3:-1W}"
        START="${4:-${YEAR_AGO}}"
        END="${5:-${TODAY}}"
        call_mcp "get_rate_interbank" "$(jq -n \
            --arg begin_date "$START" --arg end_date "$END" \
            --arg symbol "$SYMBOL" --arg indicator "$INDICATOR" \
            '{"begin_date":$begin_date,"end_date":$end_date,"symbol":$symbol,"indicator":$indicator}')"
        ;;
    tax)
        # 国家税收
        START="${2:-${YEAR_AGO}}"
        END="${3:-${TODAY}}"
        call_mcp "get_national_tax_revenue" "$(jq -n --arg begin_date "$START" --arg end_date "$END" \
            '{"begin_date":$begin_date,"end_date":$end_date}')"
        ;;
    budget)
        # 财政预算
        START="${2:-${YEAR_AGO}}"
        END="${3:-${TODAY}}"
        call_mcp "get_fiscal_budget" "$(jq -n --arg begin_date "$START" --arg end_date "$END" \
            '{"begin_date":$begin_date,"end_date":$end_date}')"
        ;;
    pmi)
        # PMI指数
        END="${2:-${TODAY}}"
        START="${3:-}"
        call_mcp "get_pmi_monthly" "$(jq -n --arg end_date "$END" --arg start_date "$START" \
            '{end_date:$end_date} + (if $start_date != "" then {start_date:$start_date} else {} end)')"
        ;;
    cpi)
        # CPI
        END="${2:-${TODAY}}"
        START="${3:-}"
        call_mcp "get_cpi_info" "$(jq -n --arg end_date "$END" --arg start_date "$START" \
            '{end_date:$end_date} + (if $start_date != "" then {start_date:$start_date} else {} end)')"
        ;;
    ppi)
        # PPI
        END="${2:-${TODAY}}"
        START="${3:-}"
        call_mcp "get_ppi_monthly" "$(jq -n --arg end_date "$END" --arg start_date "$START" \
            '{end_date:$end_date} + (if $start_date != "" then {start_date:$start_date} else {} end)')"
        ;;
    gdp)
        # GDP季度
        END="${2:-${TODAY}}"
        START="${3:-}"
        call_mcp "get_gdp_info_quarterly" "$(jq -n --arg end_date "$END" --arg start_date "$START" \
            '{end_date:$end_date} + (if $start_date != "" then {start_date:$start_date} else {} end)')"
        ;;
    unemployment)
        # 失业率
        END="${2:-${TODAY}}"
        START="${3:-}"
        call_mcp "get_unemployment_rate" "$(jq -n --arg end_date "$END" --arg start_date "$START" \
            '{end_date:$end_date} + (if $start_date != "" then {start_date:$start_date} else {} end)')"
        ;;
    house)
        # 主要城市房价
        # 用法: macro.sh house <城市> [结束日期] [开始日期]
        CITY="${2:-北京}"
        END="${3:-${TODAY}}"
        START="${4:-}"
        call_mcp "get_major_city_house_price" "$(jq -n \
            --arg city "$CITY" --arg end_date "$END" --arg start_date "$START" \
            '{city:$city,end_date:$end_date} + (if $start_date != "" then {start_date:$start_date} else {} end)')"
        ;;
    *)
        echo '{"error": "未知类型，支持: lpr, bond, pboc, pboc_week, rrr, rmb_rate, interbank, tax, budget, pmi, cpi, ppi, gdp, unemployment, house"}'
        exit 1
        ;;
esac
