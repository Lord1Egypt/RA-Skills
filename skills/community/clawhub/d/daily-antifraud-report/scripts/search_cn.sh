#!/bin/bash
# 国内新闻搜索脚本 - 使用百度搜索

QUERY="$1"
NUM="${2:-10}"

# 百度搜索API (可替换为其他国内搜索API)
BAIDU_API="https://www.baidu.com/s?wd=${QUERY}&rn=${NUM}"

echo "正在搜索: ${QUERY}"
curl -s "${BAIDU_API}" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" | grep -oP '<h3 class="news-title.*?">.*?<a href="(.*?)".*?>(.*?)</a>.*?</h3>' | head -${NUM} || echo "搜索完成"
