#!/bin/bash

# Design Analysis Skill - 安装和测试脚本
# 用法: ./install.sh [test]

set -e

echo "╔════════════════════════════════════════╗"
echo "║  Design Analysis Skill - 安装脚本       ║"
echo "╚════════════════════════════════════════╝"

# 检查Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 错误: 未找到 Node.js，请先安装 Node.js"
    exit 1
fi

echo "✅ Node.js 版本: $(node --version)"

# 技能目录
SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
echo "📁 技能目录: $SKILL_DIR"

# 检查必要文件
echo "🔍 检查文件..."
for file in index.js run.js SKILL.md package.json; do
    if [ -f "$SKILL_DIR/$file" ]; then
        echo "   ✓ $file"
    else
        echo "   ✗ $file 缺失"
        exit 1
    fi
done

# 运行依赖检查（如果有）
echo ""
echo "📦 检查依赖..."
echo "   (本技能无外部依赖)"

# 创建符号链接到OpenClaw技能目录（可选）
OPENCLAW_SKILLS_DIR="$HOME/.openclaw/workspace/skills"
if [ -d "$OPENCLAW_SKILLS_DIR" ]; then
    echo ""
    echo "🔗 OpenClaw技能目录检测到: $OPENCLAW_SKILLS_DIR"
    if [ "$(basename "$SKILL_DIR")" = "design-analysis" ]; then
        echo "   ✓ 技能已经位于OpenClaw技能目录，无需额外操作"
    else
        echo "   提示: 确保 $SKILL_DIR 在 OpenClaw技能搜索路径中"
    fi
fi

# 运行测试（如果请求）
if [ "$1" = "test" ] || [ "$1" = "--test" ]; then
    echo ""
    echo "🧪 运行测试..."
    if [ -f "test.js" ]; then
        node test.js
    else
        echo "⚠️  未找到 test.js，跳过测试"
    fi
fi

echo ""
echo "╔════════════════════════════════════════╗"
echo "║  ✅ 技能安装/检查完成                   ║"
echo "╚════════════════════════════════════════╝"
echo ""
echo "使用方法:"
echo "  1. 命令行测试:"
echo "     node run.js ~/Desktop/01.DesignAnalysis ~/Desktop/output.html"
echo ""
echo "  2. 在OpenClaw中使用:"
echo "     请分析 ~/Desktop/01.DesignAnalysis 文件夹中的设计素材"
echo ""
echo "  3. 运行测试套件:"
echo "     ./install.sh test"
echo ""
echo "文档:"
echo "   - SKILL.md - 技能详细文档"
echo "   - OPENCLAW.md - OpenClaw集成指南"
echo "   - README.md - 项目说明"
echo ""