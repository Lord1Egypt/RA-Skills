#!/bin/bash

# Daily Brief - 每日简报
# 整合天气和百度热搜

# 默认城市
DEFAULT_CITY="Shanghai"
CITY=${1:-$DEFAULT_CITY}

# 默认显示前10条热搜
TOP_N=10

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# 获取天气
get_weather() {
    echo -e "${PURPLE}🌤️  天气${NC}"
    local weather=$(curl -s "wttr.in/$CITY?format=3" 2>/dev/null)
    if [ $? -eq 0 ] && [ -n "$weather" ]; then
        echo -e "   $weather"
    else
        echo -e "   获取失败，请检查网络"
    fi
    echo ""
}

# 获取百度热搜
get_news() {
    echo -e "${BLUE}🔥 百度热搜${NC}"
    
    local hot_data=$(curl -s "https://top.baidu.com/api/board?platform=wise&tab=realtime" 2>/dev/null)
    
    if [ $? -eq 0 ] && [ -n "$hot_data" ]; then
        # 解析JSON并显示前TOP_N条
        local count=0
        while IFS= read -r word; do
            if [ $count -lt $TOP_N ]; then
                count=$((count + 1))
                echo -e "   ${YELLOW}$count.${NC} $word"
            fi
        done < <(echo "$hot_data" | grep -o '"word":"[^"]*"' | sed 's/"word":"//;s/"$//')
    else
        echo -e "   获取失败，请检查网络"
    fi
    echo ""
}

# 今日提示
get_tip() {
    local tips=(
        "又是新的一天，加油！"
        "记得多喝水哦~"
        "保持好心情，事事顺利！"
        "工作再忙，也要注意休息~"
        "今天也要元气满满！"
    )
    local random_tip=${tips[$((RANDOM % ${#tips[@]}))]}
    echo -e "${GREEN}💡 今日提示: $random_tip${NC}"
}

# 主函数
main() {
    echo ""
    echo -e "${BLUE}╔════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║     📅 $(date '+%Y-%m-%d') 每日简报     ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════╝${NC}"
    echo ""
    
    get_weather
    get_news
    get_tip
    
    echo ""
}

# 运行
main
