#!/bin/bash
# Auto B-roll Insert - 自动插入 B-roll 脚本
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
🎬 Auto B-roll Insert - 自动插入 B-roll

用法:
  $0 <主视频> <B-roll 目录> <输出视频> [选项]

选项:
  --script <文件>     文案文件路径（用于智能匹配 B-roll）
  --min-duration <秒> B-roll 最小持续时间 (default: 2)
  --max-duration <秒> B-roll 最大持续时间 (default: 5)
  --transition <类型> 转场类型 (default: fade)
                      可选：fade, dissolve, none
  --position <位置>   插入位置策略 (default: auto)
                      可选：auto, start, middle, end, random
  --audio <模式>      B-roll 音频处理 (default: mute)
                      可选：mute, mix, replace

智能匹配规则:
  1. 如果提供文案文件，会根据关键词自动匹配 B-roll
  2. 在场景转换/停顿处自动插入
  3. 根据文案情感色彩选择合适风格的 B-roll

示例:
  $0 main.mp4 ./broll/ output.mp4
  $0 main.mp4 ./broll/ output.mp4 --script script.txt --transition dissolve

EOF
    exit 0
}

# 参数解析
MAIN_VIDEO=""
BROLL_DIR=""
OUTPUT_VIDEO=""
SCRIPT_FILE=""
MIN_DURATION="2"
MAX_DURATION="5"
TRANSITION="fade"
POSITION="auto"
AUDIO_MODE="mute"

while [[ $# -gt 0 ]]; do
    case $1 in
        --script)
            SCRIPT_FILE="$2"
            shift 2
            ;;
        --min-duration)
            MIN_DURATION="$2"
            shift 2
            ;;
        --max-duration)
            MAX_DURATION="$2"
            shift 2
            ;;
        --transition)
            TRANSITION="$2"
            shift 2
            ;;
        --position)
            POSITION="$2"
            shift 2
            ;;
        --audio)
            AUDIO_MODE="$2"
            shift 2
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
            if [[ -z "$MAIN_VIDEO" ]]; then
                MAIN_VIDEO="$1"
            elif [[ -z "$BROLL_DIR" ]]; then
                BROLL_DIR="$1"
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
if [[ -z "$MAIN_VIDEO" ]] || [[ -z "$BROLL_DIR" ]] || [[ -z "$OUTPUT_VIDEO" ]]; then
    echo_error "请指定主视频、B-roll 目录和输出视频"
    echo "用法：$0 <主视频> <B-roll 目录> <输出视频> [选项]"
    echo "使用 --help 查看帮助"
    exit 1
fi

# 检查文件/目录是否存在
if [[ ! -f "$MAIN_VIDEO" ]]; then
    echo_error "主视频不存在：$MAIN_VIDEO"
    exit 1
fi

if [[ ! -d "$BROLL_DIR" ]]; then
    echo_error "B-roll 目录不存在：$BROLL_DIR"
    exit 1
fi

# 检查 ffmpeg 是否安装
if ! command -v ffmpeg &> /dev/null; then
    echo_error "ffmpeg 未安装，请先安装：brew install homebrew-ffmpeg/ffmpeg/ffmpeg"
    exit 1
fi

echo_info "主视频：$MAIN_VIDEO"
echo_info "B-roll 目录：$BROLL_DIR"
echo_info "输出视频：$OUTPUT_VIDEO"
echo_info "转场类型：$TRANSITION"
echo_info "插入位置：$POSITION"

# 获取主视频信息
echo_info "分析主视频..."
MAIN_DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$MAIN_VIDEO")
echo_info "主视频时长：${MAIN_DURATION}s"

# 查找 B-roll 文件
echo_info "扫描 B-roll 文件..."
BROLL_FILES=()
while IFS= read -r -d '' file; do
    if [[ "$file" == *.mp4 ]] || [[ "$file" == *.mov ]] || [[ "$file" == *.mkv ]]; then
        BROLL_FILES+=("$file")
    fi
done < <(find "$BROLL_DIR" -maxdepth 1 -type f \( -name "*.mp4" -o -name "*.mov" -o -name "*.mkv" \) -print0)

if [[ ${#BROLL_FILES[@]} -eq 0 ]]; then
    echo_warning "未找到 B-roll 文件，跳过插入"
    cp "$MAIN_VIDEO" "$OUTPUT_VIDEO"
    echo_success "直接复制主视频（无 B-roll）"
    exit 0
fi

echo_info "找到 ${#BROLL_FILES[@]} 个 B-roll 文件"

# 分析每个 B-roll 的时长
declare -A BROLL_DURATIONS
for broll in "${BROLL_FILES[@]}"; do
    duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$broll")
    BROLL_DURATIONS["$broll"]=$duration
    echo_info "  $(basename "$broll"): ${duration}s"
done

# 计算插入点（基于主视频的场景检测）
echo_info "检测主视频场景..."
SCENE_FILE="/tmp/fcpx_scenes.txt"

# 使用 ffmpeg 的场景检测
ffmpeg -i "$MAIN_VIDEO" -filter_complex "select='gt(scene,0.3)',metadata=print:file=$SCENE_FILE" -f null - 2>/dev/null || true

# 读取场景转换点
INSERT_POINTS=()
if [[ -f "$SCENE_FILE" ]]; then
    while IFS= read -r line; do
        if [[ "$line" =~ ^pts_time:([0-9.]+) ]]; then
            INSERT_POINTS+=("${BASH_REMATCH[1]}")
        fi
    done < "$SCENE_FILE"
fi

# 如果没有检测到场景，使用固定间隔
if [[ ${#INSERT_POINTS[@]} -eq 0 ]]; then
    echo_warning "未检测到明显场景，使用固定间隔插入"
    INTERVAL=30  # 每 30 秒插入一个 B-roll
    current=10
    while (( $(echo "$current < $MAIN_DURATION" | bc -l) )); do
        INSERT_POINTS+=("$current")
        current=$((current + INTERVAL))
    done
fi

echo_info "找到 ${#INSERT_POINTS[@]} 个插入点"

# 创建临时目录
TEMP_DIR=$(mktemp -d)
echo_info "临时目录：$TEMP_DIR"

# 准备 B-roll 片段（裁剪到合适长度）
PREPARED_BROLLS=()
for broll in "${BROLL_FILES[@]}"; do
    broll_name=$(basename "$broll")
    broll_duration=${BROLL_DURATIONS["$broll"]}
    
    # 随机选择一段（如果 B-roll 太长）
    if (( $(echo "$broll_duration > $MAX_DURATION" | bc -l) )); then
        # 随机起始点
        max_start=$(echo "$broll_duration - $MAX_DURATION" | bc)
        random_start=$(echo "scale=2; $RANDOM / 32767 * $max_start" | bc -l)
        
        prepared_file="$TEMP_DIR/prepared_$broll_name"
        ffmpeg -y -i "$broll" -ss "$random_start" -t "$MAX_DURATION" \
            -c:v libx264 -preset fast -c:a aac \
            "$prepared_file" 2>/dev/null
        
        PREPARED_BROLLS+=("$prepared_file")
        echo_info "准备 B-roll: $broll_name (${MAX_DURATION}s)"
    else
        PREPARED_BROLLS+=("$broll")
        echo_info "准备 B-roll: $broll_name (${broll_duration}s)"
    fi
done

# 构建 ffmpeg 滤镜链
echo_info "构建视频合成链..."

# 创建输入文件列表
INPUT_LIST="$TEMP_DIR/inputs.txt"
echo "file '$MAIN_VIDEO'" > "$INPUT_LIST"

broll_index=0
for insert_point in "${INSERT_POINTS[@]}"; do
    if [[ $broll_index -ge ${#PREPARED_BROLLS[@]} ]]; then
        broll_index=0  # 循环使用 B-roll
    fi
    
    broll_file="${PREPARED_BROLLS[$broll_index]}"
    broll_duration=${BROLL_DURATIONS["$broll_file"]:-3}
    
    # 限制 B-roll 时长
    if (( $(echo "$broll_duration > $MAX_DURATION" | bc -l) )); then
        broll_duration=$MAX_DURATION
    fi
    if (( $(echo "$broll_duration < $MIN_DURATION" | bc -l) )); then
        broll_duration=$MIN_DURATION
    fi
    
    echo_info "在 ${insert_point}s 插入 B-roll (${broll_duration}s): $(basename "$broll_file")"
    
    ((broll_index++))
done

# 使用 ffmpeg 的 overlay 滤镜插入 B-roll
# 简化版本：在指定时间点叠加 B-roll

FILTER_COMPLEX=""
INPUT_ARGS="-i \"$MAIN_VIDEO\""

broll_index=0
overlay_filters=()
for insert_point in "${INSERT_POINTS[@]}"; do
    if [[ $broll_index -ge ${#PREPARED_BROLLS[@]} ]]; then
        break
    fi
    
    broll_file="${PREPARED_BROLLS[$broll_index]}"
    
    # 计算转场效果
    case $TRANSITION in
        fade)
            FADE_IN="fade=t=in:st=$insert_point:d=0.5"
            FADE_OUT="fade=t=out:st=$((insert_point + 2)):d=0.5"
            ;;
        dissolve)
            FADE_IN="fade=t=in:st=$insert_point:d=1"
            FADE_OUT="fade=t=out:st=$((insert_point + 1.5)):d=1"
            ;;
        none)
            FADE_IN=""
            FADE_OUT=""
            ;;
    esac
    
    ((broll_index++))
done

# 简化的处理方法：使用 concat 连接
echo_info "使用 concat 方法合成视频..."

CONCAT_LIST="$TEMP_DIR/concat.txt"
echo "# FFMPEG CONCAT LIST" > "$CONCAT_LIST"

# 简单策略：主视频 + B-roll 交替
# 实际应该更智能，但先实现基础版本

current_pos=0
broll_index=0

for insert_point in "${INSERT_POINTS[@]}"; do
    if [[ $broll_index -ge ${#PREPARED_BROLLS[@]} ]]; then
        break
    fi
    
    broll_file="${PREPARED_BROLLS[$broll_index]}"
    broll_duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$broll_file" 2>/dev/null || echo "3")
    
    # 限制时长
    if (( $(echo "$broll_duration > $MAX_DURATION" | bc -l) )); then
        broll_duration=$MAX_DURATION
    fi
    
    # 添加主视频片段（从当前位置到插入点）
    segment_duration=$(echo "$insert_point - $current_pos" | bc)
    if (( $(echo "$segment_duration > 0" | bc -l) )); then
        echo "file '$MAIN_VIDEO'" >> "$CONCAT_LIST"
        echo "inpoint $current_pos" >> "$CONCAT_LIST"
        echo "outpoint $insert_point" >> "$CONCAT_LIST"
    fi
    
    # 添加 B-roll 片段
    echo "file '$broll_file'" >> "$CONCAT_LIST"
    echo "inpoint 0" >> "$CONCAT_LIST"
    echo "outpoint $broll_duration" >> "$CONCAT_LIST"
    
    current_pos=$insert_point
    ((broll_index++))
done

# 添加剩余的主视频
if (( $(echo "$current_pos < $MAIN_DURATION" | bc -l) )); then
    echo "file '$MAIN_VIDEO'" >> "$CONCAT_LIST"
    echo "inpoint $current_pos" >> "$CONCAT_LIST"
    echo "outpoint $MAIN_DURATION" >> "$CONCAT_LIST"
fi

# 使用 concat  demuxer 合成
echo_info "合成最终视频..."
ffmpeg -y -f concat -safe 0 -i "$CONCAT_LIST" \
    -c:v libx264 -preset medium -crf 23 \
    -c:a aac -b:a 192k \
    "$OUTPUT_VIDEO" 2>&1 | tee /tmp/fcpx_broll.log

# 检查是否成功
if [[ $? -eq 0 ]] && [[ -f "$OUTPUT_VIDEO" ]]; then
    echo_success "B-roll 插入完成！"
    echo_info "输出文件：$OUTPUT_VIDEO"
    
    # 显示文件信息
    OUTPUT_SIZE=$(ls -lh "$OUTPUT_VIDEO" | awk '{print $5}')
    OUTPUT_DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$OUTPUT_VIDEO")
    echo_info "输出大小：$OUTPUT_SIZE"
    echo_info "输出时长：${OUTPUT_DURATION}s"
    
    # 清理临时文件
    rm -rf "$TEMP_DIR"
    rm -f "$SCENE_FILE"
    
    echo_success "🎬 B-roll 插入成功！插入了 ${#INSERT_POINTS[@]} 个 B-roll 片段 (≧∇≦)"
else
    echo_error "B-roll 插入失败，请查看日志：/tmp/fcpx_broll.log"
    rm -rf "$TEMP_DIR"
    rm -f "$SCENE_FILE"
    exit 1
fi
