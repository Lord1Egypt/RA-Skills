#!/bin/bash
# 飞书图片发送 - 发送指定图片（智能压缩）

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

# 显示使用说明
show_usage() {
    echo "使用方法: $0 <图片路径>"
    echo ""
    echo "示例:"
    echo "  $0 ~/Desktop/image.png"
    echo "  $0 ~/Downloads/photo.jpg"
    echo ""
    echo "功能说明:"
    echo "  - 小图片 (< ${COMPRESS_SIZE_MB}MB): 直接发送"
    echo "  - 中等图片 (${COMPRESS_SIZE_MB}-${MAX_SIZE_MB}MB): 压缩后发送"
    echo "  - 大图片 (> ${MAX_SIZE_MB}MB): 发送压缩版和原图版"
    exit 1
}

# 检查依赖
check_dependencies() {
    if ! command -v python3 &> /dev/null; then
        echo "错误: python3 命令不可用"
        exit 1
    fi
    
    if [ ! -f "$UTILS_FILE" ]; then
        echo "错误: 工具文件不存在: $UTILS_FILE"
        exit 1
    fi
}

# 检查文件格式
check_file_format() {
    local file_path="$1"
    local extension="${file_path##*.}"
    extension="${extension,,}"
    
    # 支持的格式列表
    local supported_formats=(${SUPPORTED_FORMATS//,/ })
    
    local is_supported=false
    for format in "${supported_formats[@]}"; do
        if [[ "$extension" == "$format" ]]; then
            is_supported=true
            break
        fi
    done
    
    if ! $is_supported; then
        echo "错误: 不支持的图片格式: $extension"
        echo "支持的格式: ${SUPPORTED_FORMATS}"
        exit 1
    fi
}

# 检查文件是否存在且可读
check_file() {
    local file_path="$1"
    
    if [ ! -f "$file_path" ]; then
        echo "错误: 文件不存在: $file_path"
        exit 1
    fi
    
    if [ ! -r "$file_path" ]; then
        echo "错误: 文件不可读: $file_path"
        exit 1
    fi
    
    # 检查文件大小
    local file_size=$(stat -f%z "$file_path" 2>/dev/null || stat -c%s "$file_path" 2>/dev/null)
    local file_size_mb=$((file_size / 1024 / 1024))
    
    if [ $file_size_mb -gt 50 ]; then
        echo "⚠️  警告: 文件较大 (${file_size_mb} MB)，处理可能需要一些时间"
    fi
}

# 创建必要的目录
create_directories() {
    mkdir -p "$WORKSPACE_DIR"
    mkdir -p "$TEMP_DIR"
}

# 主函数
main() {
    # 检查参数
    if [ $# -eq 0 ]; then
        show_usage
    fi
    
    local image_path="$1"
    
    echo "🖼️  飞书图片发送 - 发送指定图片（智能压缩）"
    echo "========================================"
    
    # 检查依赖
    check_dependencies
    
    # 检查文件格式
    check_file_format "$image_path"
    
    # 检查文件
    check_file "$image_path"
    
    # 创建目录
    create_directories
    
    # 获取文件信息
    local filename=$(basename "$image_path")
    local name="${filename%.*}"
    local extension="${filename##*.}"
    local timestamp=$(date +%Y%m%d_%H%M%S)
    
    echo "📁 文件名: $filename"
    echo "📏 文件路径: $image_path"
    
    # 检查文件大小
    local file_size=$(stat -f%z "$image_path" 2>/dev/null || stat -c%s "$image_path" 2>/dev/null)
    local file_size_mb=$((file_size / 1024 / 1024))
    
    echo "📊 文件大小: ${file_size_mb} MB"
    
    # 使用Python工具处理图片
    echo "🔄 智能处理图片..."
    if python3 "$UTILS_FILE" process_image "$image_path" "${name}_${timestamp}"; then
        echo "🎉 图片已智能处理并发送到飞书"
    else
        echo "❌ 图片处理失败"
        exit 1
    fi
}

# 运行主函数
main "$@"