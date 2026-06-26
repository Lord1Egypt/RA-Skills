#!/bin/bash
# 批量转录脚本
# 自动处理目录中的所有音频文件

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/../.venv"

# 默认参数
MODEL="large-v3-turbo"
LANGUAGE="zh"
DEVICE="cpu"
COMPUTE_TYPE="auto"
OUTPUT_DIR="./transcripts"
FORMATS="mp3 wav m4a flac ogg webm"

# 显示帮助信息
show_help() {
    echo "批量转录脚本"
    echo ""
    echo "用法: $0 [选项] [音频目录]"
    echo ""
    echo "选项:"
    echo "  -h, --help            显示此帮助信息"
    echo "  -m, --model MODEL     指定模型 (默认: large-v3-turbo)"
    echo "  -l, --language LANG   指定语言代码 (默认: zh)"
    echo "  -d, --device DEVICE   计算设备: auto, cpu, cuda (默认: cpu)"
    echo "  -c, --compute TYPE    计算类型: auto, int8, float16, float32 (默认: auto)"
    echo "  -o, --output DIR      输出目录 (默认: ./transcripts)"
    echo "  --word-timestamps     包含词级时间戳"
    echo "  --json                输出 JSON 格式"
    echo "  --vad                 启用语音活动检测"
    echo ""
    echo "示例:"
    echo "  $0 ./audio_files"
    echo "  $0 -m large-v3-turbo -l en --device cuda ./recordings"
    echo "  $0 --model small --device cpu --compute-type int8 ./interviews"
    echo ""
    exit 0
}

# 解析命令行参数
POSITIONAL_ARGS=()
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            ;;
        -m|--model)
            MODEL="$2"
            shift 2
            ;;
        -l|--language)
            LANGUAGE="$2"
            shift 2
            ;;
        -d|--device)
            DEVICE="$2"
            shift 2
            ;;
        -c|--compute)
            COMPUTE_TYPE="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --word-timestamps)
            WORD_TIMESTAMPS="--word-timestamps"
            shift
            ;;
        --json)
            JSON_OUTPUT="--json"
            shift
            ;;
        --vad)
            VAD="--vad"
            shift
            ;;
        -*|--*)
            echo "错误: 未知选项 $1"
            exit 1
            ;;
        *)
            POSITIONAL_ARGS+=("$1")
            shift
            ;;
    esac
done

# 设置位置参数
set -- "${POSITIONAL_ARGS[@]}"

# 检查输入目录
if [ $# -eq 0 ]; then
    INPUT_DIR="."
else
    INPUT_DIR="$1"
fi

if [ ! -d "$INPUT_DIR" ]; then
    echo "错误: 输入目录不存在: $INPUT_DIR"
    exit 1
fi

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 激活虚拟环境
if [ -f "$VENV_DIR/bin/activate" ]; then
    source "$VENV_DIR/bin/activate"
else
    echo "警告: 未找到虚拟环境，尝试直接使用 Python"
fi

# 设置环境变量（国内镜像加速）
export HF_HOME=/config/huggingface
export HF_ENDPOINT=https://hf-mirror.com

echo "========================================"
echo "批量转录开始"
echo "输入目录: $INPUT_DIR"
echo "输出目录: $OUTPUT_DIR"
echo "模型: $MODEL"
echo "语言: $LANGUAGE"
echo "设备: $DEVICE"
echo "计算类型: $COMPUTE_TYPE"
echo "========================================"
echo ""

# 统计变量
TOTAL_FILES=0
SUCCESS_COUNT=0
FAIL_COUNT=0

# 处理音频文件
for format in $FORMATS; do
    for audio_file in "$INPUT_DIR"/*."$format" "$INPUT_DIR"/*."${format^^}"; do
        if [ -f "$audio_file" ]; then
            TOTAL_FILES=$((TOTAL_FILES + 1))
            
            filename=$(basename "$audio_file")
            base_name="${filename%.*}"
            output_file="$OUTPUT_DIR/$base_name.txt"
            
            echo "处理 [$TOTAL_FILES]: $filename"
            
            # 构建命令
            cmd="python3 $SCRIPT_DIR/transcribe.py \"$audio_file\" \
                --model \"$MODEL\" \
                --language \"$LANGUAGE\" \
                --device \"$DEVICE\" \
                --compute-type \"$COMPUTE_TYPE\" \
                --output \"$output_file\""
            
            # 添加可选参数
            [ -n "$WORD_TIMESTAMPS" ] && cmd="$cmd $WORD_TIMESTAMPS"
            [ -n "$JSON_OUTPUT" ] && cmd="$cmd $JSON_OUTPUT"
            [ -n "$VAD" ] && cmd="$cmd $VAD"
            
            # 执行转录
            if eval "$cmd" 2>/dev/null; then
                echo "  ✓ 完成: $output_file"
                SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
            else
                echo "  ✗ 失败: $filename"
                FAIL_COUNT=$((FAIL_COUNT + 1))
            fi
            
            echo ""
        fi
    done
done

# 处理完成
echo "========================================"
echo "批量转录完成"
echo "总计文件: $TOTAL_FILES"
echo "成功: $SUCCESS_COUNT"
echo "失败: $FAIL_COUNT"
echo "输出目录: $OUTPUT_DIR"
echo "========================================"

# 生成摘要文件
if [ $SUCCESS_COUNT -gt 0 ]; then
    SUMMARY_FILE="$OUTPUT_DIR/转录摘要.txt"
    {
        echo "批量转录摘要"
        echo "生成时间: $(date)"
        echo "输入目录: $INPUT_DIR"
        echo "输出目录: $OUTPUT_DIR"
        echo "模型: $MODEL"
        echo "语言: $LANGUAGE"
        echo "设备: $DEVICE"
        echo "计算类型: $COMPUTE_TYPE"
        echo ""
        echo "文件统计:"
        echo "- 总计文件: $TOTAL_FILES"
        echo "- 成功转录: $SUCCESS_COUNT"
        echo "- 失败: $FAIL_COUNT"
        echo ""
        echo "转录文件列表:"
        find "$OUTPUT_DIR" -name "*.txt" -type f | while read file; do
            echo "- $(basename "$file")"
        done
    } > "$SUMMARY_FILE"
    
    echo "摘要已保存到: $SUMMARY_FILE"
fi

# 停用虚拟环境（如果激活了）
if type deactivate >/dev/null 2>&1; then
    deactivate
fi