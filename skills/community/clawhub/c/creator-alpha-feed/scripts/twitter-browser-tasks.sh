#!/bin/bash
###############################################################################
# X(Twitter) 公共页面收集脚本（隐私安全版）
# 用法: ./twitter-browser-tasks.sh [日期]
###############################################################################

DATE="${1:-$(date +%Y-%m-%d)}"
OUTPUT_DIR="${HOME}/.openclaw/workspace/ai-content-pipeline/collected/${DATE}"
mkdir -p "$OUTPUT_DIR"

OUTPUT_FILE="$OUTPUT_DIR/x-browser-tasks.sh"

cat > "$OUTPUT_FILE" << 'EOF'
#!/bin/bash
# X 公共页面收集任务（在 OpenClaw 中执行）

echo "========== X 公共页面内容收集 =========="
echo "安全要求:"
echo "1. 仅访问公开账号页/公开搜索页"
echo "2. 禁止访问首页流(home)、私信、通知页"
echo "3. 禁止采集任何私密会话信息"
echo ""

ACCOUNTS=(
  "sama:OpenAI CEO"
  "gdb:OpenAI cofounder"
  "karpathy:AI researcher"
  "DrJimFan:NVIDIA researcher"
  "ylecun:Meta AI"
)

echo "📋 收集任务（公开页面）:"

INDEX=1
for account_info in "${ACCOUNTS[@]}"; do
  IFS=':' read -r account desc <<< "$account_info"
  echo "$INDEX. 访问 @$account ($desc)..."
  echo "   执行: browser open 'https://x.com/$account'"
  echo "   执行: wait 3000"
  echo "   执行: browser snapshot"
  echo ""
  ((INDEX++))
done

echo "$INDEX. 搜索AI公开话题..."
echo "   执行: browser open 'https://x.com/search?q=AI%20OR%20GPT%20OR%20Claude&src=typed_query&f=live'"
echo "   执行: wait 5000"
echo "   执行: browser snapshot"
echo ""

echo "========== 收集完成 =========="
echo "请仅提取公开帖文信息。"
EOF

chmod +x "$OUTPUT_FILE"

echo "✅ 任务已生成: $OUTPUT_FILE"
echo ""
echo "手动示例（公开页面）:"
echo "browser open 'https://x.com/sama'"
echo "wait 3000"
echo "browser snapshot"
