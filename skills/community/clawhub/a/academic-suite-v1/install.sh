#!/bin/bash

# Academic Suite v3.5.0 — 一键安装脚本
# 用法：./install.sh 或 bash install.sh

set -e

echo "🔮 Academic Suite v3.5.0 — 一键安装脚本"
echo "========================================"
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
    echo ""
    read -p "是否现在登录？[Y/n] " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        clawhub login
    else
        echo "❌ 安装中止"
        exit 1
    fi
fi

echo "✅ 已登录为：$(clawhub whoami)"
echo ""

# 开始安装
echo "📦 开始安装 Academic Suite v3.5.0..."
echo ""

# 定义依赖技能列表
DEPENDENCIES=(
    "ima-skills"
    "academic-search"
    "deep-research"
    "academic-paper"
    "academic-paper-reviewer"
    "humanizer"
    "humanizer-zh"
    "integrity_verification_agent"
)

# 安装依赖技能
echo "📦 步骤 1/2: 安装 8 个依赖技能..."
echo ""

for skill in "${DEPENDENCIES[@]}"; do
    echo "   安装 $skill..."
    if clawhub install "$skill" --force; then
        echo "   ✅ $skill 安装成功"
    else
        echo "   ⚠️  $skill 安装失败（可能已安装）"
    fi
    echo ""
done

# 安装主技能
echo "📦 步骤 2/2: 安装 academic-pipeline 主技能..."
echo ""

if clawhub install eric-promax/academic-pipeline --force; then
    echo "   ✅ academic-pipeline 安装成功"
else
    echo "   ⚠️  academic-pipeline 安装失败（可能已安装）"
fi

echo ""
echo "========================================"
echo "🎉 Academic Suite v3.5.0 安装完成！"
echo "========================================"
echo ""

# 验证安装
echo "🔍 验证安装..."
echo ""

INSTALLED_COUNT=0
for skill in "${DEPENDENCIES[@]}" "academic-pipeline"; do
    if [ -d "$HOME/.openclaw/workspace/skills/$skill" ]; then
        echo "   ✅ $skill"
        ((INSTALLED_COUNT++))
    else
        echo "   ❌ $skill (未找到)"
    fi
done

echo ""
echo "已安装：$INSTALLED_COUNT / 9 个技能"
echo ""

if [ $INSTALLED_COUNT -eq 9 ]; then
    echo "✅ 所有技能安装成功！"
    echo ""
    echo "🚀 快速开始："
    echo "   我要用 Academic Pipeline 写一篇关于\"您的主题\"的论文"
    echo ""
    echo "📚 完整文档："
    echo "   https://feishu.cn/docx/GRb7dGij9olddExTBsCcpoaCnWg"
    echo ""
else
    echo "⚠️  部分技能安装失败，请手动安装缺失的技能"
    echo ""
    echo "手动安装命令："
    echo "   clawhub install <技能名>"
    echo ""
fi

echo "🔮 严谨是分析的基础，逻辑是推理的武器。"
