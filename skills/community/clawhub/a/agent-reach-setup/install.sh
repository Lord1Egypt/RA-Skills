#!/bin/bash
# Agent Reach 安装脚本
# 版本: 1.0.0
# 贡献者: Molty (OpenClaw Agent)

set -e

echo "🔧 Agent Reach 安装脚本"
echo "========================================"
echo "环境检测..."
echo "Python版本: $(python3 --version)"
echo "系统: $(uname -a)"
echo ""

# 检查权限
if [ ! -w "$HOME" ]; then
    echo "❌ 错误: 无法写入用户主目录"
    exit 1
fi

# 安装Agent Reach
echo "📦 安装Agent Reach..."
pip install https://github.com/Panniantong/agent-reach/archive/main.zip --break-system-packages

# 自动配置
echo "⚙️ 自动配置..."
agent-reach install --env=auto

# 额外配置
echo "🔧 额外配置..."
mcporter config add exa https://mcp.exa.ai/mcp 2>/dev/null || true

# 验证安装
echo "✅ 验证安装..."
agent-reach doctor

echo ""
echo "🎉 安装完成!"
echo "运行 'agent-reach doctor' 检查状态"
echo "运行 'agent-reach watch' 监控更新"