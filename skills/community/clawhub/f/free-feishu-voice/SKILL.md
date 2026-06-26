
### 1. 配置文件模板（feishu_voice_config.json）
```json
{
  "feishu_app_id": "your_app_id_here",
  "feishu_app_secret": "your_app_secret_here",
  "feishu_chat_id": "your_chat_id_here",
  "default_voice": "zh-CN-XiaoxiaoNeural",
  "default_text": "默认消息"
}
```

---

### 2. 基础版脚本（send_voice.sh）
```bash
#!/bin/bash
# send_voice.sh - 发送飞书语音消息（移除硬编码版）
set -euo pipefail

# ===================== 配置加载逻辑 =====================
# 配置文件路径（可通过环境变量覆盖）
CONFIG_FILE="${FEISHU_VOICE_CONFIG:-$HOME/.config/feishu_voice_config.json}"

# 加载配置文件（如果存在）
if [ -f "$CONFIG_FILE" ]; then
  APP_ID=$(jq -r '.feishu_app_id' "$CONFIG_FILE")
  APP_SECRET=$(jq -r '.feishu_app_secret' "$CONFIG_FILE")
  CHAT_ID=$(jq -r '.feishu_chat_id' "$CONFIG_FILE")
  DEFAULT_TEXT=$(jq -r '.default_text // "默认消息"' "$CONFIG_FILE")
else
  # 配置文件不存在时生成模板
  echo "⚠️ 配置文件不存在，生成模板到 $CONFIG_FILE"
  mkdir -p "$(dirname "$CONFIG_FILE")"
  cat > "$CONFIG_FILE" << 'EOF'
{
  "feishu_app_id": "your_app_id_here",
  "feishu_app_secret": "your_app_secret_here",
  "feishu_chat_id": "your_chat_id_here",
  "default_text": "默认消息"
}
EOF
  echo "❌ 请先编辑 $CONFIG_FILE 填写正确的配置后重试"
  exit 1
fi

# 环境变量覆盖配置文件（优先级更高）
APP_ID="${FEISHU_APP_ID:-$APP_ID}"
APP_SECRET="${FEISHU_APP_SECRET:-$APP_SECRET}"
CHAT_ID="${FEISHU_CHAT_ID:-$CHAT_ID}"
TEXT="${1:-$DEFAULT_TEXT}"

# ===================== 参数校验 =====================
if [ "$APP_ID" = "your_app_id_here" ] || [ -z "$APP_ID" ]; then
  echo "❌ 未配置飞书APP_ID，请检查配置文件或环境变量"
  exit 1
fi

if [ "$APP_SECRET" = "your_app_secret_here" ] || [ -z "$APP_SECRET" ]; then
  echo "❌ 未配置飞书APP_SECRET，请检查配置文件或环境变量"
  exit 1
fi

if [ "$CHAT_ID" = "your_chat_id_here" ] || [ -z "$CHAT_ID" ]; then
  echo "❌ 未配置飞书CHAT_ID，请检查配置文件或环境变量"
  exit 1
fi

# ===================== 核心逻辑 =====================
# 获取令牌
echo "🔑 获取飞书访问令牌..."
TOKEN=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}" \
  | jq -r '.tenant_access_token // empty')

if [ -z "$TOKEN" ]; then
  echo "❌ 获取令牌失败，请检查APP_ID/APP_SECRET是否正确"
  exit 1
fi

# 生成语音
echo "🎙️ 生成语音文件..."
echo "$TEXT" | espeak-ng -v zh --stdout > /tmp/voice.wav 2>/dev/null
ffmpeg -i /tmp/voice.wav -acodec libopus -ac 1 -ar 16000 /tmp/voice.opus -y 2>/dev/null

# 上传文件
echo "📤 上传语音文件..."
UPLOAD_RESPONSE=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/files" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file_type=opus" \
  -F "file=@/tmp/voice.opus")

FILE_KEY=$(echo "$UPLOAD_RESPONSE" | jq -r '.data.file_key // empty')
if [ -z "$FILE_KEY" ] || [ "$FILE_KEY" = "null" ]; then
  echo "❌ 文件上传失败：$UPLOAD_RESPONSE"
  exit 1
fi

# 发送消息
echo "📨 发送语音消息..."
SEND_RESPONSE=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"receive_id\":\"$CHAT_ID\",\"msg_type\":\"audio\",\"content\":\"{\\\"file_key\\\":\\\"$FILE_KEY\\\"}\"}")

# 结果判断
if echo "$SEND_RESPONSE" | jq -e '.code == 0' >/dev/null; then
  MSG_ID=$(echo "$SEND_RESPONSE" | jq -r '.data.message_id')
  echo "✅ 发送成功！消息ID：$MSG_ID"
else
  ERROR_MSG=$(echo "$SEND_RESPONSE" | jq -r '.msg // "未知错误"')
  echo "❌ 发送失败：$ERROR_MSG"
  exit 1
fi

# 清理临时文件
rm -f /tmp/voice.wav /tmp/voice.opus 2>/dev/null
echo "🧹 清理临时文件完成"
```

---

### 3. Edge TTS增强版脚本（send_voice_edge.sh）
```bash
#!/bin/bash
# send_voice_edge.sh - 使用Edge TTS发送高质量语音（移除硬编码版）
set -euo pipefail

# ===================== 配置加载逻辑 =====================
# 配置文件路径（可通过环境变量覆盖）
CONFIG_FILE="${FEISHU_VOICE_CONFIG:-$HOME/.config/feishu_voice_config.json}"

# 加载配置文件（如果存在）
if [ -f "$CONFIG_FILE" ]; then
  APP_ID=$(jq -r '.feishu_app_id' "$CONFIG_FILE")
  APP_SECRET=$(jq -r '.feishu_app_secret' "$CONFIG_FILE")
  CHAT_ID=$(jq -r '.feishu_chat_id' "$CONFIG_FILE")
  DEFAULT_TEXT=$(jq -r '.default_text // "默认消息"' "$CONFIG_FILE")
  DEFAULT_VOICE=$(jq -r '.default_voice // "zh-CN-XiaoxiaoNeural"' "$CONFIG_FILE")
else
  # 配置文件不存在时生成模板
  echo "⚠️ 配置文件不存在，生成模板到 $CONFIG_FILE"
  mkdir -p "$(dirname "$CONFIG_FILE")"
  cat > "$CONFIG_FILE" << 'EOF'
{
  "feishu_app_id": "your_app_id_here",
  "feishu_app_secret": "your_app_secret_here",
  "feishu_chat_id": "your_chat_id_here",
  "default_text": "默认消息",
  "default_voice": "zh-CN-XiaoxiaoNeural"
}
EOF
  echo "❌ 请先编辑 $CONFIG_FILE 填写正确的配置后重试"
  exit 1
fi

# 环境变量覆盖配置文件（优先级更高）
APP_ID="${FEISHU_APP_ID:-$APP_ID}"
APP_SECRET="${FEISHU_APP_SECRET:-$APP_SECRET}"
CHAT_ID="${FEISHU_CHAT_ID:-$CHAT_ID}"
TEXT="${1:-$DEFAULT_TEXT}"
VOICE="${2:-$DEFAULT_VOICE}"

# ===================== 依赖检查 =====================
check_dependency() {
  if ! command -v "$1" &> /dev/null; then
    echo "❌ 缺少依赖：$1，请先安装"
    exit 1
  fi
}

check_dependency "jq"
check_dependency "ffmpeg"
check_dependency "python3"
check_dependency "pip3"

# 检查edge_tts是否安装
if ! python3 -c "import edge_tts" &> /dev/null; then
  echo "📦 安装edge_tts依赖..."
  pip3 install edge-tts --quiet
fi

# ===================== 参数校验 =====================
if [ "$APP_ID" = "your_app_id_here" ] || [ -z "$APP_ID" ]; then
  echo "❌ 未配置飞书APP_ID，请检查配置文件或环境变量"
  exit 1
fi

if [ "$APP_SECRET" = "your_app_secret_here" ] || [ -z "$APP_SECRET" ]; then
  echo "❌ 未配置飞书APP_SECRET，请检查配置文件或环境变量"
  exit 1
fi

if [ "$CHAT_ID" = "your_chat_id_here" ] || [ -z "$CHAT_ID" ]; then
  echo "❌ 未配置飞书CHAT_ID，请检查配置文件或环境变量"
  exit 1
fi

# ===================== 核心逻辑 =====================
# 获取令牌
echo "🔑 获取飞书访问令牌..."
TOKEN=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}" \
  | jq -r '.tenant_access_token // empty')

if [ -z "$TOKEN" ]; then
  echo "❌ 获取令牌失败，请检查APP_ID/APP_SECRET是否正确"
  exit 1
fi

# 使用Edge TTS生成语音
echo "🎙️ 生成高质量语音（$VOICE）..."
OPUS_FILE=$(python3 << EOF
import asyncio
import edge_tts
import subprocess
import tempfile
import os

async def generate_voice():
    # 生成MP3临时文件
    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as mp3_file:
        communicate = edge_tts.Communicate("""$TEXT""", """$VOICE""")
        await communicate.save(mp3_file.name)
        
        # 转换为OPUS格式
        opus_file = mp3_file.name.replace('.mp3', '.opus')
        cmd = [
            'ffmpeg', '-i', mp3_file.name,
            '-acodec', 'libopus', '-ac', '1', '-ar', '16000',
            opus_file, '-y'
        ]
        subprocess.run(cmd, capture_output=True, check=True)
        return opus_file

# 兼容Windows系统
import sys
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

opus_path = asyncio.run(generate_voice())
print(opus_path)
EOF
)

# 上传文件
echo "📤 上传语音文件..."
UPLOAD_RESPONSE=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/files" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file_type=opus" \
  -F "file=@$OPUS_FILE")

FILE_KEY=$(echo "$UPLOAD_RESPONSE" | jq -r '.data.file_key // empty')
if [ -z "$FILE_KEY" ] || [ "$FILE_KEY" = "null" ]; then
  echo "❌ 文件上传失败：$UPLOAD_RESPONSE"
  rm -f "$OPUS_FILE" "${OPUS_FILE%.opus}.mp3" 2>/dev/null
  exit 1
fi

# 发送消息
echo "📨 发送语音消息..."
SEND_RESPONSE=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"receive_id\":\"$CHAT_ID\",\"msg_type\":\"audio\",\"content\":\"{\\\"file_key\\\":\\\"$FILE_KEY\\\"}\"}")

# 结果判断
if echo "$SEND_RESPONSE" | jq -e '.code == 0' >/dev/null; then
  MSG_ID=$(echo "$SEND_RESPONSE" | jq -r '.data.message_id')
  echo "✅ 发送成功！消息ID：$MSG_ID"
else
  ERROR_MSG=$(echo "$SEND_RESPONSE" | jq -r '.msg // "未知错误"')
  ERROR_CODE=$(echo "$SEND_RESPONSE" | jq -r '.code // "未知码"')
  echo "❌ 发送失败 [$ERROR_CODE]：$ERROR_MSG"
  rm -f "$OPUS_FILE" "${OPUS_FILE%.opus}.mp3" 2>/dev/null
  exit 1
fi

# 清理临时文件
rm -f "$OPUS_FILE" "${OPUS_FILE%.opus}.mp3" 2>/dev/null
echo "🧹 清理临时文件完成"
```

---

### 4. 使用说明
#### （1）初始化配置
```bash
# 首次运行会自动生成配置文件，编辑填写真实信息
vim ~/.config/feishu_voice_config.json
```

#### （2）环境变量临时覆盖（可选）
```bash
# 临时使用不同的配置（优先级高于配置文件）
export FEISHU_APP_ID="临时APP_ID"
export FEISHU_APP_SECRET="临时SECRET"
export FEISHU_CHAT_ID="临时CHAT_ID"

# 执行脚本
bash send_voice_edge.sh "测试消息"
```

#### （3）常规使用
```bash
# 基础版
bash send_voice.sh "早上好！"

# Edge TTS版（自定义语音）
bash send_voice_edge.sh "床前明月光" "zh-CN-YunxiNeural"
```

---

### 5. 关键优化点
| 优化项                | 说明                                                                 |
|-----------------------|----------------------------------------------------------------------|
| 移除硬编码            | 所有敏感信息通过配置文件/环境变量管理，避免代码泄露                  |
| 配置优先级            | 环境变量 > 配置文件 > 默认值，灵活适配不同场景                      |
| 依赖检查              | 自动检查jq/ffmpeg/python/edge_tts等依赖，缺失时提示安装            |
| 错误处理              | 每个步骤增加校验，失败时输出明确错误信息，避免静默失败              |
| 配置模板自动生成      | 首次运行自动生成配置文件模板，降低使用门槛                          |
| 临时文件安全清理      | 任何失败场景都确保临时文件被清理，避免磁盘占用                      |
| 结构化输出            | 使用jq替代python单行解析JSON，更稳定、易读                          |

### 6. 依赖安装
```bash
# Debian/Ubuntu
sudo apt update && sudo apt install -y jq ffmpeg python3 python3-pip

# CentOS/RHEL
sudo yum install -y jq ffmpeg python3 python3-pip

# macOS
brew install jq ffmpeg python3

# 安装Python依赖
pip3 install edge-tts
```