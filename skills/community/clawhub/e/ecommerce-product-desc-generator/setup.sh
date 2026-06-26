#!/bin/bash
# 安装脚本
set -e

echo "🛒 电商产品描述批量生成器 - 安装"

# 检查 Python 版本
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python 版本: $PYTHON_VERSION"

# 创建符号链接（可选）
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 直接运行测试
echo ""
echo "运行测试..."
cd "$SCRIPT_DIR"
python3 -m pytest tests/test_generator.py -v --tb=short

echo ""
echo "✅ 安装完成！"
echo ""
echo "使用示例："
echo "  python3 $SCRIPT_DIR/cli.py '蓝牙耳机' '3C数码' --all-platforms"
echo "  python3 $SCRIPT_DIR/cli.py --csv products.csv --format markdown"
