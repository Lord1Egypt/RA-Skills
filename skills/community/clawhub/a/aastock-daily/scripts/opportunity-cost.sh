#!/bin/bash
#==============================================================================
# A股日报 - 机会成本对比
# 每周日推送，持仓股息率 vs 其他投资渠道
#==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

main() {
    log INFO "开始生成机会成本对比报告"
    
    local output=""
    output="$(build_header "机会成本对比" "$(date '+%H:%M')")"
    output="${output}\n📅 持仓股息收益 vs 其他投资渠道"
    output="${output}\n"
    
    # 1. 各渠道收益率对比
    output="${output}\n📊 主流投资渠道收益率"
    output="${output}\n$(get_yield_comparison)"
    
    # 2. 持仓股息率分析
    output="${output}\n\n💰 持仓股股息率分析"
    output="${output}\n$(get_portfolio_yield)"
    
    # 3. 风险收益对比
    output="${output}\n\n⚖️ 风险收益对比"
    output="${output}\n$(get_risk_comparison)"
    
    # 4. 综合建议
    output="${output}\n\n🎯 综合建议"
    output="${output}\n$(get_recommendation)"
    
    output="${output}\n\n$(divider)"
    output="${output}\n💡 本报告仅供参考，不构成投资建议"
    
    echo -e "$output"
    log INFO "机会成本对比报告生成完成"
}

get_yield_comparison() {
    echo "  ┌─────────────────────┬────────┐"
    echo "  │ 投资渠道            │ 年化   │"
    echo "  ├─────────────────────┼────────┤"
    echo "  │ 🏦 银行存款(1年)   │ ~1.5%  │"
    echo "  │ 📈 货币基金        │ ~2.0%  │"
    echo "  │ 📊 国债(10年)     │ ~2.2%  │"
    echo "  │ 🏠 房租收益       │ ~2.0%  │"
    echo "  │ 📉 沪深300指数    │ ~8-10% │"
    echo "  │ 💎 黄金           │ ~5-8%  │"
    echo "  ├─────────────────────┼────────┤"
    echo "  │ 🟢 持仓高股息股    │ ~4.5%  │"
    echo "  └─────────────────────┴────────┘"
}

get_portfolio_yield() {
    echo "  📋 持仓股股息率参考:"
    echo ""
    echo "  🟢 第一梯队 (高息 >4%):"
    echo "     • 中国石化: ~5.0-5.5%"
    echo "     • 中国建筑: ~4.5-5.0%"
    echo "     • 山西焦煤: ~4.0-5.0%"
    echo ""
    echo "  🟡 第二梯队 (中息 3-4%):"
    echo "     • 中国电信: ~4.0-4.5%"
    echo "     • 中国广核: ~3.5-4.0%"
    echo ""
    echo "  🔵 第三梯队 (低息 <3%):"
    echo "     • 京沪高铁: ~2.0-2.5%"
    echo "     • 广深铁路: ~1.5-2.0%"
    echo "     • 京东方A: ~1.0-2.0%"
    echo "     • 中国电建: ~2.0-2.5%"
    echo ""
    echo "  📊 持仓加权平均股息率: ~3.5-4.0%"
}

get_risk_comparison() {
    echo "  ┌─────────────────────┬────────┬────────┐"
    echo "  │ 投资渠道            │ 年化   │ 风险   │"
    echo "  ├─────────────────────┼────────┼────────┤"
    echo "  │ 🏦 银行存款        │ 1.5%   │ ★☆☆☆☆ │"
    echo "  │ 📊 国债            │ 2.2%   │ ★☆☆☆☆ │"
    echo "  │ 📈 货币基金        │ 2.0%   │ ★☆☆☆☆ │"
    echo "  │ 💎 黄金            │ 5-8%   │ ★★★☆☆ │"
    echo "  │ 📉 沪深300        │ 8-10%  │ ★★★★☆ │"
    echo "  ├─────────────────────┼────────┼────────┤"
    echo "  │ 💰 持仓高股息股    │ 4.0%   │ ★★☆☆☆ │"
    echo "  └─────────────────────┴────────┴────────┘"
    echo ""
    echo "  📝 注: 股票有价格波动风险，但高股息策略"
    echo "        天然带'安全垫'，股息可对冲部分跌幅"
}

get_recommendation() {
    echo "  ✅ 当前持仓优势:"
    echo "     1. 股息率跑赢存款/货币基金约2%"
    echo "     2. 国企背景，现金流稳定，分红有保障"
    echo "     3. 防御性强，适合震荡市"
    echo ""
    echo "  ⚠️ 潜在风险:"
    echo "     1. 经济增长放缓可能影响业绩"
    echo "     2. 行业集中度高(基建/能源)"
    echo "     3. 股价波动可能吞噬股息收益"
    echo ""
    echo "  💡 操作建议:"
    echo "     • 继续持有高息仓位作为'压舱石'"
    echo "     • 适当关注京东方等成长股弹性"
    echo "     • 若风险偏好提升，可考虑定投沪深300"
}

main "$@"
