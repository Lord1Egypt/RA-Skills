#!/bin/bash
# Bing Search + Jina.ai 免费搜索脚本
# 用法: ./bing_search.sh '{"query": "关键词", "max_results": 5}'

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
JSON_INPUT="$1"

if [ -z "$JSON_INPUT" ]; then
    echo "用法: ./bing_search.sh '{\"query\": \"关键词\", \"max_results\": 5}'"
    echo ""
    echo "示例:"
    echo '  ./bing_search.sh "{\"query\": \"Python 教程\"}"'
    echo '  ./bing_search.sh "{\"query\": \"AI news\", \"max_results\": 5}"'
    exit 1
fi

# 解析 JSON 参数
QUERY=$(echo "$JSON_INPUT" | jq -r '.query // empty')
MAX_RESULTS=$(echo "$JSON_INPUT" | jq -r '.max_results // 5')

if [ -z "$QUERY" ]; then
    echo "错误: 需要 query 参数"
    exit 1
fi

# 限制结果数量 (1-10)
if [ "$MAX_RESULTS" -gt 10 ] || [ "$MAX_RESULTS" -lt 1 ]; then
    MAX_RESULTS=5
fi

# URL 编码查询词
ENCODED_QUERY=$(echo "$QUERY" | jq -sRr @uri)

# 记录开始时间
START_TIME=$(date +%s.%N)

# 使用 Jina.ai 提取 Bing 搜索结果
RESPONSE=$(curl -s --max-time 30 "https://r.jina.ai/http://bing.com/search?q=${ENCODED_QUERY}&setlang=zh")

# 计算响应时间
END_TIME=$(date +%s.%N)
RESPONSE_TIME=$(echo "$END_TIME - $START_TIME" | bc)

# 检查响应
if [ -z "$RESPONSE" ] || [ "$RESPONSE" = "null" ]; then
    echo "{\"error\": \"搜索失败，请检查网络连接\"}"
    exit 1
fi

# 检查是否被拦截
if echo "$RESPONSE" | grep -q "Too Many Requests\|CAPTCHA\|blocked"; then
    echo "{\"error\": \"请求过于频繁，请稍后重试\"}"
    exit 1
fi

# 检查是否返回错误页面
if echo "$RESPONSE" | head -5 | grep -q "^Error\|^error"; then
    echo "{\"error\": \"搜索服务暂时不可用\"}"
    exit 1
fi

# 使用 Python 解析结果（更可靠）
RESULTS=$(python3 -c "
import sys
import json
import re

response = '''$RESPONSE'''

# 提取搜索结果
pattern = r'(\d+)\.\s+\[(.+?)\]\((https?://[^\)]+)\)'
matches = re.findall(pattern, response)

results = []
for i, (num, title, url) in enumerate(matches[:$MAX_RESULTS]):
    # 清理标题
    title = title.strip()
    results.append({'title': title, 'url': url})

print(json.dumps(results))
" 2>/dev/null)

# 如果 Python 解析失败，使用备用方案
if [ -z "$RESULTS" ] || [ "$RESULTS" = "[]" ]; then
    # 简单提取前几行返回
    RESULTS='[{"title": "搜索结果", "url": ""}]'
fi

# 输出最终 JSON
echo "$RESULTS" | jq -c --arg query "$QUERY" --argjson rt "$RESPONSE_TIME" '{
    query: $query,
    results: .,
    response_time: ($rt | floor * 100 / 100)
}'