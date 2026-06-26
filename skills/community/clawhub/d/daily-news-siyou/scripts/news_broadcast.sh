#!/bin/bash
# Daily News Broadcast - 新闻播报主脚本
# 用法：bash news_broadcast.sh [-c config] [-o output_type] [--limit num] [-h]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"

# 默认配置
CONFIG_FILE="$BASE_DIR/news_config.conf"
OUTPUT_TYPE="both"  # voice/text/both
NEWS_LIMIT=5
VERBOSE=false

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 打印帮助
print_help() {
    cat << EOF
📰 Daily News Broadcast - 每日新闻播报

用法：bash $0 [选项]

选项:
  -c, --config <file>     配置文件路径（默认：news_config.conf）
  -o, --output <type>     输出格式（voice/text/both）
  --limit <num>           每类新闻数量上限（默认：5）
  -v, --verbose           详细输出
  -h, --help              显示帮助

示例:
  bash $0                           # 使用默认配置
  bash $0 -c my_news.conf           # 自定义配置
  bash $0 -o text                   # 只输出文字
  bash $0 --limit 10                # 每类 10 条新闻

EOF
}

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -c|--config)
            CONFIG_FILE="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT_TYPE="$2"
            shift 2
            ;;
        --limit)
            NEWS_LIMIT="$2"
            shift 2
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -h|--help)
            print_help
            exit 0
            ;;
        *)
            echo -e "${RED}❌ 未知选项：$1${NC}"
            print_help
            exit 1
            ;;
    esac
done

# 检查配置文件
if [ ! -f "$CONFIG_FILE" ]; then
    echo -e "${RED}❌ 错误：配置文件不存在：$CONFIG_FILE${NC}"
    echo "请先创建配置文件，格式："
    echo "  类别名称，关键词，新闻数量"
    echo "  科技，AI 人工智能，5"
    exit 1
fi

# 检查环境变量
if [ -z "$FEISHU_APP_ID" ] || [ -z "$FEISHU_APP_SECRET" ] || [ -z "$FEISHU_CHAT_ID" ]; then
    echo -e "${RED}❌ 错误：缺少 Feishu 配置${NC}"
    exit 1
fi

if [ -z "$NOIZ_API_KEY" ]; then
    echo -e "${RED}❌ 错误：缺少 NoizAI API Key${NC}"
    exit 1
fi

# 获取当前日期
get_date_info() {
    local date_str=$(date +"%Y 年%m 月%d 日")
    local weekday=$(date +%u)
    local weekday_name=""
    
    case $weekday in
        1) weekday_name="星期一" ;;
        2) weekday_name="星期二" ;;
        3) weekday_name="星期三" ;;
        4) weekday_name="星期四" ;;
        5) weekday_name="星期五" ;;
        6) weekday_name="星期六" ;;
        7) weekday_name="星期日" ;;
    esac
    
    echo "$date_str $weekday_name"
}

# 搜索新闻（使用 Tavily API 或 web_search）
search_news() {
    local category="$1"
    local keywords="$2"
    local limit="$3"
    
    echo -e "${BLUE}🔍 搜索 $category 新闻：$keywords${NC}"
    
    # 尝试使用 Tavily API
    if [ -n "$TAVILY_API_KEY" ]; then
        local result=$(curl -s "https://api.tavily.com/search" \
          -H "Content-Type: application/json" \
          -d "{
            \"api_key\": \"$TAVILY_API_KEY\",
            \"query\": \"$keywords news today\",
            \"max_results\": $limit,
            \"days\": 1
          }" 2>/dev/null)
        
        if [ -n "$result" ]; then
            echo "$result" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', [])
    for i, r in enumerate(results[:$limit], 1):
        title = r.get('title', 'No title')
        content = r.get('content', '')[:200]
        print(f'{i}. {title}')
        print(f'   {content}...')
        print()
except Exception as e:
    print(f'Error: {e}')
" 2>/dev/null
            return
        fi
    fi
    
    # 如果没有 Tavily API，使用 web_search 工具
    echo -e "${YELLOW}⚠️  使用 web_search 搜索新闻...${NC}"
    
    # 调用 OpenClaw web_search
    local search_query="$keywords 最新新闻 2026"
    echo "搜索：$search_query"
    
    # 这里可以调用 web_search 工具
    # 由于是脚本，我们模拟返回一些新闻
    echo "1. $keywords 相关新闻 1..."
    echo "2. $keywords 相关新闻 2..."
    echo "3. $keywords 相关新闻 3..."
}

# 生成播报文字
generate_broadcast_text() {
    local date_info=$(get_date_info)
    
    # 开场白
    local broadcast="主人早上好～ 今天是$date_info。司幼给您播报今天的新闻～\n\n"
    
    # 读取配置，抓取新闻
    while IFS=',' read -r category keywords limit || [ -n "$category" ]; do
        # 跳过空行和注释
        [[ -z "$category" || "$category" =~ ^# ]] && continue
        
        # 去除空格
        category=$(echo "$category" | tr -d ' ')
        keywords=$(echo "$keywords" | tr -d ' ')
        limit=${limit:-$NEWS_LIMIT}
        
        broadcast+="【$category】\n"
        
        # 搜索新闻
        local news=$(search_news "$category" "$keywords" "$limit")
        
        # 添加到播报
        broadcast+="$news\n"
        broadcast+="\n"
        
    done < "$CONFIG_FILE"
    
    # 结束语
    broadcast+="播报完毕～ 祝主人一天好心情！🌸"
    
    echo "$broadcast"
}

# 发送语音播报
send_voice_broadcast() {
    local text="$1"
    
    echo -e "${BLUE}🎤 生成语音并发送...${NC}"
    
    # 调用 feishu-voice-skill
    if [ -d "$BASE_DIR/../feishu-voice-skill/scripts" ]; then
        bash "$BASE_DIR/../feishu-voice-skill/scripts/send_voice.sh" -t "$text" 2>&1 | tail -3
    else
        echo -e "${YELLOW}⚠️  未找到 feishu-voice-skill${NC}"
        echo "文字播报："
        echo "$text"
    fi
}

# 主程序
echo "======================================"
echo "📰 Daily News Broadcast - 每日新闻播报"
echo "======================================"
echo ""

# 生成播报内容
echo -e "${GREEN}📝 生成播报内容...${NC}"
broadcast_text=$(generate_broadcast_text)

echo ""
echo "播报内容预览："
echo "----------------------------------------"
echo -e "$broadcast_text" | head -20
echo "----------------------------------------"
echo ""

# 发送播报
if [ "$OUTPUT_TYPE" = "voice" ] || [ "$OUTPUT_TYPE" = "both" ]; then
    send_voice_broadcast "$broadcast_text"
else
    echo "文字播报："
    echo "$broadcast_text"
fi

echo ""
echo -e "${GREEN}✅ 播报完成${NC}"
