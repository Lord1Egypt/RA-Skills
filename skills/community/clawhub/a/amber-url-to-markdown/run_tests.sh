#!/bin/bash
# Amber Url to Markdown - 测试运行脚本

set -e

echo "========================================"
echo "Amber Url to Markdown - 运行测试"
echo "========================================"
echo ""

# 检查 pytest 是否安装
if ! command -v pytest &> /dev/null; then
    echo "⚠️  pytest 未安装，正在安装..."
    pip install pytest -q
fi

# 运行测试
echo "🚀 开始运行测试..."
echo ""

cd "$(dirname "$0")"
pytest tests/ -v --tb=short

echo ""
echo "========================================"
echo "✅ 测试完成！"
echo "========================================"
