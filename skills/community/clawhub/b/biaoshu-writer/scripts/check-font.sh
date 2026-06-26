#!/bin/bash
# biaoshu-writer 字体检查脚本 v2.0
# 运行方式: bash check-font.sh

set -e

# 检测操作系统
detect_os() {
    case "$(uname -s)" in
        Darwin*)  echo "macos" ;;
        Linux*)   echo "linux" ;;
        MINGW*|CYGWIN*|MSYS*) echo "windows" ;;
        *)        echo "unknown" ;;
    esac
}

FONT_PATH="$HOME/Library/Fonts/SimSun.ttf"
LINUX_FONT_PATH="/usr/share/fonts/truetype/SimSun.ttf"
OS=$(detect_os)

echo "╔══════════════════════════════════════════════════╗"
echo "║     🔍 biaoshu-writer 字体检查工具 v2.0        ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""

# 检查字体
check_font() {
    if [ -f "$FONT_PATH" ]; then
        echo "✅ SimSun 字体已安装"
        echo "   路径: $FONT_PATH"
        ls -lh "$FONT_PATH"
        echo ""
        echo "✨ 可以正常使用 biaoshu-writer 了！"
        return 0
    fi
    return 1
}

# 显示安装说明
show_install_guide() {
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "❌ SimSun 字体未安装"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    case "$OS" in
        macos)
            echo "📱 macOS 安装方法："
            echo ""
            echo "方法1：从Windows电脑复制（推荐）"
            echo "  1. 找一台Windows电脑"
            echo "  2. 打开 C:\\Windows\\Fonts"
            echo "  3. 找到 SimSun.ttf 文件（注意不是SimSun.ttc）"
            echo "  4. 复制到 Mac 的 ~/Library/Fonts/ 文件夹"
            echo "  5. 重新打开终端，运行: bash check-font.sh"
            echo ""
            echo "方法2：从网上下载"
            echo "  1. 搜索 'SimSun.ttf下载'"
            echo "  2. 下载得到 .ttf 文件"
            echo "  3. 放入 ~/Library/Fonts/"
            ;;
        windows)
            echo "🪟 Windows 安装方法："
            echo ""
            echo "  1. 下载 SimSun.ttf 文件"
            echo "  2. 右键 → 全部提取"
            echo "  3. 复制到 C:\\Windows\\Fonts"
            echo "  4. 如提示覆盖，确认即可"
            ;;
        linux)
            echo "🐧 Linux 安装方法："
            echo ""
            echo "  # 创建用户字体目录"
            echo "  mkdir -p ~/.fonts"
            echo "  cp SimSun.ttf ~/.fonts/"
            echo "  fc-cache -fv"
            ;;
    esac
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📋 验证安装："
    echo "   ls -lh ~/Library/Fonts/SimSun.ttf"
    echo "   # 看到文件路径 = 安装成功"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "💡 提示：安装完成后重新打开终端再运行本脚本"
}

# 主程序
echo "🔍 检测系统: $OS"
echo ""

if check_font; then
    exit 0
else
    show_install_guide
    exit 1
fi