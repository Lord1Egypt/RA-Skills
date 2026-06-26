#!/bin/bash
# 简化的图片处理工具

# 检查ImageMagick
check_imagemagick() {
    if command -v convert &> /dev/null; then
        echo "✅ ImageMagick已安装"
        return 0
    else
        echo "❌ ImageMagick未安装"
        echo "安装: brew install imagemagick 或 sudo apt-get install imagemagick"
        return 1
    fi
}

# 调整单张图片尺寸
resize_image() {
    local input="$1"
    local output="$2"
    local width="$3"
    local height="$4"
    
    if [ ! -f "$input" ]; then
        echo "错误: 文件不存在: $input"
        return 1
    fi
    
    convert "$input" -resize "${width}x${height}^" -gravity center -extent "${width}x${height}" "$output"
    echo "✅ 调整完成: $input → $output"
}

# 转换单张图片格式
convert_image() {
    local input="$1"
    local output="$2"
    local format="$3"
    
    if [ ! -f "$input" ]; then
        echo "错误: 文件不存在: $input"
        return 1
    fi
    
    convert "$input" "$output"
    echo "✅ 转换完成: $input → $output"
}

# 优化单张图片质量
optimize_image() {
    local input="$1"
    local output="$2"
    local quality="$3"
    
    if [ ! -f "$input" ]; then
        echo "错误: 文件不存在: $input"
        return 1
    fi
    
    convert "$input" -quality "$quality" "$output"
    echo "✅ 优化完成: $input → $output (质量: ${quality}%)"
}

# 显示帮助
show_help() {
    echo "📸 图片处理工具"
    echo ""
    echo "用法: $0 <命令> [参数]"
    echo ""
    echo "命令:"
    echo "  resize   调整图片尺寸"
    echo "           $0 resize 输入图片 输出图片 宽度 高度"
    echo ""
    echo "  convert  转换图片格式"
    echo "           $0 convert 输入图片 输出图片.格式"
    echo ""
    echo "  optimize 优化图片质量"
    echo "           $0 optimize 输入图片 输出图片 质量(1-100)"
    echo ""
    echo "示例:"
    echo "  $0 resize photo.jpg resized.jpg 800 600"
    echo "  $0 convert image.jpg image.png"
    echo "  $0 optimize photo.jpg optimized.jpg 85"
}

# 主函数
main() {
    if [ $# -eq 0 ]; then
        show_help
        exit 0
    fi
    
    command="$1"
    shift
    
    # 检查ImageMagick
    check_imagemagick || exit 1
    
    case "$command" in
        resize)
            if [ $# -ne 4 ]; then
                echo "错误: 需要4个参数"
                show_help
                exit 1
            fi
            resize_image "$1" "$2" "$3" "$4"
            ;;
        convert)
            if [ $# -ne 2 ]; then
                echo "错误: 需要2个参数"
                show_help
                exit 1
            fi
            convert_image "$1" "$2" "${2##*.}"
            ;;
        optimize)
            if [ $# -ne 3 ]; then
                echo "错误: 需要3个参数"
                show_help
                exit 1
            fi
            optimize_image "$1" "$2" "$3"
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            echo "未知命令: $command"
            show_help
            exit 1
            ;;
    esac
}

# 执行
main "$@"