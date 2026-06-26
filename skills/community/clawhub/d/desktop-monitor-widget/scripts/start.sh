#!/bin/bash
# 启动桌面监控悬浮球

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WIDGET_PY="$SCRIPT_DIR/widget-web.py"

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "错误：需要 Python3"
    exit 1
fi

# 检查 psutil
if ! python3 -c "import psutil" 2>/dev/null; then
    echo "正在安装 psutil..."
    pip3 install psutil --break-system-packages -q 2>/dev/null || pip3 install psutil -q
fi

echo "🖥️  启动系统监控悬浮球..."
echo ""
echo "提示："
echo "  - 窗口会自动打开浏览器"
echo "  - 数据每 2 秒自动刷新"
echo "  - 按 Ctrl+C 停止服务"
echo ""

python3 "$WIDGET_PY"
