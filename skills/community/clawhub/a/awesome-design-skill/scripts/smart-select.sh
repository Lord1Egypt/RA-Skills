#!/bin/bash
# 智能选择设计风格
# 根据用户需求关键词匹配最合适的设计风格
# 如果没有匹配则随机选择

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DESIGN_MD_DIR="$SCRIPT_DIR/../design-md"
STYLES_JSON="$SCRIPT_DIR/styles.json"

# 如果没有参数，随机选择
if [ -z "$1" ]; then
    # 调用 random-style.sh
    "$SCRIPT_DIR/random-style.sh"
    exit 0
fi

# 用户需求文本
QUERY="$*"

# 转换为小写便于匹配
QUERY_LOWER=$(echo "$QUERY" | tr '[:upper:]' '[:lower:]')

# 定义关键词到风格的映射
# 格式: "关键词:风格名"
KEYWORD_MAP=(
    # 暗色/深色主题
    "dark:linear.app"
    "深色:linear.app"
    "暗黑:linear.app"
    "暗色:linear.app"
    "黑色:vercel"
    "纯黑:framer"

    # 亮色/浅色主题
    "light:apple"
    "浅色:apple"
    "亮色:apple"
    "白色:ollama"
    "米白:cursor"
    "温暖:cursor"

    # 产品类型
    "项目管理:linear.app"
    "issue:linear.app"
    "任务:linear.app"
    "看板:linear.app"

    "支付:stripe"
    "金融:stripe"
    "fintech:stripe"
    "api:stripe"

    "旅行:airbnb"
    "民宿:airbnb"
    "预订:airbnb"
    "booking:airbnb"

    "音乐:spotify"
    "播放器:spotify"
    "media:spotify"
    "音频:elevenlabs"
    "语音:elevenlabs"

    "笔记:notion"
    "文档:notion"
    "知识:notion"
    "workspace:notion"

    "设计:figma"
    "协作:figma"
    "creative:framer"
    "创意:framer"

    "开发者:vercel"
    "developer:vercel"
    "代码:cursor"
    "编程:cursor"
    "编辑器:cursor"
    "ide:cursor"
    "terminal:warp"
    "终端:warp"
    "命令行:warp"

    "ai:claude"
    "人工智能:claude"
    "llm:mistral.ai"
    "大模型:minimax"
    "chatbot:claude"
    "对话:claude"
    "助手:claude"

    "landing:linear.app"
    "首页:linear.app"
    "产品页:apple"
    "展示:apple"

    "dashboard:linear.app"
    "仪表盘:linear.app"
    "后台:linear.app"

    "企业:stripe"
    "enterprise:stripe"
    "b2b:stripe"

    "开源:supabase"
    "open source:supabase"

    "效率:raycast"
    "productivity:raycast"
    "mac:raycast"

    "加密:coinbase"
    "crypto:coinbase"
    "区块链:coinbase"

    "电商:airbnb"
    "购物:airbnb"
    "商品:airbnb"

    "数据分析:posthog"
    "analytics:posthog"
    "数据:clickhouse"

    "邮件:resend"
    "email:resend"

    "日历:cal"
    "日程:cal"
    "预约:cal"

    "自动化:zapier"
    "workflow:zapier"
    "集成:composio"

    "高端:apple"
    "豪华:bmw"
    "品牌:apple"

    "简洁:notion"
    "minimal:notion"
    "极简:vercel"

    "专业:linear.app"
    "professional:linear.app"

    "友好:notion"
    "friendly:notion"
    "温暖:cursor"

    "现代:vercel"
    "modern:vercel"
    "科技:nvidia"
    "硬件:nvidia"
    "gpu:nvidia"

    "出行:uber"
    "地图:uber"
    "transportation:uber"

    "社交:pinterest"
    "图片:pinterest"
    "瀑布流:pinterest"

    "监控:sentry"
    "调试:sentry"
    "error:sentry"

    "数据库:mongodb"
    "database:mongodb"
    "nosql:mongodb"
    "olap:clickhouse"

    "cms:sanity"
    "内容:sanity"
    "content:sanity"

    "表格:airtable"
    "spreadsheet:airtable"

    "移动:expo"
    "mobile:expo"
    "react native:expo"

    "航天:spacex"
    "太空:spacex"
    "rocket:spacex"

    "游戏:nvidia"
    "gaming:nvidia"
    "性能:nvidia"

    "视频:runwayml"
    "video:runwayml"

    "无代码:webflow"
    "no-code:webflow"
    "网站构建:webflow"
)

# 搜索匹配
BEST_MATCH=""
MATCH_SCORE=0

for mapping in "${KEYWORD_MAP[@]}"; do
    KEYWORD="${mapping%%:*}"
    STYLE="${mapping##*:}"

    # 检查关键词是否在查询中
    if [[ "$QUERY_LOWER" == *"$KEYWORD"* ]]; then
        # 简单计分：更长的关键词匹配得分更高
        KEYWORD_LEN=${#KEYWORD}
        if [ $KEYWORD_LEN -gt $MATCH_SCORE ]; then
            BEST_MATCH="$STYLE"
            MATCH_SCORE=$KEYWORD_LEN
        fi
    fi
done

# 如果找到匹配
if [ -n "$BEST_MATCH" ]; then
    # 验证风格是否存在
    if [ -f "$DESIGN_MD_DIR/$BEST_MATCH/DESIGN.md" ]; then
        echo "$BEST_MATCH"
        exit 0
    fi
fi

# 没有匹配，随机选择
"$SCRIPT_DIR/random-style.sh"
