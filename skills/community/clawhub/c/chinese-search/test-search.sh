#!/bin/bash
# 中文搜索引擎测试脚本

QUERY="${1:-OpenClaw 技能}"
echo "测试搜索：$QUERY"
echo "===================="

# 1. 必应中国 (✅ 工作正常)
echo -e "\n🔍 必应中国:"
curl -s "https://cn.bing.com/search?q=${QUERY}&count=3" | grep -o '<title>[^<]*</title>' | head -1

# 2. 搜狗微信 (✅ 工作正常)
echo -e "\n🔍 搜狗微信:"
curl -s "https://weixin.sogou.com/weixin?type=2&query=${QUERY}&ie=utf8" | grep -o '<title>[^<]*</title>' | head -1

# 3. 百度搜索 (⚠️ 需要特殊处理)
echo -e "\n🔍 百度搜索:"
curl -s -A "Mozilla/5.0" "https://www.baidu.com/s?wd=${QUERY}&rn=3" | grep -o '<title>[^<]*</title>' | head -1

# 4. 知乎搜索 (需要调整格式)
echo -e "\n🔍 知乎搜索:"
curl -s -A "Mozilla/5.0" "https://www.zhihu.com/search?type=content&q=${QUERY// /+}&size=3" | grep -o '<title>[^<]*</title>' | head -1

# 5. 360 搜索
echo -e "\n🔍 360 搜索:"
curl -s -A "Mozilla/5.0" "https://www.so.com/s?q=${QUERY}&pn=3" | grep -o '<title>[^<]*</title>' | head -1

# 6. 头条搜索
echo -e "\n🔍 头条搜索:"
curl -s -A "Mozilla/5.0" "https://so.toutiao.com/search?keyword=${QUERY}&pd=synthesis&pn=3" | grep -o '<title>[^<]*</title>' | head -1

echo -e "\n===================="
echo "测试完成"
