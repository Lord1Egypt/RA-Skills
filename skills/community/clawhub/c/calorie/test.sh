#!/bin/bash
# Food Calorie Calculator - 测试脚本

cd "$(dirname "$0")"

echo "=================================="
echo "🍽️  Food Calorie Calculator 测试"
echo "=================================="
echo ""

# 检查图片参数
if [ -z "$1" ]; then
    echo "用法：./test.sh <图片路径>"
    echo ""
    echo "示例："
    echo "  ./test.sh data/food.jpg"
    echo "  ./test.sh ~/Downloads/lunch.jpg"
    echo ""
    echo "请先准备一张食物照片！"
    exit 1
fi

# 检查文件是否存在
if [ ! -f "$1" ]; then
    echo "❌ 错误：图片文件不存在：$1"
    exit 1
fi

echo "📸 测试图片：$1"
echo ""
echo "正在识别食物并计算卡路里..."
echo "──────────────────────────────"
echo ""

# 运行计算器
python3 src/calorie_calculator.py "$1"

echo ""
echo "──────────────────────────────"
echo "✅ 测试完成！"
