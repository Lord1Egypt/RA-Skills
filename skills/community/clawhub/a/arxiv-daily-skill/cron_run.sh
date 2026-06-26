#!/bin/bash
# arXiv 每日论文推送 - Cron 执行脚本（带飞书推送）
# 每天工作日 9:00 自动执行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_FILE="/tmp/arxiv_daily_$(date +%Y%m%d).md"
AFFILIATIONS_DB="$SCRIPT_DIR/affiliations_db.json"

echo "🚀 开始执行 arXiv 每日论文推送..."
echo "📅 日期：$(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 步骤 1: 执行论文获取脚本
echo "📝 步骤 1: 获取论文列表..."
cd "$SCRIPT_DIR"
python3 fetch_arxiv.py > "$OUTPUT_FILE" 2>&1

if [ $? -ne 0 ]; then
    echo "❌ 论文获取失败"
    cat "$OUTPUT_FILE"
    exit 1
fi

echo "✅ 论文获取成功"
echo ""

# 步骤 2: 提取目录部分用于推送预览
echo "📦 步骤 2: 生成推送内容..."
PREVIEW_FILE="/tmp/arxiv_preview_$(date +%Y%m%d).txt"
head -30 "$OUTPUT_FILE" > "$PREVIEW_FILE"

# 步骤 3: 飞书推送
echo "📤 步骤 3: 发送飞书推送..."

# 读取飞书 webhook URL（从配置文件或环境变量）
FEISHU_WEBHOOK="${FEISHU_WEBHOOK_URL:-}"

if [ -z "$FEISHU_WEBHOOK" ]; then
    # 尝试从配置文件读取
    if [ -f "$SCRIPT_DIR/feishu_config.json" ]; then
        FEISHU_WEBHOOK=$(cat "$SCRIPT_DIR/feishu_config.json" | python3 -c "import sys,json; print(json.load(sys.stdin).get('webhook_url', ''))")
    fi
fi

if [ -n "$FEISHU_WEBHOOK" ]; then
    # 生成推送消息（Markdown 格式）
    MESSAGE=$(cat <<EOF
{
    "msg_type": "interactive",
    "card": {
        "header": {
            "title": {
                "tag": "plain_text",
                "content": "📚 今日 ArXiv 论文推送 ($(date '+%Y-%m-%d'))"
            },
            "template": "blue"
        },
        "elements": [
            {
                "tag": "markdown",
                "content": "$(cat "$PREVIEW_FILE" | sed 's/"/\\"/g' | head -20)"
            },
            {
                "tag": "action",
                "actions": [
                    {
                        "tag": "button",
                        "text": {
                            "tag": "plain_text",
                            "content": "📄 查看完整报告"
                        },
                        "url": "file://$OUTPUT_FILE",
                        "type": "default"
                    }
                ]
            }
        ]
    }
}
EOF
)
    
    # 发送飞书消息
    RESPONSE=$(curl -s -X POST "$FEISHU_WEBHOOK" \
        -H "Content-Type: application/json" \
        -d "$MESSAGE")
    
    echo "$RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print('✅ 推送成功' if d.get('StatusCode')==0 else '❌ 推送失败：'+str(d))"
else
    echo "⚠️  未配置飞书 Webhook，跳过推送"
    echo "💡 配置方法：设置环境变量 FEISHU_WEBHOOK_URL 或创建 feishu_config.json"
fi

echo ""
echo "📄 完整报告：$OUTPUT_FILE"
echo "✅ 执行完成"
