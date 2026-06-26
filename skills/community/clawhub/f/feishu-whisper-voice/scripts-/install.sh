#!/bin/bash
# Feishu Whisper Voice - 快速安装脚本

set -e

echo "🎤 飞书 Whisper + TTS 语音交互技能包"
echo "====================================="
echo ""

# 检测系统
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macOS"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="Linux"
else
    OS="Unknown"
fi

echo "检测到操作系统：$OS"
echo ""

# 检查 Python 环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python，请先安装 Python 3.8+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✓ Python 版本：$PYTHON_VERSION"

# 检查 pip
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "❌ 未找到 pip，请先安装"
    exit 1
fi

pip=$(command -v pip3 || command -v pip)
echo "✓ Pip: $pip"
echo ""

# 创建虚拟环境（推荐）
VENV_DIR=".venv_whisper"
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv $VENV_DIR
fi

source $VENV_DIR/bin/activate
echo "✓ 虚拟环境已激活：$VENV_DIR"
echo ""

# 安装核心依赖
echo "🔧 安装核心依赖..."
pip install faster-whisper torch --upgrade

echo ""
echo "✅ 核心依赖安装完成！"
echo ""

# 可选：安装 Whisper.cpp (本地轻量级方案)
read -p "是否安装 whisper.cpp (本地运行，无需 GPU)? [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📦 安装 whisper.cpp..."
    
    if command -v brew &> /dev/null; then
        # macOS Homebrew
        brew install whisper-cpp
        echo "✓ Whisper.cpp (Homebrew) 已安装"
    elif command -v apt-get &> /dev/null; then
        # Ubuntu/Debian
        sudo apt-get update
        sudo apt-get install -y whisper-cpp
        echo "✓ Whisper.cpp (apt) 已安装"
    else
        # 源码编译
        git clone https://github.com/ggerganov/whisper.cpp
        cd whisper.cpp && make
        cd ..
        echo "✓ Whisper.cpp (源码编译) 已安装"
    fi
    
    echo ""
fi

# 可选：安装高级 TTS 服务
echo "🎤 高级 TTS 服务（可选）"
echo ""
read -p "是否安装 Azure Cognitive Services SDK? [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    pip install azure-cognitiveservices-speech
    echo "✓ Azure TTS SDK 已安装"
fi

read -p "是否安装 ElevenLabs CLI? [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    pip install elevenlabs
    echo "✓ ElevenLabs SDK 已安装"
fi

echo ""

# 配置环境变量提示
echo "🔑 配置环境变量（可选）"
echo ""
read -p "是否配置 OpenAI API Key? [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "export OPENAI_API_KEY=\"your_api_key\"" >> ~/.bashrc || true
    echo "export OPENAI_API_KEY=\"your_api_key\"" >> ~/.zshrc || true
    echo "✓ OpenAI API Key 配置已添加到 shell rc 文件"
fi

echo ""

# 下载 Whisper 模型（首次运行自动下载）
echo "📥 Whisper 模型说明:"
echo ""
echo "首次运行时，Whisper 会自动下载模型文件到 ~/.cache/torch/hub/"
echo ""
echo "推荐模型大小:"
echo "  - base (142MB): 通用场景，CPU 友好"
echo "  - small (466MB): 生产环境，平衡性能"
echo "  - medium (769MB): 高精度需求，需要 GPU"
echo ""

# 测试安装
echo "🧪 运行安装测试..."
python3 << 'EOF'
import sys
try:
    from faster_whisper import WhisperModel
    print("✓ Faster Whisper 库导入成功")
    
    # 尝试加载模型（仅检查，不实际下载）
    try:
        model = WhisperModel("base", device="cpu")
        print("✓ Whisper 模型可以正常加载")
    except Exception as e:
        print(f"⚠️ 模型加载警告：{e}")
        
except ImportError as e:
    print(f"❌ 导入失败：{e}")
    sys.exit(1)

print("")
print("🎉 安装测试通过！可以开始使用 Whisper 了！")
EOF

echo ""
echo "====================================="
echo "✅ 安装完成！下一步："
echo ""
echo "1. 阅读 SKILL.md 了解使用方法"
echo "2. 配置环境变量（可选）:"
echo "   - OPENAI_API_KEY (使用 OpenAI Whisper API)"
echo "   - AZURE_SUBSCRIPTION_KEY (使用 Azure TTS)"
echo ""
echo "3. 开始处理语音消息！🎤"
echo "====================================="
