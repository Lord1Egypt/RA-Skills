#!/usr/bin/env bash
# setup.sh - 加载微信公众号环境变量
# Usage: source ./setup.sh

SKILL_DIR="/root/.openclaw/workspace/skills/ai-news-publisher"
TOOLS_MD="$HOME/.openclaw/workspace/TOOLS.md"

# 检查 TOOLS.md
if [ ! -f "$TOOLS_MD" ]; then
    echo "❌ 找不到 TOOLS.md: $TOOLS_MD"
    echo ""
    echo "请添加微信公众号凭证："
    echo ""
    echo "  ## 🔐 WeChat Official Account"
    echo "  export WECHAT_APP_ID=your_app_id"
    echo "  export WECHAT_APP_SECRET=your_app_secret"
    exit 1
fi

# 提取凭证
WECHAT_APP_ID=$(grep "export WECHAT_APP_ID=" "$TOOLS_MD" | head -1 | sed 's/.*export WECHAT_APP_ID=//' | tr -d ' ')
WECHAT_APP_SECRET=$(grep "export WECHAT_APP_SECRET=" "$TOOLS_MD" | head -1 | sed 's/.*export WECHAT_APP_SECRET=//' | tr -d ' ')

if [ -z "$WECHAT_APP_ID" ] || [ -z "$WECHAT_APP_SECRET" ]; then
    echo "❌ 无法从 TOOLS.md 读取凭证！"
    echo ""
    echo "请确保格式正确："
    echo "  export WECHAT_APP_ID=your_app_id"
    echo "  export WECHAT_APP_SECRET=your_app_secret"
    exit 1
fi

export WECHAT_APP_ID
export WECHAT_APP_SECRET

echo "✅ 微信公众号环境变量已加载！"
echo ""
echo "  WECHAT_APP_ID=${WECHAT_APP_ID:0:10}..."
echo "  WECHAT_APP_SECRET=******"
