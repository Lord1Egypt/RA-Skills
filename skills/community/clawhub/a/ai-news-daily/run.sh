#!/bin/bash
cd "$(dirname "$0")"

echo "📰 AI 新闻日报 v1.0.2"
echo "======================"
echo ""

# 检查数据库是否存在，不存在则初始化
if [ ! -f "data/news.db" ]; then
    echo "🔄 首次运行，初始化数据库..."
    mkdir -p data
fi

# 1. 抓取新闻
echo "📥 正在抓取新闻..."
python3 src/daily_fetch.py

if [ $? -ne 0 ]; then
    echo "❌ 抓取失败"
    exit 1
fi

echo ""
echo "✅ 抓取完成！"
echo ""
echo "💡 消息已保存到: data/openclaw_message.txt"
echo ""
echo "📅 每天早上 9:00 会自动推送"
echo "   手动推送请运行: python3 src/push.py"
