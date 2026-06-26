#!/bin/bash
# 这是 Cocktail-Boy 技能的主入口点
# 用于从 OpenClaw 系统调用

skill_dir="$HOME/.openclaw/workspace/skills/cocktail-boy"
db_file="$skill_dir/data/rohan_cocktails.csv"

if [ ! -f "$db_file" ]; then
    echo "❌ 鸡尾酒数据库未找到，请检查技能安装"
    exit 1
fi

# 显示帮助信息
echo "🍹 **Cocktail-Boy - 您的私人调酒师** 🍹"
echo ""
echo "💡 可以直接说："
echo "   • \"我想喝 martini\" → 查询特定鸡尾酒"
echo "   • \"有什么威士忌的酒？\" → 搜索含某原料的鸡尾酒"
echo "   • \"推荐一款鸡尾酒\" → 随机推荐"
echo ""
echo "🔧 技能路径：$skill_dir"
echo "📊 数据库：$db_file (1635+ 配方)"
