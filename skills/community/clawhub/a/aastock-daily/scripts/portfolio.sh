#!/bin/bash
#==============================================================================
# A股日报 - 持仓追踪 v4
# 支持：持仓股吧舆情 + 事件预警
#==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

main() {
    local session="${1:-晚间}"
    log INFO "开始生成持仓追踪报告 (${session}) - 含股吧+事件预警"
    
    if is_weekend; then
        echo "📺 周末休市，持仓追踪暂停"
        return 0
    fi
    
    local portfolio=$(get_portfolio)
    if [ -z "$portfolio" ] || [ "$portfolio" = "[]" ]; then
        echo "⚠️ 持仓列表为空，请检查 config.json"
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
    
    local time_label=""
    [ "$session" = "早间" ] && time_label="09:30" || time_label="18:00"
    
    local output=""
    output="$(build_header "持仓追踪(${session})" "$time_label")"
    output="${output}\n🏠 共 ${stock_count} 只持仓股"
    output="${output}\n"
    
    # 解析持仓列表并获取数据
    local stocks_data=$(echo "$portfolio" | python3 -c "
import json,sys
try:
    stocks = json.load(sys.stdin)
    for s in stocks:
        name = s.get('name','')
        code = s.get('code','')
        # 判断交易所 (6开头上海, 0/3开头深圳)
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
        output="${output}\n$(get_stock_report "$name" "$code" "$secid" "$count")"
        output="${output}\n"
        count=$((count + 1))
    done <<< "$stocks_data"
    
    # 事件预警（仅晚间推送）
    if [ "$session" = "晚间" ]; then
        output="${output}\n$(divider)"
        output="${output}\n⚠️ 持仓股事件预警"
        output="${output}\n$(get_event_alerts)"
    fi
    
    output="${output}\n$(divider)"
    output="${output}\n💡 持仓信息仅供参考，不构成投资建议"
    
    echo -e "$output"
    log INFO "持仓追踪报告生成完成 (含股吧+事件预警)"
}

get_stock_report() {
    local name="$1"
    local code="$2"
    local secid="$3"
    local index="$4"
    
    local info=""
    info="${info}\n${index}. ${name} (${code})"
    
    # 获取实时行情
    local quote=$(get_stock_quote "$secid")
    IFS='|' read -r q_name price change pct flow <<< "$quote"
    
    if [ "$price" != "-" ] && [ -n "$price" ]; then
        local sign=""
        local emoji="📊"
        [ "$(echo "$pct > 0" | bc 2>/dev/null)" = "1" ] && sign="+" && emoji="📈"
        [ "$(echo "$pct < 0" | bc 2>/dev/null)" = "1" ] && emoji="📉"
        
        info="${info}\n   价格: ${price} (${sign}${change} ${sign}${pct}%) ${emoji}"
        
        # 主力资金
        if [ -n "$flow" ] && [ "$flow" != "0" ]; then
            flow_str=$(python3 -c "
flow = float('${flow}')
if abs(flow) >= 100000000:
    print(f'{flow/100000000:.2f}亿')
elif abs(flow) >= 10000:
    print(f'{flow/10000:.2f}万')
else:
    print(f'{flow:.0f}')
" 2>/dev/null)
            info="${info}\n   主力: ${flow_str}"
        fi
    else
        info="${info}\n   (等待开盘...)"
    fi
    
    # 获取最新公告
    local news_result=$(news_search "${name} ${code} 公告 研报" 1)
    local news=$(echo "$news_result" | python3 -c "
import json,sys
try:
    data = json.load(sys.stdin)
    items = data.get('data',{}).get('data',{}).get('llmSearchResponse',{}).get('data',[])
    if items:
        for item in items[:1]:
            title = item.get('title','')[:45].replace('<BR/>',' ').replace('<br/>',' ')
            source = item.get('source','')
            date = item.get('date','')[:10]
            print(f'📢 最新: {title}')
except:
    pass
" 2>/dev/null)
    
    [ -n "$news" ] && info="${info}\n   ${news}"
    
    # 获取股吧舆情
    local guba_result=$(news_search "${name} 散户 投资者 股吧 观点" 3)
    local guba=$(echo "$guba_result" | python3 -c "
import json,sys
try:
    data = json.load(sys.stdin)
    items = data.get('data',{}).get('data',{}).get('llmSearchResponse',{}).get('data',[])
    comments = []
    seen = set()
    for item in items:
        title = item.get('title','')
        source = item.get('source','') or ''
        if any(x in source for x in ['互动易', '上证互动', '股吧', '社区', '投资者']) or '请问' in title or '吗？' in title or '怎么看' in title or '持有' in title:
            title = title[:40].replace('<BR/>',' ').replace('<br/>',' ')
            if title not in seen:
                seen.add(title)
                comments.append(title)
    for c in comments[:2]:
        print(f'💬 {c}')
except:
    pass
" 2>/dev/null)
    
    if [ -n "$guba" ]; then
        info="${info}\n   💬 股吧舆情:"
        while IFS= read -r line; do
            [ -n "$line" ] && info="${info}\n   ${line}"
        done <<< "$guba"
    else
        info="${info}\n   💬 股吧: 暂无热议"
    fi
    
    echo "$info"
}

get_event_alerts() {
    # 搜索持仓相关的解禁、减持、业绩预警
    local stocks=$(echo "$(get_portfolio)" | python3 -c "
import json,sys
try:
    stocks = json.load(sys.stdin)
    print(' '.join([s.get('name','') for s in stocks]))
except:
    print('')
" 2>/dev/null)
    
    local result=$(news_search "${stocks} 解禁 减持 业绩预告 增减持" 8)
    
    echo "$result" | python3 -c "
import json,sys
try:
    data = json.load(sys.stdin)
    items = data.get('data',{}).get('data',{}).get('llmSearchResponse',{}).get('data',[])
    
    alerts = []
    keywords = ['解禁', '减持', '业绩', '预亏', '预减', '预增', '预盈', '增减持', '风险']
    
    for item in items:
        title = item.get('title','')
        if any(k in title for k in keywords):
            title_short = title[:50].replace('<BR/>',' ').replace('<br/>',' ')
            source = item.get('source','') or '未知'
            date = item.get('date','')[:10]
            
            # 判断类型
            if '解禁' in title:
                emoji = '🔶'
            elif '减持' in title:
                emoji = '🔴'
            elif any(k in title for k in ['预亏', '预减', '风险']):
                emoji = '🔴'
            elif any(k in title for k in ['预增', '预盈', '增持']):
                emoji = '🟢'
            else:
                emoji = '🟡'
            
            alerts.append(f'{emoji} {title_short}')
            alerts.append(f'   ({source} | {date})')
    
    # 去重
    seen = set()
    for a in alerts:
        if a not in seen:
            seen.add(a)
            print(f'  {a}')
    
    if not alerts:
        print('  ✅ 暂无重大事件预警')
except:
    print('  数据加载中...')
" 2>/dev/null || echo "  数据加载中..."
}

main "$@"
