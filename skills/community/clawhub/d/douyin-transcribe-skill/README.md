# 抖音视频智能助手 🎬🧠

一个 [OpenClaw](https://openclaw.ai) Skill，让你的 AI 助手能"看"抖音视频——转录、总结、讨论、归档。

## ✨ 效果

> 你：（发一个抖音链接）
>
> AI：
> 📹 **如何用AI做副业月入过万**
> 👤 张三说AI
>
> **要点总结：**
> 1. 选择一个垂直细分领域
> 2. 用AI工具做最小可行产品
> 3. 通过短视频引流测试市场
>
> **一句话概括：** 讲了AI时代个人副业的起步方法，核心是"小步快跑、快速验证"。
>
> 💡 逐字稿已保存。回复"看原文"查看，"存起来"归档到知识库。

### 五种模式

| 你说什么 | AI做什么 |
|---------|---------|
| 只发链接 | 🧠 AI总结要点（默认） |
| "转文字" | 📝 给完整逐字稿 |
| "总结一下" | 📋 详细总结+适用场景 |
| "存到知识库" | 📚 转录+总结+归档 |
| "你怎么看" | 💬 分析讨论+给建议 |

- ⚡ 3分钟视频 → **6秒**转完
- 💰 **完全免费**（Groq 免费 API）
- 🎯 中文优化，自动加标点分段
- 🧠 AI智能处理，不只是逐字稿

## 🚀 安装

### 1. 安装 ffmpeg

**Mac：** `brew install ffmpeg`

**Windows：** 从 [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) 下载 release full 版本，解压后将 `bin` 目录加入 PATH。

**Linux：** `sudo apt install ffmpeg`

### 2. 获取 Groq API Key（免费）

1. 打开 [console.groq.com](https://console.groq.com)
2. Google 或 GitHub 登录（不需要信用卡）
3. **API Keys** → **Create API Key** → 复制（`gsk_` 开头）

### 3. 配置

```bash
cd ~/.openclaw/workspace/skills/douyin-transcribe
cp .env.example .env
# 编辑 .env，填入 GROQ_API_KEY
```

### 4. 完成！

对你的 OpenClaw AI 发抖音链接就行。

## 🔧 工作原理

```
抖音链接 → 浏览器打开 → 提取DASH音频流（~1MB，不下载视频）
         → Groq Whisper large-v3 语音识别（免费，3秒）
         → Groq LLM 标点分段（免费，1秒）
         → AI 智能处理（总结/讨论/归档）
```

**为什么不用 yt-dlp？** 抖音反爬太严。通过 OpenClaw 浏览器直接提取音频流，100% 可靠。

**为什么用 Groq？** 免费 + 快（硬件加速，比 OpenAI 快 10 倍）。

## 📋 依赖

| 依赖 | 费用 | 用途 |
|------|------|------|
| ffmpeg | 免费 | 音频处理 |
| Groq API | 免费 | 语音识别 + 标点 |
| OpenClaw Browser | N/A | 打开抖音页面 |

## 🐛 常见问题

**Q: 支持多长的视频？**
A: 10 分钟以内没问题（Groq 限制 25MB 音频）。

**Q: 支持其他平台吗？**
A: 本地视频文件都支持。在线平台目前只优化了抖音。

**Q: 浏览器没登录抖音？**
A: 手动在 OpenClaw 浏览器里登录一次即可，状态会保持。

## 📜 License

MIT

## 🙏 致谢

- [OpenClaw](https://openclaw.ai) — AI Agent 平台
- [Groq](https://groq.com) — 免费高速 Whisper API
- [FFmpeg](https://ffmpeg.org) — 音频处理
