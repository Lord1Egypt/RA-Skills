#!/bin/bash

# 直接测试新闻解析逻辑
echo "=== 测试新闻解析逻辑 ==="

# 设置API密钥
export TAVILY_API_KEY="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"

# 获取新闻
news_result=$(node ~/.openclaw/workspace/skills/tavily-search/scripts/search.mjs "site:news.cn 今日国际 OR site:xinhuanet.com 今日要闻 OR site:people.com.cn 国际新闻 $(date +%Y-%m-%d)" -n 6 --topic news --days 1)

echo "API返回结果长度: ${#news_result}"
echo ""

# 检查API响应
if [ -z "$news_result" ]; then
    echo "❌ 新闻信息获取失败"
    exit 1
fi

# 提取新闻内容
echo "📰 今日国际要闻（$(date +%Y-%m-%d））："

# 提取Answer部分并提取关键信息
answer_section=$(echo "$news_result" | sed -n '/## Answer/,/## Sources/p' | sed '1d;$d')

echo "Answer部分长度: ${#answer_section}"
echo ""

if [ -n "$answer_section" ]; then
    echo "✅ Answer部分提取成功"
    echo "Answer内容:"
    echo "$answer_section"
    echo ""
    
    # 提取关键新闻点（按句子分割）
    news_points=$(echo "$answer_section" | sed 's/\.\s*/\n/g' | grep -v '^$' | head -6)
    
    echo "提取的新闻点:"
    echo "$news_points" | head -10
    echo ""
    
    if [ -n "$news_points" ]; then
        echo "✅ 新闻点提取成功"
        processed_news="📰 今日国际要闻（$(date +%Y-%m-%d)）："
        
        echo "$news_points" | while IFS= read -r point; do
            if [ -n "$point" ]; then
                echo "处理新闻点: $point"
                processed_news="${processed_news}\\n\\n• $point"
            fi
        done
        
        echo "最终处理结果:"
        echo "$processed_news"
    else
        echo "❌ 新闻点提取失败"
        exit 1
    fi
else
    echo "❌ Answer部分提取失败"
    exit 1
fi

echo ""
echo "=== 测试完成 ==="