# 抖音视频分析 / Douyin Video Analysis

把一个抖音链接，变成真正有用的分析材料。
Turn a Douyin link into something actually useful.

这个 skill 会尽可能抓取页面信息、下载音频、转写口播、总结内容、提取有用信息与对应证据，然后再做批判性思维分析，而不是停留在表层热评。
This skill captures the page, downloads audio when possible, transcribes speech, summarizes the content, extracts useful information plus evidence, and then performs critical-thinking analysis instead of shallow hot takes.

它适合那些想理解短视频，而不是只想跟着情绪跑的人。
It is built for people who want to understand short-form videos, not just react to them.

---

# 为什么做这个 skill / Why this skill exists

## 中文
大多数短视频分析最后都会掉进两个坑：
1. 只看标题、元信息或页面摘要，根本没碰真实口播内容
2. 直接进入情绪化评论，没有把事实、主张、证据和判断拆开

这个 skill 就是专门拿来绕开这两个坑的。
它真正的价值，不只是下载或转写。
而是它强制采用一种更靠谱的分析顺序：
- 先抓内容
- 再转写
- 再总结
- 再提炼有用信息与证据
- 最后再批判

## English
Most video analysis falls into one of two bad patterns:
1. it only reads the title, metadata, or page summary and never touches the spoken content
2. it jumps straight into emotional commentary without separating facts, claims, evidence, and judgment

This skill is designed to avoid both.
Its real value is not just downloading or transcription.
Its real value is the analysis order it enforces:
- capture first
- transcribe second
- summarize third
- extract useful information + evidence fourth
- criticize last

---

# 这个 skill 能做什么 / What this skill does

## 中文
给一个抖音短链或完整视频链接，这个 skill 可以：
1. 解析真实视频页
2. 抓取标题、页面元信息、可见文字、账号信息
3. 检查浏览器已加载资源，并在可行时提取音频流
4. 将音频下载到本地临时目录
5. 使用本地 Whisper 流水线进行音频转写
6. 在 Obsidian 中生成转写笔记
7. 在 Obsidian 中生成结构化分析笔记
8. 在做判断前，先对视频内容进行总结
9. 提取视频中真正有用的信息，并对应视频自己给出的证据
10. 进行批判性思维分析，包括：标题策略、是否像 AI 写稿、说服技巧、夸大成分、逻辑质量等

## English
Given a Douyin short URL or full video URL, this skill can:
1. resolve the real video page
2. extract title, metadata, visible page text, and creator info
3. inspect browser-loaded resources and capture audio when possible
4. download the audio to a local temp directory
5. transcribe the audio with a local Whisper pipeline
6. generate a transcript note in Obsidian
7. generate a structured analysis note in Obsidian
8. summarize the video before judging it
9. extract useful information and pair it with the evidence offered by the video itself
10. perform critical-thinking analysis, including title strategy, AI-writing likelihood, persuasion tactics, exaggeration, and reasoning quality

---

# 最适合的使用场景 / Best use cases

## 中文
以下场景最适合使用：
- 想分析一个抖音视频，而不是只看标题和封面
- 想判断文案是否像 AI 生成 / AI 辅助
- 想把视频口播内容保存为笔记
- 想拆解视频中的说服 / 操控 / 叙事套路
- 想判断一个视频到底是有信息价值，还是浅薄、夸张、误导
- 想建立自己的短视频研究资料库

## English
Use this skill when you want to:
- analyze a Douyin video beyond its title or thumbnail
- check whether a script feels AI-generated or AI-assisted
- preserve the video's spoken content in notes
- break down persuasion / manipulation / rhetoric patterns
- evaluate whether a video is informative, shallow, exaggerated, or misleading
- build a research archive of short-form videos

---

# 工作流程 / Workflow

## 中文
这个 skill 的固定流程是：
1. 在 Chrome 中打开抖音链接
2. 解析真实视频页
3. 抓取标题、元信息和页面可见文字
4. 检查浏览器资源加载记录
5. 如果可行，抓取并下载音频
6. 将音频转写成原始文本
7. 将转写写入 Obsidian 笔记
8. 用固定模板创建分析笔记
9. 先对视频内容做总结
10. 列出有用信息 + 对应证据
11. 再做批判性思维分析
12. 返回笔记路径和结论

## English
This skill follows a fixed pipeline:
1. open the Douyin URL in Chrome
2. resolve the canonical video page
3. extract title, metadata, and visible text
4. inspect browser resource entries
5. capture and download audio if available
6. transcribe audio to raw text
7. write transcript note into Obsidian
8. create analysis note with a stable template
9. summarize the video content
10. list useful information + corresponding evidence
11. perform critical-thinking analysis
12. return note paths and final conclusions

---

# 输出结果 / Output

## 中文
典型输出包括：
- 一份 Obsidian 转写笔记
- 一份 Obsidian 分析笔记
- 一份聊天中的总结说明，告诉你：
  - 视频到底在说什么
  - 有哪些真正有用的信息
  - 视频自己给了哪些证据
  - 标题有没有夸张或偷换概念
  - 文案是否像 AI 辅助生成
  - 哪些地方值得信，哪些地方要打折看

典型笔记文件：
- `OpenClaw/Inbox/YYYY-MM-DD 抖音视频口播转写 - <topic>.md`
- `OpenClaw/Inbox/YYYY-MM-DD 抖音视频分析 - <topic>.md`

## English
Typical outputs include:
- a transcript note in Obsidian
- an analysis note in Obsidian
- a chat summary that explains:
  - what the video is saying
  - what useful information it contains
  - what evidence it gives
  - whether the title is exaggerated
  - whether the script looks AI-assisted
  - what parts are worth trusting or doubting

Typical note files:
- `OpenClaw/Inbox/YYYY-MM-DD 抖音视频口播转写 - <topic>.md`
- `OpenClaw/Inbox/YYYY-MM-DD 抖音视频分析 - <topic>.md`

---

# 分析结构 / Analysis structure

## 中文
这个 skill 的分析结构是故意设计成“先还原内容，再下判断”，避免上来就嘴炮。
它会明确区分：
1. 视频到底在讲什么
2. 内容总结
3. 有用信息 + 对应证据
4. 标题 / 钩子分析
5. AI 生成概率判断
6. 批判性思维分析
7. 可执行结论 / 有用启发

## English
The analysis is intentionally structured to avoid shallow hot takes.
It separates:
1. what the video actually says
2. a concise summary
3. useful information + evidence
4. title/hook analysis
5. AI-generated likelihood
6. critical-thinking critique
7. practical takeaways

---

# 如何使用 / How to use it

## 中文
在聊天里你可以直接这样说：
- “分析这个抖音视频：<链接>”
- “按抖音分析固定流程跑这个链接：<链接>”
- “把这个抖音视频转写并批判性分析：<链接>”

## English
In chat, you can simply say:
- "Analyze this Douyin video: <url>"
- "Run the Douyin analysis pipeline on this link: <url>"
- "Transcribe and critically analyze this Douyin video: <url>"

---

# 辅助脚本 / Helper scripts

## 1) 抓页面 + 抓音频 / Grab page + audio
```bash
python3 skills/douyin-video-analysis/helpers/douyin_grab.py '<douyin-url>'
```

### 中文
这个脚本会：
- 在 Chrome 中打开抖音页面
- 抓真实 URL、标题、元信息、正文预览
- 读取浏览器已加载资源
- 找到候选音频链接
- 尝试带认证信息下载音频
- 返回 JSON 结果

### English
This script:
- opens the Douyin page in Chrome
- captures canonical URL, title, metadata, body preview
- inspects browser-loaded resources
- finds a candidate audio URL
- attempts authenticated audio download
- returns JSON

## 2) 转写 + 生成笔记 / Transcribe + create notes
```bash
python3 skills/douyin-video-analysis/helpers/transcribe_and_note.py \
  --audio-file /tmp/douyin_transcribe/audio_latest.mp4 \
  --title '<video-title>' \
  --source-url '<shared-url>' \
  --page-url '<canonical-url>' \
  --account '<creator>' \
  --topic '<short-topic>'
```

### 中文
这个脚本会：
- 用 `mlx-whisper` 转写音频
- 生成 Obsidian 转写笔记
- 生成 Obsidian 分析笔记骨架
- 返回两个笔记路径的 JSON

### English
This script:
- transcribes audio with `mlx-whisper`
- creates a transcript note in Obsidian
- creates an analysis note skeleton in Obsidian
- returns both note paths as JSON

## 3) 跑完整流程 / Run the full pipeline
```bash
python3 skills/douyin-video-analysis/helpers/run_douyin_pipeline.py '<douyin-url>'
```

### 中文
这个总控脚本会把主要步骤串起来：
- 解析页面
- 抓音频
- 做转写
- 生成笔记

### English
This controller script chains the major steps:
- resolve page
- grab audio
- transcribe
- create notes

## 4) 生成标准分析模板 / Finalize analysis note
```bash
python3 skills/douyin-video-analysis/helpers/finalize_analysis_note.py \
  --topic '<topic>' \
  --source-url '<shared-url>' \
  --page-url '<canonical-url>' \
  --account '<creator>' \
  --title '<title>' \
  --duration '<duration>' \
  --basis meta visible raw_transcript cleaned \
  --transcript-note '<transcript-note-stem>'
```

### 中文
这个脚本会应用固定分析模板，并补齐分析笔记头部信息。

### English
This script applies the stable analysis template and fills the note header.

---

# 运行要求 / Requirements

## 中文
当前默认依赖 Bob 机器上的这些条件：
- macOS
- 已安装 Google Chrome
- 可用的 browser bridge 脚本
- 对 `/tmp/douyin_transcribe/` 有写权限
- 支持 Python venv
- 可在临时 venv 中安装 `mlx-whisper`
- 已配置 BobVault Obsidian 路径

## English
Current assumptions on Bob's machine:
- macOS
- Google Chrome available
- browser bridge scripts available
- temp write access to `/tmp/douyin_transcribe/`
- Python venv support
- `mlx-whisper` can be installed in the temp venv
- Obsidian vault available at the configured BobVault path

---

# 限制说明 / Limits

## 中文
- 如果抖音反爬策略变化，部分媒体链接可能失效。
- 转写质量取决于 Whisper 模型大小。
- 专有名词、数字、人物名称可能需要人工清洗。
- 批判性分析仍然适合由人/智能体来做判断，不适合完全自动化成盲目结论。

## English
- Some Douyin media URLs may fail if anti-bot behavior changes.
- Transcript quality depends on the chosen Whisper model.
- Proper nouns, numbers, and names may need cleanup.
- Critical analysis still benefits from human/agent judgment; it should not be fully automated into blind conclusions.

---

# 为什么它不只是“转写工具” / Why this skill is different

## 中文
这个 skill 不只是下载器或转写工具。
它真正的价值在于，它强制采用一种更克制的分析顺序：
- 先总结
- 再提炼信息和证据
- 最后再批判

这个顺序能减少“先入为主的嘴炮”，让分析质量更稳。

## English
This skill is not just a downloader or transcript helper.
Its real value is that it forces a disciplined analysis order:
- summarize first
- extract useful information second
- critique third

That order helps reduce shallow takes and improves reasoning quality.
