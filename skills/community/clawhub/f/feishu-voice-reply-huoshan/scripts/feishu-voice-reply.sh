#!/bin/bash
#
# 飞书语音回复自动化脚本
# 使用火山引擎 TTS 生成特色音色语音，通过飞书 API 发送语音消息
#
# 用法：./feishu-voice-reply.sh "要转换的文本" [音色] [用户 ID]
# 示例：./feishu-voice-reply.sh "你好呀" "ICL_zh_female_tiaopigongzhu_tob" "ou_xxxxxx"
#

set -e

# 参数
TEXT="${1:-你好呀，我是语音助手}"

# 音色配置：复制火山引擎音色列表中的音色 ID 到此处
# 可用音色示例:
#   ICL_zh_female_tiaopigongzhu_tob        - 调皮公主 (女，活泼可爱) ✅已测试
#   zh_male_beijingxiaoye_emo_v2_mars_bigtts - 北京小爷 emo (男) ✅已测试
#   zh_female_wanwanxiao_mars_bigtts       - 弯弯笑 (女，甜美)
#   zh_female_jingjing_mars_bigtts         - 晶晶 (女，清新)
#   zh_female_qingwan_mars_bigtts          - 轻婉 (女，温柔)
#   zh_male_beijingxiaoye_mars_bigtts      - 北京小爷 (男，北京腔)
# 完整音色列表：https://www.volcengine.com/docs/6561/1257544?lang=zh
SPEAKER="${2:-ICL_zh_female_tiaopigongzhu_tob}"
USER_ID="${3:-${FEISHU_DEFAULT_USER_ID:-}}"

# 配置文件（从环境变量读取）
# 火山引擎 API 配置
if [ -z "$VOLC_API_KEY" ]; then
    echo "❌ 错误：VOLC_API_KEY 环境变量未设置"
    echo "请在 ~/.openclaw/.env 或系统环境变量中设置 VOLC_API_KEY"
    exit 1
fi

if [ -z "$VOLC_RESOURCE_ID" ]; then
    echo "❌ 错误：VOLC_RESOURCE_ID 环境变量未设置"
    echo "请在 ~/.openclaw/.env 或系统环境变量中设置 VOLC_RESOURCE_ID"
    exit 1
fi

# 飞书应用配置
if [ -z "$FEISHU_APP_ID" ]; then
    echo "❌ 错误：FEISHU_APP_ID 环境变量未设置"
    echo "请在 ~/.openclaw/.env 或系统环境变量中设置 FEISHU_APP_ID"
    exit 1
fi

if [ -z "$FEISHU_APP_SECRET" ]; then
    echo "❌ 错误：FEISHU_APP_SECRET 环境变量未设置"
    echo "请在 ~/.openclaw/.env 或系统环境变量中设置 FEISHU_APP_SECRET"
    exit 1
fi

# 临时文件
TMP_MP3="/tmp/voice-tts-$.mp3"
TMP_OPUS="/tmp/voice-tts-$.opus"

# 清理函数
cleanup() {
    rm -f "$TMP_MP3" "$TMP_OPUS" 2>/dev/null
}
trap cleanup EXIT

echo "🎤 飞书语音回复"
echo "================"
echo "📝 文本：$TEXT"
echo "🎵 音色：$SPEAKER"
echo "👤 用户：${USER_ID:-当前会话用户}"
echo ""

# 步骤 1：生成 TTS 音频
echo "⏳ 步骤 1/5: 生成火山引擎 TTS 音频..."
RESPONSE=$(curl -sL -X POST 'https://openspeech.bytedance.com/api/v3/tts/unidirectional' \
  -H "x-api-key: $VOLC_API_KEY" \
  -H "X-Api-Resource-Id: $VOLC_RESOURCE_ID" \
  -H 'Content-Type: application/json' \
  -d "{
      \"req_params\": {
          \"text\": \"$TEXT\",
          \"speaker\": \"$SPEAKER\",
          \"additions\": \"{\\\"disable_markdown_filter\\\":true,\\\"enable_language_detector\\\":true}\",
          \"audio_params\": {
              \"format\": \"mp3\",
              \"sample_rate\": 24000
          }
      }
  }")

CODE=$(echo "$RESPONSE" | jq -r '.code // empty')
if [ "$CODE" != "0" ]; then
    echo "❌ TTS 生成失败：$(echo "$RESPONSE" | jq -r '.message')"
    exit 1
fi

echo "$RESPONSE" | jq -r '.data' | base64 -d > "$TMP_MP3"

if [ ! -f "$TMP_MP3" ] || [ ! -s "$TMP_MP3" ]; then
    echo "❌ TTS 音频文件生成失败"
    exit 1
fi

echo "✅ TTS 生成成功"

# 步骤 2：转换为 Opus 格式
echo "⏳ 步骤 2/5: 转换为 Opus 格式..."
ffmpeg -i "$TMP_MP3" -c:a libopus -b:a 32k "$TMP_OPUS" -y 2>/dev/null

if [ ! -f "$TMP_OPUS" ] || [ ! -s "$TMP_OPUS" ]; then
    echo "❌ Opus 格式转换失败"
    exit 1
fi

echo "✅ Opus 转换成功 ($(ls -lh "$TMP_OPUS" | awk '{print $5}'))"

# 步骤 3：获取飞书 Tenant Access Token
echo "⏳ 步骤 3/5: 获取飞书 Access Token..."
TOKEN_RESPONSE=$(curl -sL -X POST 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' \
  -H 'Content-Type: application/json' \
  -d "{
    \"app_id\": \"$FEISHU_APP_ID\",
    \"app_secret\": \"$FEISHU_APP_SECRET\"
  }")

TOKEN=$(echo "$TOKEN_RESPONSE" | jq -r '.tenant_access_token')
TOKEN_CODE=$(echo "$TOKEN_RESPONSE" | jq -r '.code // 0')

if [ -z "$TOKEN" ] || [ "$TOKEN" = "null" ] || [ "$TOKEN_CODE" != "0" ]; then
    echo "❌ 获取飞书 token 失败：$(echo "$TOKEN_RESPONSE" | jq -r '.msg')"
    exit 1
fi

echo "✅ Access Token 获取成功"

# 步骤 4：上传 Opus 文件获取 file_key
echo "⏳ 步骤 4/5: 上传音频文件到飞书..."
UPLOAD_RESPONSE=$(curl -sL -X POST 'https://open.feishu.cn/open-apis/im/v1/files' \
  -H "Authorization: Bearer $TOKEN" \
  -F 'file_type=opus' \
  -F 'file_name=voice.opus' \
  -F 'duration=6000' \
  -F "file=@$TMP_OPUS")

FILE_KEY=$(echo "$UPLOAD_RESPONSE" | jq -r '.data.file_key')
UPLOAD_CODE=$(echo "$UPLOAD_RESPONSE" | jq -r '.code // 999')

if [ -z "$FILE_KEY" ] || [ "$FILE_KEY" = "null" ] || [ "$UPLOAD_CODE" != "0" ]; then
    echo "❌ 上传文件失败：$(echo "$UPLOAD_RESPONSE" | jq -r '.msg')"
    exit 1
fi

echo "✅ 文件上传成功 (file_key: $FILE_KEY)"

# 步骤 5：发送语音消息
echo "⏳ 步骤 5/5: 发送语音消息..."

# 如果没有指定 USER_ID，提示用户
if [ -z "$USER_ID" ]; then
    echo "⚠️  未指定接收者 USER_ID"
    echo "请设置 FEISHU_DEFAULT_USER_ID 环境变量或在命令中指定用户 ID"
    echo ""
    echo "用法示例:"
    echo "  $0 \"$TEXT\" \"$SPEAKER\" \"ou_xxxxxx\""
    exit 1
fi

SEND_RESPONSE=$(curl -sL -X POST 'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id' \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d "{
    \"receive_id\": \"$USER_ID\",
    \"msg_type\": \"audio\",
    \"content\": \"{\\\"file_key\\\":\\\"$FILE_KEY\\\"}\"
  }")

SEND_CODE=$(echo "$SEND_RESPONSE" | jq -r '.code // 999')

if [ "$SEND_CODE" != "0" ]; then
    echo "❌ 发送语音消息失败：$(echo "$SEND_RESPONSE" | jq -r '.msg')"
    exit 1
fi

MESSAGE_ID=$(echo "$SEND_RESPONSE" | jq -r '.data.message_id')
echo "✅ 语音消息发送成功！"
echo ""
echo "================"
echo "📬 消息 ID: $MESSAGE_ID"
echo "🎵 音色：$SPEAKER"
echo "👤 接收者：$USER_ID"
echo "================"
echo ""

exit 0
