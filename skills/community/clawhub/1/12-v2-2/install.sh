#!/bin/bash
# V2.2量化交易系统安装脚本

echo "================================"
echo " AI量化交易系统 V2.2 安装"
echo "================================"

# 检查Python3
echo "[1/4] 检查Python环境..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3未安装，请先安装Python3"
    exit 1
fi
echo "✓ Python3已安装: $(python3 --version)"

# 安装依赖
echo ""
echo "[2/4] 安装依赖包..."
pip3 install akshare pandas numpy pyyaml 2>/dev/null || {
    echo "⚠ 部分依赖安装失败，请手动安装："
    echo "  pip3 install akshare pandas numpy pyyaml"
}

# 测试系统
echo ""
echo "[3/4] 测试系统..."
cd "$(dirname "$0")"
python3 tests/系统测试脚本.py

# 完成
echo ""
echo "[4/4] 安装完成！"
echo ""
echo "快速开始:"
echo "  1. 查看文档: cat README.md"
echo "  2. 运行测试: python3 tests/系统测试脚本.py"
echo "  3. 运行回测: python3 tests/完整回测系统.py"
echo "  4. 一键部署: bash 一键部署脚本.sh"
echo ""
echo "祝投资顺利！"
