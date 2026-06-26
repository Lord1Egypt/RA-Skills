#!/bin/bash
# 分批上传 Markdown 内容到飞书文档
# 解决 feishu_doc append 把整个内容当成一个块的问题
#
# 使用方法：
#   bash upload-to-feishu-batch.sh <doc_token> <markdown_file>
#
# 原理：
#   将 Markdown 按段落分割，每次 append 一小批内容
#   飞书会自动解析 Markdown 并创建多个块

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

echo "📄 开始分批上传到飞书..."
echo "文档 token: $DOC_TOKEN"
echo "文件: $MARKDOWN_FILE"
echo ""

# 统计总行数
TOTAL_LINES=$(wc -l < "$MARKDOWN_FILE")
echo "总行数: $TOTAL_LINES"
echo ""

# 分批大小（每次上传的行数）
BATCH_SIZE=100

# 当前行号
CURRENT_LINE=1

# 批次计数
BATCH_NUM=1

while [ $CURRENT_LINE -le $TOTAL_LINES ]; do
  END_LINE=$((CURRENT_LINE + BATCH_SIZE - 1))
  if [ $END_LINE -gt $TOTAL_LINES ]; then
    END_LINE=$TOTAL_LINES
  fi
  
  echo "📝 批次 $BATCH_NUM: 第 $CURRENT_LINE-$END_LINE 行"
  
  # 提取这批内容
  CONTENT=$(sed -n "${CURRENT_LINE},${END_LINE}p" "$MARKDOWN_FILE")
  
  # 保存到临时文件（供 OpenClaw 读取）
  echo "$CONTENT" > /tmp/batch-content-$BATCH_NUM.txt
  
  echo "  ✓ 内容已准备，等待 OpenClaw 执行 feishu_doc append"
  echo ""
  
  CURRENT_LINE=$((END_LINE + 1))
  BATCH_NUM=$((BATCH_NUM + 1))
  
  # 延迟，避免 API 限流
  sleep 0.3
done

echo "✅ 分批准备完成！"
echo ""
echo "📋 需要在 OpenClaw 中执行以下命令："
echo ""

# 生成 OpenClaw 命令
BATCH_NUM=1
CURRENT_LINE=1
while [ $CURRENT_LINE -le $TOTAL_LINES ]; do
  END_LINE=$((CURRENT_LINE + BATCH_SIZE - 1))
  if [ $END_LINE -gt $TOTAL_LINES ]; then
    END_LINE=$TOTAL_LINES
  fi
  
  echo "# 批次 $BATCH_NUM"
  echo "feishu_doc append --doc_token $DOC_TOKEN --content \"\$(cat /tmp/batch-content-$BATCH_NUM.txt)\""
  echo ""
  
  CURRENT_LINE=$((END_LINE + 1))
  BATCH_NUM=$((BATCH_NUM + 1))
done

echo "💡 提示：这个脚本只是准备工具，实际上传需要在 OpenClaw 会话中分批调用 feishu_doc。"
