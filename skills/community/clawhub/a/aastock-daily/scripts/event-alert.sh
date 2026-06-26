#!/bin/bash
#==============================================================================
# A股日报 - 事件预警
# 持仓股重要事件：解禁、增减持、业绩预告
#==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

main() {
    log INFO "开始生成事件预警报告"
    
    local portfolio=$(get_portfolio)
    if [ -z "$portfolio" ] || [ "$portfolio" = "[]" ]; then
        echo "⚠️ 持仓列表为空"
        return 0
    fi
    
    local output=""
    output="$(build_header "事件预警" "$(date '+%H:%M')")"
    output="${output}\n⚠️ 持仓股重要事件提醒"
    output="${output}\n"
    
    # 获取近期重要资讯（含解禁、减持、业绩预告等）
    output="${output}\n📅 近期重要事件"
    output="${output}\n$(get_important_events)"
    
    output="${output}\n\n$(divider)"
    output="${output}\n💡 橙色预警 = 注意风险 | 红色预警 = 谨慎"
    
    echo -e "$output"
    log INFO "事件预警报告生成完成"
}

get_important_events() {
    # 搜索近期重要事件
    local result=$(news_search "解禁 减持 业绩预告 大股东增减持 A股 重要 2026年3月" 10)
    
    echo "$result" | python3 -c "
import json,sys
try:
    data = json.load(sys.stdin)
    items = data.get('data',{}).get('data',{}).get('llmSearchResponse',{}).get('data',[])
    
    # 按类型分类
   解禁 = []
    减持 = []
    业绩 = []
    增持 = []
    
    keywords解禁 = ['解禁', '限售股', '上市流通']
    keywords减持 = ['减持', '拟减持', '大非', '小非']
    keywords增持 = ['增持', '拟增持', '大笔买入']
    keywords业绩 = ['业绩预告', '业绩快报', '预亏', '预减', '预盈', '预增']
    
    for item in items:
        title = item.get('title','')
        source = item.get('source','')
        date = item.get('date','')[:10]
        
        # 筛选相关标题
        if not any(k in title for k in keywords解禁 + keywords减持 + keywords增持 + keywords业绩):
            continue
            
        # 分类
        if any(k in title for k in keywords解禁):
            类型 = '🔶 解禁'
        elif any(k in title for k in keywords减持):
            类型 = '🔴 减持'
        elif any(k in title for k in keywords增持):
            类型 = '🟢 增持'
        elif any(k in title for k in keywords业绩):
            类型 = '🟡 业绩'
        else:
            continue
            
        title_short = title[:45].replace('<BR/>',' ').replace('<br/>',' ')
        if len(title) > 45:
            title_short += '...'
            
        print(f'  {类型}')
        print(f'  • {title_short}')
        print(f'    ({source} | {date})')
        print('')
except Exception as e:
    print('  数据加载中...')
" 2>/dev/null || echo "  数据加载中..."
}

main "$@"
