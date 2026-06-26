#!/bin/bash
# screen-vision Skill 一键安装脚本
# 用法: bash install.sh [--api-key YOUR_KEY] [--headless] [--desktop]

set -e

API_KEY=""
MODE=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --api-key)  API_KEY="$2"; shift 2;;
        --headless) MODE="headless"; shift;;
        --desktop)  MODE="desktop"; shift;;
        *) echo "未知参数: $1"; exit 1;;
    esac
done

echo "╔══════════════════════════════════════╗"
echo "║   screen-vision Skill 安装向导       ║"
echo "╚══════════════════════════════════════╝"
echo ""

# 1. 确定安装目录
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_NAME="screen-vision"
SKILLS_DIR="$HOME/.openclaw/workspace/skills"
TARGET_DIR="$SKILLS_DIR/$SKILL_NAME"

echo "[1/5] 安装目录: $TARGET_DIR"
mkdir -p "$SKILLS_DIR"

# 如果不在 skills 目录下，先复制过去
if [ "$SCRIPT_DIR" != "$TARGET_DIR" ]; then
    cp -r "$SCRIPT_DIR" "$TARGET_DIR"
    echo "  ✅ 文件已复制到 $TARGET_DIR"
else
    echo "  ✅ 已在正确目录"
fi

# 2. 检测平台
echo ""
echo "[2/5] 检测平台..."
OS="$(uname -s)"
case "$OS" in
    Linux*)  PLATFORM="linux";;
    Darwin*) PLATFORM="macos";;
    MINGW*|MSYS*|CYGWIN*) PLATFORM="windows";;
    *)       echo "❌ 不支持的平台: $OS"; exit 1;;
esac
echo "  平台: $PLATFORM ($OS)"

# 3. 检测模式 (仅 Linux)
if [ "$PLATFORM" = "linux" ] && [ -z "$MODE" ]; then
    if [ -n "$DISPLAY" ] || [ -n "$WAYLAND_DISPLAY" ]; then
        MODE="desktop"
        echo "  模式: desktop (检测到桌面环境)"
    else
        MODE="headless"
        echo "  模式: headless (无桌面环境)"
    fi
elif [ -z "$MODE" ]; then
    MODE="desktop"
fi

# 4. 安装依赖
echo ""
echo "[3/5] 安装系统依赖 (需要 sudo)..."
case "$PLATFORM" in
    linux)
        bash "$TARGET_DIR/scripts/setup/setup-linux.sh" --"$MODE"
        ;;
    macos)
        bash "$TARGET_DIR/scripts/setup/setup-mac.sh"
        ;;
    windows)
        python3 "$TARGET_DIR/scripts/setup/setup-win.py"
        ;;
esac

# 5. 配置 API Key
echo ""
echo "[4/5] 配置 API Key..."
CONFIG_FILE="$TARGET_DIR/config.json"
if [ -n "$API_KEY" ]; then
    # 用命令行参数的 key
    cp "$TARGET_DIR/config.example.json" "$CONFIG_FILE"
    # 用 sed 替换
    if command -v python3 &>/dev/null; then
        python3 -c "
import json
with open('$CONFIG_FILE') as f: c = json.load(f)
c['vision']['apiKey'] = '$API_KEY'
with open('$CONFIG_FILE', 'w') as f: json.dump(c, f, indent=2)
"
    fi
    echo "  ✅ API Key 已配置"
elif [ -f "$CONFIG_FILE" ]; then
    echo "  ✅ 已有配置文件"
else
    cp "$TARGET_DIR/config.example.json" "$CONFIG_FILE"
    echo "  ⚠️  请编辑 $CONFIG_FILE 填入你的 API Key"
    echo "     或设置环境变量: export SV_VISION_API_KEY=你的key"
fi

# 6. 验证
echo ""
echo "[5/5] 验证安装..."
OK=true

# 检查 Python
if command -v python3 &>/dev/null; then
    echo "  ✅ Python3"
else
    echo "  ❌ Python3 未找到"
    OK=false
fi

# 检查平台工具
case "$PLATFORM" in
    linux)
        command -v scrot &>/dev/null && echo "  ✅ scrot" || { echo "  ❌ scrot"; OK=false; }
        command -v xdotool &>/dev/null && echo "  ✅ xdotool" || { echo "  ❌ xdotool"; OK=false; }
        ;;
    macos)
        command -v cliclick &>/dev/null && echo "  ✅ cliclick" || { echo "  ❌ cliclick"; OK=false; }
        ;;
esac

# 检查 Python 库
python3 -c "from PIL import Image; print('  ✅ Pillow')" 2>/dev/null || { echo "  ❌ Pillow"; OK=false; }

echo ""
if $OK; then
    echo "╔══════════════════════════════════════╗"
    echo "║   ✅ 安装成功！                      ║"
    echo "╠══════════════════════════════════════╣"
    echo "║                                       ║"
    echo "║  下一步:                              ║"
    echo "║  1. 编辑 config.json 填入 API Key     ║"
    echo "║  2. 重启 OpenClaw gateway             ║"
    echo "║  3. 告诉 AI: '帮我操作电脑'           ║"
    if [ "$MODE" = "headless" ]; then
        echo "║  4. 启动虚拟桌面: sv-start            ║"
    fi
    echo "║                                       ║"
    echo "╚══════════════════════════════════════╝"
else
    echo "⚠️  部分依赖缺失，请检查上方错误信息"
fi
