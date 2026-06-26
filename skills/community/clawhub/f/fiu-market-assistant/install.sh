#!/bin/bash
# fiu-market-assistant Quick Setup Script

set -e

echo "🚀 FIU Market Assistant 快速配置"
echo "================================"
echo ""

# Check if token provided
if [ -z "$1" ]; then
    echo "用法: $0 <FIU_MCP_TOKEN>"
    echo ""
    echo "示例: $0 eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."
    echo ""
    echo "获取 Token: https://ai.szfiu.com/auth/login"
    exit 1
fi

TOKEN="$1"
CONFIG_DIR="$HOME/.fiu-market"
CONFIG_FILE="$CONFIG_DIR/config"

# Create config directory
mkdir -p "$CONFIG_DIR"

# Save token
echo "export FIU_MCP_TOKEN=\"$TOKEN\"" > "$CONFIG_FILE"
echo "✅ Token 已保存到 $CONFIG_FILE"

# Create .mcp.json for Claude Code
MCP_FILE="$HOME/.mcp.json"

# Check if .mcp.json exists
if [ -f "$MCP_FILE" ]; then
    echo "📝 检测到已有 .mcp.json，将更新..."
    # Backup
    cp "$MCP_FILE" "$MCP_FILE.bak"
fi

# Create MCP config
cat > "$MCP_FILE" << 'MCPEOF'
{
  "mcpServers": {
    "stockHkF10": {
      "description": "港股市场F10数据",
      "transport": "streamable_http",
      "url": "https://ai.szfiu.com/stock_hk_f10/",
      "headers": {
        "Authorization": "Bearer TOKEN_PLACEHOLDER"
      }
    },
    "stockUsF10": {
      "description": "美股市场F10数据",
      "transport": "streamable_http",
      "url": "https://ai.szfiu.com/stock_us_f10/",
      "headers": {
        "Authorization": "Bearer TOKEN_PLACEHOLDER"
      }
    },
    "stockCnF10": {
      "description": "A股市场F10数据",
      "transport": "streamable_http",
      "url": "https://ai.szfiu.com/stock_cn_f10/",
      "headers": {
        "Authorization": "Bearer TOKEN_PLACEHOLDER"
      }
    },
    "stockHkSdk": {
      "description": "港股市场SDK数据",
      "transport": "streamable_http",
      "url": "https://ai.szfiu.com/stock_hk_sdk/",
      "headers": {
        "Authorization": "Bearer TOKEN_PLACEHOLDER"
      }
    },
    "stockUsSdk": {
      "description": "美股市场SDK数据",
      "transport": "streamable_http",
      "url": "https://ai.szfiu.com/stock_us_sdk/",
      "headers": {
        "Authorization": "Bearer TOKEN_PLACEHOLDER"
      }
    },
    "stockCnSdk": {
      "description": "A股市场SDK数据",
      "transport": "streamable_http",
      "url": "https://ai.szfiu.com/stock_cn_sdk/",
      "headers": {
        "Authorization": "Bearer TOKEN_PLACEHOLDER"
      }
    },
    "szfiuToolkit": {
      "description": "FIU检索证券代码服务",
      "transport": "streamable_http",
      "url": "https://ai.szfiu.com/toolkit/"
    }
  }
}
MCPEOF

# Replace placeholder with actual token
sed -i "s/TOKEN_PLACEHOLDER/$TOKEN/g" "$MCP_FILE"

echo "✅ MCP 配置已保存到 $MCP_FILE"

# Test connectivity
echo ""
echo "🧪 测试连接..."

TEST_RESPONSE=$(curl -s -X POST "https://ai.szfiu.com/toolkit/" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json, text/event-stream" \
    -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}')

if echo "$TEST_RESPONSE" | grep -q "tools"; then
    echo "✅ 连接测试成功!"
else
    echo "⚠️  连接测试失败，请检查 Token 是否有效"
fi

echo ""
echo "================================"
echo "🎉 配置完成!"
echo ""
echo "请执行以下操作:"
echo "1. 重启 Claude Code / OpenClaw"
echo "2. 使用自然语言查询，如:"
echo "   - 查询腾讯控股行情"
echo "   - 显示苹果日K线"
echo "   - 搜索腾讯"
echo ""
echo "或使用命令:"
echo "   /fiu-market-assistant quote 00700"
echo "   /fiu-market-assistant search 腾讯"