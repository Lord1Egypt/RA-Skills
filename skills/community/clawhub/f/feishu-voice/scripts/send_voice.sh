#!/bin/bash
# 飞书语音消息发送脚本（使用 Coze TTS）
# 将文本转换为语音并发送到飞书

set -e

# 参数检查
TEXT="$1"
VOICE_PARAM="$2"
SPEED_PARAM="$3"
RECEIVER_PARAM="$4"

if [ -z "$TEXT" ]; then
  echo "❌ 错误：缺少文本参数"
  echo ""
  echo "用法: $0 <文本> [voice_id] [语速] [接收者]"
  echo ""
  echo "参数："
  echo "  文本    - 要转换为语音的文字（必需）"
  echo "  voice_id - Coze 音色 ID（默认 1）"
  echo "  语速    - 0.5-2.0（默认 1.0）"
  echo "  接收者  - 飞书 open_id（可选，自动选择应用）"
  echo ""
  echo "示例："
  echo "  $0 \"你好，这是一条语音消息\""
  echo "  $0 \"你好\" 2 1.2"
  exit 1
fi

# 根据接收者选择应用凭证
if [ -n "$RECEIVER_PARAM" ]; then
  RECEIVER="$RECEIVER_PARAM"
  # 如果接收者匹配应用 B，使用应用 B 的凭证
  if [ "$RECEIVER" = "$FEISHU_RECEIVER_B" ]; then
    APP_ID="${FEISHU_APP_ID_B}"
    APP_SECRET="${FEISHU_APP_SECRET_B}"
  else
    APP_ID="${FEISHU_APP_ID}"
    APP_SECRET="${FEISHU_APP_SECRET}"
  fi
else
  # 默认使用应用 A
  APP_ID="${FEISHU_APP_ID}"
  APP_SECRET="${FEISHU_APP_SECRET}"
  RECEIVER="${FEISHU_RECEIVER}"
fi

# 音色和语速
VOICE_ID="${VOICE_PARAM:-1}"
SPEED="${SPEED_PARAM:-1.0}"

# 显示任务信息
echo "🎤 飞书语音消息发送（Coze TTS）"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📝 文本: $TEXT"
echo "🎙️  Voice ID: $VOICE_ID"
echo "⚡ 语速: $SPEED"
echo "👤 接收者: ${RECEIVER:0:20}..."
echo ""

# 1. 获取飞书访问令牌
echo "🔑 获取飞书 token..."
TOKEN_RESPONSE=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d "{\"app_id\": \"$APP_ID\", \"app_secret\": \"$APP_SECRET\"}")

TOKEN=$(echo "$TOKEN_RESPONSE" | jq -r '.tenant_access_token')
CODE=$(echo "$TOKEN_RESPONSE" | jq -r '.code')

if [ "$CODE" != "0" ] || [ "$TOKEN" = "null" ] || [ -z "$TOKEN" ]; then
  echo "❌ 获取 token 失败"
  echo "错误信息：$TOKEN_RESPONSE"
  exit 1
fi
echo "✅ Token 获取成功 (有效期: $(echo "$TOKEN_RESPONSE" | jq -r '.expire')秒)"

# 2. 生成 MP3 音频（使用 coze-tts）
echo ""
echo "🎙️ 使用 Coze TTS 生成音频..."

# 获取脚本所在目录的父目录（技能根目录）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# 尝试多种方式找到 coze-tts 脚本
TTS_SCRIPT=""

# 方式1: 相对于当前技能的路径（同级目录）
if [ -f "$SKILL_DIR/../coze-tts/scripts/text_to_speech.sh" ]; then
  TTS_SCRIPT="$SKILL_DIR/../coze-tts/scripts/text_to_speech.sh"
# 方式2: 从环境变量获取工作区路径
elif [ -n "$OPENCLAW_WORKSPACE" ] && [ -f "$OPENCLAW_WORKSPACE/skills/coze-tts/scripts/text_to_speech.sh" ]; then
  TTS_SCRIPT="$OPENCLAW_WORKSPACE/skills/coze-tts/scripts/text_to_speech.sh"
# 方式3: 尝试常见的工作区路径
else
  for WORKSPACE in "$HOME/.openclaw/workspace" "$HOME/openclaw/workspace" "/opt/openclaw/workspace"; do
    if [ -f "$WORKSPACE/skills/coze-tts/scripts/text_to_speech.sh" ]; then
      TTS_SCRIPT="$WORKSPACE/skills/coze-tts/scripts/text_to_speech.sh"
      break
    fi
  done
fi

if [ -z "$TTS_SCRIPT" ] || [ ! -f "$TTS_SCRIPT" ]; then
  echo "❌ 错误：找不到 coze-tts 脚本"
  echo "   请确保 coze-tts 技能已安装"
  echo "   或设置 OPENCLAW_WORKSPACE 环境变量指向工作区目录"
  exit 1
fi

bash "$TTS_SCRIPT" "$TEXT" -o /tmp/feishu-voice-temp.mp3 -f mp3 -v "$VOICE_ID" > /dev/null 2>&1

if [ ! -f /tmp/feishu-voice-temp.mp3 ]; then
  echo "❌ TTS 生成失败"
  exit 1
fi
echo "✅ TTS 音频生成完成"

# 3. 应用语速调整（如果需要）
if [ "$SPEED" != "1.0" ] && [ "$SPEED" != "1" ]; then
  echo ""
  echo "🔄 调整语速为 ${SPEED}x..."
  ffmpeg -y -i /tmp/feishu-voice-temp.mp3 \
    -filter:a "atempo=$SPEED" \
    -c:a libmp3lame -q:a 2 \
    /tmp/feishu-voice-speed.mp3 > /dev/null 2>&1
  mv /tmp/feishu-voice-speed.mp3 /tmp/feishu-voice-temp.mp3
  echo "✅ 语速调整完成"
fi

# 4. 转换为 opus 格式
echo ""
echo "🔄 转换为 opus 格式..."
ffmpeg -y -i /tmp/feishu-voice-temp.mp3 \
  -c:a libopus \
  -b:a 24k \
  /tmp/feishu-voice.opus > /dev/null 2>&1

if [ ! -f /tmp/feishu-voice.opus ]; then
  echo "❌ 格式转换失败"
  exit 1
fi
echo "✅ 格式转换完成"

# 5. 读取音频时长并转换为毫秒
echo ""
echo "⏱️  读取音频时长..."
EXACT_DURATION=$(ffprobe -v error -show_entries format=duration \
  -of default=noprint_wrappers=1:nokey=1 /tmp/feishu-voice.opus)

if [ -z "$EXACT_DURATION" ]; then
  echo "❌ 无法读取时长"
  exit 1
fi

# 转换为毫秒（飞书 API 要求）
DURATION_MS=$(awk "BEGIN {printf \"%.0f\", $EXACT_DURATION * 1000}")

echo "✅ 时长: ${EXACT_DURATION}秒 (${DURATION_MS}毫秒)"

# 6. 上传文件到飞书（duration 用毫秒）
echo ""
echo "📤 上传到飞书服务器..."
UPLOAD_RESPONSE=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/files" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@/tmp/feishu-voice.opus" \
  -F "file_type=opus" \
  -F "file_name=voice.opus" \
  -F "duration=$DURATION_MS")

UPLOAD_CODE=$(echo "$UPLOAD_RESPONSE" | jq -r '.code')
if [ "$UPLOAD_CODE" != "0" ]; then
  echo "❌ 上传失败"
  echo "$UPLOAD_RESPONSE" | jq .
  exit 1
fi

FILE_KEY=$(echo "$UPLOAD_RESPONSE" | jq -r '.data.file_key')
echo "✅ 文件上传成功 (file_key: ${FILE_KEY:0:30}...)"

# 7. 发送音频消息（duration 用毫秒）
echo ""
echo "📨 发送音频消息..."
SEND_RESPONSE=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"receive_id\": \"$RECEIVER\",
    \"msg_type\": \"audio\",
    \"content\": \"{\\\"file_key\\\": \\\"$FILE_KEY\\\", \\\"duration\\\": $DURATION_MS}\"
  }")

SEND_CODE=$(echo "$SEND_RESPONSE" | jq -r '.code')
if [ "$SEND_CODE" != "0" ]; then
  echo "❌ 发送失败"
  echo "$SEND_RESPONSE" | jq .
  exit 1
fi

# 8. 清理临时文件
rm -f /tmp/feishu-voice-temp.mp3 /tmp/feishu-voice-speed.mp3 /tmp/feishu-voice.opus 2>/dev/null || true

# 9. 完成
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 语音消息发送成功！"
echo ""
echo "📊 统计信息："
echo "   • 文本长度: ${#TEXT} 字符"
DUR_SEC=$(awk "BEGIN {printf \"%.1f\", $DURATION_MS / 1000}")
echo "   • 音频时长: ${DUR_SEC} 秒"
echo "   • Voice ID: $VOICE_ID"
echo "   • 语速: $SPEED"
echo ""
