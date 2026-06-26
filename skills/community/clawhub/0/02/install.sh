#!/bin/bash
# AI联网搜索技能 - 安装脚本

echo "=========================================="
echo "AI联网搜索技能 - 安装向导"
echo "=========================================="

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3"
    exit 1
fi

echo "✓ Python版本: $(python3 --version)"

# 创建虚拟环境
read -p "是否创建虚拟环境? (y/n): " create_venv

if [ "$create_venv" = "y" ]; then
    python3 -m venv venv
    source venv/bin/activate
    echo "✓ 虚拟环境已创建"
fi

# 安装依赖
echo "安装依赖包..."
pip install -r requirements.txt

# 创建启动脚本
cat > run.sh << 'EOF'
#!/bin/bash
source venv/bin/activate
python web_search.py
EOF

chmod +x run.sh

echo ""
echo "=========================================="
echo "安装完成！"
echo "=========================================="
echo "使用方法:"
echo "  ./run.sh"
echo "  python web_search.py"
