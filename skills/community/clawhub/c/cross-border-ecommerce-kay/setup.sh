#!/bin/bash
# 跨境电商选品工具 - 安装脚本
set -e

echo "🛒 跨境电商选品工具安装"

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -q flask flask-cors

# 安装CLI工具（可选）
echo "✅ 安装完成！"
echo ""
echo "用法："
echo "  source venv/bin/activate"
echo "  python cli.py keyword <关键词>      # 关键词分析"
echo "  python cli.py profit --cost 10 --price 35  # 利润计算"
echo "  python cli.py listing <产品名>       # AI Listing生成"
