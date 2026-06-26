#!/bin/bash
# FCPX Assistant WebUI Launcher
# Made by Steve & Steven (≧∇≦)

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo_banner() {
    cat << EOF
${CYAN}
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║          🎬 FCPX Assistant WebUI Launcher                ║
║                                                          ║
║              Made by Steve & Steven (≧∇≦)                ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
${NC}
EOF
}

echo_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
echo_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
echo_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
echo_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
WEBUI_DIR="$SCRIPT_DIR/webui"
VENV_DIR="$SCRIPT_DIR/.venv"

echo_banner

echo_info "FCPX Assistant 目录：$SCRIPT_DIR"
echo_info "WebUI 目录：$WEBUI_DIR"

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null; then
    echo_error "Python3 未安装，请先安装 Python 3.8+"
    echo "macOS: brew install python@3.11"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo_info "Python 版本：$PYTHON_VERSION"

# 检查并创建虚拟环境
if [[ ! -d "$VENV_DIR" ]]; then
    echo_info "创建 Python 虚拟环境..."
    python3 -m venv "$VENV_DIR"
    echo_success "虚拟环境创建完成"
else
    echo_info "虚拟环境已存在"
fi

# 激活虚拟环境
echo_info "激活虚拟环境..."
source "$VENV_DIR/bin/activate"

# 安装/更新依赖
echo_info "检查并安装依赖..."

# 创建 requirements.txt
REQUIREMENTS_FILE="$WEBUI_DIR/requirements.txt"
cat > "$REQUIREMENTS_FILE" << EOF
gradio>=4.0.0
numpy>=1.20.0
pillow>=9.0.0
EOF

# 安装依赖
pip3 install -q -r "$REQUIREMENTS_FILE" --upgrade

echo_success "依赖安装完成"

# 检查依赖
echo_info "检查 Gradio 安装..."
if ! python3 -c "import gradio" 2>/dev/null; then
    echo_error "Gradio 安装失败"
    exit 1
fi

GRADIO_VERSION=$(python3 -c "import gradio; print(gradio.__version__)")
echo_info "Gradio 版本：$GRADIO_VERSION"

# 创建输出目录
OUTPUT_DIR="$HOME/Movies/fcpx-assistant-outputs"
mkdir -p "$OUTPUT_DIR"
echo_info "输出目录：$OUTPUT_DIR"

# 启动 WebUI
echo ""
echo_success "准备启动 WebUI..."
echo ""
echo_info "访问地址："
echo -e "  ${CYAN}本地：http://localhost:7861${NC}"
echo -e "  ${CYAN}局域网：http://$(hostname).local:7861${NC}"
echo ""
echo_info "按 Ctrl+C 停止服务"
echo ""
echo_separator() {
    echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

echo_separator

# 启动应用
cd "$WEBUI_DIR"
python3 app.py
