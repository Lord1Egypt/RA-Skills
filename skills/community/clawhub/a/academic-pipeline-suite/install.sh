#!/bin/bash

# Academic Suite v3.5.0 — 一键安装脚本
# 将所有依赖技能打包在本技能包内，无需联网下载
# 用法：./install.sh 或 bash install.sh

set -e

SUITE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$SUITE_DIR/skills"
TARGET_DIR="$HOME/.openclaw/workspace/skills"

echo "🔮 Academic Suite v3.5.0 — 一键安装脚本"
echo "========================================"
echo ""

# 检查 skill 目录是否存在
if [ ! -d "$SKILLS_DIR" ]; then
    echo "❌ 错误：skills 目录不存在"
    echo "请确保您下载的是完整包"
    exit 1
fi

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
    "academic-pipeline"
)

echo "📦 开始安装 9 个技能..."
echo ""

# 从打包目录复制到 skills 目录
for skill in "${DEPENDENCIES[@]}"; do
    if [ -d "$SKILLS_DIR/$skill" ]; then
        echo "   安装 $skill..."
        rm -rf "$TARGET_DIR/$skill"
        cp -r "$SKILLS_DIR/$skill" "$TARGET_DIR/"
        echo "   ✅ $skill 安装成功"
    else
        echo "   ⚠️  $skill 未找到（跳过）"
    fi
done

echo ""
echo "========================================"
echo "🎉 Academic Suite v3.5.0 安装完成！"
echo "========================================"
echo ""

# 验证安装
echo "🔍 验证安装..."
echo ""

INSTALLED_COUNT=0
for skill in "${DEPENDENCIES[@]}"; do
    if [ -d "$TARGET_DIR/$skill" ]; then
        echo "   ✅ $skill"
        ((INSTALLED_COUNT++))
    else
        echo "   ❌ $skill (未找到)"
    fi
done

echo ""
echo "已安装：$INSTALLED_COUNT / ${#DEPENDENCIES[@]} 个技能"
echo ""

if [ $INSTALLED_COUNT -eq ${#DEPENDENCIES[@]} ]; then
    echo "✅ 所有技能安装成功！"
    echo ""
    echo "🚀 快速开始："
    echo "   我要用 Academic Pipeline 写一篇论文"  
    echo ""
    echo "📚 完整文档："
    echo "   https://feishu.cn/docx/GRb7dGij9olddExTBsCcpoaCnWg"
    echo ""
else
    echo "⚠️  部分技能安装失败"
fi

echo "🔮 严谨是分析的基础，逻辑是推理的武器。"