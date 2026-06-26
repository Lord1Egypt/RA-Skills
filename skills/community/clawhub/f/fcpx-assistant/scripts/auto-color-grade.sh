#!/bin/bash
# Auto Color Grade - 自动调色脚本
# Made by Steve & Steven (≧∇≦)

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
echo_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
echo_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
echo_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 使用帮助
show_help() {
    cat << EOF
🎨 Auto Color Grade - 自动调色

用法:
  $0 <输入视频> <输出视频> [选项]

选项:
  --style <风格>     调色风格预设 (default: natural)
                     可选：natural, cinematic, vintage, fresh, warm, cool
  --intensity <强度> 调色强度 0.0-1.0 (default: 0.7)
  --preview          仅生成预览（前 10 秒）
  --help             显示此帮助信息

风格说明:
  natural   - 自然风格，轻微增强
  cinematic - 电影感，高对比度，冷色调
  vintage   - 复古风格，暖色调，降低饱和度
  fresh     - 清新风格，提高饱和度和亮度
  warm      - 温暖风格，增强橙黄色调
  cool      - 冷色风格，增强蓝绿色调

示例:
  $0 input.mp4 output.mp4 --style cinematic
  $0 input.mp4 output.mp4 --style vintage --intensity 0.5

EOF
    exit 0
}

# 参数解析
INPUT_VIDEO=""
OUTPUT_VIDEO=""
STYLE="natural"
INTENSITY="0.7"
PREVIEW=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --style)
            STYLE="$2"
            shift 2
            ;;
        --intensity)
            INTENSITY="$2"
            shift 2
            ;;
        --preview)
            PREVIEW=true
            shift
            ;;
        --help)
            show_help
            ;;
        -*)
            echo_error "未知选项：$1"
            echo "使用 --help 查看帮助"
            exit 1
            ;;
        *)
            if [[ -z "$INPUT_VIDEO" ]]; then
                INPUT_VIDEO="$1"
            elif [[ -z "$OUTPUT_VIDEO" ]]; then
                OUTPUT_VIDEO="$1"
            else
                echo_error "参数过多：$1"
                exit 1
            fi
            shift
            ;;
    esac
done

# 检查参数
if [[ -z "$INPUT_VIDEO" ]] || [[ -z "$OUTPUT_VIDEO" ]]; then
    echo_error "请指定输入和输出视频文件"
    echo "用法：$0 <输入视频> <输出视频> [选项]"
    echo "使用 --help 查看帮助"
    exit 1
fi

# 检查文件是否存在
if [[ ! -f "$INPUT_VIDEO" ]]; then
    echo_error "输入文件不存在：$INPUT_VIDEO"
    exit 1
fi

# 检查 ffmpeg 是否安装
if ! command -v ffmpeg &> /dev/null; then
    echo_error "ffmpeg 未安装，请先安装：brew install homebrew-ffmpeg/ffmpeg/ffmpeg"
    exit 1
fi

echo_info "输入视频：$INPUT_VIDEO"
echo_info "输出视频：$OUTPUT_VIDEO"
echo_info "调色风格：$STYLE"
echo_info "调色强度：$INTENSITY"

# 获取视频信息
echo_info "分析视频信息..."
DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$INPUT_VIDEO")
echo_info "视频时长：${DURATION}s"

# 如果是预览模式，只处理前 10 秒
if [[ "$PREVIEW" == true ]]; then
    echo_info "预览模式：仅处理前 10 秒"
    DURATION="10"
    PREVIEW_ARGS="-t 10"
else
    PREVIEW_ARGS=""
fi

# 根据风格设置 ffmpeg 滤镜参数
case $STYLE in
    natural)
        # 自然风格：轻微增强对比度和饱和度
        COLOR_FILTER="eq=contrast=1.1:saturation=1.15:brightness=0.02:gamma=1.05"
        ;;
    cinematic)
        # 电影感：高对比度，冷色调，暗角
        COLOR_FILTER="eq=contrast=1.3:saturation=0.9:brightness=-0.02:gamma=0.95,curves=vintage,lenscorrection=cx=0.5:cy=0.5:k1=-0.2:k2=0.1"
        ;;
    vintage)
        # 复古风格：暖色调，降低饱和度，添加颗粒感
        COLOR_FILTER="eq=contrast=1.15:saturation=0.7:brightness=0.05:gamma=1.1,curves=vintage,colorchannelmixer=.9:.1:0:0:.9:.1:0:0:.9:.1:0:0:0:0:0:1"
        ;;
    fresh)
        # 清新风格：提高饱和度和亮度
        COLOR_FILTER="eq=contrast=1.05:saturation=1.4:brightness=0.08:gamma=1.02"
        ;;
    warm)
        # 温暖风格：增强橙黄色调
        COLOR_FILTER="eq=contrast=1.1:saturation=1.2:brightness=0.03,curves=vintage,colorchannelmixer=1:0:0:0:0.9:0.1:0:0:0.9:0.1:0:0:0:0:0:1"
        ;;
    cool)
        # 冷色风格：增强蓝绿色调
        COLOR_FILTER="eq=contrast=1.15:saturation=1.1:brightness=-0.02:gamma=0.98,colorchannelmixer=0.9:0.1:0:0:0.9:0.1:0:0:0.9:0.1:0:0:0:0:0:1"
        ;;
    *)
        echo_error "未知的调色风格：$STYLE"
        echo "可选风格：natural, cinematic, vintage, fresh, warm, cool"
        exit 1
        ;;
esac

# 应用强度
if [[ "$INTENSITY" != "1.0" ]]; then
    echo_info "应用强度调整：$INTENSITY"
    # 强度调整通过混合原视频实现
    MIX_RATIO=$(echo "scale=2; $INTENSITY" | bc)
fi

# 创建临时目录
TEMP_DIR=$(mktemp -d)
TEMP_OUTPUT="$TEMP_DIR/colored.mp4"

echo_info "开始调色..."
echo_info "使用滤镜：$COLOR_FILTER"

# 执行调色
if [[ "$PREVIEW" == true ]]; then
    ffmpeg -y -i "$INPUT_VIDEO" -t 10 \
        -vf "$COLOR_FILTER" \
        -c:v libx264 -preset medium -crf 23 \
        -c:a aac -b:a 192k \
        "$TEMP_OUTPUT" 2>&1 | tee /tmp/fcpx_colorgrade.log
else
    ffmpeg -y -i "$INPUT_VIDEO" \
        -vf "$COLOR_FILTER" \
        -c:v libx264 -preset medium -crf 23 \
        -c:a aac -b:a 192k \
        "$TEMP_OUTPUT" 2>&1 | tee /tmp/fcpx_colorgrade.log
fi

# 检查是否成功
if [[ $? -eq 0 ]]; then
    # 如果强度不是 1.0，需要混合原视频
    if [[ "$INTENSITY" != "1.0" ]] && [[ "$PREVIEW" == false ]]; then
        echo_info "混合原视频（强度：$INTENSITY）..."
        ffmpeg -y -i "$INPUT_VIDEO" -i "$TEMP_OUTPUT" \
            -filter_complex "[0:v][1:v]mix=$MIX_RATIO:1-$MIX_RATIO[outv]" \
            -map "[outv]" -map 1:a \
            -c:v libx264 -preset medium -crf 23 \
            -c:a aac -b:a 192k \
            "$OUTPUT_VIDEO" 2>&1 | tee -a /tmp/fcpx_colorgrade.log
        rm -f "$TEMP_OUTPUT"
    else
        mv "$TEMP_OUTPUT" "$OUTPUT_VIDEO"
    fi
    
    echo_success "调色完成！"
    echo_info "输出文件：$OUTPUT_VIDEO"
    
    # 显示文件信息
    if [[ -f "$OUTPUT_VIDEO" ]]; then
        OUTPUT_SIZE=$(ls -lh "$OUTPUT_VIDEO" | awk '{print $5}')
        echo_info "输出大小：$OUTPUT_SIZE"
    fi
    
    # 清理临时目录
    rm -rf "$TEMP_DIR"
    
    echo_success "🎨 调色成功！(≧∇≦)"
else
    echo_error "调色失败，请查看日志：/tmp/fcpx_colorgrade.log"
    rm -rf "$TEMP_DIR"
    exit 1
fi
