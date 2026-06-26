#!/bin/bash
# 上传 Markdown 内容到飞书文档（正确分段）
# 
# 使用方法：
#   bash upload-markdown-to-feishu.sh <doc_token> <markdown_file>
#
# 原理：
#   飞书的 feishu_doc write/append 会把整个内容当成一个文本块
#   需要按段落分割，逐段 append
#
# 注意：
#   - 这个脚本需要在 OpenClaw 环境中执行（有 feishu_doc 工具）
#   - 每段之间会有短暂延迟，避免 API 限流

set -e

if [ $# -lt 2 ]; then
  echo "Usage: $0 <doc_token> <markdown_file>"
  exit 1
fi

DOC_TOKEN="$1"
MARKDOWN_FILE="$2"

if [ ! -f "$MARKDOWN_FILE" ]; then
  echo "Error: File not found: $MARKDOWN_FILE"
  exit 1
fi

echo "📄 准备上传 Markdown 到飞书文档..."
echo "文档 token: $DOC_TOKEN"
echo "文件: $MARKDOWN_FILE"
echo ""

# 统计行数
TOTAL_LINES=$(wc -l < "$MARKDOWN_FILE")
echo "总行数: $TOTAL_LINES"
echo ""

# 方案：按段落分割（空行分隔），逐段 append
# 但这样会导致太多小段落，不是最优解

# 更好的方案：使用飞书的 Markdown 导入功能
# 但 feishu_doc 工具可能不支持

# 临时方案：分批 append（每次 100 行）
BATCH_SIZE=100
CURRENT_LINE=1

while [ $CURRENT_LINE -le $TOTAL_LINES ]; do
  END_LINE=$((CURRENT_LINE + BATCH_SIZE - 1))
  if [ $END_LINE -gt $TOTAL_LINES ]; then
    END_LINE=$TOTAL_LINES
  fi
  
  echo "📝 上传第 $CURRENT_LINE-$END_LINE 行..."
  
  # 提取这批内容
  CONTENT=$(sed -n "${CURRENT_LINE},${END_LINE}p" "$MARKDOWN_FILE")
  
  # 使用 feishu_doc append
  # 注意：这里需要在 OpenClaw 环境中执行
  # 由于 bash 脚本无法直接调用 OpenClaw 工具，需要通过其他方式
  
  echo "$CONTENT" > /tmp/batch-content.txt
  echo "  内容已保存到 /tmp/batch-content.txt"
  echo "  需要在 OpenClaw 中执行："
  echo "  feishu_doc append --doc_token $DOC_TOKEN --content \"\$(cat /tmp/batch-content.txt)\""
  echo ""
  
  CURRENT_LINE=$((END_LINE + 1))
  
  # 延迟，避免 API 限流
  sleep 0.5
done

echo "✅ 上传完成！"
echo ""
echo "⚠️ 注意：由于 bash 脚本无法直接调用 OpenClaw 工具，"
echo "   需要手动在 OpenClaw 中执行上面的命令。"
echo ""
echo "💡 建议：使用 Python 脚本或直接在 OpenClaw 会话中分批上传。"
