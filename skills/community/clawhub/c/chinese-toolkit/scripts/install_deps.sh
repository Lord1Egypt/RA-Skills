#!/bin/bash
# OpenClaw中文工具包依赖安装脚本

set -e

echo "🚀 开始安装OpenClaw中文工具包依赖..."

# 检查Python版本
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "📦 Python版本: $PYTHON_VERSION"

# 创建虚拟环境（可选）
if [ ! -d "venv" ]; then
    echo "🔧 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
if [ -f "venv/bin/activate" ]; then
    echo "🔧 激活虚拟环境..."
    source venv/bin/activate
fi

# 安装Python依赖
echo "📦 安装Python依赖..."
pip install --upgrade pip
pip install -r ../requirements.txt

# 安装系统依赖
echo "🔧 安装系统依赖..."

# 检测操作系统
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux (Ubuntu/Debian)
    echo "🐧 检测到Linux系统"
    sudo apt-get update
    sudo apt-get install -y tesseract-ocr tesseract-ocr-chi-sim ffmpeg
    
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "🍎 检测到macOS系统"
    if ! command -v brew &> /dev/null; then
        echo "❌ Homebrew未安装，请先安装Homebrew"
        exit 1
    fi
    brew install tesseract tesseract-lang ffmpeg
    
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Windows
    echo "🪟 检测到Windows系统"
    echo "⚠️  请手动安装以下软件:"
    echo "  1. Tesseract OCR: https://github.com/UB-Mannheim/tesseract/wiki"
    echo "  2. FFmpeg: https://ffmpeg.org/download.html"
    
else
    echo "⚠️  未知操作系统，请手动安装依赖"
fi

# 设置环境变量
echo "🔧 设置环境变量..."
export TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata

# 创建配置文件示例
if [ ! -f "../config.json" ]; then
    echo "📝 创建配置文件示例..."
    cp ../config.example.json ../config.json
    echo "✅ 请编辑 config.json 文件配置API密钥"
fi

# 测试安装
echo "🧪 测试安装..."
python3 -c "import jieba; print('✅ jieba 安装成功')"
python3 -c "from pypinyin import lazy_pinyin; print('✅ pypinyin 安装成功')"
python3 -c "import opencc; print('✅ opencc 安装成功')"

echo ""
echo "🎉 安装完成！"
echo ""
echo "📋 下一步:"
echo "  1. 编辑 config.json 配置API密钥"
echo "  2. 运行测试: python -m pytest tests/"
echo "  3. 查看示例: python examples/basic_usage.py"
echo ""
echo "💡 使用提示:"
echo "  - 设置百度翻译API: export BAIDU_TRANSLATE_APP_ID='your_id'"
echo "  - 设置百度翻译密钥: export BAIDU_TRANSLATE_APP_KEY='your_key'"
echo ""
echo "🆘 帮助:"
echo "  - 查看文档: cat ../SKILL.md"
echo "  - 运行帮助: python chinese_tools.py --help"