# 🔥 DouBao ATA Subtitle

豆包语音 ATA (Automatic Time Alignment) 自动字幕打轴 Skill 
本技能由OpenClaw构建
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://github.com/openclaw/openclaw)

## ✨ 功能特性

- 🎯 **自动打轴**：将音频 + 文本转换为带毫秒级时间轴的字幕
- 📝 **多格式支持**：输出 SRT 或 ASS 格式字幕
- 🔧 **灵活配置**：支持环境变量或配置文件两种鉴权方式
- 🧪 **演示模式**：无 API 密钥也可体验基本功能

## 📦 快速开始
[创建豆包语音应用](https://console.volcengine.com/speech/app)
自动字幕打轴应用，获取APP ID、	Access Token、Secret Key 有20小时试用
<img width="1107" height="761" alt="398d4eed-4abe-497e-96c0-9fd0adae4f39" src="https://github.com/user-attachments/assets/7dfabbe1-b1d7-44e7-b071-007641d0cbad" />

### 安装

```bash
# 方式 1: 克隆到 OpenClaw skills 目录
cd ~/.openclaw/workspace/skills
git clone https://github.com/BlackEight4752/volcengine-ata-subtitle.git

# 方式 2: 通过 ClawHub（待发布）
clawhub install volcengine-ata-subtitle
```

### 配置 API 密钥

**方式 A - 环境变量**：
```bash
export VOLC_ATA_APP_ID="your-app-id"
export VOLC_ATA_TOKEN="your-access-token"
export VOLC_ATA_API_BASE="https://openspeech.bytedance.com"
```

**方式 B - 配置文件** (`~/.volcengine_ata.conf`)：
```ini
[credentials]
appid = your-app-id
access_token = your-access-token
secret_key = your-secret-key

[api]
base_url = https://openspeech.bytedance.com
submit_path = /api/v1/vc/ata/submit
query_path = /api/v1/vc/ata/query
```

### 使用示例

```bash
# 基础用法：音频 + 文本 → SRT 字幕
python3 ~/.openclaw/workspace/skills/volcengine-ata-subtitle/volc_ata.py \
  --audio storage/audio.wav \
  --text storage/subtitle.txt \
  --output storage/subtitles/final.srt

# 输出 ASS 格式
python3 ~/.openclaw/workspace/skills/volcengine-ata-subtitle/volc_ata.py \
  --audio storage/audio.wav \
  --text storage/subtitle.txt \
  --output storage/subtitles/final.ass \
  --format ass
```

## 📋 输入要求

### 音频文件
- **格式**：WAV (PCM)
- **采样率**：16000 Hz (16kHz)
- **声道**：单声道
- **编码**：16-bit PCM

从视频提取：
```bash
ffmpeg -i input.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 audio.wav
```

### 文本文件
- **格式**：纯文本 (UTF-8)
- **结构**：每句一行
- **无标点**：ATA 会自动处理
- **无时间戳**：只需纯文本

示例：
```
主人闹钟没响睡过头了
我们俩轮流用鼻子拱他脸
他以为地震了抱着枕头就跑
```|

## 📁 文件结构

```
volcengine-ata-subtitle/
├── SKILL.md              # OpenClaw Skill 文档
├── volc_ata.py           # Python CLI 工具
├── _meta.json            # Skill 元数据
├── config.example.conf   # 配置示例
├── LICENSE               # MIT License
└── README.md             # 本文件
```

## 🔗 相关链接

- [OpenClaw 文档](https://github.com/openclaw/openclaw)
- [豆包语音快速入门]([https://www.volcengine.com/docs/4761/102177](https://www.volcengine.com/docs/6561/163043?lang=zh))

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🤝 贡献

欢迎提交 Issue 和 PR！

---

**Made with 🖤 by Double Dog Radio Project**
