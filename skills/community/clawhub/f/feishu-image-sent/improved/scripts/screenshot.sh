#!/bin/bash
# 飞书图片发送 - 系统截图（智能压缩）

set -e

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
UTILS_FILE="$SCRIPT_DIR/../utils.py"
CONFIG_FILE="$SCRIPT_DIR/../config/settings.sh"

# 加载配置
if [ -f "$CONFIG_FILE" ]; then
    source "$CONFIG_FILE"
else
    echo "错误: 配置文件不存在: $CONFIG_FILE"
    exit 1
fi

# 检查依赖
check_dependencies() {
    if ! command -v /usr/sbin/screencapture &> /dev/null; then
        echo "错误: screencapture 命令不可用"
        exit 1
    fi
    
    if ! command -v python3 &> /dev/null; then
        echo "错误: python3 命令不可用"
        exit 1
    fi
    
    if [ ! -f "$UTILS_FILE" ]; then
        echo "错误: 工具文件不存在: $UTILS_FILE"
        exit 1
    fi
}

# 创建必要的目录
create_directories() {
    mkdir -p "$WORKSPACE_DIR"
    mkdir -p "$TEMP_DIR"
}

# 清理临时文件
cleanup() {
    if [ -n "$TEMP_FILE" ] && [ -f "$TEMP_FILE" ]; then
        rm -f "$TEMP_FILE"
    fi
}

# 主函数
main() {
    echo "🖥️  飞书图片发送 - 系统截图（智能压缩）"
    echo "========================================"
    
    # 检查依赖
    check_dependencies
    
    # 创建目录
    create_directories
    
    # 设置陷阱，确保退出时清理
    trap cleanup EXIT
    
    # 生成时间戳和文件名
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    TEMP_FILE="$TEMP_DIR/screenshot_${TIMESTAMP}.png"
    FINAL_NAME="screenshot_${TIMESTAMP}.png"
    
    echo "📸 正在截取屏幕..."
    
    # 执行截图
    if /usr/sbin/screencapture -x -t png "$TEMP_FILE"; then
        echo "✅ 截图成功: $TEMP_FILE"
        
        # 检查文件大小
        FILE_SIZE=$(stat -f%z "$TEMP_FILE" 2>/dev/null || stat -c%s "$TEMP_FILE" 2>/dev/null)
        FILE_SIZE_MB=$((FILE_SIZE / 1024 / 1024))
        
        echo "📏 图片大小: ${FILE_SIZE_MB} MB"
        
        # 使用Python工具处理图片
        echo "🔄 智能处理图片..."
        if python3 "$UTILS_FILE" process_image "$TEMP_FILE" "$FINAL_NAME"; then
            echo "🎉 图片已智能处理并发送到飞书"
        else
            echo "❌ 图片处理失败"
            exit 1
        fi
        
    else
        echo "❌ 截图失败"
        exit 1
    fi
}

# 运行主函数
main "$@"