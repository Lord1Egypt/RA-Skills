#!/bin/bash
# FinStep MCP - 公司信息服务
# 用法: company.sh <type> <keyword> [params...]

BASE_URL="http://fintool-mcp.finstep.cn/company_info"
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

TODAY=$(date +%Y-%m-%d)
# 默认查上一季度末
LAST_QUARTER=$(date -d "$(date +%Y-%m-01) -3 months" +%Y-%m-%d 2>/dev/null || date +%Y-%m-%d)

case "$TYPE" in
    base)
        # 公司基本信息
        call_mcp "get_company_base_info" "{\"keyword\":\"${KEYWORD}\"}"
        ;;
    security)
        # 证券信息
        call_mcp "get_company_security_info" "{\"keyword\":\"${KEYWORD}\"}"
        ;;
    holders_num)
        # 股东人数
        # 用法: company.sh holders_num "600519" [结束日期] [开始日期]
        END="${3:-${TODAY}}"
        START="${4:-}"
        if [ -n "$START" ]; then
            call_mcp "get_share_holder_number" "{\"keyword\":\"${KEYWORD}\",\"end_date\":\"${END}\",\"begin_date\":\"${START}\"}"
        else
            call_mcp "get_share_holder_number" "{\"keyword\":\"${KEYWORD}\",\"end_date\":\"${END}\"}"
        fi
        ;;
    holders)
        # 股东信息
        # 用法: company.sh holders "600519" <类型> [结束日期]
        # 类型: 01=十大股东, 02=十大流通股东
        INFO_TYPE="${3:-01}"
        END="${4:-${TODAY}}"
        call_mcp "get_share_holder_info" "{\"keyword\":\"${KEYWORD}\",\"info_type_code\":\"${INFO_TYPE}\",\"end_date\":\"${END}\"}"
        ;;
    business)
        # 主营业务财务
        call_mcp "get_business_financial" "{\"keyword\":\"${KEYWORD}\"}"
        ;;
    profit)
        # 经营利润
        # 用法: company.sh profit "600519" [结束日期] [开始日期] [类型]
        END="${3:-${TODAY}}"
        START="${4:-}"
        PTYPE="${5:-}"
        PARAMS="{\"keyword\":\"${KEYWORD}\",\"end_date\":\"${END}\""
        [ -n "$START" ] && PARAMS="${PARAMS},\"start_date\":\"${START}\""
        [ -n "$PTYPE" ] && PARAMS="${PARAMS},\"operating_profit_type\":\"${PTYPE}\""
        PARAMS="${PARAMS}}"
        call_mcp "get_operating_profit" "$PARAMS"
        ;;
    finance)
        # 财务信息
        # 用法: company.sh finance "600519" [结束日期]
        END="${3:-${TODAY}}"
        call_mcp "get_finance_info" "{\"keyword\":\"${KEYWORD}\",\"end_date\":\"${END}\"}"
        ;;
    balance)
        # 资产负债表
        # 用法: company.sh balance "600519" [结束日期] [开始日期]
        END="${3:-${TODAY}}"
        START="${4:-}"
        if [ -n "$START" ]; then
            call_mcp "get_balance_sheet" "{\"keyword\":\"${KEYWORD}\",\"end_date\":\"${END}\",\"start_date\":\"${START}\"}"
        else
            call_mcp "get_balance_sheet" "{\"keyword\":\"${KEYWORD}\",\"end_date\":\"${END}\"}"
        fi
        ;;
    cashflow)
        # 现金流量表
        END="${3:-${TODAY}}"
        START="${4:-}"
        if [ -n "$START" ]; then
            call_mcp "get_cash_flow" "{\"keyword\":\"${KEYWORD}\",\"end_date\":\"${END}\",\"start_date\":\"${START}\"}"
        else
            call_mcp "get_cash_flow" "{\"keyword\":\"${KEYWORD}\",\"end_date\":\"${END}\"}"
        fi
        ;;
    income)
        # 利润表
        END="${3:-${TODAY}}"
        START="${4:-}"
        if [ -n "$START" ]; then
            call_mcp "get_income_statement" "{\"keyword\":\"${KEYWORD}\",\"end_date\":\"${END}\",\"start_date\":\"${START}\"}"
        else
            call_mcp "get_income_statement" "{\"keyword\":\"${KEYWORD}\",\"end_date\":\"${END}\"}"
        fi
        ;;
    valuation)
        # 估值指标(每日)
        # 用法: company.sh valuation "600519" [结束日期] [开始日期]
        END="${3:-${TODAY}}"
        START="${4:-}"
        if [ -n "$START" ]; then
            call_mcp "get_valuation_metrics_daily" "{\"keyword\":\"${KEYWORD}\",\"end_date\":\"${END}\",\"begin_date\":\"${START}\"}"
        else
            call_mcp "get_valuation_metrics_daily" "{\"keyword\":\"${KEYWORD}\",\"end_date\":\"${END}\"}"
        fi
        ;;
    rd)
        # 研发费用
        END="${3:-${TODAY}}"
        START="${4:-}"
        if [ -n "$START" ]; then
            call_mcp "get_research_development_expense" "{\"keyword\":\"${KEYWORD}\",\"end_date\":\"${END}\",\"begin_date\":\"${START}\"}"
        else
            call_mcp "get_research_development_expense" "{\"keyword\":\"${KEYWORD}\",\"end_date\":\"${END}\"}"
        fi
        ;;
    index)
        # 财务指标
        END="${3:-${TODAY}}"
        START="${4:-}"
        if [ -n "$START" ]; then
            call_mcp "get_financial_index" "{\"keyword\":\"${KEYWORD}\",\"end_date\":\"${END}\",\"begin_date\":\"${START}\"}"
        else
            call_mcp "get_financial_index" "{\"keyword\":\"${KEYWORD}\",\"end_date\":\"${END}\"}"
        fi
        ;;
    industry)
        # 申万行业分类
        call_mcp "get_stock_industry_sws" "{\"keyword\":\"${KEYWORD}\"}"
        ;;
    analytics)
        # 财务分析指标
        END="${3:-}"
        START="${4:-}"
        PARAMS="{\"keyword\":\"${KEYWORD}\""
        [ -n "$END" ] && PARAMS="${PARAMS},\"end_date\":\"${END}\""
        [ -n "$START" ] && PARAMS="${PARAMS},\"begin_date\":\"${START}\""
        PARAMS="${PARAMS}}"
        call_mcp "get_financial_analytics_metric" "$PARAMS"
        ;;
    audit)
        # 审计意见
        END="${3:-${TODAY}}"
        START="${4:-}"
        if [ -n "$START" ]; then
            call_mcp "get_audit_opinion" "{\"keyword\":\"${KEYWORD}\",\"end_date\":\"${END}\",\"begin_date\":\"${START}\"}"
        else
            call_mcp "get_audit_opinion" "{\"keyword\":\"${KEYWORD}\",\"end_date\":\"${END}\"}"
        fi
        ;;
    holdings)
        # 持股信息
        END="${3:-${TODAY}}"
        START="${4:-}"
        if [ -n "$START" ]; then
            call_mcp "get_stock_holdings" "{\"keyword\":\"${KEYWORD}\",\"end_date\":\"${END}\",\"begin_date\":\"${START}\"}"
        else
            call_mcp "get_stock_holdings" "{\"keyword\":\"${KEYWORD}\",\"end_date\":\"${END}\"}"
        fi
        ;;
    transfer)
        # 转送计划
        START="${3:-}"
        if [ -n "$START" ]; then
            call_mcp "get_transfer_plan" "{\"keyword\":\"${KEYWORD}\",\"begin_date\":\"${START}\"}"
        else
            call_mcp "get_transfer_plan" "{\"keyword\":\"${KEYWORD}\"}"
        fi
        ;;
    *)
        echo '{"error": "未知类型，支持: base, security, holders_num, holders, business, profit, finance, balance, cashflow, income, valuation, rd, index, industry, analytics, audit, holdings, transfer"}'
        exit 1
        ;;
esac
