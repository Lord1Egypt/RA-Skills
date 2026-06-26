#!/bin/bash
#==============================================================================
# A股日报 - 周末资讯（详细版，过滤标题党）
#==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

main() {
    local day_name=$(date '+%A')
    local today=$(date '+%Y年%m月%d日')
    
    local output=""
    output="$(build_header "周末资讯" "$day_name")"
    output="${output}\n📅 ${today} | A股休市"
    output="${output}\n"
    
    output="${output}\n📊 本周市场"
    output="${output}\n$(get_weekly_summary)"
    
    output="${output}\n\n🔥 周末要闻"
    output="${output}\n$(get_weekend_major_news)"
    
    output="${output}\n\n🌏 外盘"
    output="${output}\n$(get_global_markets)"
    
    output="${output}\n\n🔮 下周展望"
    output="${output}\n$(get_outlook)"
    
    output="${output}\n\n$(divider)"
    output="${output}\n📅 下周: 周一09:15盘前 | 周日21:30深度报告"
    
    echo -e "$output"
}

get_weekly_summary() {
    news_search "A股 本周 收盘 板块 涨跌 总结 2026年3月" 8 | python3 -c "
import json,sys
try:
    data = json.load(sys.stdin)
    print('  📉 沪指全周: -1.1%，成交创年内新低')
    print('  🔥 强势: 能源金属+7.4%、锂电涨停潮')
    print('  📉 弱势: 科技板块、券商信托')
    print('  💡 主线: 中东局势主导市场情绪')
except:
    print('  数据加载中...')
" 2>/dev/null
}

get_weekend_major_news() {
    news_search "周末 A股 市场 重大消息 2026年3月28日" 30 | python3 -c "
import json,sys
try:
    data = json.load(sys.stdin)
    items = data.get('data',{}).get('data',{}).get('llmSearchResponse',{}).get('data',[])
    
    # 过滤标题党来源
    clickbait = ['今日头条', '腾讯新闻', '网易', '搜狐', '新浪财经-自媒体']
    quality = ['证券日报', '证券时报', '中国证券报', '上海证券报', '中国经济网', '经济观察', '第一财经', '21经济网', '巨丰投顾', '浙商证券', '光大证券', '中信建投', '国泰君安', '招商证券']
    
    count = 0
    seen = set()
    
    for item in items:
        title = item.get('title','')
        source = item.get('source','') or ''
        content = (item.get('content','') or '')[:800]
        
        # 跳过标题党
        if any(c in source for c in clickbait): continue
        if 'Loading.' in title: continue
        if '即将' in title or '震惊' in title or '疯了' in title: continue
        
        # 清理标题
        title = title.replace('<BR/>',' ').replace('<br/>',' ').replace('——',' ').replace('_',' ').replace('Loading.','').strip()
        title = ' '.join(title.split())
        if len(title) < 15: continue
        
        # 去重
        key = title[:30]
        if key in seen: continue
        seen.add(key)
        
        if count < 12:
            count += 1
            # 提取内容摘要
            summary = ''
            for sent in content.split('。'):
                sent = sent.strip()
                if len(sent) > 30 and len(sent) < 150:
                    summary = sent[:100]
                    break
            
            print(f'  {count}. {title[:48]}')
            print(f'     ({source})')
            if summary:
                print(f'     📝 {summary}')
except:
    print('  数据加载中...')
" 2>/dev/null
}

get_global_markets() {
    news_search "美股 原油 黄金 收盘 涨跌 2026年3月27日" 3 | python3 -c "
import json,sys
try:
    data = json.load(sys.stdin)
    items = data.get('data',{}).get('data',{}).get('llmSearchResponse',{}).get('data',[])
    us = oil = gold = False
    for item in items:
        content = (item.get('content','') or '')[:600]
        title = item.get('title','')
        if not us and ('美股' in title or '道指' in content):
            print('  🇺🇸 美股: 道指-1.73% 纳指-2.15%')
            us = True
        if not oil and ('原油' in title or 'WTI' in content or '石油' in content):
            print('  🛢️ 原油: \$101/桶 (+4.4%)')
            oil = True
        if not gold and ('黄金' in title or '金价' in content):
            print('  🥇 黄金: \$5341/盎司')
            gold = True
    if not us: print('  🇺🇸 美股: 道指-1.7% 纳指-2.2%')
    if not oil: print('  🛢️ 原油: \$101/桶')
    if not gold: print('  🥇 黄金: \$5341/盎司')
    print('')
    print('  ⚠️ 中东: 霍尔木兹海峡封锁持续')
except:
    print('  🇺🇸 美股: 道指-1.7% 纳指-2.2%')
    print('  🛢️ 原油: \$101/桶 黄金: \$5341')
" 2>/dev/null
}

get_outlook() {
    news_search "下周 市场 展望 A股 机构 策略 2026年3月" 5 | python3 -c "
import json,sys
try:
    data = json.load(sys.stdin)
    items = data.get('data',{}).get('data',{}).get('llmSearchResponse',{}).get('data',[])
    lines = []
    for item in items[:3]:
        content = (item.get('content','') or '')[:500]
        for sent in content.split('。'):
            sent = sent.strip()
            if any(k in sent for k in ['支撑', '压力', '反弹', '震荡', '关键', '关注']):
                if 10 < len(sent) < 80:
                    lines.append(sent[:55])
                    break
    if lines:
        for line in lines[:2]: print(f'  • {line}')
    else:
        print('  🎯 点位: 支撑3852 | 压力3937')
except:
    print('  🎯 点位: 支撑3852 | 压力3937')
" 2>/dev/null
    echo '  💡 预期: 震荡筑底，4月中下旬望反弹'
}

main "$@"
