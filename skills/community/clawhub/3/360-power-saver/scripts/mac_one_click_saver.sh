#!/bin/bash
# 360 Power Saver - 一键省电™ 模块 (macOS 版本)
# 分析系统电源状态并弹窗展示

# 获取电源信息
get_power_info() {
    # 获取电池状态
    battery_status=$(pmset -g batt 2>/dev/null)
    
    if echo "$battery_status" | grep -q "Battery"; then
        charge_percent=$(echo "$battery_status" | grep -o '[0-9]*%' | tr -d '%' | head -1)
        
        if echo "$battery_status" | grep -q "charging"; then
            power_source="⚡ 电源适配器 (充电中)"
        elif echo "$battery_status" | grep -q "charged"; then
            power_source="⚡ 电源适配器 (已充满)"
        else
            power_source="🔋 电池供电"
        fi
    else
        charge_percent="N/A"
        power_source="🔌 桌面设备 (电源适配器)"
    fi

    # 获取 CPU 信息
    cpu_name=$(sysctl -n machdep.cpu.brand_string 2>/dev/null | head -1)
    cpu_cores=$(sysctl -n hw.ncpu 2>/dev/null)

    # 获取内存信息
    mem_total=$(sysctl -n hw.memsize 2>/dev/null)
    mem_total_gb=$((mem_total / 1024 / 1024 / 1024))

    # 获取内存使用
    mem_info=$(vm_stat 2>/dev/null)
    free_pages=$(echo "$mem_info" | grep "free" | awk '{print $3}' | tr -d '.')
    active_pages=$(echo "$mem_info" | grep "active" | awk '{print $3}' | tr -d '.')
    inactive_pages=$(echo "$mem_info" | grep "inactive" | awk '{print $3}' | tr -d '.')
    
    page_size=4096
    used_mem=$(( (active_pages + inactive_pages) * page_size / 1024 / 1024 / 1024 ))
    
    if [ "$mem_total_gb" -gt 0 ]; then
        mem_percent=$(( used_mem * 100 / mem_total_gb ))
    else
        mem_percent=0
    fi

    # 进度条
    bar_len=$(( mem_percent / 10 ))
    bar=$(printf '█%.0s' $(seq 1 $bar_len 2>/dev/null))$(printf '░%.0s' $(seq 1 $(( 10 - bar_len )) 2>/dev/null))

    # 构建消息
    msg="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   360°省电大师 - 一键省电
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ 电源状态: $power_source"

    if [ "$charge_percent" != "N/A" ]; then
        msg+="
🔋 电池电量: ${charge_percent}%"
    fi

    msg+="

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   系统信息
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🖥️ CPU: ${cpu_name:-"未知"}
📈 核心数: ${cpu_cores:-"未知"} 核

💾 内存占用: [$bar] ${mem_percent}%
   已使用: ${used_mem} GB / ${mem_total_gb} GB

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 优化建议
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    # 添加建议
    if [ "$charge_percent" != "N/A" ] && [ "$charge_percent" -lt 30 ] && echo "$power_source" | grep -q "电池"; then
        msg+="
• 电量较低，建议尽快充电"
    fi

    if [ "$mem_percent" -gt 80 ]; then
        msg+="
• 内存占用较高，建议关闭不需要的应用"
    fi

    if echo "$power_source" | grep -q "电池"; then
        msg+="
• 正在使用电池供电，可降低屏幕亮度延长续航"
    fi

    msg+="

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    # 弹窗展示
    osascript -e "display dialog \"$msg\" buttons {\"确定\"} default button \"确定\" with title \"360°省电大师 - 一键省电\""
}

# 执行
get_power_info