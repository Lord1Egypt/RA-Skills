#!/bin/bash

# 提醒模块

# 发送提醒消息
send_reminder() {
    local message="$1"
    echo "🔔 提醒: $message"
}

# 早餐提醒
breakfast_reminder() {
    send_reminder "早餐时间到了！记得吃一顿营养丰富的早餐哦～🍳"
    echo "   建议: 搭配蛋白质（鸡蛋、牛奶）和碳水（面包、燕麦）"
}

# 午餐提醒
lunch_reminder() {
    send_reminder "午餐时间到了！吃饱了才有力气减肥哦～🥗"
    echo "   建议: 多吃蔬菜，适量主食和蛋白质，七分饱刚刚好"
}

# 晚餐提醒
dinner_reminder() {
    send_reminder "晚餐时间到了！记得早点吃晚餐，睡前3小时不进食哦～🥣"
    echo "   建议: 清淡为主，避免高油高糖食物"
}

# 步数提醒
steps_reminder() {
    local today=$(date +%Y%m%d)
    local daily_file="$DATA_DIR/daily_records/${today}.json"
    
    if [[ -f "$daily_file" ]]; then
        local current_steps=$(grep -o '"steps": [0-9]*' "$daily_file" | grep -o '[0-9]*')
        local target_steps=$(grep -o '"target_steps": [0-9]*' "$daily_file" | grep -o '[0-9]*')
        
        if (( current_steps < target_steps * 5 / 10 )); then
            send_reminder "目前只走了${current_steps}步，距离目标还差$((target_steps - current_steps))步！🏃"
            echo "   起来活动一下吧，久坐伤身哦～"
        elif (( current_steps < target_steps * 8 / 10 )); then
            send_reminder "已经走了${current_steps}步，还差$((target_steps - current_steps))步就达标了！💪"
        else
            send_reminder "太棒了！已经走了${current_steps}步，快达标了！🎉"
        fi
    else
        send_reminder "记得记录今日步数哦！健康生活从走路开始～🚶"
    fi
}

# 睡前总结提醒
bedtime_summary_reminder() {
    send_reminder "一天快要结束了！来看看今天的成果吧～🌙"
    echo ""
    show_daily_summary
    echo ""
    echo "💤 早点休息，充足的睡眠对减肥也很重要哦！"
    echo "明天继续加油！晚安～😴"
}

# 饮水提醒
water_reminder() {
    send_reminder "该喝水啦！保持充足的水分摄入有助于新陈代谢哦～💧"
    echo "   建议: 每天喝2-3升水，每隔1-2小时喝一杯"
}

# 鼓励消息
encouragement_message() {
    local messages=(
        "你做得很棒！继续保持，目标就在前方！🌟"
        "每一步都算数，每一天都在进步！💪"
        "相信自己，你可以做到的！✨"
        "坚持就是胜利，今天也是元气满满的一天！🌈"
        "健康减肥，快乐生活！为你骄傲！🎉"
        "不要着急，慢慢来，好身材需要时间沉淀～🌱"
        "今天的努力是明天的收获，加油！🏆"
    )
    
    local random_index=$((RANDOM % ${#messages[@]}))
    echo "💬 ${messages[$random_index]}"
}

# 检查提醒时间（供定时任务调用）
check_reminder_time() {
    local hour=$(date +%H)
    local minute=$(date +%M)
    
    # 早餐提醒 7:30-8:30
    if (( hour == 7 && minute >= 30 )) || (( hour == 8 && minute < 30 )); then
        breakfast_reminder
    fi
    
    # 午餐提醒 11:30-12:30
    if (( hour == 11 && minute >= 30 )) || (( hour == 12 && minute < 30 )); then
        lunch_reminder
    fi
    
    # 晚餐提醒 17:30-18:30
    if (( hour == 17 && minute >= 30 )) || (( hour == 18 && minute < 30 )); then
        dinner_reminder
    fi
    
    # 步数提醒 10:00, 15:00, 20:00
    if (( hour == 10 && minute < 10 )) || (( hour == 15 && minute < 10 )) || (( hour == 20 && minute < 10 )); then
        steps_reminder
    fi
    
    # 睡前总结 22:00
    if (( hour == 22 && minute < 10 )); then
        bedtime_summary_reminder
    fi
}
