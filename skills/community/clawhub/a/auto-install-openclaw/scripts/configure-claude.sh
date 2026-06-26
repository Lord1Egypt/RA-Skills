#!/bin/bash
# Claude API 中转站配置脚本
# 用法：./configure-claude.sh

set -e

echo "🔑 Claude API 中转站配置"
echo "========================"

# 配置信息
API_URL="https://ai.jiexi6.cn"
CONFIG_DIR=~/.openclaw/config

# 创建配置目录
mkdir -p "$CONFIG_DIR"

# 获取 API Key
echo ""
echo "请输入您的 AI 中转站 API Key："
read -s API_KEY
echo ""

if [ -z "$API_KEY" ]; then
    echo "❌ API Key 不能为空"
    exit 1
fi

# 备份旧配置
if [ -f "$CONFIG_DIR/models.json" ]; then
    cp "$CONFIG_DIR/models.json" "$CONFIG_DIR/models.json.bak.$(date +%Y%m%d%H%M%S)"
fi

# 创建模型配置
echo "⚙️  创建模型配置..."
cat > "$CONFIG_DIR/models.json" << EOF
{
  "models": {
    "claude": {
      "provider": "openai-compatible",
      "baseUrl": "${API_URL}/v1",
      "apiKey": "${API_KEY}",
      "models": [
        "claude-sonnet-4-5-20250929",
        "claude-opus-4-5-20250929",
        "claude-3-5-sonnet-20241022"
      ]
    },
    "default": "claude-sonnet-4-5-20250929"
  }
}
EOF

echo "✅ 模型配置已保存到：$CONFIG_DIR/models.json"

# 测试连接
echo ""
echo "🧪 测试 API 连接..."
RESPONSE=$(curl -s -X POST "${API_URL}/v1/models" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json")

if echo "$RESPONSE" | grep -q "error"; then
    echo "⚠️  API 连接测试失败，请检查 API Key 和网络连接"
    echo "响应：$RESPONSE"
else
    echo "✅ API 连接测试成功"
fi

# 刷新 OpenClaw 模型配置
echo ""
echo "🔄 刷新 OpenClaw 模型配置..."
if command -v openclaw &> /dev/null; then
    openclaw models refresh 2>/dev/null || echo "⚠️  刷新失败，请手动重启网关"
fi

echo ""
echo "✅ Claude API 配置完成！"
echo ""
echo "配置信息："
echo "  API URL: ${API_URL}"
echo "  默认模型：claude-sonnet-4-5-20250929"
echo ""
echo "下一步："
echo "1. 运行 'openclaw gateway restart' 重启网关"
echo "2. 运行 'openclaw models list' 查看可用模型"
