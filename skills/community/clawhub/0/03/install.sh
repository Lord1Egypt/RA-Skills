#!/bin/bash
# AI视觉识别技能 - 安装脚本

echo "=========================================="
echo "AI视觉识别技能 - 安装向导"
echo "=========================================="

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3"
    exit 1
fi

echo "✓ Python版本: $(python3 --version)"

# 选择模式
echo ""
echo "请选择安装模式:"
echo "1. API模式 (轻量，推荐，需要API密钥)"
echo "2. 本地模式 (完整，需下载模型约500MB)"

read -p "请选择 (1/2, 默认1): " mode_choice

# 创建虚拟环境
read -p "是否创建虚拟环境? (y/n): " create_venv

if [ "$create_venv" = "y" ]; then
    python3 -m venv venv
    source venv/bin/activate
    echo "✓ 虚拟环境已创建"
fi

# 安装依赖
if [ "$mode_choice" = "2" ]; then
    echo "安装完整依赖（本地模式）..."
    pip install Pillow torch transformers
else
    echo "安装API模式依赖..."
    pip install Pillow openai anthropic
fi

# 创建启动脚本
cat > run.sh << 'EOF'
#!/bin/bash
if [ -f venv/bin/activate ]; then
    source venv/bin/activate
fi
python vision_ai.py
EOF

chmod +x run.sh

echo ""
echo "=========================================="
echo "安装完成！"
echo "=========================================="
echo ""
echo "使用方法:"
echo "  ./run.sh"
echo ""
if [ "$mode_choice" = "1" ]; then
    echo "API模式使用提示:"
    echo "  设置OpenAI密钥: export OPENAI_API_KEY=sk-xxx"
    echo "  设置Anthropic密钥: export ANTHROPIC_API_KEY=sk-ant-xxx"
else
    echo "本地模式提示:"
    echo "  首次运行会自动下载模型，请确保网络畅通"
fi
