---
name: douyin-transcribe
description: |
  抖音视频转文字。用户发抖音链接或视频文件，自动转录为带标点的中文文本。
  触发词：抖音、转文字、转录、视频转文本、douyin、transcribe
---

# 抖音视频转文字 🎬➡️📝

将抖音视频自动转录为带标点分段的中文文本。

用户只需要发一个抖音链接或视频文件，你来完成所有工作。

---

## 首次使用？先帮用户完成配置

当用户第一次触发这个 Skill 时，你需要先检查环境是否就绪。
按以下顺序检查，**缺什么就引导用户补什么**：

### 检查 1：.env 文件是否存在

检查 Skill 目录下是否有 `.env` 文件：
```
read: <skill目录>/.env
```

如果不存在，从 `.env.example` 复制一份：
```
exec: cp <skill目录>/.env.example <skill目录>/.env
```

### 检查 2：Groq API Key

读取 `.env`，检查 `GROQ_API_KEY` 是否已填写（不是 `gsk_your_key_here`）。

如果未填写，**告诉用户**：

> 需要一个免费的 Groq API Key 来做语音识别。获取步骤：
>
> 1. 打开 https://console.groq.com
> 2. 用 Google 或 GitHub 账号登录（不需要信用卡，完全免费）
> 3. 点左侧 **API Keys** → **Create API Key**
> 4. 名字随便填，点 Submit
> 5. 复制生成的 Key（以 `gsk_` 开头），发给我
>
> 拿到 Key 后发给我，我帮你配好。

用户发来 Key 后，更新 `.env` 文件中的 `GROQ_API_KEY=<用户的key>`。

### 检查 3：ffmpeg

运行以下命令检查 ffmpeg 是否安装：
```
exec: ffmpeg -version
```

如果报错（未找到命令），**告诉用户**：

> 还需要安装 ffmpeg（音频处理工具）：
>
> **Mac 用户：** 打开终端，运行 `brew install ffmpeg`
>
> **Windows 用户：**
> 1. 打开 https://www.gyan.dev/ffmpeg/builds/
> 2. 下载 "release full" 版本（.zip 文件）
> 3. 解压到 `C:\ffmpeg`
> 4. 把 `C:\ffmpeg\bin` 添加到系统环境变量 PATH
> 5. 重启终端，运行 `ffmpeg -version` 验证
>
> **Linux 用户：** 运行 `sudo apt install ffmpeg`
>
> 装好了告诉我！

### 检查通过后

告诉用户：

> ✅ 配置完成！以后你可以：
> - 直接发抖音链接给我，我自动转成文字
> - 发视频文件给我，我也能转
>
> 试试看？发个抖音链接过来吧！

---

## 使用方式 1：用户发来抖音链接

当用户发来包含 `douyin.com` 的链接时，按以下步骤操作：

### 步骤 1：启动浏览器

```
browser(action="start", profile="openclaw")
```

如果浏览器已经在运行，跳过此步。

### 步骤 2：打开抖音链接

```
browser(action="navigate", url="<用户发的链接>", profile="openclaw")
```

抖音短链接会自动跳转到完整页面。

### 步骤 3：等待视频播放，提取音频信息

等待 3-5 秒让视频开始播放，然后执行：

```
browser(action="act", kind="evaluate", profile="openclaw", fn=下方代码)
```

**提取代码：**
```javascript
() => {
  const entries = performance.getEntriesByType('resource');
  const audioEntry = entries.find(e => e.name.includes('media-audio'));
  const title = document.querySelector('h1')?.textContent?.trim() ||
                document.querySelector('[data-e2e="video-desc"]')?.textContent?.trim() ||
                document.title;
  const authorEl = document.querySelector('[data-e2e="video-account-link"]') ||
                   document.querySelector('.author-name');
  const author = authorEl?.textContent?.trim();
  return {
    audioUrl: audioEntry?.name || null,
    title: title || '未知标题',
    author: author || '未知作者'
  };
}
```

**如果 `audioUrl` 为 null**（视频还没开始播放），等 5 秒后再执行一次。
如果重试 2-3 次仍然为 null，可能需要用户先在浏览器中登录抖音网页版。

### 步骤 4：运行转录脚本

设置环境变量并调用脚本。注意 `<skill目录>` 替换为这个 SKILL.md 所在的实际目录路径。

**Windows PowerShell：**
```powershell
$env:DOUYIN_AUDIO_URL = "<步骤3拿到的audioUrl>"
$env:DOUYIN_TITLE = "<步骤3拿到的title>"
$env:DOUYIN_AUTHOR = "<步骤3拿到的author>"
cd "<skill目录>"
node scripts/transcribe.js "<用户的原始链接>"
```

**Linux/Mac Bash：**
```bash
cd "<skill目录>"
DOUYIN_AUDIO_URL="<audioUrl>" \
DOUYIN_TITLE="<title>" \
DOUYIN_AUTHOR="<author>" \
node scripts/transcribe.js "<用户的原始链接>"
```

设置 timeout 为 120 秒（长视频可能需要更多时间）。

### 步骤 5：返回结果

脚本成功后，读取 `douyin-transcripts/` 目录下最新的 `.md` 文件，把**文字内容**发给用户。

不需要发整个 Markdown 文件头，只发标题和正文部分即可。格式示例：

> **转录完成** ✅
>
> 📹 标题：xxx
> 👤 博主：xxx
> ⏱️ 耗时：x秒
>
> ---
> （正文内容）

---

## 使用方式 2：用户发来视频文件

当用户通过飞书/Telegram/Discord 等发来视频文件时：

### 步骤 1：保存文件到本地

如果平台提供了文件路径，直接使用。如果需要下载（如飞书），保存到 `<skill目录>/temp/` 下。

### 步骤 2：运行脚本

```bash
cd "<skill目录>"
node scripts/transcribe.js "<视频文件的完整路径>"
```

### 步骤 3：返回结果

同上，读取最新的 `.md` 文件，发正文给用户。

---

## 使用方式 3：用户发来文字描述的链接

用户有时会发类似这样的分享文本：

> 7.94 复制打开抖音，看看【xxx的作品】标题内容 https://v.douyin.com/xxxxx/ 06/13

从中提取 `https://v.douyin.com/xxxxx/` 部分，然后按方式 1 处理。

---

## 技术说明

### 工作原理

```
抖音链接 → 浏览器打开页面 → 从 DASH 流提取音频 URL（不下载视频，只下音频）
         → ffmpeg 下载音频流（~1MB，1秒）
         → Groq Whisper large-v3 语音识别（免费，3秒）
         → Groq LLM 标点分段（免费，1秒）
         → 保存 Markdown 文件
```

### 为什么这么做

- **不用 yt-dlp**：抖音反爬严格，yt-dlp 需要 cookies 且经常失败
- **只下音频**：不需要下载整个视频，音频只有 ~1MB，比视频小 20-50 倍
- **用 Groq 不用 OpenAI**：Groq 完全免费且速度快 10 倍

### 依赖

| 依赖 | 必须？ | 费用 | 用途 |
|------|--------|------|------|
| Node.js | ✅ | 免费 | 运行脚本（OpenClaw 自带） |
| ffmpeg | ✅ | 免费 | 音频处理 |
| Groq API Key | ✅ | 免费 | 语音识别 + 标点分段 |
| OpenClaw Browser | 推荐 | N/A | 打开抖音页面提取音频 |

### 配置文件 (.env)

```env
# 必填
GROQ_API_KEY=gsk_xxxxx

# 可选（如果想用 OpenAI 替代 Groq）
# STT_PROVIDER=openai
# OPENAI_API_KEY=sk-xxxxx

# 可选（自定义路径）
# FFMPEG_PATH=/usr/local/bin/ffmpeg
# OUTPUT_DIR=./douyin-transcripts
```

### 文件结构

```
douyin-transcribe/
├── SKILL.md              ← 你正在读的操作指南
├── README.md             ← 给人看的说明
├── _meta.json            ← Skill 元数据
├── .env.example          ← 配置模板
├── .env                  ← 用户的配置（不提交 git）
├── .gitignore
├── scripts/
│   └── transcribe.js     ← 核心脚本
├── douyin-transcripts/   ← 输出目录（自动创建）
└── temp/                 ← 临时文件（自动清理）
```

---

## 故障排查

| 问题 | 原因 | 解决 |
|------|------|------|
| `audioUrl` 为 null | 视频没开始播放 | 等几秒重试；或用户需要登录抖音网页版 |
| ffmpeg 未找到 | 没装或不在 PATH | 引导用户安装 ffmpeg |
| Groq API 429 错误 | 频率限制 | 等 1 分钟再试 |
| 音频文件过大 >25MB | 视频太长 | 建议用户发短一点的视频 |
| 浏览器打开后是登录页 | 未登录抖音 | 让用户在浏览器中手动登录一次即可 |
