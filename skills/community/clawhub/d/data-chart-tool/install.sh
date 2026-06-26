#!/bin/bash
# data-visualizer 安装脚本

set -e

echo "📊 正在安装 data-visualizer..."

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未找到 python3，请先安装 Python 3.7+"
    exit 1
fi

echo "✅ Python 检查通过"

# 安装依赖
echo "📦 正在安装依赖..."
pip install matplotlib pandas openpyxl

echo ""
echo "🎉 data-visualizer 安装完成！"
echo ""
echo "使用方法："
echo "  python source/data_visualizer.py --help"
echo ""
echo "快速开始："
echo "  # 从 CSV 生成折线图"
echo "  python source/data_visualizer.py -i data.csv -t line --x-col date --y-col value"
echo ""
echo "  # 生成柱状图"
echo "  python source/data_visualizer.py -i data.csv -t bar --x-col category --y-col value"
echo ""
echo "  # 配合 tushare-finance 使用"
echo "  tushare stock_daily --ts_code 000001.SZ -o stock.csv"
echo "  python source/data_visualizer.py -i stock.csv -t line --x-col trade_date --y-col close"
echo ""
