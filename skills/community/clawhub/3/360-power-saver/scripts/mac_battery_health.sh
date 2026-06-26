#!/bin/bash
# 360 Power Saver - 电池健康分析™ 模块 (macOS 版本)
# 获取电池信息并弹窗展示

# 获取电池信息
get_battery_info() {
    # 检查是否有电池
    if ! system_profiler SPPowerDataType 2>/dev/null | grep -q "Battery Information"; then
        osascript -e 'display dialog "未检测到电池设备。本功能仅适用于 MacBook。" buttons {"确定"} default button "确定" with title "360°省电大师 - 电池健康分析"'
        exit 0
    fi

    # 获取电池详细信息
    battery_info=$(system_profiler SPPowerDataType 2>/dev/null)

    # 提取关键信息
    cycle_count=$(echo "$battery_info" | grep "Cycle Count" | awk '{print $3}')
    condition=$(echo "$battery_info" | grep "Condition" | sed 's/.*: //')
    max_capacity=$(echo "$battery_info" | grep "Maximum Capacity" | awk '{print $3}')

    # 获取电量百分比和充电状态
    battery_status=$(pmset -g batt 2>/dev/null)
    charge_percent=$(echo "$battery_status" | grep -o '[0-9]*%' | tr -d '%' | head -1)
    
    if echo "$battery_status" | grep -q "charging"; then
        charging_status="⚡ 充电中"
    elif echo "$battery_status" | grep -q "charged"; then
        charging_status="✅ 已充满"
    else
        charging_status="🔋 放电中"
    fi

    # 构建消息
    msg="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   360°省电大师 - 电池健康分析
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔋 当前电量: ${charge_percent}%
📊 电池状态: ${charging_status}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   电池详细信息
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 循环次数: ${cycle_count:-"未知"} 次
📋 电池状态: ${condition:-"未知"}
📋 最大容量: ${max_capacity:-"未知"}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 提示：可在「系统信息」中查看更详细的电池报告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    # 弹窗展示
    osascript -e "display dialog \"$msg\" buttons {\"确定\"} default button \"确定\" with title \"360°省电大师 - 电池健康分析\""
}

# 执行
get_battery_info