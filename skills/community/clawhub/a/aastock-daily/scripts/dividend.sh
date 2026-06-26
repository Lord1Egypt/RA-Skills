#!/bin/bash
#==============================================================================
# A股日报 - 分红追踪
# 每周日推送，持仓股分红日历
#==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

main() {
    log INFO "开始生成分红追踪报告"
    
    local portfolio=$(get_portfolio)
    if [ -z "$portfolio" ] || [ "$portfolio" = "[]" ]; then
        echo "⚠️ 持仓列表为空"
        return 0
    fi
    
    # 计算持仓成本和预估股息收益
    local portfolio_value=$(echo "$portfolio" | python3 -c "
import json,sys
try:
    # 模拟持仓（实际应该从用户配置读取）
    # 这里按每只股票持有10000股估算（可配置）
    holdings = {
        '中国建筑': 10000,  # 按5元计算
        '中国广核': 10000,   # 按3元计算
        '中国电建': 10000,   # 按4元计算
        '京沪高铁': 10000,   # 按5元计算
        '中国电信': 10000,   # 按6元计算
        '广深铁路': 10000,   # 按3元计算
        '京东方': 10000,     # 按4元计算
        '中国石化': 10000,   # 按5元计算
        '山西焦煤': 10000,   # 按6元计算
    }
    for name, shares in holdings.items():
        print(f'{name}|{shares}')
except:
    pass
" 2>/dev/null)
    
    local output=""
    output="$(build_header "分红追踪" "$(date '+%H:%M')")"
    output="${output}\n📅 持仓股分红日历"
    output="${output}\n"
    
    # 搜索近期分红相关公告
    output="${output}\n💰 近期分红公告"
    output="${output}\n$(get_dividend_news)"
    
    output="${output}\n\n📊 持仓股息收益估算"
    output="${output}\n$(get_dividend_estimate)"
    
    output="${output}\n\n$(divider)"
    output="${output}\n💡 实际收益以公司公告和持仓数量为准"
    
    echo -e "$output"
    log INFO "分红追踪报告生成完成"
}

get_dividend_news() {
    # 搜索持仓股的分红相关公告
    local stocks=$(echo "$(get_portfolio)" | python3 -c "
import json,sys
try:
    stocks = json.load(sys.stdin)
    print(' '.join([s.get('name','') for s in stocks]))
except:
    print('')
" 2>/dev/null)
    
    local result=$(news_search "${stocks} 分红 派息 除权 登记日 股权登记" 15)
    
    echo "$result" | python3 -c "
import json,sys
try:
    data = json.load(sys.stdin)
    items = data.get('data',{}).get('data',{}).get('llmSearchResponse',{}).get('data',[])
    
    dividends = []
    for item in items:
        title = item.get('title','')
        if any(k in title for k in ['分红', '派息', '除权', '登记日', '派现', '10派']):
            source = item.get('source','') or '未知'
            date = item.get('date','')[:10]
            title_short = title[:50].replace('<BR/>',' ').replace('<br/>',' ')
            
            # 判断类型
            if '除权' in title or '分红' in title:
                emoji = '⏳'
            elif '派息' in title or '派现' in title:
                emoji = '✅'
            else:
                emoji = '📋'
            
            dividends.append((emoji, title_short, source, date))
    
    # 去重
    seen = set()
    for emoji, title, source, date in dividends:
        if title not in seen and len(dividends) < 20:
            seen.add(title)
            print(f'  {emoji} {title}')
            print(f'      ({source} | {date})')
    
    if not dividends:
        print('  暂无最新分红公告')
except:
    print('  数据加载中...')
" 2>/dev/null || echo "  数据加载中..."
}

get_dividend_estimate() {
    # 模拟股息率估算
    echo "  📋 基于公开信息的股息率参考:"
    echo ""
    echo "  ✅ 已派发/待派发:"
    echo "     中国建筑: ~4.5-5.0% (10派2.5左右)"
    echo "     中国石化: ~5.0-5.5% (10派2.8左右)"
    echo "     中国电信: ~4.0-4.5% (10派2.5左右)"
    echo "     中国广核: ~3.5-4.0% (10派1.8左右)"
    echo "     山西焦煤: ~4.0-5.0% (10派3左右)"
    echo ""
    echo "  ⏳ 待公告:"
    echo "     京沪高铁、广深铁路、中国电建"
    echo "     (铁路/基建类股息率相对较低)"
    echo ""
    echo "  📊 整体估算:"
    echo "     持仓平均股息率: ~4.0-4.5%"
    echo "     若持仓市值50万，预估年股息: ~2-2.5万"
}

main "$@"
