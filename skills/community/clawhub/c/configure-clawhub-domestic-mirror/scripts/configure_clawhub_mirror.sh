#!/bin/bash
# ClawHub 国内镜像配置脚本
# 自动配置环境变量并验证配置有效性

set -e

MIRROR_URL="https://cn.clawhub-mirror.com"
BASHRC="$HOME/.bashrc"

echo "🦞 ClawHub 国内镜像配置脚本"
echo "================================"

# 检查是否已配置
if grep -q "CLAWHUB_REGISTRY=$MIRROR_URL" "$BASHRC" 2>/dev/null; then
    echo "✅ ClawHub 镜像已配置"
else
    echo "🔧 配置 ClawHub 国内镜像..."
    cat >> "$BASHRC" << EOF

# ClawHub 国内镜像配置
export CLAWHUB_REGISTRY=$MIRROR_URL
export CLAWHUB_SITE=$MIRROR_URL
EOF
    echo "✅ 环境变量已添加到 $BASHRC"
fi

# 使配置在当前会话生效
echo "🔄 使配置生效..."
source "$BASHRC"

# 验证配置
echo "🔍 验证配置..."
if command -v clawhub &> /dev/null; then
    clawhub search "git" && echo "✅ 配置验证成功 - 国内镜像可用"
else
    echo "⚠️  warning: clawhub 命令未找到，请确认 CLI 已安装"
fi

echo ""
echo "📌 注意：新打开的终端会自动加载配置，无需额外操作"
