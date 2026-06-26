#!/bin/bash
# 基金分析技能安装脚本

SKILL_DIR="$HOME/.codebuddy/skills/fund-analyzer"

echo "📦 正在安装基金分析技能..."

# 检查目录是否存在
if [ ! -d "$SKILL_DIR" ]; then
    echo "❌ 错误: 技能目录不存在"
    exit 1
fi

# 设置脚本执行权限
echo "🔧 设置脚本执行权限..."
chmod +x "$SKILL_DIR/scripts/"*.py

# 检查Python是否可用
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3，请先安装Python"
    exit 1
fi

echo "✅ 安装完成!"
echo ""
echo "使用方法:"
echo "  查询净值:   python3 $SKILL_DIR/scripts/query_fund_nav.py <基金代码>"
echo "  历史走势:   python3 $SKILL_DIR/scripts/query_fund_history.py <基金代码>"
echo "  基金筛选:   python3 $SKILL_DIR/scripts/fund_screener.py --rank 近1年 --top 10"
echo "  持仓分析:   python3 $SKILL_DIR/scripts/query_fund_holding.py <基金代码>"
echo "  基金对比:   python3 $SKILL_DIR/scripts/compare_funds.py <基金代码1> <基金代码2>"
echo ""
echo "详细说明请查看: $SKILL_DIR/references/guide.md"
