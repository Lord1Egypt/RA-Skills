#!/bin/bash

# Academic Suite v3.5.0 — 发布脚本
# 用法：./publish.sh 或 bash publish.sh

set -e

echo "🔮 Academic Suite v3.5.0 — 发布脚本"
echo "===================================="
echo ""

# 检查 clawhub 是否已安装
if ! command -v clawhub &> /dev/null; then
    echo "❌ 错误：clawhub 未安装"
    echo "请先安装 clawhub: npm install -g clawhub"
    exit 1
fi

echo "✅ clawhub 已安装：$(clawhub --version)"
echo ""

# 检查是否已登录
echo "📝 检查 ClawHub 登录状态..."
if ! clawhub whoami &> /dev/null; then
    echo "⚠️  未登录 ClawHub"
    echo "请先运行：clawhub login"
    exit 1
fi

echo "✅ 已登录为：$(clawhub whoami)"
echo ""

# 获取当前目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "📂 当前目录：$SCRIPT_DIR"
echo ""

# 验证必要文件
echo "🔍 验证必要文件..."
REQUIRED_FILES=("SKILL.md" "README.md" "clawhub.json" "install.sh")

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✅ $file"
    else
        echo "   ❌ $file (缺失)"
        exit 1
    fi
done

echo ""
echo "✅ 所有必要文件存在"
echo ""

# 发布
echo "📦 准备发布到 ClawHub..."
echo ""
read -p "确认发布 academic-suite v3.5.0 到 ClawHub？[Y/n] " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ 发布取消"
    exit 0
fi

echo ""
echo "🚀 执行发布..."
echo ""

# 使用 clawhub publish 命令
if clawhub publish .; then
    echo ""
    echo "===================================="
    echo "🎉 发布成功！"
    echo "===================================="
    echo ""
    echo "📦 ClawHub 页面："
    echo "   https://clawhub.ai/eric-promax/academic-suite"
    echo ""
    echo "📦 安装命令："
    echo "   clawhub install eric-promax/academic-suite"
    echo ""
else
    echo ""
    echo "❌ 发布失败"
    echo ""
    echo "请检查："
    echo "1. 是否已登录 ClawHub"
    echo "2. 是否有发布权限"
    echo "3. 版本号是否已存在"
    echo ""
    exit 1
fi

echo "🔮 严谨是分析的基础，逻辑是推理的武器。"
