---
name: douyin-transcribe
description: |
  抖音视频智能助手。用户发抖音链接或视频文件，自动转录并智能处理（总结/逐字稿/归档/讨论）。
  触发词：抖音、douyin.com、转文字、转录、视频转文本、douyin、transcribe
---

# 抖音视频智能助手 🎬🧠

用户发一个抖音链接，你就能"看到"视频内容——转录、总结、讨论、归档，一条龙。

---

## 触发条件

以下情况触发此 Skill：
1. 用户消息包含 `douyin.com` 链接（短链或长链都算）
2. 用户发来视频文件 + 提到"转文字/转录"等
3. 用户发来类似 `7.94 复制打开抖音...` 的分享文本（提取其中链接）

---

## 第一步：判断用户意图

根据用户消息，判断属于以下哪种模式：

| 模式 | 触发信号 | 用户说的话举例 |
|------|---------|--------------|
| **默认模式** | 只发了链接，没有额外指令 | `https://v.douyin.com/xxx` |
| **逐字稿模式** | 明确要原文/逐字稿 | "转文字"、"逐字稿"、"转录出来" |
| **总结模式** | 要总结/要点 | "总结一下"、"讲了啥"、"帮我看看" |
| **归档模式** | 要保存/收藏 | "存到知识库"、"收藏一下"、"记下来" |
| **讨论模式** | 要讨论/评价 | "你怎么看"、"有道理吗"、"值不值得做" |

**判断不了时，用默认模式。**

---

## 第二步：转录视频

无论哪种模式，都需要先拿到逐字稿。

### 方式 A：用户发来抖音链接

#### A1. 启动浏览器

```
browser(action="start", profile="openclaw")
```

如果浏览器已运行，跳过。

#### A2. 打开链接

```
browser(action="navigate", url="<链接>", profile="openclaw")
```

#### A3. 等待播放，提取音频

等 3-5 秒让视频播放，然后执行：

```
browser(action="act", kind="evaluate", profile="openclaw", fn=下方代码)
```

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

如果 `audioUrl` 为 null，等 5 秒重试（最多 3 次）。仍然为 null 可能需要用户先登录抖音网页版。

#### A4. 运行转录脚本

`<skill目录>` 替换为这个 SKILL.md 所在的实际目录路径。

**Windows PowerShell：**
```powershell
$env:DOUYIN_AUDIO_URL = "<audioUrl>"
$env:DOUYIN_TITLE = "<title>"
$env:DOUYIN_AUTHOR = "<author>"
cd "<skill目录>"
node scripts/transcribe.js "<原始链接>"
```

**Linux/Mac：**
```bash
cd "<skill目录>"
DOUYIN_AUDIO_URL="<audioUrl>" DOUYIN_TITLE="<title>" DOUYIN_AUTHOR="<author>" node scripts/transcribe.js "<原始链接>"
```

设 timeout 120 秒。

#### A5. 读取逐字稿

脚本成功后，读取 `douyin-transcripts/` 目录下最新的 `.md` 文件，拿到完整逐字稿文本。

### 方式 B：用户发来视频文件

保存文件到 `<skill目录>/temp/`，然后：

```bash
cd "<skill目录>"
node scripts/transcribe.js "<视频文件路径>"
```

读取最新 `.md` 输出文件。

### 方式 C：用户发来分享文本

从文本中提取 `https://v.douyin.com/xxxxx/` 链接，按方式 A 处理。

---

## 第三步：根据模式输出结果

### 🔹 默认模式（最常用）

**用户只发了链接，没说要干嘛。给最有价值的输出。**

1. 读完逐字稿后，**你自己做一个总结**（不调脚本，你就是 LLM）
2. 总结格式：

> **📹 {视频标题}**
> 👤 {博主名}
>
> **要点总结：**
> 1. {要点1}
> 2. {要点2}
> 3. {要点3}
> ...（3-7个要点，视内容长度而定）
>
> **一句话概括：** {用一句话说清楚这个视频讲了什么}
>
> ---
> 💡 逐字稿已保存。回复"看原文"查看完整逐字稿，"存起来"归档到知识库。

3. **不要**甩一大段逐字稿——用户扔链接过来是想快速了解内容，不是要读作文

### 🔹 逐字稿模式

用户明确要逐字稿，直接给：

> **📹 {标题}** | 👤 {博主}
>
> ---
> {完整逐字稿内容}

如果逐字稿太长（>2000字），先给前 1000 字 + "内容较长，已保存完整版到 `{文件路径}`"。

### 🔹 总结模式

比默认模式更详细的总结：

> **📹 {标题}** | 👤 {博主}
>
> ## 核心观点
> {2-3段话概括视频主旨}
>
> ## 关键要点
> 1. **{要点标题}**：{展开说明}
> 2. **{要点标题}**：{展开说明}
> ...
>
> ## 适用场景
> {这个内容对用户有什么用，适合什么人看}

### 🔹 归档模式

1. 先做总结（同默认模式）
2. 保存到知识库目录 `<workspace>/douyin-knowledge/`（workspace 指 OpenClaw 工作目录）
3. 文件名格式：`{YYYY-MM-DD}-{简短标题}.md`
4. 文件内容包含：来源链接、博主、总结、完整逐字稿

```markdown
# {视频标题}

**来源**: {抖音链接}
**博主**: {博主名}
**日期**: {归档日期}

## 总结
{AI 总结内容}

## 完整逐字稿
{逐字稿全文}
```

5. 告诉用户：

> ✅ 已归档到 `douyin-knowledge/{文件名}`
> {简短总结}

如果用户提到飞书/Notion 等具体平台，用对应工具创建文档。

### 🔹 讨论模式

1. 先做总结
2. 然后给出你的看法/分析：

> **📹 {标题}** | 👤 {博主}
>
> **要点：** {3-5个要点}
>
> **我的看法：**
> {你对内容的分析——同意什么、质疑什么、对用户有什么启发}
>
> {如果和用户的工作/计划相关，指出关联}

---

## 后续交互

转录完成后，用户可能会追问。常见追问及处理：

| 用户说 | 你做什么 |
|--------|---------|
| "看原文" / "逐字稿" | 展示完整逐字稿 |
| "存起来" / "归档" | 执行归档模式 |
| "你怎么看" | 给出分析讨论 |
| "他说的XX是什么意思" | 基于逐字稿回答 |
| "帮我提取金句" | 从逐字稿中挑出精彩句子 |
| "发到飞书" | 用飞书工具创建文档 |

**关键**：逐字稿已经在你上下文里了，后续追问不需要重新转录。

---

## 首次使用？先帮用户配置

当用户第一次触发时，按以下顺序检查环境。**缺什么补什么。**

### 检查 1：.env 文件

```
read: <skill目录>/.env
```

不存在则从 `.env.example` 复制。

### 检查 2：Groq API Key

读 `.env`，检查 `GROQ_API_KEY` 是否已填（不是 `gsk_your_key_here`）。

如果未填，告诉用户：

> 需要一个免费的 Groq API Key 来做语音识别。
>
> 1. 打开 https://console.groq.com
> 2. Google/GitHub 登录（免费，不要信用卡）
> 3. API Keys → Create API Key
> 4. 复制 Key（`gsk_` 开头）发给我

拿到 Key 后更新 `.env`。

### 检查 3：ffmpeg

```
exec: ffmpeg -version
```

没装则引导安装（Mac: `brew install ffmpeg`，Windows: gyan.dev 下载，Linux: `apt install ffmpeg`）。

---

## 技术说明

### 工作原理

```
抖音链接 → 浏览器打开 → DASH 音频流 URL → ffmpeg 下载（~1MB）
         → Groq Whisper large-v3（免费，3秒）
         → Groq LLM 标点分段（免费，1秒）
         → Agent 智能处理（总结/讨论/归档）
```

### 依赖

| 依赖 | 必须？ | 费用 |
|------|--------|------|
| ffmpeg | ✅ | 免费 |
| Groq API Key | ✅ | 免费 |
| OpenClaw Browser | 推荐 | N/A |

### 文件结构

```
douyin-transcribe/
├── SKILL.md              ← 你正在读的操作指南
├── README.md             ← 面向人类的说明
├── _meta.json            ← 元数据 + 触发词
├── .env.example          ← 配置模板
├── .env                  ← 用户配置（不提交 git）
├── .gitignore
├── scripts/
│   └── transcribe.js     ← 转录脚本
├── douyin-transcripts/   ← 逐字稿输出（自动创建）
└── temp/                 ← 临时文件（自动清理）
```

### 故障排查

| 问题 | 解决 |
|------|------|
| audioUrl 为 null | 等几秒重试；或登录抖音网页版 |
| ffmpeg 未找到 | 引导安装 |
| Groq 429 | 等 1 分钟再试 |
| 音频 >25MB | 建议更短的视频 |
