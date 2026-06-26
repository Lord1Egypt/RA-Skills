---
name: douyin-to-obsidian
version: 1.0.1
description: |
  将抖音视频内容保存到 Obsidian 笔记。自动转录视频、AI 摘要结构化、写入 Obsidian。
  触发词：抖音保存到笔记、抖音存obsidian、douyin to obsidian、抖音笔记、保存抖音、
  记录抖音、抖音内容存档、视频笔记、抖音转笔记。
  当用户发送抖音链接（douyin.com 或 v.douyin.com）并要求保存/记录时触发。
---

# 抖音 → Obsidian 笔记

将抖音视频/图文内容自动转录、摘要、结构化后存入 Obsidian。

---

## 配置

配置文件：`<skill目录>/config.json`

```json
{
  "vault": "你的Obsidian仓库名",
  "folder": "抖音笔记",
  "groqApiKey": "gsk_xxx"
}
```

`groqApiKey` — Groq API Key（免费，用于 Whisper 语音转文字）。获取：https://console.groq.com

### 首次使用检查

读取 `<skill目录>/config.json`。如果不存在或字段为空，询问用户：

1. **Obsidian 仓库名**（vault name）— 打开 Obsidian 后在左上角看到的名字
2. **目标文件夹** — 笔记存放的文件夹名（如 `抖音笔记`、`Clippings` 等）

拿到后写入 config.json，后续不再询问。

---

## 依赖

- **Groq API Key** — 配置在本 skill 的 `config.json` 中（Whisper 转录）
- **agent-browser** — 浏览器自动化（提取抖音页面音频流）
- **ffmpeg** — 音频格式转换
- **Obsidian CLI** — 写入笔记

首次使用前检查上述依赖是否就绪。

---

## 工作流程

### 收到抖音链接后

#### 步骤 1：提取音频并转录

**1a. 打开页面**
```bash
agent-browser open "<用户发的抖音链接>"
```

**1b. 提取音频 URL 和标题**
```bash
agent-browser eval 'performance.getEntriesByType("resource").find(e => e.name.includes("media-audio-und-mp4a"))?.name'
agent-browser eval 'document.querySelector("h1")?.textContent?.trim()'
```

**1c. 下载音频流**

抖音使用 DASH 分流，视频和音频分开。用 curl 下载（不能用 ffmpeg 直接抓流）：
```bash
curl -L -H "Referer: https://www.douyin.com/" -o /tmp/douyin_audio_raw.m4a "<audioUrl>"
```

**1d. 转换格式并转录**
```bash
ffmpeg -y -i /tmp/douyin_audio_raw.m4a -vn -ar 16000 -ac 1 -c:a libmp3lame -q:a 2 /tmp/douyin_audio.mp3
```

直接调用 Groq Whisper API（不走 transcribe.js，避免脚本内部路径冲突）：
```bash
GROQ_API_KEY=$(python3 -c "import json; print(json.load(open('<skill目录>/config.json'))['groqApiKey'])")
curl -s https://api.groq.com/openai/v1/audio/transcriptions \
  -H "Authorization: Bearer $GROQ_API_KEY" \
  -F file="@/tmp/douyin_audio.mp3" \
  -F model="whisper-large-v3" \
  -F language="zh" \
  -F response_format="verbose_json"
```

**1e. 清理**
```bash
rm -f /tmp/douyin_audio_raw.m4a /tmp/douyin_audio.mp3
agent-browser close
```

**图文帖**：无视频/音频时，用 `agent-browser get text` 提取页面文案作为"转录内容"。

#### 步骤 2：AI 摘要 + 结构化

拿到转录文本后，生成：

1. **一句话总结**（30 字以内，用作 blockquote）
2. **核心要点**（3-7 个要点，每个 1-2 句）
3. **关键金句**（如有）
4. **实操建议**（可选，3-5 条）

#### 步骤 3：组装笔记

```markdown
---
tags:
  - 抖音
  - 视频笔记
created: YYYY-MM-DD HH:MM
source: douyin
---

# {视频标题}

> {一句话总结}

## 核心要点

- 要点 1
- 要点 2

## 关键金句

> "金句内容"

## 原始转录

{完整转录文本}

---

**来源**: [{视频标题}]({原始链接})
```

#### 步骤 4：写入 Obsidian

读取 config.json 获取 vault 和 folder：

1. **创建笔记**：
```bash
obsidian vault="<vault名>" create path="<folder>/抖音-{标题简称}-{YYYYMMDD}.md" content="<组装好的markdown>" silent
```

文件名规则：标题取前 20 字符，去掉 `/ \ : * ? " < > |`，日期 YYYYMMDD。

2. **设置属性**：
```bash
obsidian vault="<vault名>" property:set name="tags" value="[抖音,视频笔记]" file="<路径>"
obsidian vault="<vault名>" property:set name="created" value="YYYY-MM-DD HH:MM" file="<路径>"
obsidian vault="<vault名>" property:set name="source" value="douyin" file="<路径>"
```

#### 步骤 5：确认

> ✅ 已保存到 Obsidian
> 📁 位置：{folder}/{文件名}
> 📝 包含：AI 摘要 + 原始转录 + 来源链接

---

## 故障排查

| 问题 | 解决 |
|------|------|
| config.json 不存在 | 首次使用会自动询问并创建 |
| Groq API Key 未配置 | 提示用户在 douyin-transcribe/.env 中配置 |
| agent-browser 未安装 | `npm install -g agent-browser` |
| 音频 URL 为 null | 等几秒重试；或用户需登录抖音网页版 |
| curl 下载的音频无法播放 | 检查 Referer header 是否带上 |
| Obsidian 命令失败 | 确认 Obsidian 已打开且仓库名正确 |
