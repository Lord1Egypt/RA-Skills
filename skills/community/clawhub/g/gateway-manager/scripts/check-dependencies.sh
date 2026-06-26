#!/bin/bash
# check-dependencies.sh - 检查系统依赖

echo "=== 检查系统依赖 ==="

ERRORS=0

# 检查操作系统
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "⚠️  警告：此技能专为 macOS 设计，当前系统：$OSTYPE"
    echo "   部分功能（LaunchAgent）可能无法正常工作"
    ERRORS=$((ERRORS + 1))
else
    echo "✅ 操作系统：macOS ($OSTYPE)"
fi

# 检查必需工具
for cmd in jq lsof plutil launchctl curl; do
    if command -v $cmd &> /dev/null; then
        echo "✅ $cmd: 已安装"
    else
        echo "❌ $cmd: 未安装"
        ERRORS=$((ERRORS + 1))
    fi
done

# 检查 Node.js
if command -v node &> /dev/null; then
    NODE_PATH=$(which node)
    echo "✅ Node.js: 已安装 ($NODE_PATH)"
else
    echo "❌ Node.js: 未安装"
    ERRORS=$((ERRORS + 1))
fi

# 检查 OpenClaw
if command -v openclaw &> /dev/null; then
    echo "✅ OpenClaw: 已安装"
else
    echo "⚠️  OpenClaw: 未找到命令（可能已安装但未在 PATH 中）"
fi

echo ""
if [ $ERRORS -eq 0 ]; then
    echo "🎉 所有依赖检查通过！"
else
    echo "⚠️  发现 $ERRORS 个问题"
    if [[ "$OSTYPE" != "darwin"* ]]; then
        echo ""
        echo "📝 提示：此技能需要 macOS 系统"
    fi
    if ! command -v jq &> /dev/null; then
        echo "📝 安装 jq: brew install jq"
    fi
fi

exit $ERRORS
