#!/usr/bin/env bash
# free-web-search 依赖安装脚本
# 用法: bash scripts/setup.sh
# 支持: --mirror <url>  指定 pip 镜像源

set -e

MIRROR="${1:-}"
if [ "$1" = "--mirror" ] && [ -n "$2" ]; then
    MIRROR="$2"
fi

PIP_ARGS=""
if [ -n "$MIRROR" ]; then
    PIP_ARGS="-i $MIRROR --trusted-host $(echo $MIRROR | sed 's|https\?://||' | cut -d/ -f1)"
fi

echo "=== free-web-search 依赖安装 ==="

# 检测 pip
if command -v pip &>/dev/null; then
    PIP=pip
elif command -v pip3 &>/dev/null; then
    PIP=pip3
else
    echo "[ERROR] 找不到 pip，请先安装 Python 3.10+"
    exit 1
fi

echo "[1/3] 安装 Python 包..."
$PIP install playwright $PIP_ARGS

echo "[2/3] 安装 Chromium 浏览器..."
playwright install chromium

echo "[3/3] 验证安装..."
python3 -c "
from playwright.sync_api import sync_playwright; print('  playwright OK')
pw = sync_playwright().start()
b = pw.chromium.launch(headless=True)
b.close()
pw.stop()
print('  chromium OK')
"

echo "=== 安装完成 ==="
