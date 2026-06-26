#!/bin/bash
# Food Calorie Calculator - 运行脚本

cd "$(dirname "$0")"

# 检查图片参数
if [ -z "$1" ]; then
    echo "用法：./run.sh <图片路径>"
    echo "示例：./run.sh data/food.jpg"
    exit 1
fi

# 运行计算器
python3 src/calorie_calculator.py "$1"
