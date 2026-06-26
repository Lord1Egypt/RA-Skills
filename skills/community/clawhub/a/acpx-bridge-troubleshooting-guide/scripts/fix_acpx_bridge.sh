#!/bin/bash
# fix_acpx_bridge.sh - 修复 acpx 桥接超时问题
# 创建 gateway.token 文件并修复 acpx 配置

set -e

echo "🦞 开始修复 acpx 桥接问题..."

# 1. 创建 ~/.openclaw 目录（如果不存在）
mkdir -p ~/.openclaw

# 2. 从 openclaw.json 提取 token 并创建 gateway.token 文件
if [ -f ~/.openclaw/openclaw.json ]; then
    TOKEN=$(grep -o '"token"[[:space:]]*:[[:space:]]*"[^"]*"' ~/.openclaw/openclaw.json | head -1 | sed 's/.*"\([^"]*\)"$/\1/')
    if [ -n "$TOKEN" ]; then
        echo "$TOKEN" > ~/.openclaw/gateway.token
        echo "✅ gateway.token 已创建"
    else
        echo "⚠️ 未在 openclaw.json 中找到 token，请手动创建 ~/.openclaw/gateway.token"
    fi
else
    echo "⚠️ ~/.openclaw/openclaw.json 不存在，请手动创建 ~/.openclaw/gateway.token"
fi

# 3. 修复 acpx 配置文件
mkdir -p ~/.acpx
cat > ~/.acpx/config.json << 'EOF'
{
  "defaultAgent": "openclaw",
  "timeout": 900,
  "agents": {
    "openclaw": {
      "command": "openclaw",
      "args": ["acp", "client"]
    }
  }
}
EOF
echo "✅ acpx 配置已修复 (~/.acpx/config.json)"

# 4. 更新 acpx 到最新版本
echo "📦 更新 acpx 到最新版本..."
npm install -g acpx@latest 2>/dev/null || echo "⚠️ npm 更新失败，请手动执行：npm install -g acpx@latest"

# 5. 验证安装
echo ""
echo "🔍 验证安装:"
acpx --version 2>/dev/null || echo "⚠️ acpx 未安装或版本检查失败"

echo ""
echo "✅ 修复完成！请执行以下命令重启 Gateway:"
echo "   openclaw gateway restart"
