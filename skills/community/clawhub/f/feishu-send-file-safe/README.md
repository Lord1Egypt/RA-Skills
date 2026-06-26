# Feishu Send File Skill

Send files, images, voice messages, and videos via Feishu/Lark API. An OpenClaw skill with standalone scripts.

[中文文档](#中文文档) | English

## Features

- 📄 **File Upload** - PDF, DOC, XLS, and other documents
- 🖼️ **Image Upload** - JPG, PNG, GIF images
- 🎵 **Voice Messages** - OPUS, MP3 audio
- 🎬 **Video Upload** - MP4 with optional thumbnail
- 😀 **Stickers** - Emoji and image stickers
- 🎴 **Interactive Cards** - Markdown formatted cards
- 🔒 **Secure** - Environment variables or config file for credentials

## Quick Start

### 1. Install

```bash
cd ~/.openclaw/workspace/skills  # or your custom skills directory
git clone https://github.com/Rabbitmeaw/feishu-send-file.git
cd feishu-send-file
```

### 2. Configure

**Option 1: Environment Variables (Recommended)**

```bash
export FEISHU_APP_ID="cli_xxxxxxxxxxxxxxxx"
export FEISHU_APP_SECRET="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export FEISHU_RECEIVE_ID="ou_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

**Option 2: Config File**

```bash
cp config.json.example config.json
# Edit config.json with your credentials
```

### 3. Usage

```bash
# Send text
./scripts/send-message.sh text "Hello!"

# Send image
./scripts/send-message.sh image "/path/to/photo.png"

# Send file
./scripts/send-message.sh file "/path/to/document.pdf"

# Send audio (opus format)
./scripts/send-message.sh audio "/path/to/voice.opus"

# Send video
./scripts/send-message.sh video "/path/to/video.mp4"

# Send Markdown card
./scripts/send-message.sh card "**Bold** *Italic*"
```

## Security

⚠️ **Important Security Tips**

1. **Never commit config.json** - It contains your Feishu app credentials
2. **Use environment variables** - Recommended for production
3. **Protect app_secret** - Never share it with anyone
4. **config.json is in .gitignore** - Prevents accidental commits

## Getting Feishu Credentials

1. Log in to [Feishu Open Platform](https://open.feishu.cn/app)
2. Create a custom app
3. Get App ID and App Secret from "Credentials & Basic Info"
4. Add required permissions:
   - `im:chat:readonly`
   - `im:message:send_as_bot`
5. Get user/group Open ID

## License

MIT License - See [LICENSE](LICENSE) file

## Contributing

Issues and Pull Requests are welcome!

---

## 中文文档

### 功能特性

- 📄 **文件发送** - 支持 PDF、DOC、XLS 等各种文档格式
- 🖼️ **图片发送** - 支持 JPG、PNG、GIF 等图片格式
- 🎵 **语音发送** - 支持 OPUS、MP3 音频格式
- 🎬 **视频发送** - 支持 MP4 视频格式（可选封面）
- 😀 **表情包** - 支持 Emoji 和图片表情
- 🎴 **卡片消息** - 支持 Markdown 格式卡片
- 🔒 **安全设计** - 使用环境变量或配置文件管理凭证

### 快速开始

```bash
# 克隆到 OpenClaw skills 目录
cd ~/.openclaw/workspace/skills
git clone https://github.com/Rabbitmeaw/feishu-send-file.git
cd feishu-send-file

# 配置（环境变量方式）
export FEISHU_APP_ID="cli_xxxxxxxxxxxxxxxx"
export FEISHU_APP_SECRET="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export FEISHU_RECEIVE_ID="ou_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# 使用
./scripts/send-message.sh text "你好！"
./scripts/send-message.sh image "/path/to/photo.png"
```

详见 [SKILL.md](SKILL.md) 完整文档。
