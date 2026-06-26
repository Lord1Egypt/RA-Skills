#!/bin/bash
#
# 机器人音色配置脚本
# 用于配置、绑定、测试火山引擎 TTS 音色
#
# 用法：
#   ./voice-config.sh set <音色 ID> [机器人名称]     # 设置/绑定音色
#   ./voice-config.sh test [音色 ID]                 # 测试音色
#   ./voice-config.sh list [女声 | 男声]             # 列出音色
#   ./voice-config.sh bind <音色 ID> <机器人>        # 绑定音色到机器人
#   ./voice-config.sh status                         # 查看当前配置
#

set -e

# 配置文件
CONFIG_FILE="${CONFIG_FILE:-$HOME/.openclaw/workspace/config/bot-voice-config.json}"
VOICE_LIST_FILE="$HOME/.openclaw/workspace/workspace/火山引擎音色列表 - 官方整理版.md"

# 环境变量（可从配置文件读取）
VOLC_API_KEY="${VOLC_API_KEY:-}"
VOLC_RESOURCE_ID="${VOLC_RESOURCE_ID:-volc.service_type.10029}"
FEISHU_APP_ID="${FEISHU_APP_ID:-}"
FEISHU_APP_SECRET="${FEISHU_APP_SECRET:-}"
FEISHU_DEFAULT_USER_ID="${FEISHU_DEFAULT_USER_ID:-}"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印函数
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 检查环境变量
check_env() {
    if [ -z "$VOLC_API_KEY" ]; then
        print_error "VOLC_API_KEY 环境变量未设置"
        exit 1
    fi
    
    if [ -z "$FEISHU_APP_ID" ] || [ -z "$FEISHU_APP_SECRET" ]; then
        print_warning "飞书应用配置未设置，无法发送测试音频"
    fi
}

# 获取飞书 Token
get_feishu_token() {
    if [ -z "$FEISHU_APP_ID" ] || [ -z "$FEISHU_APP_SECRET" ]; then
        return 1
    fi
    
    TOKEN=$(curl -sL -X POST 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' \
      -H 'Content-Type: application/json' \
      -d "{
        \"app_id\": \"$FEISHU_APP_ID\",
        \"app_secret\": \"$FEISHU_APP_SECRET\"
      }" | jq -r '.tenant_access_token')
    
    if [ -z "$TOKEN" ] || [ "$TOKEN" = "null" ]; then
        return 1
    fi
    
    echo "$TOKEN"
}

# 生成 TTS 音频
generate_tts() {
    local text="$1"
    local speaker="$2"
    local output_file="$3"
    
    print_info "正在生成 TTS 音频..."
    
    RESPONSE=$(curl -sL -X POST 'https://openspeech.bytedance.com/api/v3/tts/unidirectional' \
      -H "x-api-key: $VOLC_API_KEY" \
      -H "X-Api-Resource-Id: $VOLC_RESOURCE_ID" \
      -H 'Content-Type: application/json' \
      -d "{
          \"req_params\": {
              \"text\": \"$text\",
              \"speaker\": \"$speaker\",
              \"additions\": \"{\\\"disable_markdown_filter\\\":true,\\\"enable_language_detector\\\":true}\",
              \"audio_params\": {
                  \"format\": \"mp3\",
                  \"sample_rate\": 24000
              }
          }
      }")
    
    CODE=$(echo "$RESPONSE" | jq -r '.code // empty')
    
    if [ "$CODE" != "0" ]; then
        print_error "TTS 生成失败：$(echo "$RESPONSE" | jq -r '.message')"
        return 1
    fi
    
    echo "$RESPONSE" | jq -r '.data' | base64 -d > "$output_file"
    
    if [ ! -s "$output_file" ]; then
        print_error "音频文件生成失败"
        return 1
    fi
    
    print_success "TTS 音频生成成功"
}

# 转换为 Opus 格式
convert_to_opus() {
    local input_file="$1"
    local output_file="$2"
    
    print_info "正在转换为 Opus 格式..."
    
    ffmpeg -i "$input_file" -c:a libopus -b:a 32k "$output_file" -y 2>/dev/null
    
    if [ ! -s "$output_file" ]; then
        print_error "格式转换失败"
        return 1
    fi
    
    print_success "Opus 转换成功"
}

# 发送飞书语音消息
send_feishu_voice() {
    local opus_file="$1"
    local user_id="${2:-$FEISHU_DEFAULT_USER_ID}"
    
    if [ -z "$FEISHU_APP_ID" ] || [ -z "$FEISHU_APP_SECRET" ]; then
        print_warning "飞书配置不完整，跳过发送"
        return 0
    fi
    
    TOKEN=$(get_feishu_token)
    
    if [ -z "$TOKEN" ]; then
        print_error "获取飞书 Token 失败"
        return 1
    fi
    
    print_info "正在上传音频文件到飞书..."
    
    UPLOAD_RESPONSE=$(curl -sL -X POST 'https://open.feishu.cn/open-apis/im/v1/files' \
      -H "Authorization: Bearer $TOKEN" \
      -F 'file_type=opus' \
      -F 'file_name=voice.opus' \
      -F 'duration=9000' \
      -F "file=@$opus_file")
    
    FILE_KEY=$(echo "$UPLOAD_RESPONSE" | jq -r '.data.file_key')
    
    if [ -z "$FILE_KEY" ] || [ "$FILE_KEY" = "null" ]; then
        print_error "上传文件失败：$(echo "$UPLOAD_RESPONSE" | jq -r '.msg')"
        return 1
    fi
    
    print_success "文件上传成功 (file_key: $FILE_KEY)"
    
    print_info "正在发送语音消息..."
    
    SEND_RESPONSE=$(curl -sL -X POST 'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id' \
      -H "Authorization: Bearer $TOKEN" \
      -H 'Content-Type: application/json' \
      -d "{
        \"receive_id\": \"$user_id\",
        \"msg_type\": \"audio\",
        \"content\": \"{\\\"file_key\\\":\\\"$FILE_KEY\\\"}\"
      }")
    
    SEND_CODE=$(echo "$SEND_RESPONSE" | jq -r '.code // 999')
    
    if [ "$SEND_CODE" != "0" ]; then
        print_error "发送失败：$(echo "$SEND_RESPONSE" | jq -r '.msg')"
        return 1
    fi
    
    MESSAGE_ID=$(echo "$SEND_RESPONSE" | jq -r '.data.message_id')
    print_success "语音消息发送成功 (message_id: $MESSAGE_ID)"
}

# 列出音色
list_speakers() {
    local filter="$1"
    
    print_info "可用音色列表"
    echo ""
    
    case "$filter" in
        女声|female)
            echo "【女声音色】"
            grep -E "ICL_zh_female_|zh_female_|saturn_zh_female_" "$VOICE_LIST_FILE" 2>/dev/null | head -20 || \
            echo "  - 邪魅御姐 - ICL_zh_female_xiangliangya_v1_tob"
            echo "  - 调皮公主 - saturn_zh_female_tiaopigongzhu_tob"
            echo "  - 甜美桃子 - zh_female_tianmeitaozi_uranus_bigtts"
            ;;
        男声|male)
            echo "【男声音色】"
            echo "  - 北京小爷 - zh_male_beijingxiaoye_emo_v2_mars_bigtts"
            echo "  - 儒雅逸辰 - zh_male_ruyayichen_uranus_bigtts"
            ;;
        *)
            echo "【热门音色】"
            echo ""
            echo "【女声】"
            echo "  1. 邪魅御姐 - ICL_zh_female_xiangliangya_v1_tob (成熟魅惑)"
            echo "  2. 调皮公主 - saturn_zh_female_tiaopigongzhu_tob (可爱俏皮)"
            echo "  3. 甜美桃子 - zh_female_tianmeitaozi_uranus_bigtts (甜美温柔)"
            echo ""
            echo "【男声】"
            echo "  1. 北京小爷 - zh_male_beijingxiaoye_emo_v2_mars_bigtts (emo 北京腔)"
            echo "  2. 儒雅逸辰 - zh_male_ruyayichen_uranus_bigtts (儒雅绅士)"
            ;;
    esac
    
    echo ""
    print_info "使用 \"设置音色 <音色 ID>\" 来切换音色"
}

# 设置音色
set_speaker() {
    local speaker_id="$1"
    local bot_name="$2"
    
    if [ -z "$speaker_id" ]; then
        print_error "请提供音色 ID"
        echo "用法：$0 set <音色 ID> [机器人名称]"
        exit 1
    fi
    
    print_info "设置音色..."
    echo ""
    echo "【配置信息】"
    echo "  - 音色 ID: $speaker_id"
    [ -n "$bot_name" ] && echo "  - 机器人：$bot_name"
    echo ""
    
    # 更新配置文件
    if [ -f "$CONFIG_FILE" ]; then
        # 备份原配置
        cp "$CONFIG_FILE" "${CONFIG_FILE}.bak"
        
        # 更新 default_speaker
        jq --arg speaker "$speaker_id" '.default_speaker = $speaker' "$CONFIG_FILE" > "${CONFIG_FILE}.tmp" && \
        mv "${CONFIG_FILE}.tmp" "$CONFIG_FILE"
        
        if [ -n "$bot_name" ]; then
            # 更新机器人绑定
            jq --arg bot "$bot_name" --arg speaker "$speaker_id" \
              '.bot_speakers[$bot] = $speaker' "$CONFIG_FILE" > "${CONFIG_FILE}.tmp" && \
            mv "${CONFIG_FILE}.tmp" "$CONFIG_FILE"
        fi
        
        print_success "配置已保存到 $CONFIG_FILE"
    else
        print_warning "配置文件不存在，跳过保存"
    fi
    
    echo ""
    print_info "发送 \"测试音色\" 来试听效果"
}

# 测试音色
test_speaker() {
    local speaker_id="${1:-}"
    
    # 从配置文件读取默认音色
    if [ -z "$speaker_id" ] && [ -f "$CONFIG_FILE" ]; then
        speaker_id=$(jq -r '.default_speaker // empty' "$CONFIG_FILE")
    fi
    
    if [ -z "$speaker_id" ]; then
        speaker_id="ICL_zh_female_xiangliangya_v1_tob"
    fi
    
    print_info "测试音色：$speaker_id"
    echo ""
    
    # 测试文本
    local test_text="你好呀，我是语音助手。很高兴为你服务，希望你喜欢我的声音！"
    
    # 临时文件
    local tmp_mp3="/tmp/voice-test-$$.mp3"
    local tmp_opus="/tmp/voice-test-$$.opus"
    
    # 生成 TTS
    if ! generate_tts "$test_text" "$speaker_id" "$tmp_mp3"; then
        rm -f "$tmp_mp3" "$tmp_opus"
        exit 1
    fi
    
    # 转换为 Opus
    if ! convert_to_opus "$tmp_mp3" "$tmp_opus"; then
        rm -f "$tmp_mp3" "$tmp_opus"
        exit 1
    fi
    
    # 发送到飞书
    if send_feishu_voice "$tmp_opus"; then
        print_success "测试音频已发送，请查收！"
    else
        print_warning "音频文件已生成：$tmp_opus"
    fi
    
    # 清理
    rm -f "$tmp_mp3" "$tmp_opus"
}

# 绑定音色到机器人
bind_speaker() {
    local speaker_id="$1"
    local bot_name="$2"
    
    if [ -z "$speaker_id" ] || [ -z "$bot_name" ]; then
        print_error "请提供音色 ID 和机器人名称"
        echo "用法：$0 bind <音色 ID> <机器人名称>"
        exit 1
    fi
    
    print_info "绑定音色到机器人..."
    echo ""
    echo "【绑定信息】"
    echo "  - 机器人：$bot_name"
    echo "  - 音色 ID: $speaker_id"
    echo ""
    
    # 更新配置文件
    if [ -f "$CONFIG_FILE" ]; then
        cp "$CONFIG_FILE" "${CONFIG_FILE}.bak"
        
        jq --arg bot "$bot_name" --arg speaker "$speaker_id" \
          '.bot_speakers[$bot] = $speaker | .default_speaker = $speaker' \
          "$CONFIG_FILE" > "${CONFIG_FILE}.tmp" && \
        mv "${CONFIG_FILE}.tmp" "$CONFIG_FILE"
        
        print_success "绑定成功！"
        echo ""
        echo "【状态】"
        echo "  ✅ 已设置为默认回复音色"
        echo "  ✅ 配置已保存"
    else
        print_warning "配置文件不存在"
    fi
}

# 查看状态
show_status() {
    print_info "当前音色配置"
    echo ""
    
    if [ -f "$CONFIG_FILE" ]; then
        echo "【配置文件】$CONFIG_FILE"
        echo ""
        
        DEFAULT=$(jq -r '.default_speaker // "未设置"' "$CONFIG_FILE")
        echo "【默认音色】$DEFAULT"
        echo ""
        
        echo "【机器人绑定】"
        jq -r '.bot_speakers | to_entries[] | "  - \(.key): \(.value)"' "$CONFIG_FILE" 2>/dev/null || \
        echo "  暂无绑定"
    else
        print_warning "配置文件不存在"
    fi
    
    echo ""
}

# 主函数
main() {
    local command="$1"
    shift || true
    
    case "$command" in
        set|设置)
            check_env
            set_speaker "$@"
            ;;
        test|测试)
            check_env
            test_speaker "$@"
            ;;
        list|列表)
            list_speakers "$@"
            ;;
        bind|绑定)
            check_env
            bind_speaker "$@"
            ;;
        status|状态)
            show_status
            ;;
        help|--help|-h)
            echo "机器人音色配置脚本"
            echo ""
            echo "用法："
            echo "  $0 set <音色 ID> [机器人名称]     # 设置/绑定音色"
            echo "  $0 test [音色 ID]                 # 测试音色"
            echo "  $0 list [女声 | 男声]             # 列出音色"
            echo "  $0 bind <音色 ID> <机器人>        # 绑定音色到机器人"
            echo "  $0 status                         # 查看当前配置"
            echo "  $0 help                           # 显示帮助"
            ;;
        *)
            print_error "未知命令：$command"
            echo "使用 \"$0 help\" 查看帮助"
            exit 1
            ;;
    esac
}

main "$@"
