#!/bin/bash
# DolphinDB 全局环境包装器
# 可在任何位置调用，自动定位技能目录

# 获取脚本所在目录（绝对路径）
SKILLS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_PARENT="$(dirname "$SKILLS_DIR")"

# 环境检测函数
init_dolphin_global_env() {
    # 如果已经初始化，直接返回
    if [ -n "$DOLPHINDB_PYTHON_BIN" ] && [ -x "$DOLPHINDB_PYTHON_BIN" ]; then
        if $DOLPHINDB_PYTHON_BIN -c "import dolphindb" 2>/dev/null; then
            return 0
        fi
    fi
    
    # 运行环境检测脚本（使用绝对路径）
    local detect_result
    detect_result=$("$SKILLS_DIR/init_dolphindb_env.py" --export 2>/dev/null)
    
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

# 导出函数供其他脚本使用
export -f init_dolphin_global_env

# 主函数
main() {
    if ! init_dolphin_global_env; then
        exit 1
    fi
    
    echo "✅ 使用 DolphinDB Python 环境：$DOLPHINDB_PYTHON_BIN"
    echo "   SDK 版本：$DOLPHINDB_SDK_VERSION"
    echo "   技能目录：$SKILLS_DIR"
    echo ""
    
    # 执行传入的脚本或命令
    if [ $# -gt 0 ]; then
        exec "$DOLPHINDB_PYTHON_BIN" "$@"
    else
        echo "用法：dolphin_global.sh <script.py> [args...]"
        echo "或：source dolphin_global.sh && dolphin_python script.py"
        echo ""
        echo "此脚本可在任何位置调用，会自动定位 DolphinDB 技能目录"
    fi
}

# 如果直接执行而不是 source
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
