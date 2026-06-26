#!/bin/bash
# FinStep MCP - 公司信息服务
# 用法: company.sh <type> <keyword> [params...]

BASE_URL="https://fintool-mcp.finstep.cn/company_info"
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
# 默认查上一季度末
LAST_QUARTER=$(date -d "$(date +%Y-%m-01) -3 months" +%Y-%m-%d 2>/dev/null || date +%Y-%m-%d)

case "$TYPE" in
    base)
        # 公司基本信息
        call_mcp "get_company_base_info" "$(jq -n --arg keyword "$KEYWORD" '{"keyword":$keyword}')"
        ;;
    security)
        # 证券信息
        call_mcp "get_company_security_info" "$(jq -n --arg keyword "$KEYWORD" '{"keyword":$keyword}')"
        ;;
    holders_num)
        # 股东人数
        # 用法: company.sh holders_num "600519" [结束日期] [开始日期]
        END="${3:-${TODAY}}"
        START="${4:-}"
        call_mcp "get_share_holder_number" "$(jq -n \
            --arg keyword "$KEYWORD" --arg end_date "$END" --arg begin_date "$START" \
            '{keyword:$keyword,end_date:$end_date} + (if $begin_date != "" then {begin_date:$begin_date} else {} end)')"
        ;;
    holders)
        # 股东信息
        # 用法: company.sh holders "600519" <类型> [结束日期]
        # 类型: 01=十大股东, 02=十大流通股东
        INFO_TYPE="${3:-01}"
        END="${4:-${TODAY}}"
        call_mcp "get_share_holder_info" "$(jq -n \
            --arg keyword "$KEYWORD" --arg info_type_code "$INFO_TYPE" --arg end_date "$END" \
            '{"keyword":$keyword,"info_type_code":$info_type_code,"end_date":$end_date}')"
        ;;
    business)
        # 主营业务财务
        call_mcp "get_business_financial" "$(jq -n --arg keyword "$KEYWORD" '{"keyword":$keyword}')"
        ;;
    profit)
        # 经营利润
        # 用法: company.sh profit "600519" [结束日期] [开始日期] [类型]
        END="${3:-${TODAY}}"
        START="${4:-}"
        PTYPE="${5:-}"
        call_mcp "get_operating_profit" "$(jq -n \
            --arg keyword "$KEYWORD" --arg end_date "$END" \
            --arg start_date "$START" --arg ptype "$PTYPE" \
            '{keyword:$keyword,end_date:$end_date} +
             (if $start_date != "" then {start_date:$start_date} else {} end) +
             (if $ptype != "" then {operating_profit_type:$ptype} else {} end)')"
        ;;
    finance)
        # 财务信息
        # 用法: company.sh finance "600519" [结束日期]
        END="${3:-${TODAY}}"
        call_mcp "get_finance_info" "$(jq -n --arg keyword "$KEYWORD" --arg end_date "$END" \
            '{"keyword":$keyword,"end_date":$end_date}')"
        ;;
    balance)
        # 资产负债表
        # 用法: company.sh balance "600519" [结束日期] [开始日期]
        END="${3:-${TODAY}}"
        START="${4:-}"
        call_mcp "get_balance_sheet" "$(jq -n \
            --arg keyword "$KEYWORD" --arg end_date "$END" --arg start_date "$START" \
            '{keyword:$keyword,end_date:$end_date} + (if $start_date != "" then {start_date:$start_date} else {} end)')"
        ;;
    cashflow)
        # 现金流量表
        END="${3:-${TODAY}}"
        START="${4:-}"
        call_mcp "get_cash_flow" "$(jq -n \
            --arg keyword "$KEYWORD" --arg end_date "$END" --arg start_date "$START" \
            '{keyword:$keyword,end_date:$end_date} + (if $start_date != "" then {start_date:$start_date} else {} end)')"
        ;;
    income)
        # 利润表
        END="${3:-${TODAY}}"
        START="${4:-}"
        call_mcp "get_income_statement" "$(jq -n \
            --arg keyword "$KEYWORD" --arg end_date "$END" --arg start_date "$START" \
            '{keyword:$keyword,end_date:$end_date} + (if $start_date != "" then {start_date:$start_date} else {} end)')"
        ;;
    valuation)
        # 估值指标(每日)
        # 用法: company.sh valuation "600519" [结束日期] [开始日期]
        END="${3:-${TODAY}}"
        START="${4:-}"
        call_mcp "get_valuation_metrics_daily" "$(jq -n \
            --arg keyword "$KEYWORD" --arg end_date "$END" --arg begin_date "$START" \
            '{keyword:$keyword,end_date:$end_date} + (if $begin_date != "" then {begin_date:$begin_date} else {} end)')"
        ;;
    rd)
        # 研发费用
        END="${3:-${TODAY}}"
        START="${4:-}"
        call_mcp "get_research_development_expense" "$(jq -n \
            --arg keyword "$KEYWORD" --arg end_date "$END" --arg begin_date "$START" \
            '{keyword:$keyword,end_date:$end_date} + (if $begin_date != "" then {begin_date:$begin_date} else {} end)')"
        ;;
    index)
        # 财务指标
        END="${3:-${TODAY}}"
        START="${4:-}"
        call_mcp "get_financial_index" "$(jq -n \
            --arg keyword "$KEYWORD" --arg end_date "$END" --arg begin_date "$START" \
            '{keyword:$keyword,end_date:$end_date} + (if $begin_date != "" then {begin_date:$begin_date} else {} end)')"
        ;;
    industry)
        # 申万行业分类
        call_mcp "get_stock_industry_sws" "$(jq -n --arg keyword "$KEYWORD" '{"keyword":$keyword}')"
        ;;
    analytics)
        # 财务分析指标
        END="${3:-}"
        START="${4:-}"
        call_mcp "get_financial_analytics_metric" "$(jq -n \
            --arg keyword "$KEYWORD" --arg end_date "$END" --arg begin_date "$START" \
            '{keyword:$keyword} +
             (if $end_date != "" then {end_date:$end_date} else {} end) +
             (if $begin_date != "" then {begin_date:$begin_date} else {} end)')"
        ;;
    audit)
        # 审计意见
        END="${3:-${TODAY}}"
        START="${4:-}"
        call_mcp "get_audit_opinion" "$(jq -n \
            --arg keyword "$KEYWORD" --arg end_date "$END" --arg begin_date "$START" \
            '{keyword:$keyword,end_date:$end_date} + (if $begin_date != "" then {begin_date:$begin_date} else {} end)')"
        ;;
    holdings)
        # 持股信息
        END="${3:-${TODAY}}"
        START="${4:-}"
        call_mcp "get_stock_holdings" "$(jq -n \
            --arg keyword "$KEYWORD" --arg end_date "$END" --arg begin_date "$START" \
            '{keyword:$keyword,end_date:$end_date} + (if $begin_date != "" then {begin_date:$begin_date} else {} end)')"
        ;;
    transfer)
        # 转送计划
        START="${3:-}"
        call_mcp "get_transfer_plan" "$(jq -n --arg keyword "$KEYWORD" --arg begin_date "$START" \
            '{keyword:$keyword} + (if $begin_date != "" then {begin_date:$begin_date} else {} end)')"
        ;;
    *)
        echo '{"error": "未知类型，支持: base, security, holders_num, holders, business, profit, finance, balance, cashflow, income, valuation, rd, index, industry, analytics, audit, holdings, transfer"}'
        exit 1
        ;;
esac
