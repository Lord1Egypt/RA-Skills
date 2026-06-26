#!/bin/bash

# Baidu Hot - 百度热搜
# 获取百度热搜榜

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 默认显示前20条
TOP_N=${1:-20}

# 获取真实百度热搜
get_hot_list() {
    echo -e "${BLUE}🔥 百度热搜榜 - $(date '+%Y-%m-%d %H:%M')${NC}"
    echo ""
    
    local hot_data=$(curl -s "https://top.baidu.com/api/board?platform=wise&tab=realtime" 2>/dev/null)
    
    if [ $? -eq 0 ] && [ -n "$hot_data" ]; then
        local count=0
        while IFS= read -r word; do
            if [ $count -lt $TOP_N ]; then
                count=$((count + 1))
                # 给前3名加特殊标记
                if [ $count -eq 1 ]; then
                    echo -e "${RED}🥇 $count. $word${NC}"
                elif [ $count -eq 2 ]; then
                    echo -e "${YELLOW}🥈 $count. $word${NC}"
                elif [ $count -eq 3 ]; then
                    echo -e "${BLUE}🥉 $count. $word${NC}"
                else
                    echo -e "$count. $word"
                fi
            fi
        done < <(echo "$hot_data" | grep -o '"word":"[^"]*"' | sed 's/"word":"//;s/"$//')
    else
        echo -e "${RED}获取失败，请检查网络连接${NC}"
    fi
    
    echo ""
    echo -e "${GREEN}💡 提示: 数据每5分钟更新一次${NC}"
}

# 主函数
main() {
    get_hot_list
}

# 运行
main
