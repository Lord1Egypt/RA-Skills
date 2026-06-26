#!/bin/bash
# Feishu Edge TTS - 使用微软 Edge TTS 发送飞书语音条
# 用法：bash send_voice.sh -t "文字内容" [-v 音色] [-r 语速] [-p 音调]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"

# 默认配置
DEFAULT_VOICE="zh-CN-XiaoxiaoNeural"
DEFAULT_RATE="0"
DEFAULT_PITCH="0"

VOICE="$DEFAULT_VOICE"
RATE="$DEFAULT_RATE"
PITCH="$DEFAULT_PITCH"
TEXT=""
OUTPUT_FILE=""
LIST_VOICES=false
NO_SEND=false

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 打印帮助
print_help() {
    cat << EOF
🎤 Feishu Edge TTS - 微软免费 TTS 发送飞书语音条

用法：bash $0 [选项]

选项:
  -t, --text <text>       要转换的文字（必需）
  -v, --voice <voice>     音色名称（默认：zh-CN-XiaoxiaoNeural）
  -r, --rate <0>          语速（-50 到 +50，默认 0）
  -p, --pitch <0>         音调（-50 到 +50，默认 0）
  -o, --output <file>     输出音频文件路径
  --list-voices           列出所有可用音色
  --no-send               只生成音频，不发送
  -h, --help              显示帮助

常用音色:
  zh-CN-XiaoxiaoNeural    女声，温暖亲切（推荐）
  zh-CN-YunxiNeural       男声，沉稳专业
  zh-CN-YunjianNeural     男声，激情澎湃
  zh-CN-XiaoyiNeural      女声，活泼可爱
  en-US-JennyNeural       女声，美式英语

示例:
  bash $0 -t "主人晚上好～"
  bash $0 -t "Hello!" -v en-US-JennyNeural
  bash $0 -t "你好" --rate 10 --pitch 5
  bash $0 --list-voices

EOF
}

# 列出所有可用音色
list_voices() {
    echo -e "${BLUE}🎤 获取可用音色列表...${NC}"
    
    if command -v edge-tts &> /dev/null; then
        edge-tts --list-voices 2>/dev/null | grep -E "zh-CN|zh-HK|zh-TW|en-US|en-GB" | head -30
    else
        echo "未安装 edge-tts，请先运行：pip install edge-tts"
    fi
}

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -t|--text)
            TEXT="$2"
            shift 2
            ;;
        -v|--voice)
            VOICE="$2"
            shift 2
            ;;
        -r|--rate)
            RATE="$2"
            shift 2
            ;;
        -p|--pitch)
            PITCH="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        --list-voices)
            LIST_VOICES=true
            shift
            ;;
        --no-send)
            NO_SEND=true
            shift
            ;;
        -h|--help)
            print_help
            exit 0
            ;;
        *)
            echo -e "${RED}❌ 未知选项：$1${NC}"
            print_help
            exit 1
            ;;
    esac
done

# 列出音色模式
if [ "$LIST_VOICES" = true ]; then
    list_voices
    exit 0
fi

# 检查必需参数
if [ -z "$TEXT" ]; then
    echo -e "${RED}❌ 错误：必须提供 -t 文字${NC}"
    print_help
    exit 1
fi

# 检查 edge-tts 是否安装
if ! command -v edge-tts &> /dev/null; then
    echo -e "${RED}❌ 错误：未安装 edge-tts${NC}"
    echo "请运行：pip install edge-tts"
    exit 1
fi

# 检查环境变量（发送时需要）
if [ "$NO_SEND" = false ]; then
    if [ -z "$FEISHU_APP_ID" ] || [ -z "$FEISHU_APP_SECRET" ] || [ -z "$FEISHU_CHAT_ID" ]; then
        echo -e "${RED}❌ 错误：缺少 Feishu 配置${NC}"
        echo "请设置："
        echo "  export FEISHU_APP_ID=\"cli_xxx\""
        echo "  export FEISHU_APP_SECRET=\"xxx\""
        echo "  export FEISHU_CHAT_ID=\"oc_xxx\""
        exit 1
    fi
fi

echo -e "${BLUE}🎤 开始生成语音...${NC}"
echo "文字：$TEXT"
echo "音色：$VOICE"
echo "语速：$RATE%"
echo "音调：$PITCH Hz"
echo ""

# 生成临时文件
TEMP_DIR=$(mktemp -d)
TEMP_MP3="$TEMP_DIR/voice.mp3"
TEMP_OPUS="$TEMP_DIR/voice.opus"

# 使用 edge-tts 生成语音
echo -e "${BLUE}🔊 调用 Edge TTS...${NC}"

# 构建参数
RATE_PARAM=""
if [ "$RATE" != "0" ]; then
    RATE_PARAM="--rate $RATE%"
fi

PITCH_PARAM=""
if [ "$PITCH" != "0" ]; then
    PITCH_PARAM="--pitch $PITCHHz"
fi

# 生成 MP3
edge-tts --voice "$VOICE" --text "$TEXT" $RATE_PARAM $PITCH_PARAM --write-media "$TEMP_MP3" 2>&1 | tail -3

if [ ! -f "$TEMP_MP3" ] || [ ! -s "$TEMP_MP3" ]; then
    echo -e "${RED}❌ 错误：语音生成失败${NC}"
    rm -rf "$TEMP_DIR"
    exit 1
fi

echo -e "${GREEN}✅ 语音生成成功${NC}"

# 转换为 OPUS 格式
echo -e "${BLUE}🔄 转换为 OPUS 格式...${NC}"
ffmpeg -i "$TEMP_MP3" -c:a libopus -b:a 32k "$TEMP_OPUS" -y 2>&1 | tail -3

if [ ! -f "$TEMP_OPUS" ] || [ ! -s "$TEMP_OPUS" ]; then
    echo -e "${RED}❌ 错误：OPUS 转换失败${NC}"
    rm -rf "$TEMP_DIR"
    exit 1
fi

echo -e "${GREEN}✅ OPUS 转换成功${NC}"

# 保存输出文件（如果指定）
if [ -n "$OUTPUT_FILE" ]; then
    cp "$TEMP_OPUS" "$OUTPUT_FILE"
    echo -e "${GREEN}✅ 已保存到：$OUTPUT_FILE${NC}"
fi

# 只生成不发送
if [ "$NO_SEND" = true ]; then
    rm -rf "$TEMP_DIR"
    echo -e "${GREEN}✅ 完成（未发送）${NC}"
    exit 0
fi

echo -e "${BLUE}📤 上传到飞书...${NC}"

# 获取 Token
TOKEN=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d "{\"app_id\":\"$FEISHU_APP_ID\",\"app_secret\":\"$FEISHU_APP_SECRET\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin).get('tenant_access_token',''))")

if [ -z "$TOKEN" ]; then
    echo -e "${RED}❌ 错误：获取 Token 失败${NC}"
    rm -rf "$TEMP_DIR"
    exit 1
fi

# 上传文件
UPLOAD_RESULT=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/files" \
  -H "Authorization: Bearer $TOKEN" \
  -F "type=audio" \
  -F "file=@$TEMP_OPUS" \
  -F "file_type=opus")

FILE_KEY=$(echo "$UPLOAD_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('data',{}).get('file_key',''))")

if [ -z "$FILE_KEY" ]; then
    echo -e "${RED}❌ 错误：文件上传失败${NC}"
    echo "$UPLOAD_RESULT"
    rm -rf "$TEMP_DIR"
    exit 1
fi

echo -e "${GREEN}✅ 文件上传成功，File Key: $FILE_KEY${NC}"

# 获取音频时长
DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$TEMP_OPUS")
DURATION_MS=$(echo "$DURATION" | awk '{printf "%.0f", $1 * 1000}')

echo -e "${BLUE}📤 发送语音消息...${NC}"

# 发送消息
RESULT=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"receive_id\":\"$FEISHU_CHAT_ID\",\"msg_type\":\"audio\",\"content\":\"{\\\"file_key\\\":\\\"$FILE_KEY\\\",\\\"duration\\\":$DURATION_MS}\"}")

MESSAGE_ID=$(echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('data',{}).get('message_id',''))")

# 清理临时文件
rm -rf "$TEMP_DIR"

# 检查结果
if [ -n "$MESSAGE_ID" ]; then
    echo -e "${GREEN}✅ 发送成功！${NC}"
    echo "Message ID: $MESSAGE_ID"
    echo "Chat ID: $FEISHU_CHAT_ID"
    echo "时长：${DURATION_MS}ms (${DURATION}s)"
else
    echo -e "${RED}❌ 发送失败${NC}"
    echo "$RESULT"
    exit 1
fi
