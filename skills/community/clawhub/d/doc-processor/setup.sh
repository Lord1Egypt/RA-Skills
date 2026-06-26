#!/bin/bash
# 文档处理 Skill 安装脚本 - v2.7.11
# 
# 功能：安装 Python 依赖（标准 pip 操作）
# 依赖列表：python-docx, openpyxl, pandas, python-dotenv
# 安全说明：从官方 PyPI 或可信镜像源安装包，无恶意代码
#
# v2.7.11 变更：AI 功能已移除，无需安装 requests 等网络相关依赖
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_NAME="$(basename "$SCRIPT_DIR")"
VENV_DIR="$HOME/.openclaw/workspace/.venvs/$SKILL_NAME"
PYTHON_CMD="python3"

# ========== 清理旧位置的虚拟环境 ==========
OLD_VENV="$SCRIPT_DIR/.venv"
if [ -d "$OLD_VENV" ]; then
    echo "⚠️  发现旧位置虚拟环境：$OLD_VENV"
    echo "   将使用统一位置：$VENV_DIR"
    rm -rf "$OLD_VENV"
    echo "✅ 已清理旧虚拟环境"
fi

# ========== 确保统一虚拟环境目录存在 ==========
mkdir -p "$(dirname "$VENV_DIR")"

echo "📦 文档处理 Skill 安装程序"
echo "================================"

# ========== 1. 检查 Python ==========
echo ""
echo "📌 检查 Python..."
if ! command -v $PYTHON_CMD &> /dev/null; then
    echo "❌ 未找到 Python 3"
    echo "   Linux: sudo apt install python3 python3-venv"
    echo "   macOS: brew install python3"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
echo "✅ Python $PYTHON_VERSION"

# ========== 2. 检查系统依赖 ==========
echo ""
echo "📌 检查系统依赖..."

# PDF 工具
PDF_OK=true
if ! command -v pdftotext &> /dev/null; then
    echo "⚠️  pdftotext 未安装 (PDF 功能将不可用)"
    PDF_OK=false
fi

if ! command -v pdfinfo &> /dev/null; then
    echo "⚠️  pdfinfo 未安装 (PDF 功能将不可用)"
    PDF_OK=false
fi

if [ "$PDF_OK" = true ]; then
    echo "✅ poppler-utils (PDF 支持)"
else
    echo ""
    echo "   安装命令:"
    echo "   Linux (Debian/Ubuntu):  sudo apt install poppler-utils"
    echo "   Linux (RHEL/CentOS):    sudo yum install poppler-utils"
    echo "   macOS:                  brew install poppler"
    echo ""
    read -p "是否继续安装？(y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# ========== 3. 创建虚拟环境 ==========
echo ""
echo "📌 创建 Python 虚拟环境..."
if [ -d "$VENV_DIR" ]; then
    echo "⚠️  虚拟环境已存在，将重新创建"
    rm -rf "$VENV_DIR"
fi

$PYTHON_CMD -m venv "$VENV_DIR"
echo "✅ 虚拟环境：$VENV_DIR"
echo "   (统一存放在 ~/.openclaw/workspace/.venvs/)"

# ========== 4. 激活虚拟环境 ==========
echo ""
echo "📌 激活虚拟环境并安装依赖..."
source "$VENV_DIR/bin/activate"

# ========== pip 镜像源配置 ==========
# 默认使用官方 PyPI
PIP_INDEX="${PIP_INDEX_URL:-https://pypi.org/simple}"

# 支持通过命令行参数指定镜像源
if [ -n "$1" ]; then
    PIP_INDEX="$1"
fi

echo "📦 使用 pip 镜像源：$PIP_INDEX"
echo "   如需使用其他镜像源，可设置环境变量或传入参数:"
echo "   方式 1: PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple ./setup.sh"
echo "   方式 2: ./setup.sh https://pypi.tuna.tsinghua.edu.cn/simple"
echo ""

# 升级 pip
echo "📦 升级 pip 工具..."
pip install --upgrade pip setuptools wheel -q --index-url "$PIP_INDEX"

# 安装 Python 依赖（标准 pip 操作）
# v2.7.11: 仅安装文档处理相关依赖，已移除 AI 相关依赖
if [ -f "$SCRIPT_DIR/requirements.txt" ]; then
    echo "📦 安装 Python 依赖（从 $PIP_INDEX）..."
    echo "   依赖列表：python-docx, openpyxl, pandas, python-dotenv"
    echo "   说明：标准文档处理库，无网络请求功能"
    pip install -r "$SCRIPT_DIR/requirements.txt" --index-url "$PIP_INDEX"
    echo "✅ Python 依赖安装完成"
else
    echo "❌ 未找到 requirements.txt"
    exit 1
fi

# ========== 5. 设置执行权限 ==========
echo ""
echo "📌 设置执行权限..."
chmod +x "$SCRIPT_DIR/doc_processor.py"
chmod +x "$SCRIPT_DIR/scripts/"*.sh 2>/dev/null || true
chmod +x "$SCRIPT_DIR/activate.sh" 2>/dev/null || true
chmod +x "$SCRIPT_DIR/check_deps.py" 2>/dev/null || true

# ========== 6. 验证安装 ==========
echo ""
echo "📌 验证安装..."
python3 -c "
import sys
sys.path.insert(0, '$SCRIPT_DIR')
try:
    from doc_processor import DocumentProcessor
    p = DocumentProcessor()
    caps = p.get_capabilities()
    print('能力检查:')
    for k, v in caps['capabilities'].items():
        status = '✅' if v else '❌'
        print(f'  {status} {k}')
except Exception as e:
    print(f'⚠️  验证失败：{e}')
"

# ========== 7. 完成 ==========
echo ""
echo "================================"
echo "✅ 安装完成!"
echo ""
echo "使用方法:"
echo "  1. 激活环境：source $SCRIPT_DIR/activate.sh"
echo "  2. 运行工具：python3 doc_processor.py --help"
echo "  3. 使用脚本：./scripts/doc-read.sh <file>"
echo ""
echo "如需卸载，删除目录即可：rm -rf $SCRIPT_DIR"
