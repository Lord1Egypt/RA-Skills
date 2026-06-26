# 抖音视频转文字 🎬➡️📝

一个 [OpenClaw](https://openclaw.ai) Skill，让你的 AI 助手能把抖音视频自动转成文字。

## ✨ 效果

> 你：（发一个抖音链接）
>
> AI：转录完成！以下是视频内容：
>
> 大家好，我是xxx，今天给大家分享一个关于……

- ⚡ 3分钟视频 → **6秒**转完（音频提取 + 语音识别 + 标点分段）
- 💰 **完全免费**（使用 Groq 免费 API）
- 🎯 支持中文，自动加标点和分段
- 📝 输出 Markdown 文件，方便存入知识库

## 🚀 安装

### 1. 安装 ffmpeg（音频处理）

**Windows：**
从 [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) 下载 release full 版本，解压后将 `bin` 目录加入系统 PATH。

**Mac：**
```bash
brew install ffmpeg
```

**Linux：**
```bash
sudo apt install ffmpeg   # Debian/Ubuntu
sudo yum install ffmpeg   # CentOS/RHEL
```

验证安装：
```bash
ffmpeg -version
```

### 2. 获取 Groq API Key（免费）

1. 打开 [console.groq.com](https://console.groq.com)
2. 用 Google 或 GitHub 登录（不需要信用卡）
3. 点击 **API Keys** → **Create API Key**
4. 填个名字（如 `douyin`），点 Submit
5. 复制生成的 Key（以 `gsk_` 开头）

### 3. 配置

```bash
cd ~/.openclaw/workspace/skills/douyin-transcribe
cp .env.example .env
```

编辑 `.env`，填入你的 Groq API Key：
```env
GROQ_API_KEY=gsk_你的key
```

### 4. 完成！

在任何 OpenClaw 对话中发送抖音链接，AI 会自动识别并转录。

## 📖 使用方式

### 发抖音链接（最简单）

直接把抖音分享链接发给你的 OpenClaw AI：

```
https://v.douyin.com/xxxxx
```

AI 会自动：打开链接 → 提取音频 → 转文字 → 加标点 → 返回结果。

### 发视频文件

也可以直接发视频文件（MP4、MOV 等），AI 会提取音频并转录。

### 命令行使用

```bash
# 转录本地视频
node scripts/transcribe.js "/path/to/video.mp4"

# 通过环境变量传入音频 URL（由 AI agent 调用）
DOUYIN_AUDIO_URL="https://..." DOUYIN_TITLE="标题" node scripts/transcribe.js "https://v.douyin.com/xxx"
```

## 🔧 工作原理

```
抖音链接 → 浏览器打开页面 → 从 DASH 流提取音频 URL
         → ffmpeg 下载音频（~1MB）
         → Groq Whisper large-v3 语音识别（免费，3秒完成）
         → Groq LLM 添加标点和分段（免费，1秒完成）
         → 输出 Markdown 文件
```

**为什么不用 yt-dlp？**

抖音反爬非常严格，yt-dlp 需要 fresh cookies 且经常失败。我们的方案通过 OpenClaw 浏览器直接打开页面（复用已登录的会话），从播放中的视频提取音频流 URL，100% 可靠。而且只下载音频不下载视频，更快更省流量。

**为什么用 Groq？**

Groq 提供免费的 Whisper large-v3 语音识别和 LLM 推理，速度极快（硬件加速），日常使用完全免费。

## 📋 依赖

| 依赖 | 用途 | 必须？ | 费用 |
|------|------|--------|------|
| ffmpeg | 音频处理 | ✅ 是 | 免费开源 |
| Groq API | 语音识别 + 标点 | ✅ 是 | 免费 |
| OpenClaw Browser | 打开抖音页面 | 推荐 | N/A |
| yt-dlp | 备选下载方式 | ❌ 可选 | 免费开源 |

## 🐛 常见问题

**Q: 转录结果有错别字怎么办？**
A: Whisper 对中文的识别准确率约 95%，专有名词（如 OpenClaw → "open call"）可能识别不准。这是语音识别的固有局限，不影响整体可读性。

**Q: 支持多长的视频？**
A: Groq Whisper API 限制音频 25MB。一般 10 分钟以内的视频没问题。超长视频建议裁剪后分段转录。

**Q: 支持其他平台吗？**
A: 目前针对抖音优化。本地视频文件（任何平台下载的）都支持。

**Q: 浏览器没有登录抖音怎么办？**
A: OpenClaw 浏览器打开抖音网页版后，手动登录一次即可（登录状态会保持）。或者用本地文件模式，不需要浏览器。

## 📜 License

MIT

## 🙏 致谢

- [OpenClaw](https://openclaw.ai) — AI Agent 平台
- [Groq](https://groq.com) — 免费高速 Whisper API
- [FFmpeg](https://ffmpeg.org) — 音频处理
