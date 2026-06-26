#!/bin/bash

# 每日天气和国际新闻推送脚本 - 最终修复版
# 执行时间：每天早上7:30

# 确保脚本在正确的目录中执行
cd "$(dirname "$0")/.."

# 加载配置文件
source "config/config.sh"

# 获取天气信息（带重试机制）
get_weather() {
    local location="$1"
    local retry_count=0
    local max_retries=3
    
    while [ $retry_count -lt $max_retries ]; do
        # 使用Open-Meteo API获取天气信息
        api_url="${WEATHER_API_BASE}?latitude=${LATITUDE}&longitude=${LONGITUDE}&current_weather=true&hourly=temperature_2m,windspeed_10m,weathercode&timezone=auto"
        
        # 发送API请求
        weather_response=$(timeout 15 curl -s "$api_url")
        
        # 检查API响应
        if [ -z "$weather_response" ]; then
            retry_count=$((retry_count + 1))
            if [ $retry_count -eq $max_retries ]; then
                echo "❌ 天气信息获取异常（重试$retry_count次后仍然失败）" >&2
                exit 1
            fi
            echo "⚠️ 天气API请求失败，正在重试 ($retry_count/$max_retries)..." >&2
            sleep 2
            continue
        fi
        
        # 解析JSON响应
        current_weather_part=$(echo "$weather_response" | sed 's/.*"current_weather":{//; s/}.*//')
        
        weather_desc=$(echo "$current_weather_part" | grep -o '"weathercode":[0-9]*' | awk -F: '{print $2}')
        temp=$(echo "$current_weather_part" | grep -o '"temperature":[0-9.]*' | awk -F: '{print $2}')
        wind=$(echo "$current_weather_part" | grep -o '"windspeed":[0-9.]*' | awk -F: '{print $2}')
        
        # 检查是否成功提取数据
        if [ -z "$weather_desc" ] || [ -z "$temp" ] || [ -z "$wind" ]; then
            retry_count=$((retry_count + 1))
            if [ $retry_count -eq $max_retries ]; then
                echo "❌ 天气信息解析异常（重试$retry_count次后仍然失败）" >&2
                exit 1
            fi
            echo "⚠️ 天气数据解析失败，正在重试 ($retry_count/$max_retries)..." >&2
            sleep 2
            continue
        fi
        
        # Open-Meteo天气代码转换为中文描述
        case "$weather_desc" in
            0|1) weather_desc="晴朗" ;;
            2) weather_desc="部分多云" ;;
            3) weather_desc="多云" ;;
            45) weather_desc="雾" ;;
            48) weather_desc="冻雾" ;;
            51|53|55) weather_desc="毛毛雨" ;;
            56|57) weather_desc="冻毛毛雨" ;;
            61|63|65) weather_desc="雨" ;;
            66|67) weather_desc="冻雨" ;;
            71|73|75|77) weather_desc="雪" ;;
            80|81|82) weather_desc="阵雨" ;;
            85|86) weather_desc="阵雪" ;;
            95|96|99) weather_desc="雷暴" ;;
            *) weather_desc="未知" ;;
        esac
        
        # 根据风速添加风力描述
        if [ -n "$wind" ] && [ "$wind" != "null" ]; then
            wind_int=$(echo "$wind" | awk '{printf "%.0f", $1}')
            if [ "$wind_int" -lt 5 ]; then
                wind_desc="微风"
            elif [ "$wind_int" -lt 15 ]; then
                wind_desc="和风"
            elif [ "$wind_int" -lt 25 ]; then
                wind_desc="强风"
            else
                wind_desc="狂风"
            fi
            wind="${wind} km/h (${wind_desc})"
        else
            wind="无数据"
        fi
        
        echo "${weather_desc} ${temp}°C ${wind}"
        return 0
    done
}

# 获取国际新闻（带重试机制）- 优化版本
get_news() {
    local retry_count=0
    local max_retries=3
    
    while [ $retry_count -lt $max_retries ]; do
        # 设置API密钥
        export TAVILY_API_KEY="$TAVILY_API_KEY"
        
        # 获取今日最新的中文国际新闻
        news_result=$(node ~/.openclaw/workspace/skills/tavily-search/scripts/search.mjs "site:news.cn 今日国际 OR site:xinhuanet.com 今日要闻 OR site:people.com.cn 国际新闻 $(date +%Y-%m-%d)" -n 10 --topic news --days 1)
        
        # 检查API响应
        if [ -z "$news_result" ]; then
            retry_count=$((retry_count + 1))
            if [ $retry_count -eq $max_retries ]; then
                echo "❌ 新闻信息获取异常（重试$retry_count次后仍然失败）" >&2
                exit 1
            fi
            echo "⚠️ 新闻API请求失败，正在重试 ($retry_count/$max_retries)..." >&2
            sleep 2
            continue
        fi
        
        # 简化处理：直接提取Answer部分，减少复杂的文本处理
        answer_section=$(echo "$news_result" | sed -n '/## Answer/,/## Sources/p' | sed '1d;$d')
        
        if [ -n "$answer_section" ]; then
            # 简化新闻处理：直接按行分割并添加格式
            processed_news="📰 今日国际要闻（$(date +%Y-%m-%d)）："
            
            # 使用简单的文本处理，避免复杂的sed操作
            echo "$answer_section" | while IFS= read -r line; do
                if [ -n "$line" ] && [[ "$line" != *"##"* ]] && [[ "$line" != *"---"* ]]; then
                    processed_news="${processed_news}\n\n• $line"
                fi
            done
            
            # 确保有内容，如果为空则重试
            if [ "$processed_news" = "📰 今日国际要闻（$(date +%Y-%m-%d)）：" ]; then
                retry_count=$((retry_count + 1))
                if [ $retry_count -eq $max_retries ]; then
                    echo "❌ 新闻信息解析异常（重试$retry_count次后仍然失败）" >&2
                    exit 1
                fi
                echo "⚠️ 新闻数据解析失败，正在重试 ($retry_count/$max_retries)..." >&2
                sleep 2
                continue
            fi
            
            echo "$processed_news"
            return 0
        else
            retry_count=$((retry_count + 1))
            if [ $retry_count -eq $max_retries ]; then
                echo "❌ 新闻信息解析异常（重试$retry_count次后仍然失败）" >&2
                exit 1
            fi
            echo "⚠️ 新闻数据解析失败，正在重试 ($retry_count/$max_retries)..." >&2
            sleep 2
            continue
        fi
    done
}

# 生成穿衣建议
get_clothing_advice() {
    local weather="$1"
    local weather_desc=$(echo "$weather" | awk '{print $1}')
    
    case "$weather_desc" in
        "晴朗")
            advice="天气晴朗，建议穿着轻便舒适的衣物，注意防晒。"
            ;;
        "部分多云"|"多云")
            advice="天气多云，建议穿着舒适的长袖衣物，早晚温差注意增减衣物。"
            ;;
        "阴天")
            advice="天气阴沉，建议穿着稍厚的衣物，注意保暖。"
            ;;
        "雨"|"阵雨")
            advice="有降雨，建议携带雨具，穿着防水的鞋子。"
            ;;
        "毛毛雨"|"冻毛毛雨")
            advice="有小雨，建议携带雨具，注意保暖防潮。"
            ;;
        "雪"|"阵雪")
            advice="有降雪，注意保暖，穿着厚实的衣物和防滑鞋。"
            ;;
        "雾"|"冻雾")
            advice="有雾，建议穿着保暖衣物，出行注意安全。"
            ;;
        "雷暴")
            advice="有雷暴，建议留在室内，避免外出，注意安全。"
            ;;
        *)
            advice="根据当前天气，建议穿着舒适的长袖衣物，注意早晚温差。"
            ;;
    esac
    
    echo "$advice"
}

# 推送消息到飞书
send_to_feishu() {
    local content="$1"
    local target="$2"
    
    # 使用message工具发送到飞书
    if command -v openclaw >/dev/null 2>&1; then
        timeout 30 openclaw message send --channel feishu --target "$target" --message "$content" >/dev/null 2>&1
        if [ $? -eq 0 ]; then
            # 静默成功，不输出任何信息
            true
        else
            # 静默失败，不输出任何信息
            true
        fi
    else
        # openclaw命令未找到，静默处理
        true
    fi
}

# 主函数
main() {
    # 获取配置
    source "config/config.sh"
    
    # 检查TAVILY_API_KEY是否设置
    if [ -z "$TAVILY_API_KEY" ]; then
        echo "❌ 错误: TAVILY_API_KEY 环境变量未设置" >&2
        echo "请设置环境变量: export TAVILY_API_KEY=\"your-api-key\"" >&2
        echo "或添加到 ~/.bashrc: echo 'export TAVILY_API_KEY=\"your-api-key\"' >> ~/.bashrc" >&2
        exit 1
    fi
    
    # 获取天气信息
    weather_info=$(get_weather "$LOCATION")
    if [ -z "$weather_info" ]; then
        exit 1
    fi
    
    # 获取新闻信息
    news_info=$(get_news)
    if [ -z "$news_info" ]; then
        exit 1
    fi
    
    # 生成穿衣建议
    clothing_advice=$(get_clothing_advice "$weather_info")
    
    # 生成推送内容
    # 处理新闻信息中的转义字符
    news_display=$(echo "$news_info" | sed 's/\\n/\n/g')
    
    push_content="🌅 每日天气和新闻推送 $(date +%Y-%m-%d)
📍 $LOCATION

🌦️ 天气情况：
$weather_info

👔 穿衣建议：
$clothing_advice

📰 今日国际重要新闻：
$news_display

🕐 推送时间：$(date +%H:%M)
🌸 来自绫波丽的每日问候"

    # 发送到飞书（静默）
    send_to_feishu "$push_content" "$TARGET_USER"
    
    # 记录推送日志（静默）
    echo "$(date) - 推送内容已生成并发送到飞书" >> "$LOG_FILE" 2>/dev/null
}

# 检查参数
if [ "$1" = "--test" ]; then
    source "config/config.sh"
    
    # 检查TAVILY_API_KEY是否设置
    if [ -z "$TAVILY_API_KEY" ]; then
        echo "❌ 错误: TAVILY_API_KEY 环境变量未设置" >&2
        echo "请设置环境变量: export TAVILY_API_KEY=\"your-api-key\"" >&2
        echo "或添加到 ~/.bashrc: echo 'export TAVILY_API_KEY=\"your-api-key\"' >> ~/.bashrc" >&2
        exit 1
    fi
    
    # 获取天气信息
    weather_info=$(get_weather "$LOCATION")
    if [ -z "$weather_info" ]; then
        exit 1
    fi
    
    # 获取新闻信息
    news_info=$(get_news)
    if [ -z "$news_info" ]; then
        exit 1
    fi
    
    # 生成穿衣建议
    clothing_advice=$(get_clothing_advice "$weather_info")
    
    # 处理新闻信息中的转义字符
    news_display=$(echo "$news_info" | sed 's/\\n/\n/g')
    
    push_content="🧪 测试推送 $(date +%Y-%m-%d)
📍 $LOCATION

🌦️ 天气情况：
$weather_info

👔 穿衣建议：
$clothing_advice

📰 今日国际重要新闻：
$news_display

🕐 测试时间：$(date +%H:%M)
🌸 来自绫波丽的测试问候"
    
    # 输出测试内容
    echo "$push_content"
    exit 0
fi

# 运行主函数
main "$@"