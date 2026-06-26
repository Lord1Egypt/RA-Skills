#!/bin/bash

# Cocktail-Boy 示例演示

echo "=========================================="
echo "🍹 Cocktail-Boy - 功能演示"
echo "=========================================="
echo ""

skill_dir="$HOME/.openclaw/workspace/skills/cocktail-boy"
script="$skill_dir/scripts/query.sh"

echo "1️⃣  查询特定鸡尾酒 (Mojito)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
"$script" search Mojito 2>/dev/null
echo ""

echo "2️⃣  查询另一个经典鸡尾酒 (Old Fashioned)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
"$script" search "Old Fashioned" 2>/dev/null
echo ""

echo "3️⃣  随机推荐一款鸡尾酒"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
"$script" recommend 2>/dev/null
echo ""

echo "✅ 演示完成！"
echo ""
echo "💡 现在可以尝试问我："
echo "   • '我想喝 mojito'"
echo "   • '有什么威士忌的酒？'"
echo "   • '推荐一款鸡尾酒'"
