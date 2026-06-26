#!/usr/bin/env bash
# Agent Quantizer - 一键部署脚本
# 用法: bash deploy.sh [目标目录]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="${1:-$HOME/.openclaw/skills/agent-quantizer}"

echo "🚀 部署 Agent Quantizer"
echo "   源: $SCRIPT_DIR"
echo "   目标: $TARGET"

# 复制文件
mkdir -p "$TARGET"/{scripts,cache}
cp "$SCRIPT_DIR/SKILL.md" "$TARGET/"
cp "$SCRIPT_DIR/config.json" "$TARGET/"
cp "$SCRIPT_DIR/scripts/quantize.sh" "$TARGET/scripts/"
cp "$SCRIPT_DIR/scripts/cache.sh" "$TARGET/scripts/"

# 设置权限
chmod +x "$TARGET/scripts/"*.sh

# 检查依赖
echo ""
echo "检查依赖..."
for cmd in jq python3 openclaw; do
    if command -v "$cmd" &>/dev/null; then
        echo "  ✅ $cmd"
    else
        echo "  ❌ $cmd (需要安装)"
    fi
done

echo ""
echo "✅ 部署完成！"
echo ""
echo "使用方法:"
echo "  quantize stats     # 查看 token 消耗"
echo "  quantize scan      # 扫描高消耗 session"
echo "  quantize compress <key>  # 压缩上下文"
echo "  quantize cache stats     # 查看缓存"
echo ""
echo "快捷方式 (可选):"
echo "  alias quantize='bash $TARGET/scripts/quantize.sh'"
