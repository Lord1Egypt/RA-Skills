#!/bin/bash
# ============================================================
# 豆包 TTS - 火山引擎语音合成 OpenClaw Skill 安装脚本
#
# 功能：
#   1. 配置火山引擎凭证（交互式或命令行参数）
#   2. 安装 Python 依赖
#
# 使用方式：
#   bash install.sh
#   bash install.sh --app-id <id> --access-token <token>
# ============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_DIR="$HOME/.config/doubao-tts"
ENV_FILE="$CONFIG_DIR/.env"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
success() { echo -e "${GREEN}✅ $1${NC}"; }
warn() { echo -e "${YELLOW}⚠️  $1${NC}"; }
error() { echo -e "${RED}❌ $1${NC}"; exit 1; }

# ============================================================
# 解析命令行参数
# ============================================================

APP_ID=""
ACCESS_TOKEN=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --app-id)
            APP_ID="$2"
            shift 2
            ;;
        --access-token)
            ACCESS_TOKEN="$2"
            shift 2
            ;;
        -h|--help)
            echo "用法: bash install.sh [选项]"
            echo ""
            echo "选项:"
            echo "  --app-id <id>            火山引擎应用 ID"
            echo "  --access-token <token>    火山引擎 Access Token"
            echo "  -h, --help               显示帮助信息"
            exit 0
            ;;
        *)
            error "未知参数: $1"
            ;;
    esac
done

# ============================================================
# 主流程
# ============================================================

echo ""
echo "=============================================="
echo "🔥 豆包 TTS - 火山引擎语音合成安装程序"
echo "=============================================="
echo ""

# 1. 检查 Python3
info "检查 Python3 环境..."
if ! command -v python3 &> /dev/null; then
    error "未找到 python3，请先安装 Python 3.8+"
fi
PYTHON_VERSION=$(python3 --version 2>&1)
success "Python 环境: $PYTHON_VERSION"

# 2. 检查 pip
info "检查 pip 环境..."
if ! python3 -m pip --version &> /dev/null; then
    error "未找到 pip，请先安装 pip"
fi
success "pip 已就绪"

# 3. 配置凭证
echo ""
info "配置火山引擎凭证..."

# 如果没有通过命令行传入，则交互式获取
if [ -z "$APP_ID" ]; then
    # 检查是否已有配置
    if [ -f "$ENV_FILE" ]; then
        EXISTING_APP_ID=$(grep "VOLCENGINE_APP_ID" "$ENV_FILE" 2>/dev/null | cut -d'=' -f2)
        if [ -n "$EXISTING_APP_ID" ]; then
            echo "   已有配置: APP_ID=${EXISTING_APP_ID:0:8}..."
            read -p "   是否覆盖？(y/N) " -n 1 -r
            echo ""
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                info "保留已有凭证配置"
                APP_ID="SKIP"
            fi
        fi
    fi

    if [ "$APP_ID" != "SKIP" ]; then
        echo ""
        echo "   请从火山引擎控制台获取凭证："
        echo "   https://console.volcengine.com/"
        echo ""
        read -p "   请输入 VOLCENGINE_APP_ID: " APP_ID
        if [ -z "$APP_ID" ]; then
            error "APP_ID 不能为空"
        fi

        read -p "   请输入 VOLCENGINE_ACCESS_TOKEN: " ACCESS_TOKEN
        if [ -z "$ACCESS_TOKEN" ]; then
            error "ACCESS_TOKEN 不能为空"
        fi
    fi
fi

# 写入配置文件
if [ "$APP_ID" != "SKIP" ]; then
    mkdir -p "$CONFIG_DIR"
    cat > "$ENV_FILE" << EOF
VOLCENGINE_APP_ID=${APP_ID}
VOLCENGINE_ACCESS_TOKEN=${ACCESS_TOKEN}
EOF
    chmod 600 "$ENV_FILE"
    success "凭证已保存到: $ENV_FILE"
fi

# 4. 安装 Python 依赖
echo ""
info "安装 Python 依赖..."
python3 -m pip install -r "$SCRIPT_DIR/requirements.txt" --quiet
success "Python 依赖安装完成"

# 5. 验证脚本可运行
echo ""
info "验证脚本..."
python3 "$SCRIPT_DIR/scripts/tts.py" --help > /dev/null 2>&1 && \
    success "脚本验证通过" || \
    warn "脚本验证失败，请检查 Python 环境"

# 6. 完成
echo ""
echo "=============================================="
success "安装完成! 🎉"
echo "=============================================="
echo ""
echo "使用方式："
echo "  python3 $SCRIPT_DIR/scripts/tts.py \"你好，世界\""
echo "  python3 $SCRIPT_DIR/scripts/tts.py story.md --voice-type zh_fa_story"
echo ""
echo "更多帮助："
echo "  python3 $SCRIPT_DIR/scripts/tts.py --help"
echo ""
