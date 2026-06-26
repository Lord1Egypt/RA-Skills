#!/bin/bash
# fund-advisor CLI 脚本
# 调用 tools 中的 fund-tools 命令

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
TOOLS_DIR="$PROJECT_ROOT/tools"
VENV_DIR="$TOOLS_DIR/venv"
INSTALL_MARKER="$VENV_DIR/.install_timestamp"
SRC_DIR="$TOOLS_DIR/src"

# 获取源代码目录的最新修改时间（秒级）
get_src_mtime() {
    if [ -d "$SRC_DIR" ]; then
        # 查找最新修改的 .py 文件，取整数部分
        find "$SRC_DIR" -name "*.py" -type f -printf '%T@\n' 2>/dev/null | sort -n | tail -1 | cut -d. -f1
    else
        echo 0
    fi
}

# 检查 venv 是否有效
check_venv() {
    [ -x "$VENV_DIR/bin/pip" ] || return 1
    [ -x "$VENV_DIR/bin/fund-tools" ] || return 1
    "$VENV_DIR/bin/pip" --version >/dev/null 2>&1 || return 1
    return 0
}

# 检查是否需要重新安装（代码已更新）
need_reinstall() {
    # 如果没有安装标记文件，需要安装
    [ -f "$INSTALL_MARKER" ] || return 0

    # 获取安装时间和源代码最新修改时间
    local install_time=$(cat "$INSTALL_MARKER" 2>/dev/null || echo 0)
    local src_mtime=$(get_src_mtime)

    # 如果源代码比安装时间新，需要重新安装
    if [ -n "$src_mtime" ] && [ "$src_mtime" -gt "$install_time" ] 2>/dev/null; then
        return 0
    fi

    return 1
}

# 安装/重新安装
do_install() {
    echo "Installing fund-tools..."
    "$VENV_DIR/bin/pip" install -e "$TOOLS_DIR" -q
    # 记录安装时间（秒级）
    date +%s > "$INSTALL_MARKER"
}

# 主逻辑
if ! check_venv; then
    echo "Creating virtual environment..."
    rm -rf "$VENV_DIR"
    python3 -m venv "$VENV_DIR"
    do_install
elif need_reinstall; then
    echo "Source code changed, reinstalling..."
    do_install
fi

# 运行命令
exec "$VENV_DIR/bin/fund-tools" "$@"