#!/bin/bash
# DolphinDB Environment Loader
# 加载已检测的环境变量，提供统一的 Python 调用接口

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 自动检测并加载 DolphinDB Python 环境
load_dolphindb_env() {
    # 如果已经加载过，直接返回
    if [ -n "$DOLPHINDB_PYTHON_BIN" ]; then
        return 0
    fi
    
    # 运行检测脚本并 eval export 语句
    eval "$(bash "$SCRIPT_DIR/detect_dolphindb_env.sh" 2>/dev/null)"
    
    if [ -z "$DOLPHINDB_PYTHON_BIN" ]; then
        echo "❌ 无法加载 DolphinDB Python 环境"
        return 1
    fi
    
    return 0
}

# 统一的 Python 调用函数
dolphin_python() {
    if ! load_dolphindb_env; then
        return 1
    fi
    
    "$DOLPHINDB_PYTHON_BIN" "$@"
}

# 统一的 pip 调用函数
dolphin_pip() {
    if ! load_dolphindb_env; then
        return 1
    fi
    
    "$DOLPHINDB_PYTHON_BIN" -m pip "$@"
}

# 显示当前环境信息
dolphin_env_info() {
    if ! load_dolphindb_env; then
        return 1
    fi
    
    echo "📊 DolphinDB Python 环境信息"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "环境变量：DOLPHINDB_PYTHON_BIN"
    echo "Python 版本：$DOLPHINDB_PYTHON_VER"
    echo "DolphinDB SDK: $DOLPHINDB_SDK_VERSION"
    echo "环境路径：$DOLPHINDB_ENV_PATH"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "使用方式:"
    echo "  dolphin_python script.py    # 运行 Python 脚本"
    echo "  dolphin_pip install xxx     # 安装包"
    echo "  \$DOLPHINDB_PYTHON_BIN ...   # 直接调用"
}

# 如果直接执行此脚本，显示环境信息
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    dolphin_env_info
fi
