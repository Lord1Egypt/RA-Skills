#!/bin/bash

# send-voice.sh - 发送飞书语音消息
#
# 用法:
#   ./send-voice.sh --to <open_id> --text "要发送的文字"
#   ./send-voice.sh --to <open_id> --file /path/to/audio.opus
#
# 参数:
#   --to <open_id>        接收者 open_id (必填)
#   --text <text>         要转为语音的文字 (与 --file 二选一)
#   --file <file>         已有音频文件路径 (支持 mp3/wav 等)
#   --voice <voice>       TTS 语音 (默认: zh-CN-XiaoxiaoNeural)
#   --rate <rate>         语速 (如 +10%, -10%, 默认: +0%)
#   --volume <volume>     音量 (如 +10%, -10%, 默认: +0%)

set -euo pipefail

# 默认值
DEFAULT_VOICE="zh-CN-XiaoxiaoNeural"
DEFAULT_RATE="+0%"
DEFAULT_VOLUME="+0%"

# 临时文件目录
TEMP_DIR="/tmp/feishu-voice-$$"
mkdir -p "$TEMP_DIR"

# 清理函数
cleanup() {
    rm -rf "$TEMP_DIR"
}

# 错误处理
error() {
    echo "错误: $1" >&2
    cleanup
    exit 1
}

# 显示帮助
show_help() {
    cat << EOF
发送飞书语音消息

用法:
  $0 --to <open_id> --text "文字内容" [选项]
  $0 --to <open_id> --file <音频文件> [选项]

必填参数:
  --to <open_id>        接收者 open_id (以 ou_ 开头)
  --text <text>         要转为语音的文字
  --file <file>         已有音频文件路径

可选参数:
  --voice <voice>       TTS 语音 (默认: $DEFAULT_VOICE)
  --rate <rate>         语速调整 (如 +10%, -10%, 默认: $DEFAULT_RATE)
  --volume <volume>     音量调整 (如 +10%, -10%, 默认: $DEFAULT_VOLUME)
  --help                显示此帮助

示例:
  $0 --to ou_123456 --text "床前明月光"
  $0 --to ou_123456 --text "通知" --voice zh-CN-YunxiNeural
  $0 --to ou_123456 --file /path/to/audio.mp3

常用语音:
  zh-CN-XiaoxiaoNeural  女声/活泼 (默认)
  zh-CN-YunxiNeural     男声/沉稳
  zh-CN-XiaoyiNeural    女声/温柔

查看可用语音:
  edge-tts --list-voices | grep zh-CN

依赖:
  edge-tts, ffmpeg, curl
EOF
}

# 解析参数
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --to)
                if [[ -z "${2:-}" ]]; then
                    error "--to 需要参数"
                fi
                RECEIVER_ID="$2"
                shift 2
                ;;
            --text)
                if [[ -z "${2:-}" ]]; then
                    error "--text 需要参数"
                fi
                TEXT="$2"
                shift 2
                ;;
            --file)
                if [[ -z "${2:-}" ]]; then
                    error "--file 需要参数"
                fi
                INPUT_FILE="$2"
                shift 2
                ;;
            --voice)
                if [[ -z "${2:-}" ]]; then
                    error "--voice 需要参数"
                fi
                VOICE="$2"
                shift 2
                ;;
            --rate)
                if [[ -z "${2:-}" ]]; then
                    error "--rate 需要参数"
                fi
                RATE="$2"
                shift 2
                ;;
            --volume)
                if [[ -z "${2:-}" ]]; then
                    error "--volume 需要参数"
                fi
                VOLUME="$2"
                shift 2
                ;;
            --help)
                show_help
                exit 0
                ;;
            *)
                error "未知参数: $1"
                ;;
        esac
    done
}

# 验证参数
validate_args() {
    # 检查必填参数
    if [[ -z "${RECEIVER_ID:-}" ]]; then
        error "必须指定 --to 参数"
    fi
    
    # 验证 open_id 格式
    if [[ ! "$RECEIVER_ID" =~ ^ou_ ]]; then
        error "open_id 必须以 'ou_' 开头，当前值: $RECEIVER_ID"
    fi
    
    # 检查 text 和 file 至少一个
    if [[ -z "${TEXT:-}" ]] && [[ -z "${INPUT_FILE:-}" ]]; then
        error "必须指定 --text 或 --file"
    fi
    
    # 检查不能同时指定 text 和 file
    if [[ -n "${TEXT:-}" ]] && [[ -n "${INPUT_FILE:-}" ]]; then
        error "--text 和 --file 不能同时指定"
    fi
    
    # 设置默认值
    VOICE="${VOICE:-$DEFAULT_VOICE}"
    RATE="${RATE:-$DEFAULT_RATE}"
    VOLUME="${VOLUME:-$DEFAULT_VOLUME}"
    
    # 验证文件存在
    if [[ -n "${INPUT_FILE:-}" ]] && [[ ! -f "$INPUT_FILE" ]]; then
        error "文件不存在: $INPUT_FILE"
    fi
}

# 获取飞书凭据
get_credentials() {
    # 从环境变量获取
    if [[ -n "${FEISHU_APP_ID:-}" ]] && [[ -n "${FEISHU_APP_SECRET:-}" ]]; then
        APP_ID="$FEISHU_APP_ID"
        APP_SECRET="$FEISHU_APP_SECRET"
        echo "✓ 从环境变量读取凭据" >&2
        return 0
    fi
    
    # 从 .env 文件获取
    if [[ -f "$HOME/.openclaw/.env" ]]; then
        APP_ID=$(grep "^FEISHU_APP_ID=" "$HOME/.openclaw/.env" | cut -d'=' -f2)
        APP_SECRET=$(grep "^FEISHU_APP_SECRET=" "$HOME/.openclaw/.env" | cut -d'=' -f2)
        
        if [[ -n "$APP_ID" ]] && [[ -n "$APP_SECRET" ]]; then
            echo "✓ 从 ~/.openclaw/.env 读取凭据" >&2
            return 0
        fi
    fi
    
    # 从 openclaw.json 获取
    if [[ -f "$HOME/.openclaw/openclaw.json" ]]; then
        if command -v jq > /dev/null 2>&1; then
            APP_ID=$(jq -r '.feishu.app_id // empty' "$HOME/.openclaw/openclaw.json")
            APP_SECRET=$(jq -r '.feishu.app_secret // empty' "$HOME/.openclaw/openclaw.json")
        else
            APP_ID=$(grep '"app_id"' "$HOME/.openclaw/openclaw.json" | cut -d'"' -f4)
            APP_SECRET=$(grep '"app_secret"' "$HOME/.openclaw/openclaw.json" | cut -d'"' -f4)
        fi
        
        if [[ -n "$APP_ID" ]] && [[ -n "$APP_SECRET" ]]; then
            echo "✓ 从 ~/.openclaw/openclaw.json 读取凭据" >&2
            return 0
        fi
    fi
    
    error "找不到飞书凭据。请设置 FEISHU_APP_ID 和 FEISHU_APP_SECRET 环境变量，或在 ~/.openclaw/.env 或 ~/.openclaw/openclaw.json 中配置"
}

# 获取 access token
get_access_token() {
    echo "获取 access_token..." >&2
    
    TOKEN_RESPONSE=$(curl -s -X POST \
        -H "Content-Type: application/json" \
        -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}" \
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal")
    
    if command -v jq > /dev/null 2>&1; then
        ACCESS_TOKEN=$(echo "$TOKEN_RESPONSE" | jq -r '.tenant_access_token')
        if [[ "$ACCESS_TOKEN" == "null" ]] || [[ -z "$ACCESS_TOKEN" ]]; then
            error "获取 token 失败: $TOKEN_RESPONSE"
        fi
    else
        ACCESS_TOKEN=$(echo "$TOKEN_RESPONSE" | grep '"tenant_access_token"' | cut -d'"' -f4)
        if [[ -z "$ACCESS_TOKEN" ]]; then
            error "获取 token 失败: $TOKEN_RESPONSE"
        fi
    fi
    
    echo "✓ 获取 access_token 成功" >&2
}

# 生成 TTS
generate_tts() {
    echo "生成语音: $TEXT" >&2
    
    MP3_FILE="$TEMP_DIR/speech.mp3"
    
    if ! command -v edge-tts > /dev/null 2>&1; then
        error "edge-tts 未安装。请运行: pip install edge-tts"
    fi
    
    edge-tts \
        --voice "$VOICE" \
        --rate "$RATE" \
        --volume "$VOLUME" \
        --text "$TEXT" \
        --write-media "$MP3_FILE" || error "TTS 生成失败"
    
    if [[ ! -f "$MP3_FILE" ]] || [[ ! -s "$MP3_FILE" ]]; then
        error "TTS 生成失败，文件为空"
    fi
    
    INPUT_FILE="$MP3_FILE"
    echo "✓ 语音生成完成" >&2
}

# 转换为 opus
convert_to_opus() {
    echo "转换为 opus 格式..." >&2
    
    if ! command -v ffmpeg > /dev/null 2>&1; then
        error "ffmpeg 未安装。请安装: sudo apt install ffmpeg 或 brew install ffmpeg"
    fi
    
    OPUS_FILE="$TEMP_DIR/audio.opus"
    
    ffmpeg \
        -i "$INPUT_FILE" \
        -c:a libopus \
        -b:a 128k \
        "$OPUS_FILE" \
        -y \
        2>/dev/null || error "转换失败"
    
    if [[ ! -f "$OPUS_FILE" ]] || [[ ! -s "$OPUS_FILE" ]]; then
        error "转换失败，文件为空"
    fi
    
    OPUS_FILE="$OPUS_FILE"
    echo "✓ 转换完成: $(du -h "$OPUS_FILE" | cut -f1)" >&2
}

# 上传文件
upload_file() {
    echo "上传文件到飞书..." >&2
    
    UPLOAD_RESPONSE=$(curl -s -X POST \
        -H "Authorization: Bearer $ACCESS_TOKEN" \
        -F "file_type=opus" \
        -F "file_name=audio.opus" \
        -F "file=@$OPUS_FILE;type=application/octet-stream" \
        "https://open.feishu.cn/open-apis/im/v1/files")
    
    if command -v jq > /dev/null 2>&1; then
        FILE_KEY=$(echo "$UPLOAD_RESPONSE" | jq -r '.data.file_key')
        if [[ "$FILE_KEY" == "null" ]] || [[ -z "$FILE_KEY" ]]; then
            error "上传失败: $UPLOAD_RESPONSE"
        fi
    else
        FILE_KEY=$(echo "$UPLOAD_RESPONSE" | grep '"file_key"' | cut -d'"' -f4)
        if [[ -z "$FILE_KEY" ]]; then
            error "上传失败: $UPLOAD_RESPONSE"
        fi
    fi
    
    echo "✓ 上传成功，file_key: $FILE_KEY" >&2
}

# 发送消息
send_message() {
    echo "发送消息..." >&2
    
    MESSAGE_RESPONSE=$(curl -s -X POST \
        -H "Authorization: Bearer $ACCESS_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{
            \"receive_id\": \"$RECEIVER_ID\",
            \"msg_type\": \"audio\",
            \"content\": \"{\\\"file_key\\\":\\\"$FILE_KEY\\\"}\"
        }" \
        "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id")
    
    if command -v jq > /dev/null 2>&1; then
        if echo "$MESSAGE_RESPONSE" | jq -e '.code == 0' > /dev/null 2>&1; then
            MESSAGE_ID=$(echo "$MESSAGE_RESPONSE" | jq -r '.data.message_id')
            echo "✓ 发送成功，message_id: $MESSAGE_ID" >&2
        else
            error "发送失败: $MESSAGE_RESPONSE"
        fi
    else
        if echo "$MESSAGE_RESPONSE" | grep -q '"code":0'; then
            MESSAGE_ID=$(echo "$MESSAGE_RESPONSE" | grep '"message_id"' | cut -d'"' -f4)
            echo "✓ 发送成功，message_id: $MESSAGE_ID" >&2
        else
            error "发送失败: $MESSAGE_RESPONSE"
        fi
    fi
}

# 主函数
main() {
    # 解析参数
    parse_args "$@"
    
    # 验证参数
    validate_args
    
    # 设置退出时清理
    trap cleanup EXIT
    
    # 获取凭据
    get_credentials
    
    # 获取 token
    get_access_token
    
    # 生成 TTS 或处理已有文件
    if [[ -n "${TEXT:-}" ]]; then
        generate_tts
    fi
    
    # 转换为 opus
    convert_to_opus
    
    # 上传文件
    upload_file
    
    # 发送消息
    send_message
    
    echo "✓ 语音消息发送完成" >&2
}

# 执行主函数
main "$@"