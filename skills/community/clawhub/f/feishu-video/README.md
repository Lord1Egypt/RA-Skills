# Feishu Audio Message Skill

[English](#english) | [中文](#中文)

---

## English

A skill for sending **voice messages** (not file attachments) to Feishu/Lark users via the Open API.

### Features

- 🎤 Send actual voice messages, not file attachments
- 🔄 Convert audio files (MP3, WAV, etc.) to OPUS format
- 📱 Support sending to users or group chats
- 🛠️ CLI tool with full argument parsing

### Requirements

- **Node.js 18+**
- **ffmpeg** - For audio conversion
- **Feishu App** with Bot capability enabled

### Installation

```bash
# Install ffmpeg (macOS)
brew install ffmpeg

# Install ffmpeg (Linux)
apt install ffmpeg
```

### Quick Start

```bash
# 1. Convert audio to OPUS format
./scripts/convert-audio.sh voice.mp3

# 2. Send voice message
node scripts/send-voice.mjs \
  --app-id "cli_xxx" \
  --app-secret "xxx" \
  --user-id "ou_xxx" \
  --audio-file "voice.opus" \
  --duration 3480
```

### Send Video Messages

```bash
# Send a video message
node scripts/send-video.mjs \
  --app-id "cli_xxx" \
  --app-secret "xxx" \
  --user-id "ou_xxx" \
  --video-file "video.mp4"

# Split large video and set segment length
node scripts/send-video.mjs \
  --user-id "ou_xxx" \
  --video-file "video.mp4" \
  --max-size-mb 25 \
  --segment-seconds 8
```

### Using in OpenClaw

This skill can be integrated into [OpenClaw](https://github.com/anthropics/claw) to enable Claude to send voice messages.

#### 1. Add as Plugin

Copy the skill folder to your OpenClaw plugins directory or reference it in your configuration:

```yaml
skills:
  - path: ./feishu-audio
```

#### 2. Configure Credentials

Set environment variables in your OpenClaw environment:

```bash
export FEISHU_APP_ID="cli_xxx"
export FEISHU_APP_SECRET="xxx"
```

#### 3. Use with Claude

Once configured, Claude can use this skill to:

- Convert audio files to Feishu-compatible format
- Upload and send voice messages to users
- Respond to voice-related requests

**Example prompts:**
- "Send this MP3 file as a voice message to user ou_xxx"
- "Convert audio.wav to Feishu voice format and send it"

### API Endpoints Used

| Endpoint | Description |
|----------|-------------|
| `/auth/v3/tenant_access_token/internal` | Get access token |
| `/im/v1/files` | Upload audio file |
| `/im/v1/messages` | Send voice message |

### Troubleshooting

| Error | Solution |
|-------|----------|
| `file type not support` | Audio must be OPUS format |
| `duration is required` | Provide duration in milliseconds |
| `permission denied` | Enable messaging scope in app |

---

## 中文

通过飞书开放 API 发送**语音消息**（不是文件附件）的技能。

### 功能特点

- 🎤 发送真正的语音消息，而不是文件附件
- 🔄 将音频文件（MP3、WAV 等）转换为 OPUS 格式
- 📱 支持发送给用户或群聊
- 🛠️ 完整参数解析的命令行工具

### 依赖要求

- **Node.js 18+**
- **ffmpeg** - 用于音频转换
- **飞书应用** - 需启用机器人能力

### 安装

```bash
# 安装 ffmpeg (macOS)
brew install ffmpeg

# 安装 ffmpeg (Linux)
apt install ffmpeg
```

### 快速开始

```bash
# 1. 将音频转换为 OPUS 格式
./scripts/convert-audio.sh voice.mp3

# 2. 发送语音消息
node scripts/send-voice.mjs \
  --app-id "cli_xxx" \
  --app-secret "xxx" \
  --user-id "ou_xxx" \
  --audio-file "voice.opus" \
  --duration 3480
```

### 发送视频消息

```bash
# 发送视频消息
node scripts/send-video.mjs \
  --app-id "cli_xxx" \
  --app-secret "xxx" \
  --user-id "ou_xxx" \
  --video-file "video.mp4"

# 大文件自动切片并设置分片时长
node scripts/send-video.mjs \
  --user-id "ou_xxx" \
  --video-file "video.mp4" \
  --max-size-mb 25 \
  --segment-seconds 8
```

### 在 OpenClaw 中使用

此技能可以集成到 [OpenClaw](https://github.com/anthropics/claw) 中，让 Claude 能够发送语音消息。

#### 1. 添加为插件

将技能文件夹复制到 OpenClaw 插件目录，或在配置中引用：

```yaml
skills:
  - path: ./feishu-audio
```

#### 2. 配置凭据

在 OpenClaw 环境中设置环境变量：

```bash
export FEISHU_APP_ID="cli_xxx"
export FEISHU_APP_SECRET="xxx"
```

#### 3. 与 Claude 配合使用

配置完成后，Claude 可以使用此技能：

- 将音频文件转换为飞书兼容格式
- 上传并发送语音消息给用户
- 响应语音相关的请求

**示例提示词：**
- "将这个 MP3 文件作为语音消息发送给用户 ou_xxx"
- "将 audio.wav 转换为飞书语音格式并发送"

### 使用的 API 端点

| 端点 | 说明 |
|------|------|
| `/auth/v3/tenant_access_token/internal` | 获取访问令牌 |
| `/im/v1/files` | 上传音频文件 |
| `/im/v1/messages` | 发送语音消息 |

### 故障排除

| 错误 | 解决方案 |
|------|----------|
| `file type not support` | 音频必须是 OPUS 格式 |
| `duration is required` | 需要提供毫秒单位的时长 |
| `permission denied` | 在应用中启用消息权限 |

---

## License

MIT
