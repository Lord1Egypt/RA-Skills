#!/bin/bash
# AI总结复盘技能 - 安装脚本

echo "=========================================="
echo "AI总结复盘技能 - 安装向导"
echo "=========================================="

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3"
    exit 1
fi

echo "✓ Python版本: $(python3 --version)"
echo ""
echo "注意: 该技能使用Python标准库，无需额外安装依赖"

# 创建启动脚本
cat > run.sh << 'EOF'
#!/bin/bash
python3 summary_review.py
EOF

chmod +x run.sh

echo ""
echo "=========================================="
echo "安装完成！"
echo "=========================================="
echo ""
echo "使用方法:"
echo "  ./run.sh"
echo "  python3 summary_review.py"
echo ""
echo "该技能已就绪，可以直接使用"
