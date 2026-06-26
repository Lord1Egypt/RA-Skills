#!/bin/bash
# ==============================================================================
# BTC V4.0 实时监控脚本（修复版 - 使用curl获取价格）
# ==============================================================================

LOG_FILE="$HOME/.okx_data/signal_monitor_v40_fixed.log"
STATE_FILE="$HOME/.okx_data/trading_state_v40.txt"
TOKEN_FILE="$HOME/.config/trading_bot/telegram_token"

BOT_TOKEN=$(cat "$TOKEN_FILE" 2>/dev/null)
CHAT_ID="5876347015"

# 初始化
init_state() {
    if [ ! -f "$STATE_FILE" ]; then
        echo "NONE|0|0|0|0" > "$STATE_FILE"
    fi
}

read_state() {
    STATE=$(cat "$STATE_FILE" 2>/dev/null)
    POSITION=$(echo "$STATE" | cut -d'|' -f1)
    ENTRY_PRICE=$(echo "$STATE" | cut -d'|' -f2)
    STOP_LOSS=$(echo "$STATE" | cut -d'|' -f3)
    TAKE_PROFIT=$(echo "$STATE" | cut -d'|' -f4)
    ENTRY_TIME=$(echo "$STATE" | cut -d'|' -f5)
}

save_state() {
    echo "$1|$2|$3|$4|$5" > "$STATE_FILE"
}

# 获取价格（多种方式）
get_price() {
    local price=""
    
    # 方式1: OKX CLI
    price=$(okx market index-tickers --instId BTC-USD 2>/dev/null | grep BTC-USD | head -1 | awk '{print $2}' | tr -d ',$' 2>/dev/null)
    
    # 方式2: 如果CLI失败，使用curl
    if [ -z "$price" ]; then
        price=$(curl -s "https://www.okx.com/api/v5/market/ticker?instId=BTC-USD" 2>/dev/null | grep -o '"last":"[0-9.]*"' | head -1 | cut -d'"' -f4)
    fi
    
    # 方式3: 备用API
    if [ -z "$price" ]; then
        price=$(curl -s "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT" 2>/dev/null | grep -o '"price":"[0-9.]*"' | cut -d'"' -f4)
    fi
    
    echo "$price"
}

send_notification() {
    local title="$1"
    local message="$2"
    
    osascript -e "display notification \"$message\" with title \"$title\" sound name \"Glass\"" 2>/dev/null
    
    if [ -n "$BOT_TOKEN" ]; then
        curl -s -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" \
            -d "chat_id=$CHAT_ID" \
            -d "text=$message" \
            -d "parse_mode=HTML" > /dev/null 2>&1
    fi
}

# 初始化
mkdir -p "$HOME/.okx_data"
init_state

echo "========================================" >> "$LOG_FILE"
echo "$(date '+%Y-%m-%d %H:%M:%S') - V4.0 修复版监控启动" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

echo "🚀 BTC V4.0 修复版监控已启动"
echo "   价格获取: OKX API + 备用源"
echo "   检查频率: 每1分钟"
echo ""

send_notification "✅ 监控启动" "BTC V4.0 修复版已启动%0A%0A🛠️ 修复内容:%0A• 价格获取更稳定%0A• 多源备用%0A• 每分钟检查"

LAST_SIGNAL_CHECK=0
COUNTER=0

while true; do
    CURRENT_TIME=$(date '+%Y-%m-%d %H:%M:%S')
    CURRENT_EPOCH=$(date +%s)
    
    # 每10次显示一次心跳
    COUNTER=$((COUNTER + 1))
    if [ $COUNTER -ge 10 ]; then
        COUNTER=0
        echo "$(date '+%H:%M:%S') - 监控运行中..." >> "$LOG_FILE"
    fi
    
    # 获取价格
    PRICE=$(get_price)
    
    read_state
    
    # 持仓中监控
    if [ "$POSITION" != "NONE" ] && [ -n "$PRICE" ] && [ "$PRICE" != "0" ]; then
        echo "$CURRENT_TIME - 持仓监控: $POSITION @ $ENTRY_PRICE, 当前: $PRICE" >> "$LOG_FILE"
        
        if [ "$POSITION" == "LONG" ]; then
            # 使用awk进行浮点数比较
            if awk "BEGIN {exit !($PRICE >= $TAKE_PROFIT)}"; then
                PNL=$(awk "BEGIN {printf \"%.2f\", ($PRICE - $ENTRY_PRICE) / $ENTRY_PRICE * 1000}")
                send_notification "🎯 止盈触发" "🎯 <b>止盈触发！</b>%0A%0A📈 做多 (LONG)%0A💰 入场: \$$ENTRY_PRICE%0A💰 当前: \$$PRICE%0A📊 盈亏: +$PNL%%25"
                echo "$CURRENT_TIME - ✅ 止盈: LONG $ENTRY_PRICE → $PRICE (+$PNL%)" >> "$LOG_FILE"
                save_state "NONE" "0" "0" "0" "0"
                POSITION="NONE"
            
            elif awk "BEGIN {exit !($PRICE <= $STOP_LOSS)}"; then
                PNL=$(awk "BEGIN {printf \"%.2f\", ($PRICE - $ENTRY_PRICE) / $ENTRY_PRICE * 1000}")
                send_notification "🛑 止损触发" "🛑 <b>止损触发！</b>%0A%0A📈 做多 (LONG)%0A💰 入场: \$$ENTRY_PRICE%0A💰 当前: \$$PRICE%0A📊 盈亏: $PNL%%25"
                echo "$CURRENT_TIME - 🛑 止损: LONG $ENTRY_PRICE → $PRICE ($PNL%)" >> "$LOG_FILE"
                save_state "NONE" "0" "0" "0" "0"
                POSITION="NONE"
            fi
            
        elif [ "$POSITION" == "SHORT" ]; then
            if awk "BEGIN {exit !($PRICE <= $TAKE_PROFIT)}"; then
                PNL=$(awk "BEGIN {printf \"%.2f\", ($ENTRY_PRICE - $PRICE) / $ENTRY_PRICE * 1000}")
                send_notification "🎯 止盈触发" "🎯 <b>止盈触发！</b>%0A%0A📉 做空 (SHORT)%0A💰 入场: \$$ENTRY_PRICE%0A💰 当前: \$$PRICE%0A📊 盈亏: +$PNL%%25"
                echo "$CURRENT_TIME - ✅ 止盈: SHORT $ENTRY_PRICE → $PRICE (+$PNL%)" >> "$LOG_FILE"
                save_state "NONE" "0" "0" "0" "0"
                POSITION="NONE"
            
            elif awk "BEGIN {exit !($PRICE >= $STOP_LOSS)}"; then
                PNL=$(awk "BEGIN {printf \"%.2f\", ($ENTRY_PRICE - $PRICE) / $ENTRY_PRICE * 1000}")
                send_notification "🛑 止损触发" "🛑 <b>止损触发！</b>%0A%0A📉 做空 (SHORT)%0A💰 入场: \$$ENTRY_PRICE%0A💰 当前: \$$PRICE%0A📊 盈亏: $PNL%%25"
                echo "$CURRENT_TIME - 🛑 止损: SHORT $ENTRY_PRICE → $PRICE ($PNL%)" >> "$LOG_FILE"
                save_state "NONE" "0" "0" "0" "0"
                POSITION="NONE"
            fi
        fi
    fi
    
    # 信号检查（每5分钟）
    if [ $((CURRENT_EPOCH - LAST_SIGNAL_CHECK)) -ge 300 ]; then
        LAST_SIGNAL_CHECK=$CURRENT_EPOCH
        
        cd "$HOME/Desktop"
        python3 btc_10x_strategy_v40.py > /tmp/strategy_output.txt 2>&1
        
        if [ -f /tmp/btc_signal.txt ]; then
            SIGNAL=$(cut -d',' -f1 /tmp/btc_signal.txt)
            SIGNAL_PRICE=$(cut -d',' -f2 /tmp/btc_signal.txt)
        else
            SIGNAL="0"
            SIGNAL_PRICE="0"
        fi
        
        # 新开仓
        if [ "$POSITION" == "NONE" ]; then
            if [ "$SIGNAL" == "1" ]; then
                ENTRY=$SIGNAL_PRICE
                STOP=$(echo "$ENTRY * 0.9955" | bc -l 2>/dev/null | cut -d'.' -f1)
                TP=$(echo "$ENTRY * 1.008" | bc -l 2>/dev/null | cut -d'.' -f1)
                [ -z "$STOP" ] && STOP=$(awk "BEGIN {printf \"%.0f\", $ENTRY * 0.9955}")
                [ -z "$TP" ] && TP=$(awk "BEGIN {printf \"%.0f\", $ENTRY * 1.008}")
                
                save_state "LONG" "$ENTRY" "$STOP" "$TP" "$CURRENT_TIME"
                send_notification "🚨 开多信号" "🚨 <b>开多信号！</b>%0A%0A📈 做多 (LONG)%0A💰 入场: \$$ENTRY%0A🛑 止损: \$$STOP%0A🎯 止盈: \$$TP"
                echo "$CURRENT_TIME - 🚨 开多: $ENTRY, 止损:$STOP, 止盈:$TP" >> "$LOG_FILE"
                
            elif [ "$SIGNAL" == "-1" ]; then
                ENTRY=$SIGNAL_PRICE
                STOP=$(awk "BEGIN {printf \"%.0f\", $ENTRY * 1.0045}")
                TP=$(awk "BEGIN {printf \"%.0f\", $ENTRY * 0.992}")
                
                save_state "SHORT" "$ENTRY" "$STOP" "$TP" "$CURRENT_TIME"
                send_notification "🚨 开空信号" "🚨 <b>开空信号！</b>%0A%0A📉 做空 (SHORT)%0A💰 入场: \$$ENTRY%0A🛑 止损: \$$STOP%0A🎯 止盈: \$$TP"
                echo "$CURRENT_TIME - 🚨 开空: $ENTRY, 止损:$STOP, 止盈:$TP" >> "$LOG_FILE"
            fi
        fi
    fi
    
    sleep 60
done
