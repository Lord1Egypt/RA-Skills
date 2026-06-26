#!/bin/bash
# Token Guard - MiniMax 5小时窗口断路器 (macOS compatible)
# 用法:
#   token-guard.sh check          # 检查是否还能跑
#   token-guard.sh increment N    # 报告本次使用了N次API调用

STATE_FILE="${HOME}/.openclaw/token-state.json"
WINDOW_LIMIT=1500
WEEKLY_LIMIT=15000
WARN_THRESHOLD=1200   # 80% of 1500
STOP_THRESHOLD=1425   # 95% of 1500

get_window_key() {
    # 返回当前5小时窗口的key (GMT+8)
    local hour=$(date +%H)
    if [ "$hour" -ge 0 ] && [ "$hour" -lt 5 ]; then echo "window_00"
    elif [ "$hour" -ge 5 ] && [ "$hour" -lt 10 ]; then echo "window_05"
    elif [ "$hour" -ge 10 ] && [ "$hour" -lt 15 ]; then echo "window_10"
    elif [ "$hour" -ge 15 ] && [ "$hour" -lt 20 ]; then echo "window_15"
    else echo "window_20"
    fi
}

init_state() {
    local window_key=$(get_window_key)
    local now=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    
    if [ ! -f "$STATE_FILE" ]; then
        cat > "$STATE_FILE" << EOF
{
  "current_window": "$window_key",
  "window_calls": 0,
  "window_started": "$now",
  "weekly_total": 0,
  "week_started": "$now",
  "last_updated": "$now"
}
EOF
    else
        local saved_window=$(python3 -c "import json; d=json.load(open('$STATE_FILE')); print(d.get('current_window',''))" 2>/dev/null)
        if [ "$saved_window" != "$window_key" ]; then
            python3 -c "
import json
d = json.load(open('$STATE_FILE'))
d['current_window'] = '$window_key'
d['window_calls'] = 0
d['window_started'] = '$now'
d['last_updated'] = '$now'
json.dump(d, open('$STATE_FILE','w'), indent=2)
" 2>/dev/null
        fi
    fi
}

do_check() {
    init_state
    
    local window_calls=$(python3 -c "import json; d=json.load(open('$STATE_FILE')); print(d.get('window_calls',0))" 2>/dev/null)
    local weekly=$(python3 -c "import json; d=json.load(open('$STATE_FILE')); print(d.get('weekly_total',0))" 2>/dev/null)
    
    local window_pct=$(python3 -c "print(round($window_calls/$WINDOW_LIMIT*100,1))")
    local weekly_pct=$(python3 -c "print(round($weekly/$WEEKLY_LIMIT*100,1))")
    
    echo "📊 Token 状态"
    echo "   窗口: $window_calls / $WINDOW_LIMIT ($window_pct%)"
    echo "   本周: $weekly / $WEEKLY_LIMIT ($weekly_pct%)"
    
    if [ $weekly -ge $WEEKLY_LIMIT ]; then
        echo "❌ 本周额度已耗尽"
        return 1
    fi
    
    if [ $window_calls -ge $WINDOW_LIMIT ]; then
        echo "❌ 当前窗口已耗尽"
        return 1
    fi
    
    if [ $window_calls -gt $STOP_THRESHOLD ]; then
        echo "🚨 窗口即将耗尽 (${window_pct}%)"
        return 1
    fi
    
    if [ $window_calls -gt $WARN_THRESHOLD ]; then
        echo "⚠️ 窗口使用率 ${window_pct}% (超过80%)"
    fi
    
    echo "✅ 可以继续"
    return 0
}

do_increment() {
    local count=${1:-1}
    init_state
    
    local now=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    python3 -c "
import json
d = json.load(open('$STATE_FILE'))
d['window_calls'] = d.get('window_calls', 0) + $count
d['weekly_total'] = d.get('weekly_total', 0) + $count
d['last_updated'] = '$now'
json.dump(d, open('$STATE_FILE','w'), indent=2)
" 2>/dev/null
    
    echo "✅ 已追加 $count 次调用"
    do_check
}

case "$1" in
    check)  do_check ;;
    increment) do_increment "$2" ;;
    *)  echo "用法: token-guard.sh [check|increment N]" ;;
esac
