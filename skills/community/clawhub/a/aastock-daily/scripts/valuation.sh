#!/bin/bash
#==============================================================================
# A股日报 - 估值监控
# 每周一推送，持仓股估值分析
#==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

main() {
    log INFO "开始生成估值监控报告"
    
    local portfolio=$(get_portfolio)
    if [ -z "$portfolio" ] || [ "$portfolio" = "[]" ]; then
        echo "⚠️ 持仓列表为空"
        return 0
    fi
    
    local stock_count=$(echo "$portfolio" | python3 -c "
import json,sys
try:
    stocks = json.load(sys.stdin)
    print(len(stocks))
except:
    print(0)
" 2>/dev/null)
    
    local output=""
    output="$(build_header "估值监控" "$(date '+%H:%M')")"
    output="${output}\n📅 每周估值追踪 | 共 ${stock_count} 只持仓"
    output="${output}\n"
    
    # 获取持仓数据
    local stocks_data=$(echo "$portfolio" | python3 -c "
import json,sys
try:
    stocks = json.load(sys.stdin)
    for s in stocks:
        name = s.get('name','')
        code = s.get('code','')
        prefix = code[:1]
        if prefix == '6':
            secid = '1.' + code
        else:
            secid = '0.' + code
        print(f'{name}|{code}|{secid}')
except:
    pass
" 2>/dev/null)
    
    local count=1
    while IFS='|' read -r name code secid; do
        [ -z "$name" ] && continue
        output="${output}\n$(get_valuation "$name" "$code" "$secid" "$count")"
        output="${output}\n"
        count=$((count + 1))
    done <<< "$stocks_data"
    
    output="${output}\n$(divider)"
    output="${output}\n💡 低PE、高股息率、低PB = 价值洼地"
    output="${output}\n⚠️ 高PE、低ROE = 警惕估值泡沫"
    
    echo -e "$output"
    log INFO "估值监控报告生成完成"
}

get_valuation() {
    local name="$1"
    local code="$2"
    local secid="$3"
    local index="$4"
    
    local info=""
    info="${info}\n${index}. ${name} (${code})"
    
    # 获取实时行情
    local quote=$(get_stock_quote "$secid")
    IFS='|' read -r q_name price change pct flow <<< "$quote"
    
    # 获取基本面数据
    local fundamentals=$(get_fundamentals "$code")
    IFS='|' read -r pe pb roe dividend eps bps <<< "$fundamentals"
    
    # 判断估值水平
    local valuation_status=""
    if [ "$pe" != "N/A" ] && [ -n "$pe" ] && [ "$pe" != "0" ] && [ "$pe" != "-" ]; then
        local pe_val=$(echo "$pe" | tr -d ',')
        if (( $(echo "$pe_val < 15" | bc -l 2>/dev/null) )); then
            valuation_status="📗 低估"
        elif (( $(echo "$pe_val > 40" | bc -l 2>/dev/null) )); then
            valuation_status="📕 高估"
        else
            valuation_status="📙 合理"
        fi
    fi
    
    # 显示价格和估值状态
    if [ "$price" != "-" ] && [ -n "$price" ]; then
        local sign=""
        [ "$(echo "$pct > 0" | bc 2>/dev/null)" = "1" ] && sign="+"
        info="${info}\n   💰 ${price}元 (${sign}${pct}%) ${valuation_status}"
    fi
    
    # 显示关键指标
    info="${info}\n   📊 估值指标:"
    
    # PE
    if [ "$pe" != "N/A" ] && [ -n "$pe" ] && [ "$pe" != "0" ] && [ "$pe" != "-" ]; then
        info="${info}\n      PE: ${pe}倍"
    fi
    
    # PB
    if [ "$pb" != "N/A" ] && [ -n "$pb" ] && [ "$pb" != "0" ] && [ "$pb" != "-" ]; then
        info="${info}\n      PB: ${pb}倍"
    fi
    
    # ROE
    if [ "$roe" != "N/A" ] && [ -n "$roe" ] && [ "$roe" != "0" ] && [ "$roe" != "-" ]; then
        info="${info}\n      ROE: ${roe}%"
    fi
    
    # 股息率
    if [ "$dividend" != "N/A" ] && [ -n "$dividend" ] && [ "$dividend" != "0" ] && [ "$dividend" != "-" ]; then
        local div_val=$(echo "$dividend" | tr -d '%')
        if (( $(echo "$div_val > 3" | bc -l 2>/dev/null) )); then
            info="${info}\n      股息率: ${dividend}% 🎯高息"
        else
            info="${info}\n      股息率: ${dividend}%"
        fi
    fi
    
    # EPS和BPS
    if [ "$eps" != "N/A" ] && [ -n "$eps" ] && [ "$eps" != "0" ] && [ "$eps" != "-" ]; then
        info="${info}\n      EPS: ${eps}元 | BPS: ${bps}元"
    fi
    
    # 净利润增速
    if [ "$roe" != "N/A" ] && [ -n "$roe" ] && [ "$roe" != "0" ] && [ "$roe" != "-" ]; then
        local roe_val=$(echo "$roe" | tr -d '%')
        if (( $(echo "$roe_val > 10" | bc -l 2>/dev/null) )); then
            info="${info}\n      📈 盈利能力优秀"
        elif (( $(echo "$roe_val > 5" | bc -l 2>/dev/null) )); then
            info="${info}\n      📊 盈利能力良好"
        fi
    fi
    
    echo "$info"
}

get_fundamentals() {
    local code="$1"
    
    # 东方财富基本面API
    local api_url="https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/ZYZBAjaxNew?type=0&code=${code}"
    
    # 判断市场
    if [[ "$code" =~ ^6 ]]; then
        api_url="https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/ZYZBAjaxNew?type=0&code=SH${code}"
    else
        api_url="https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/ZYZBAjaxNew?type=0&code=SZ${code}"
    fi
    
    local result=$(curl -s "$api_url" 2>/dev/null)
    
    if [ -z "$result" ] || echo "$result" | grep -q "error"; then
        echo "N/A|N/A|N/A|N/A|N/A|N/A"
        return
    fi
    
    # 解析JSON
    echo "$result" | python3 -c "
import json,sys
try:
    data = json.load(sys.stdin)
    items = data.get('data', [])
    if items:
        latest = items[0]
        pe = latest.get('XSJLL', 'N/A')  # 市盈率
        pb = round(latest.get('BPS', 0) / 10000, 2) if latest.get('BPS') else 'N/A'  # 市净率
        eps = latest.get('EPSXS', 'N/A')  # 每股收益
        bps = latest.get('BPS', 'N/A')  # 每股净资产
        roe = latest.get('ROEJQ', 'N/A')  # 净资产收益率
        profit_growth = latest.get('PARENTNETPROFITTZ', 'N/A')  # 净利润增速
        
        # 格式化
        pe_str = f'{float(pe):.1f}' if pe and pe != 'N/A' else 'N/A'
        pb_str = f'{float(pb):.2f}' if pb and pb != 'N/A' else 'N/A'
        eps_str = f'{float(eps):.2f}' if eps and eps != 'N/A' else 'N/A'
        bps_str = f'{float(bps):.2f}' if bps and bps != 'N/A' else 'N/A'
        roe_str = f'{float(roe):.2f}' if roe and roe != 'N/A' else 'N/A'
        
        # 股息率估算（简单用近一年分红/股价，需要实时价格，这里用固定值）
        # 实际应该用: 分红/当前股价
        dividend_est = 'N/A'
        
        print(f'{pe_str}|{pb_str}|{roe_str}|{dividend_est}|{eps_str}|{bps_str}')
    else:
        print('N/A|N/A|N/A|N/A|N/A|N/A')
except Exception as e:
    print('N/A|N/A|N/A|N/A|N/A|N/A')
" 2>/dev/null || echo "N/A|N/A|N/A|N/A|N/A|N/A"
}

main "$@"
