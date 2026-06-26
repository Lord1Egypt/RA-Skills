#!/bin/bash
# AI总结复盘技能 v2.0 - 安装脚本

echo "=========================================="
echo "AI总结复盘技能 v2.0 - 增强版"
echo "=========================================="

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3"
    exit 1
fi

echo "✓ Python版本: $(python3 --version)"

# 安装依赖
echo ""
echo "安装依赖包..."

# OpenAI兼容SDK（支持智谱、DeepSeek、通义等）
pip install openai -q

# Anthropic SDK（可选）
read -p "是否安装Anthropic Claude支持？(y/n): " install_claude

if [ "$install_claude" = "y" ]; then
    pip install anthropic -q
    echo "✓ Anthropic SDK已安装"
fi

# 创建启动脚本
cat > run.sh << 'EOF'
#!/bin/bash
if [ -f venv/bin/activate ]; then
    source venv/bin/activate
fi
python3 summary_review_llm.py
EOF

chmod +x run.sh

echo ""
echo "=========================================="
echo "安装完成！"
echo "=========================================="
echo ""
echo "使用方法:"
echo "  ./run.sh"
echo "  python3 summary_review_llm.py"
echo ""
echo "配置API密钥:"
echo "  方式1: python3 ../llm_config.py"
echo "  方式2: export ZHIPU_API_KEY='your-key'"
echo ""
echo "支持的提供商:"
echo "  - zhipu (智谱AI)"
echo "  - openai (GPT)"
echo "  - anthropic (Claude)"
echo "  - deepseek"
echo "  - qwen (通义千问)"
echo "  - moonshot (Kimi)"
echo ""
echo "提示: 未配置API时将使用基础总结功能"
