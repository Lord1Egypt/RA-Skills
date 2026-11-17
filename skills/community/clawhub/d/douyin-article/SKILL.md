---
name: douyin-article
slug: douyin-article
displayName: 音视频批量转录为结构化逐字稿
version: 4.1.2
summary: 批量转录任意平台音视频为结构化 Markdown 逐字稿（三层字幕探测 + 双语对比 + 全平台支持）
license: MIT-0
description: |
  批量转录抖音/B站/小宇宙/YouTube/Vimeo/TikTok/Twitter 等平台音视频为结构化 Markdown 逐字稿（每视频独立 .md）。三层字幕探测 + 双语对比 + 全平台支持（yt-dlp 1700+ extractor）。触发词：抖音批量转录、B站批量转录、小宇宙转录、YouTube转录、双语转录、批量转录视频链接。Do NOT use for 单视频转录（用 douyin-transcribe）、作者主页抓取、纯视频文件下载（不转录）、纯字幕提取（不转录）。
allowed-tools: "Bash(python:*) Bash(curl:*) Bash(ffmpeg:*) Bash(ffprobe:*) Bash(yt-dlp:*) Bash(agent-browser:*)"
model: "claude-opus-4-5"
effort: "medium"
metadata:
  author: trae-solo
  version: 4.1.2
  category: content-creation
  openclaw:
    requires:
      bins:
        - python
        - ffmpeg
        - ffprobe
      anyBins:
        - yt-dlp
        - agent-browser
        - curl
    envVars:
      - name: HTTPS_PROXY
        required: false
        description: 可选，YouTube/受限网络的 HTTPS 代理
      - name: HTTP_PROXY
        required: false
        description: 可选，HTTP 代理
      - name: http_proxy
        required: false
        description: 可选，HTTP 代理（小写变体，部分库只读小写）
      - name: https_proxy
        required: false
        description: 可选，HTTPS 代理（小写变体）
      - name: HF_ENDPOINT
        required: false
        description: 可选，HuggingFace 镜像端点（默认 https://hf-mirror.com，国内 Whisper 模型下载加速）
      - name: SKIP_CERT_CHECK
        required: false
        description: 可选，置 1 时跳过证书校验（默认启用证书校验；仅用户在受限网络明确选择时使用）
    emoji: "🎬"
    homepage: https://github.com/EdwardWason/douyin-article
---

# 音视频批量转录为结构化逐字稿（全平台 + 双语对比）

## 任务

把**多个**音视频链接批量转录为带语义切分的 Markdown 逐字稿（每视频一个独立 .md 文件）。

**v4.0 三大特性**：
1. **全平台支持**：抖音/B站/小宇宙/YouTube + yt-dlp 1700+ 平台（Vimeo/TikTok/Twitter/X/Twitch/TED 等）
2. **字幕优先**：平台有字幕时直接拉取，跳过 Whisper 转录（节省 95% 能耗）
3. **双语对比**：非中文内容自动翻译为中文，输出「中文译文 + 英文原文 blockquote」段落对比格式

**做**：批量转录 + 语义切分 + 结构化输出 + 双语对比翻译
**不做**：单视频转录、作者主页抓取、纯视频文件下载（不转录）、纯字幕提取（不转录）、PDF/HTML 输出、关键帧抽帧

## 触发词

抖音批量转录、批量转录抖音、B站批量转录、批量转录B站、小宇宙转录、批量转录播客、YouTube转录、批量转录YouTube、双语转录、YouTube双语、Vimeo转录、TikTok转录、批量转录视频链接

## 权限声明

| 能力类别 | 是否使用 | 说明 |
|---------|---------|------|
| 网络访问 | ✅ | B站公共 API、抖音 CDN、YouTube transcript API；YouTube 走 HTTPS_PROXY 代理 |
| 文件读写 | ✅ | 读 inputs.txt；写 outputs/ 目录（音频/字幕/转录稿/工作表）；可手动清理 |
| 环境变量 | ✅ | HTTPS_PROXY/HTTP_PROXY（YouTube 代理） |
| subprocess | ✅ | python、yt-dlp、ffmpeg、ffprobe、curl、agent-browser |
| 外部 API | ✅ | B站公共 API（api.bilibili.com）、YouTube transcript API |

**用户警告**：脚本会下载视频/音频流到 `outputs/` 目录，调用 ffmpeg/yt-dlp/agent-browser 等外部进程。Whisper 转录会占用 GPU/CPU 资源（字幕可用时自动跳过）。删除 `outputs/` 目录可清理全部中间产物。

## 输出格式

每个视频输出一个独立 .md，结构固定。**v4.0 单语模式**（中文内容或未翻译）：

```markdown
# {标题}

> 作者: {作者}
> 来源: 抖音
> 原始链接: {url}
> 转录工具: faster-whisper (small) + opencc
> 转录日期: {YYYY-MM-DD}
> 路由: {route}（{路由名}）
> 路由原因: {一句话}
> 时长: {HH:mm:ss}
> 场景数: {N}
> 语言: 中文

---

## 目录
1. [场景1标题](#01-场景1)
2. [场景2标题](#02-场景2)

---

## 01. {场景标题}（{mm:ss}-{mm:ss}）

{完整内容，保留推理/例子/数字/限定条件}

<details><summary>切分原因</summary>{reason}</details>

---

## 02. {场景标题}（{mm:ss}-{mm:ss}）
...
```

**v4.0 双语对比模式**（非中文内容，自动翻译后）：

```markdown
# {English Title}

> 作者: {Author}
> 来源: YouTube
> 原始链接: {url}
> 转录工具: 平台字幕 (youtube-transcript-api)
> 转录日期: {YYYY-MM-DD}
> 路由: lesson（教学课）
> 路由原因: {一句话}
> 时长: {HH:mm:ss}
> 场景数: {N}
> 语言: en → 中文（双语对比）

---

## 目录
1. [场景1标题](#01-场景1)
2. [场景2标题](#02-场景2)

---

## 01. {场景标题}（{mm:ss}-{mm:ss}）

中文译文段落，按场景边界切分的完整语义段落...

> **原文**：English original text in the same scene range...

<details><summary>切分原因</summary>{reason}</details>

---

## 02. {场景标题}（{mm:ss}-{mm:ss}）

中文译文继续段落...

> **原文**：More English text...
```

## 规则

**6 条硬规则（v4.0 升级）**：

1. **阶段分工**：阶段 1-3 由脚本执行，阶段 3.5 翻译由主对话循环执行（next-batch → AI 翻译 → apply），阶段 4 由主对话执行（读工作表→写 boundaries），阶段 5 由脚本执行
2. **保留时间戳**：阶段 2 转录必须保留每个 segment 的 start/end/text，这是阶段 4 语义切分对齐的基础
3. **禁止机械切分**：阶段 4 切分必须按语义边界（知识点结束/论点完成/问答闭合），禁止按 60/90 秒固定时长切
4. **边界覆盖**：第一个场景 start_sec=0.0，最后一个 end_sec >= 视频时长，场景之间不能重叠或空隙
5. **每场景必带 title 和 reason**：title 简短描述内容（如"课程介绍"），reason 具体说明为什么在这里切（如"知识点结束，进入例句解析"）
6. **v4.0 字幕优先**：平台有字幕时（YouTube/B站/通用平台），优先用 yt-dlp 拉取字幕（手动 > 自动），跳过 Whisper 转录；只有字幕不可用时才 fallback 到音频下载 + Whisper

**6 路由模型**（详见 [`references/route-rules.md`](references/route-rules.md)）：
`lesson`（教学课）/ `explainer`（科普解读）/ `conversation`（访谈对话）/ `demo`（操作演示）/ `narrative`（叙事讲述）/ `bulletin`（资讯速览）

**Light-plus 原则**：不是摘要，必须保留推理、例子、数字、限定条件、分歧、问答、重复强调

**v4.0 双语翻译契约**：
- segment 是不可变翻译单元（1 cue 1 segment），不做 smart 合并
- 80 segment/批 + 前后 2 个只读 context
- manifest 是唯一状态源，可从任意批次恢复
- 翻译由主对话（active session model）完成，零外部 API 依赖

## 示例

完整的批量执行示例、边界情况示例、字幕不可用 fallback 示例详见 [`references/examples.md`](references/examples.md)。

## 首次使用配置

详见 [`references/troubleshooting.md`](references/troubleshooting.md) 的"首次使用配置"章节。

## 扩展参考

- **[`references/pipeline-details.md`](references/pipeline-details.md)** — 5 阶段管线详细执行步骤 + 平台支持矩阵
- **[`references/route-rules.md`](references/route-rules.md)** — 6 路由模型规则详解
- **[`references/troubleshooting.md`](references/troubleshooting.md)** — 故障排查表 + 首次使用配置
- **[`references/examples.md`](references/examples.md)** — 完整示例集

## 依赖

| 依赖 | 用途 | 安装 | 平台 |
|------|------|------|------|
| Python 3.9+ | 运行脚本 | 系统自带 | 全部 |
| ffmpeg/ffprobe | 音频提取 | `winget install Gyan.FFmpeg` | 全部 |
| yt-dlp | 视频/音频/字幕下载 | `pip install -U yt-dlp` | B站+YouTube+通用平台 |
| agent-browser | 抖音浏览器自动化 | `npm install -g agent-browser` | 仅抖音 |
| youtube-transcript-api | YouTube 字幕 API | `pip install youtube-transcript-api` | 仅YouTube |
| faster-whisper | 语音转录 | `pip install faster-whisper` | 字幕不可用时的 fallback |
| opencc-python-reimplemented | 繁简转换 | `pip install opencc-python-reimplemented` | Whisper 转录时 |
| curl | 下载音频流 | Windows 自带 | 抖音+小宇宙 |

## 平台支持矩阵

详见 [`references/pipeline-details.md`](references/pipeline-details.md) 的"平台支持矩阵"章节。
