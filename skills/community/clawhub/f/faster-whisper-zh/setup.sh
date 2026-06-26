#!/usr/bin/env bash
# faster-whisper 技能安装脚本
# 创建虚拟环境并安装依赖包（支持 GPU 加速）

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"

echo "🎙️ 正在设置 faster-whisper 技能..."

# 检测操作系统
OS="$(uname -s)"
ARCH="$(uname -m)"

case "$OS" in
    Linux*)  OS_TYPE="linux" ;;
    Darwin*) OS_TYPE="macos" ;;
    *)       OS_TYPE="unknown" ;;
esac

echo "✓ 平台: $OS_TYPE ($ARCH)"

# 检查 Python 3.10+
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python 3。请安装 Python 3.10 或更高版本。"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]); then
    echo "❌ 需要 Python 3.10+ (当前版本: $PYTHON_VERSION)"
    exit 1
fi

echo "✓ Python $PYTHON_VERSION"

# 检查 ffmpeg（必需）
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ 未找到 ffmpeg（音频处理必需）"
    echo ""
    echo "安装 ffmpeg:"
    if [ "$OS_TYPE" = "macos" ]; then
        echo "   brew install ffmpeg"
    else
        echo "   Ubuntu/Debian: sudo apt install ffmpeg"
        echo "   Fedora: sudo dnf install ffmpeg"
        echo "   Arch: sudo pacman -S ffmpeg"
        echo "   CentOS/RHEL: sudo yum install ffmpeg"
    fi
    echo ""
    exit 1
fi

echo "✓ 找到 ffmpeg"

# 检测 GPU/加速可用性
HAS_CUDA=false
HAS_APPLE_SILICON=false
GPU_NAME=""
NVIDIA_SMI=""

if [ "$OS_TYPE" = "linux" ]; then
    # 检查 NVIDIA GPU (Linux/WSL)
    # 首先在 PATH 中查找 nvidia-smi
    if command -v nvidia-smi &> /dev/null; then
        NVIDIA_SMI="nvidia-smi"
    else
        # WSL2: nvidia-smi 在 /usr/lib/wsl/lib/ 中（默认不在 PATH）
        # 检查是否在 WSL2 中并在相应目录查找
        if grep -qi microsoft /proc/version 2>/dev/null; then
            # 在 WSL2 中 - 在 WSL 库目录中搜索 nvidia-smi
            for wsl_smi in /usr/lib/wsl/lib/nvidia-smi /usr/lib/wsl/drivers/*/nvidia-smi; do
                if [ -f "$wsl_smi" ]; then
                    NVIDIA_SMI="$wsl_smi"
                    echo "✓ 检测到 WSL2"
                    break
                fi
            done
        fi
    fi
    
    # 如果找到 nvidia-smi，获取 GPU 信息
    if [ -n "$NVIDIA_SMI" ]; then
        GPU_NAME=$($NVIDIA_SMI --query-gpu=name --format=csv,noheader 2>/dev/null | head -1)
        if [ -n "$GPU_NAME" ]; then
            HAS_CUDA=true
        fi
    fi
elif [ "$OS_TYPE" = "macos" ]; then
    # 检查 Apple Silicon
    if [ "$ARCH" = "arm64" ]; then
        HAS_APPLE_SILICON=true
        GPU_NAME="Apple Silicon"
        echo "✓ 检测到 Apple Silicon"
    fi
fi

if [ "$HAS_CUDA" = true ]; then
    echo "✓ 检测到 GPU: $GPU_NAME"
fi

# 创建虚拟环境
if [ -d "$VENV_DIR" ]; then
    echo "✓ 虚拟环境已存在"
else
    echo "正在创建虚拟环境..."
    if command -v uv &> /dev/null; then
        uv venv "$VENV_DIR" --python python3
    else
        python3 -m venv "$VENV_DIR"
    fi
    echo "✓ 虚拟环境创建完成"
fi

# 安装依赖包
echo "正在安装 faster-whisper..."
if command -v uv &> /dev/null; then
    uv pip install --python "$VENV_DIR/bin/python" -r "$SCRIPT_DIR/requirements.txt"
else
    "$VENV_DIR/bin/pip" install --upgrade pip
    "$VENV_DIR/bin/pip" install -r "$SCRIPT_DIR/requirements.txt"
fi

# 根据平台安装 PyTorch
if [ "$HAS_CUDA" = true ]; then
    echo ""
    echo "🚀 正在安装支持 CUDA 的 PyTorch..."
    echo "   这将使您的 GPU 转录速度提升约 10-20 倍。"
    echo ""
    if command -v uv &> /dev/null; then
        uv pip install --python "$VENV_DIR/bin/python" torch --index-url https://download.pytorch.org/whl/cu121
    else
        "$VENV_DIR/bin/pip" install torch --index-url https://download.pytorch.org/whl/cu121
    fi
    echo "✓ PyTorch with CUDA 安装完成"
elif [ "$OS_TYPE" = "macos" ]; then
    echo ""
    echo "🍎 正在安装 macOS 版 PyTorch..."
    if command -v uv &> /dev/null; then
        uv pip install --python "$VENV_DIR/bin/python" torch
    else
        "$VENV_DIR/bin/pip" install torch
    fi
    echo "✓ PyTorch 安装完成"
    if [ "$HAS_APPLE_SILICON" = true ]; then
        echo "ℹ️  注意：faster-whisper 在 macOS 上使用 CPU（Apple Silicon 仍然很快！）"
    fi
else
    echo ""
    echo "ℹ️  未检测到 NVIDIA GPU。使用 CPU 模式。"
    echo "   如果您有 GPU，请确保已安装 CUDA 驱动程序。"
fi

# 使脚本可执行
chmod +x "$SCRIPT_DIR/scripts/"*

echo ""
echo "✅ 安装完成！"
echo ""
if [ "$HAS_CUDA" = true ]; then
    echo "🚀 GPU 加速已启用 — 预计速度约为实时 20 倍"
elif [ "$HAS_APPLE_SILICON" = true ]; then
    echo "🍎 Apple Silicon — 预计 CPU 速度约为实时 3-5 倍"
else
    echo "💻 CPU 模式 — 转录速度较慢但功能正常"
fi
echo ""
echo "使用方法："
echo "  $SCRIPT_DIR/.venv/bin/python3 $SCRIPT_DIR/scripts/transcribe.py 音频文件.mp3"
echo ""
echo "首次运行将下载模型（distil-large-v3 约 756MB）。"
echo ""
echo "环境变量建议设置："
echo "  export HF_HOME=/config/huggingface"
echo "  export HF_ENDPOINT=https://hf-mirror.com  # 国内镜像加速"
echo ""
echo "中文转录示例："
echo "  .venv/bin/python3 scripts/transcribe.py 会议录音.mp3 --language zh --device auto"
echo ""
echo "如需帮助，请查看 SKILL.md 文档。"