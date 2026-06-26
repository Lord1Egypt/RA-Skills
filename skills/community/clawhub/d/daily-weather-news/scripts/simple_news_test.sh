#!/bin/bash

# 简化的新闻解析测试
echo "=== 简化新闻解析测试 ==="

# 设置API密钥
export TAVILY_API_KEY="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"

# 获取新闻
echo "正在获取新闻..."
news_result=$(node ~/.openclaw/workspace/skills/tavily-search/scripts/search.mjs "site:news.cn 今日国际 OR site:xinhuanet.com 今日要闻 OR site:people.com.cn 国际新闻 $(date +%Y-%m-%d)" -n 6 --topic news --days 1)

# 检查API响应
if [ -z "$news_result" ]; then
    echo "❌ 新闻信息获取失败"
    exit 1
fi

echo "✅ API调用成功"

# 提取Answer部分
answer_section=$(echo "$news_result" | sed -n '/## Answer/,/## Sources/p' | sed '1d;$d')

if [ -n "$answer_section" ]; then
    echo "✅ Answer部分提取成功"
    
    # 提取关键新闻点
    news_points=$(echo "$answer_section" | sed 's/\.\s*/\n/g' | grep -v '^$' | head -6)
    
    if [ -n "$news_points" ]; then
        echo "✅ 新闻点提取成功"
        echo ""
        echo "📰 今日国际要闻（$(date +%Y-%m-%d））："
        echo ""
        
        echo "$news_points" | while IFS= read -r point; do
            if [ -n "$point" ]; then
                echo "• $point"
            fi
        done
        
        echo ""
        echo "=== 测试成功 ==="
    else
        echo "❌ 新闻点提取失败"
        exit 1
    fi
else
    echo "❌ Answer部分提取失败"
    exit 1
fi