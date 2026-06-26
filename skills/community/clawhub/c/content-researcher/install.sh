#!/bin/bash
# content-researcher 安装脚本

set -e

echo "🔍 正在安装 content-researcher..."

if ! command -v python3 &> /dev/null; then
    echo "❌ 需要 Python 3.7+"
    exit 1
fi

# 检查 summarize 技能是否安装
if ! command -v summarize &> /dev/null; then
    echo "⚠️  需要安装 summarize 技能"
    echo "   运行: clawhub install summarize"
fi

echo "✅ content-researcher 安装完成！"
echo ""
echo "使用：content-researcher --keywords \"AI,自媒体\" --output research_report.md"
echo "文档：cat SKILL.md"
