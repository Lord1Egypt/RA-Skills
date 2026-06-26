#!/usr/bin/env bash
# setup_biliup.sh — 检查并安装 biliup（Python 版官方 CLI）
# 项目主页: https://github.com/biliup/biliup
# 安装方式: pip install biliup（官方 PyPI 包，无需手动下载二进制）
# 使用: bash scripts/setup_biliup.sh

set -euo pipefail

BINARY_NAME="biliup"

echo "🔍 检查 biliup 是否已安装..."

# 检查是否已在 PATH 中
if command -v "$BINARY_NAME" &>/dev/null; then
    CURRENT_VERSION=$("$BINARY_NAME" --version 2>/dev/null | head -1 || echo "unknown")
    echo "✅ biliup 已安装: $CURRENT_VERSION"
    echo "   路径: $(command -v "$BINARY_NAME")"
    exit 0
fi

# 检查 ~/.local/bin（pip install --user 的常见安装路径）
LOCAL_BIN="$HOME/.local/bin/$BINARY_NAME"
if [ -f "$LOCAL_BIN" ]; then
    echo "✅ biliup 已存在于 $LOCAL_BIN"
    echo "   （若命令不可用，请将 ~/.local/bin 加入 PATH）"
    exit 0
fi

echo "📦 未检测到 biliup，开始安装（pip install biliup）..."

# 优先尝试 pipx（隔离环境，推荐）
if command -v pipx &>/dev/null; then
    echo "🛠️  使用 pipx 安装..."
    pipx install biliup
    echo "✅ biliup 安装成功（pipx）"
    exit 0
fi

# 回退到 pip install --user
if command -v pip3 &>/dev/null; then
    echo "🛠️  使用 pip3 install --user 安装..."
    pip3 install --user biliup
elif command -v pip &>/dev/null; then
    echo "🛠️  使用 pip install --user 安装..."
    pip install --user biliup
else
    echo "❌ 未找到 pip 或 pipx，请手动安装 Python 包管理器后重试"
    echo "   参考: https://pip.pypa.io/en/stable/installation/"
    exit 1
fi

# 安装后再检查一次
if command -v "$BINARY_NAME" &>/dev/null; then
    echo "✅ biliup 安装成功: $(biliup --version 2>/dev/null | head -1)"
else
    echo "✅ 安装完成"
    echo "💡 若命令不可用，请将以下内容添加到 ~/.bashrc 或 ~/.zshrc:"
    echo "   export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo "   然后执行: source ~/.bashrc"
fi
