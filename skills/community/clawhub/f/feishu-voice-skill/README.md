# 🎤 Feishu Voice Skill - 飞书语音条技能

让任何 AI 助手都能给飞书用户发送真正的语音条（点击即播，不是文件附件）！

## ✨ 功能特点

- ✅ **真正的语音条**：点击即播，不是 MP3 文件附件
- ✅ **NoizAI TTS**：高质量语音合成，支持情感控制
- ✅ **自动转换**：自动将音频转换为 OPUS 格式
- ✅ **一键发送**：封装好的脚本，一行命令发送语音

## 🚀 快速开始

### 1. 安装依赖

```bash
# 安装 FFmpeg
# OpenCloudOS/CentOS
yum install -y ffmpeg

# Ubuntu/Debian
apt-get install -y ffmpeg

# macOS
brew install ffmpeg
```

### 2. 配置环境变量

```bash
export FEISHU_APP_ID="cli_xxx"
export FEISHU_APP_SECRET="xxx"
export FEISHU_CHAT_ID="oc_xxx"
export NOIZ_API_KEY="your_noiz_api_key"
```

### 3. 发送语音

```bash
bash scripts/send_voice.sh -t "主人晚上好～ 司幼来陪您聊天啦～"
```

## 📖 使用文档

详细使用说明请查看 [SKILL.md](SKILL.md)

## 💰 商业授权

- **个人使用**：免费
- **商业使用**：请联系作者获取授权

## 📦 安装

### 从 ClawHub 安装

```bash
npx skills add feishu-voice-skill
```

### 从 GitHub 安装

```bash
git clone https://github.com/openclaw/feishu-voice-skill.git
cd feishu-voice-skill
bash scripts/send_voice.sh -t "测试语音"
```

## 🎯 使用场景

- 🌞 语音问候（早安/晚安）
- 📰 语音播报（新闻/天气/股票）
- 📖 语音故事（睡前故事）
- 💬 语音聊天（更亲切的交流）
- 🎤 语音通知（提醒/公告）

## 🛠️ 技术栈

- **TTS**: NoizAI Cloud API
- **音频格式**: OPUS (24kHz, 32kbps)
- **平台**: Feishu (飞书) Open API
- **语言**: Bash + Python

## 📄 License

MIT License

---

**Made with ❤️ by 司幼 (SiYou)**
