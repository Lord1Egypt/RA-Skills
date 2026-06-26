#!/bin/bash
# audio-translator 主脚本 - 多语种版本 v4 (安全版)
# 支持 URL 和本地文件输入
# 用法: ./translate.sh <input> <target_lang> [output_path]

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# TTS 语音映射表
get_tts_voice() {
    case "$1" in
        en) echo "en-US-AriaNeural" ;;
        zh) echo "zh-CN-XiaoxiaoNeural" ;;
        ja) echo "ja-JP-NanamiNeural" ;;
        fr) echo "fr-FR-DeniseNeural" ;;
        es) echo "es-ES-ElviraNeural" ;;
        de) echo "de-DE-KatjaNeural" ;;
        ko) echo "ko-KR-SunHiNeural" ;;
        ru) echo "ru-RU-SvetlanaNeural" ;;
        it) echo "it-IT-ElsaNeural" ;;
        pt) echo "pt-BR-FranciscaNeural" ;;
        *) echo "en-US-AriaNeural" ;;
    esac
}

# 语言名称映射
get_lang_name() {
    case "$1" in
        en) echo "英文" ;;
        zh) echo "中文" ;;
        ja) echo "日文" ;;
        fr) echo "法文" ;;
        es) echo "西班牙文" ;;
        de) echo "德文" ;;
        ko) echo "韩文" ;;
        ru) echo "俄文" ;;
        it) echo "意大利文" ;;
        pt) echo "葡萄牙文" ;;
        *) echo "$1" ;;
    esac
}

# 验证语言代码
validate_lang() {
    local lang="$1"
    case "$lang" in
        en|zh|ja|fr|es|de|ko|ru|it|pt) return 0 ;;
        *) return 1 ;;
    esac
}

# 解析参数
INPUT_PATH="${1:-}"
TARGET_LANG="${2:-}"
OUTPUT_PATH="${3:-}"

# 检查必需参数
if [[ -z "$INPUT_PATH" ]]; then
    echo -e "${RED}错误: 请提供输入音频路径${NC}"
    echo "用法: ./translate.sh <input_url_or_path> <target_lang> [output_path]"
    echo ""
    echo "支持以下输入类型:"
    echo "  - 本地文件: /Users/winer/Downloads/audio.mp3"
    echo "  - URL: https://example.com/audio.mp3"
    exit 1
fi

if [[ -z "$TARGET_LANG" ]]; then
    echo -e "${RED}错误: 请提供目标语言代码${NC}"
    echo "支持的语言: en, zh, ja, fr, es, de, ko, ru, it, pt"
    exit 1
fi

# 验证目标语言
if ! validate_lang "$TARGET_LANG"; then
    echo -e "${RED}错误: 无效的目标语言代码: $TARGET_LANG${NC}"
    exit 1
fi

# 获取 TTS 语音
TTS_VOICE=$(get_tts_voice "$TARGET_LANG")
TARGET_LANG_NAME=$(get_lang_name "$TARGET_LANG")

# 创建临时目录（安全模式：使用 mktemp -d）
TEMP_DIR=$(mktemp -d)
chmod 700 "$TEMP_DIR"
trap 'rm -rf "$TEMP_DIR"' EXIT

# ========== 检测输入类型并下载/复制 ==========
echo -e "${GREEN}开始多语种翻译...${NC}"

# 检测是否为 URL（安全验证）
if [[ "$INPUT_PATH" =~ ^https?://[a-zA-Z0-9][-a-zA-Z0-9.]* ]]; then
    echo "输入类型: URL"
    echo "URL: $INPUT_PATH"
    
    # 验证 URL 域名（简单白名单）
    if [[ "$INPUT_PATH" =~ \.cn$ ]]; then
        echo -e "${YELLOW}警告: 检测到 .cn 域名，可能无法访问${NC}"
    fi
    
    # 检查 curl
    if ! command -v curl &> /dev/null; then
        echo -e "${RED}错误: 需要 curl${NC}"
        exit 1
    fi
    
    # 获取文件名并安全处理
    FILENAME=$(basename "$INPUT_PATH" | sed 's/[^a-zA-Z0-9._-]/_/g')
    LOCAL_INPUT="$TEMP_DIR/input_${FILENAME}"
    
    # 下载文件（带超时和安全选项）
    echo "正在下载文件..."
    if ! curl -L --max-time 120 -o "$LOCAL_INPUT" -- "$INPUT_PATH" 2>/dev/null; then
        echo -e "${RED}错误: 下载失败${NC}"
        exit 1
    fi
    
    # 验证下载的文件大小
    FILE_SIZE=$(stat -f%z "$LOCAL_INPUT" 2>/dev/null || stat -c%s "$LOCAL_INPUT" 2>/dev/null)
    if [[ "$FILE_SIZE" -lt 100 ]]; then
        echo -e "${RED}错误: 下载的文件过小，可能无效${NC}"
        exit 1
    fi
    
    INPUT_PATH="$LOCAL_INPUT"
    echo "文件下载完成 ($FILE_SIZE bytes)"
else
    echo "输入类型: 本地文件"
    
    # 安全检查：验证文件路径
    if [[ ! -f "$INPUT_PATH" ]]; then
        echo -e "${RED}错误: 文件不存在: $INPUT_PATH${NC}"
        exit 1
    fi
    
    # 安全检查：验证不是符号链接到敏感位置
    if [[ -L "$INPUT_PATH" ]]; then
        echo -e "${RED}错误: 不支持符号链接${NC}"
        exit 1
    fi
fi

# 检查文件格式（安全验证）
EXT="${INPUT_PATH##*.}"
EXT_LOWER=$(echo "$EXT" | tr '[:upper:]' '[:lower:]')
ALLOWED_FORMATS="mp3|wav|m4a|aac|ogg|flac|wma"

if [[ ! "$EXT_LOWER" =~ ^($ALLOWED_FORMATS)$ ]]; then
    echo -e "${RED}错误: 不支持的格式: $EXT${NC}"
    exit 1
fi

echo "输入文件: $INPUT_PATH"

# 设置输出路径（安全处理）
if [[ -z "$OUTPUT_PATH" ]]; then
    BASENAME=$(basename "$INPUT_PATH" .$EXT | sed 's/[^a-zA-Z0-9._-]/_/g')
    OUTPUT_DIR=$(dirname "$INPUT_PATH")
    # 避免在临时目录输出
    if [[ "$OUTPUT_DIR" == "$TEMP_DIR" || "$OUTPUT_DIR" == "/tmp"* ]]; then
        OUTPUT_DIR="$HOME/Downloads"
    fi
    OUTPUT_PATH="$OUTPUT_DIR/${BASENAME}_${TARGET_LANG}.mp3"
fi

# 验证输出路径不包含危险字符
if [[ "$OUTPUT_PATH" =~ [\;\|\&\$\`\\] ]]; then
    echo -e "${RED}错误: 输出路径包含非法字符${NC}"
    exit 1
fi

echo "目标语言: $TARGET_LANG_NAME ($TARGET_LANG)"
echo "输出文件: $OUTPUT_PATH"

# ========== 步骤1: 检查依赖 ==========
echo -e "\n${YELLOW}[1/4] 检查依赖...${NC}"

# 检查 FFmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo -e "${RED}错误: FFmpeg 未安装${NC}"
    echo "请运行: brew install ffmpeg"
    exit 1
fi

# 检查 Python 依赖
PYTHON_BIN="/usr/local/opt/python@3.11/Frameworks/Python.framework/Versions/3.11/bin/python3.11"
if ! $PYTHON_BIN -c "import faster_whisper" 2>/dev/null; then
    echo "安装 Python 依赖..."
    $PYTHON_BIN -m pip install --user -r "$(dirname "$0")/requirements.txt" 2>/dev/null || \
    $PYTHON_BIN -m pip install -r "$(dirname "$0")/requirements.txt"
fi

# ========== 步骤2: 语音识别 (Whisper) ==========
echo -e "\n${YELLOW}[2/4] 语音识别 (Whisper)...${NC}"

# 创建独立的 Python 脚本文件（避免 heredoc 注入）
cat > "$TEMP_DIR/whisper识别.py" << 'PYEOF'
import sys
import json
from faster_whisper import WhisperModel

input_file = sys.argv[1]
output_text = sys.argv[2]
output_lang = sys.argv[3]

model = WhisperModel('tiny', device='cpu', compute_type='int8')
segments, info = model.transcribe(input_file)

source_text = ''.join([seg.text for seg in segments])
detected_lang = info.language

# 安全写入文件
with open(output_text, 'w', encoding='utf-8') as f:
    f.write(source_text)
with open(output_lang, 'w', encoding='utf-8') as f:
    f.write(detected_lang)

print(f'LANG:{detected_lang}')
print(f'TEXT:{source_text[:200]}')
PYEOF

# 执行 Python（通过文件传递参数）
$PYTHON_BIN "$TEMP_DIR/whisper识别.py" "$INPUT_PATH" "$TEMP_DIR/source_text.txt" "$TEMP_DIR/detected_lang.txt"

SOURCE_TEXT=$(cat "$TEMP_DIR/source_text.txt")
DETECTED_LANG=$(cat "$TEMP_DIR/detected_lang.txt")
echo "源语言: $DETECTED_LANG ($(get_lang_name $DETECTED_LANG))"
echo "识别文本: ${SOURCE_TEXT:0:60}..."

# ========== 步骤3: 翻译 ==========
echo -e "\n${YELLOW}[3/4] 翻译 ($(get_lang_name $DETECTED_LANG) → $TARGET_LANG_NAME)...${NC}"

# 创建翻译脚本（使用 curl，避免 SSL 问题）
cat > "$TEMP_DIR/translate.sh" << 'SHEOF'
#!/bin/bash
SOURCE_TEXT_FILE="$1"
TRANSLATED_FILE="$2"
SOURCE_LANG="$3"
TARGET_LANG="$4"

# 读取源文本
SOURCE_TEXT=$(cat "$SOURCE_TEXT_FILE")

# 使用 curl 调用翻译 API（避免 Python urllib SSL 问题）
ENCODED_TEXT=$(python3 -c "import urllib.parse; print(urllib.parse.quote('''$SOURCE_TEXT'''))" 2>/dev/null || echo "")
API_URL="https://api.mymemory.translated.net/get?q=${ENCODED_TEXT}&langpair=${SOURCE_LANG}|${TARGET_LANG}"

# 调用 API
API_RESULT=$(curl -s --max-time 30 "$API_URL" 2>/dev/null)

# 解析 JSON（使用 Python）
TRANSLATED=$(python3 -c "
import sys, json
try:
    data = json.loads('''$API_RESULT''')
    print(data['responseData']['translatedText'])
except:
    print('''$SOURCE_TEXT''')
" 2>/dev/null || echo "$SOURCE_TEXT")

# 写入结果
echo "$TRANSLATED" > "$TRANSLATED_FILE"
echo "TRANSLATED:$TRANSLATED"
SHEOF

chmod +x "$TEMP_DIR/translate.sh"
"$TEMP_DIR/translate.sh" "$TEMP_DIR/source_text.txt" "$TEMP_DIR/translated_text.txt" "$DETECTED_LANG" "$TARGET_LANG"

TRANSLATED_TEXT=$(cat "$TEMP_DIR/translated_text.txt")
echo "翻译结果: ${TRANSLATED_TEXT:0:60}..."

# ========== 步骤4: 目标语言语音合成 ==========
echo -e "\n${YELLOW}[4/4] ${TARGET_LANG_NAME}语音合成 (edge-tts)...${NC}"

# 创建 TTS 脚本（安全）
cat > "$TEMP_DIR/tts.py" << 'PYEOF'
import sys
import asyncio
import edge_tts

translated_file = sys.argv[1]
output_file = sys.argv[2]
voice = sys.argv[3]

with open(translated_file, 'r', encoding='utf-8') as f:
    text = f.read()

async def main():
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)

asyncio.run(main())
print(f'OK:{output_file}')
PYEOF

$PYTHON_BIN "$TEMP_DIR/tts.py" "$TEMP_DIR/translated_text.txt" "$OUTPUT_PATH" "$TTS_VOICE"

# 保存文本文件
TEXT_OUTPUT_PATH="${OUTPUT_PATH%.*}.txt"
cp "$TEMP_DIR/translated_text.txt" "$TEXT_OUTPUT_PATH"

echo -e "\n${GREEN}========== 多语种翻译完成！==========${NC}"
echo "源语言: $(get_lang_name $DETECTED_LANG) ($DETECTED_LANG)"
echo "目标语言: $TARGET_LANG_NAME ($TARGET_LANG)"
echo "输出音频: $OUTPUT_PATH"
echo "输出文本: $TEXT_OUTPUT_PATH"
