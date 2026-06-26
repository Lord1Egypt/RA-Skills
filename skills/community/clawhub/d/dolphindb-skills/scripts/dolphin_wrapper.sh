#!/bin/bash
# DolphinDB Python 环境包装器
# 自动检测并使用正确的 Python 环境执行 DolphinDB 脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(dirname "$SCRIPT_DIR")"

# 环境检测函数
init_dolphin_env() {
    # 如果已经初始化，直接返回
    if [ -n "$DOLPHINDB_PYTHON_BIN" ] && [ -x "$DOLPHINDB_PYTHON_BIN" ]; then
        # 验证是否真的有 dolphindb
        if $DOLPHINDB_PYTHON_BIN -c "import dolphindb" 2>/dev/null; then
            return 0
        fi
    fi
    
    # 运行环境检测脚本
    local detect_result
    detect_result=$("$SCRIPT_DIR/init_dolphindb_env.py" --export 2>/dev/null)
    
    if [ $? -eq 0 ]; then
        # 解析输出并设置环境变量
        while IFS= read -r line; do
            if [[ "$line" == export* ]]; then
                eval "$line"
            fi
        done <<< "$detect_result"
        
        if [ -n "$DOLPHINDB_PYTHON_BIN" ]; then
            return 0
        fi
    fi
    
    echo "❌ 无法初始化 DolphinDB Python 环境" >&2
    return 1
}

# 主函数
main() {
    if ! init_dolphin_env; then
        exit 1
    fi
    
    echo "✅ 使用 DolphinDB Python 环境：$DOLPHINDB_PYTHON_BIN"
    echo "   SDK 版本：$DOLPHINDB_SDK_VERSION"
    echo ""
    
    # 执行传入的脚本或命令
    if [ $# -gt 0 ]; then
        exec "$DOLPHINDB_PYTHON_BIN" "$@"
    else
        echo "用法：dolphin_wrapper.sh <script.py> [args...]"
        echo "或：source dolphin_wrapper.sh && dolphin_python script.py"
    fi
}

# 如果直接执行而不是 source
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
