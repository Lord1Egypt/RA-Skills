#!/bin/bash
# 携程笔记全自动发布启动脚本

echo "🚀 携程笔记全自动发布"
echo "======================"

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python3，请先安装"
    exit 1
fi

# 检查 Playwright
if ! python3 -c "import playwright" 2>/dev/null; then
    echo "📦 安装 Playwright..."
    pip3 install playwright
    playwright install chromium
fi

# 运行发布脚本
cd "$(dirname "$0")"
python3 ctrip_auto_publish.py