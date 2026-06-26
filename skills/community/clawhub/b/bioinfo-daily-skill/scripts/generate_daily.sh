#!/bin/bash
#
# Bioinfo Daily Wrapper Script
# 生成日报并创建飞书文档
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# 加载 .env 文件（如果存在）
if [ -f "$SKILL_DIR/.env" ]; then
    source "$SKILL_DIR/.env"
fi

# 获取日期
YESTERDAY=$(date -d "yesterday" +%Y/%m/%d)
DATE_STR=$(date -d "yesterday" +%Y%m%d)

echo "🔬 开始生成生物信息学日报..."
echo "📅 日期: $YESTERDAY"

# 检查环境变量
if [ -z "$NCBI_EMAIL" ]; then
    echo "❌ 错误: 未设置 NCBI_EMAIL 环境变量"
    echo "   请在 ~/.openclaw/openclaw.json 中配置或设置环境变量"
    exit 1
fi

if [ -z "$NCBI_API_KEY" ]; then
    echo "❌ 错误: 未设置 NCBI_API_KEY 环境变量"
    echo "   请在 ~/.openclaw/openclaw.json 中配置或设置环境变量"
    exit 1
fi

# 生成日报
python3 ~/.openclaw/workspace/skills/bioinfo-daily/scripts/pubmed_search.py > /tmp/bioinfo_daily_${DATE_STR}.log 2>&1

if [ $? -ne 0 ]; then
    echo "❌ 日报生成失败"
    cat /tmp/bioinfo_daily_${DATE_STR}.log
    exit 1
fi

echo "✅ 日报生成完成"

# 读取生成的日报内容
REPORT_FILE="/tmp/bioinfo_daily_${DATE_STR}.txt"
MD_FILE="/tmp/bioinfo_daily_${DATE_STR}.md"

if [ ! -f "$REPORT_FILE" ]; then
    echo "❌ 日报文件不存在: $REPORT_FILE"
    exit 1
fi

# 提取摘要（前30行）
SUMMARY=$(head -30 "$REPORT_FILE" | grep "📝" | head -1)

# 创建飞书文档标题
DOC_TITLE="生物信息学日报 - ${YESTERDAY}"

echo "📄 创建飞书文档: $DOC_TITLE"

# 读取日报内容
CONTENT=$(cat "$REPORT_FILE")

# 转换为 Markdown 格式（简单处理）
MD_CONTENT="# 📰 生物信息学日报\n\n📅 ${YESTERDAY}\n\n${CONTENT}"\n
# 保存 Markdown 文件
echo "$MD_CONTENT" > "$MD_FILE"

echo "📥 文件已保存:"
echo "   文本: $REPORT_FILE"
echo "   Markdown: $MD_FILE"
echo ""
echo "💡 下一步:"
echo "   请使用 feishu_doc 工具创建文档并上传内容"
echo "   文档标题: $DOC_TITLE"
echo ""
echo "✅ 日报生成流程完成!"
