#!/bin/bash
# OpenClaw 必备技能一键安装脚本

set -e

echo "=================================================="
echo "   OpenClaw 必备技能一键安装"
echo "=================================================="
echo ""

# 必备技能列表
ESSENTIAL_SKILLS=(
    "skill-vetter"
    "tavily-search"
    "self-improving-agent"
    "memory-os"
    "find-skills"
    "skill-creator"
    "summarize"
    "notion"
)

# 检查 skillhub 是否可用
if ! command -v skillhub &> /dev/null; then
    echo "❌ skillhub CLI 未安装"
    echo "请先安装: npm install -g skills-store-cli"
    exit 1
fi

echo "📦 将安装以下必备技能："
echo ""
echo "五星推荐 ⭐️⭐️⭐️⭐️⭐️："
for skill in skill-vetter tavily-search self-improving-agent memory-os find-skills skill-creator; do
    echo "  ⭐️ $skill"
done
echo ""
echo "四星推荐 ⭐️⭐️⭐️⭐️："
for skill in summarize notion; do
    echo "  $skill"
done
echo ""
echo "共计 ${#ESSENTIAL_SKILLS[@]} 个技能"
echo ""

read -p "确认安装？(y/n): " confirm
if [[ "$confirm" != "y" ]]; then
    echo "已取消"
    exit 0
fi

echo ""
echo "🚀 开始安装..."
echo ""

SUCCESS=0
FAILED=0
FAILED_LIST=()

for skill in "${ESSENTIAL_SKILLS[@]}"; do
    echo "📦 安装 $skill..."
    if skillhub install "$skill" --force 2>/dev/null; then
        echo "  ✅ $skill 安装成功"
        ((SUCCESS++))
    else
        echo "  ❌ $skill 安装失败"
        ((FAILED++))
        FAILED_LIST+=("$skill")
    fi
done

echo ""
echo "=================================================="
echo "   安装完成"
echo "=================================================="
echo "✅ 成功: $SUCCESS"
echo "❌ 失败: $FAILED"

if [ ${#FAILED_LIST[@]} -gt 0 ]; then
    echo ""
    echo "失败的技能："
    for skill in "${FAILED_LIST[@]}"; do
        echo "  - $skill"
    done
    echo ""
    echo "可以稍后手动安装："
    echo "  skillhub install <技能名> --force"
fi

echo ""
echo "📋 需要配置的技能："
echo "  - tavily-search: 需要 Tavily API Key (https://tavily.com)"
echo "  - notion: 需要 Notion Integration Token (https://www.notion.so/my-integrations)"
echo ""
echo "其他技能无需配置，安装即可使用。"
