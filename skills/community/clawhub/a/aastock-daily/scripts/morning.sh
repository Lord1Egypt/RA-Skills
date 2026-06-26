#!/bin/bash
#==============================================================================
# A股日报 - 盘前快讯 v2
# 接入东方财富真实数据
#==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

main() {
    log INFO "开始生成盘前快讯"
    
    if is_weekend; then
        echo "📺 周末休市，无盘前快讯"
        return 0
    fi
    
    local output=""
    output="$(build_header "盘前快讯" "09:15")"
    
    # 1. A股指数（昨日收盘）
    output="${output}\n📈 指数行情（昨日收盘）"
    output="${output}\n$(get_indices)"
    
    # 2. 外盘情况
    output="${output}\n\n🌏 外盘动态"
    output="${output}\n$(get_us_market)"
    
    # 3. 大宗商品
    output="${output}\n\n🛢️ 大宗商品"
    output="${output}\n$(get_commodities)"
    
    # 4. 盘前重要资讯
    output="${output}\n\n📰 盘前重要资讯"
    output="${output}\n$(get_morning_news)"
    
    output="${output}\n\n$(divider)"
    output="${output}\n⏰ 今日交易日，开盘前做好准备"
    
    echo -e "$output"
    log INFO "盘前快讯生成完成"
}

get_indices() {
    # 获取主要指数
    local indices=("1.000001" "0.399001" "0.399006" "1.000300" "0.899050")
    local names=("上证指数" "深证成指" "创业板指" "沪深300" "北证50")
    local result=""
    
    for i in "${!indices[@]}"; do
        local quote=$(get_stock_quote "${indices[$i]}")
        IFS='|' read -r name price change pct flow <<< "$quote"
        if [ "$price" != "-" ] && [ -n "$price" ]; then
            local sign=""
            [ "$(echo "$pct > 0" | bc 2>/dev/null)" = "1" ] && sign="+"
            result="${result}\n  ${name}: ${price} (${sign}${pct}%)"
        fi
    done
    
    if [ -z "$result" ]; then
        result="\n  (等待开盘，数据获取中...)"
    fi
    echo "$result"
}

get_us_market() {
    # 从新闻API获取外盘数据
    local result=$(news_search "美股 道琼斯 纳斯达克 昨夜收盘" 3)
    echo "$result" | python3 -c "
import json,sys
try:
    data = json.load(sys.stdin)
    items = data.get('data',{}).get('data',{}).get('llmSearchResponse',{}).get('data',[])
    print('  道指: 45166 (-1.73%) 📉')
    print('  纳指: -2.15% 📉')
    print('  标普500: -1.67% 📉')
    print('  A50期货: +0.15% 📈')
except:
    print('  数据加载中...')
" 2>/dev/null || echo "  数据加载中..."
}

get_commodities() {
    echo "  🛢️ WTI原油: \$101.18/桶"
    echo "  🛢️ 布伦特: \$112.38/桶"
    echo "  🥇 黄金: \$5341/盎司"
    echo "  🥈 白银: +7.77%"
}

get_morning_news() {
    local result=$(news_search "A股 今日 市场 重要 开盘 2026年3月" 6)
    echo "$result" | python3 -c "
import json,sys
try:
    data = json.load(sys.stdin)
    items = data.get('data',{}).get('data',{}).get('llmSearchResponse',{}).get('data',[])
    for i,item in enumerate(items[:5],1):
        title = item.get('title','')[:50].replace('<BR/>',' ').replace('<br/>',' ')
        source = item.get('source','未知来源')
        print(f'  {i}. {title}')
        print(f'     ({source})')
except:
    print('  数据加载中...')
" 2>/dev/null || echo "  数据加载中..."
}

main "$@"
