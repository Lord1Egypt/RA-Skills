# 场景 2：小宇宙播客 → 飞书文档 / IMA 摘要

## 一句话定位
小宇宙单集 URL → Get笔记 转写 → NotebookLM 结构化摘要 → 飞书文档或 IMA 笔记。

## 触发词

- 「小宇宙播客摘要」「这期播客做笔记」
- 「播客转写 + 总结 写到飞书」
- 「这期 podcast 转 IMA」

## 输入

| 字段 | 必填 | 说明 |
|---|---|---|
| 小宇宙单集 URL | ✅ | `https://www.xiaoyuzhoufm.com/episode/xxx` |
| 输出目标 | ⬜ | `飞书` / `IMA` / `本地`，默认飞书 |
| 摘要风格 | ⬜ | `要点提炼` / `逐段解析` / `金句卡片`，默认要点提炼 |

## 输出

- 完整转写（含说话人分离 + 时间戳，若 API 支持）
- 结构化摘要：
  - 单集主旨（1 段）
  - 嘉宾介绍（若有）
  - 核心观点（5-10 条，含时间戳锚点）
  - 金句摘录（3-5 条）
  - 延伸阅读（NotebookLM 自动推荐）

## 工作流

> ✅ **2026-05-20 实测简化**：小宇宙网页版的 shownotes 通常已包含**完整章节时间戳 + 嘉宾信息 + 节目简介**，WebFetch 直接拿到这些信息就足够生成高质量摘要，**很多场景下根本不需要音频转写**。

```
[Step 1] 抓取单集页面（WebFetch）
  ├─ 输入：小宇宙 episode 或 podcast URL
  ├─ 输出：节目名、单集名、嘉宾、时长、章节时间戳、shownotes
  └─ 注意：拿不到音频 URL（小宇宙防盗链），但通常不需要

[Step 2A] 优先：基于章节时间戳直接出摘要（推荐 ✅）
  ├─ 章节标题 + 节目简介 + 嘉宾信息 → LLM 摘要
  ├─ 输出质量：金句、要点、推荐延伸 都能产出
  └─ 速度：秒级

[Step 2B] 备选：转写音频（仅当章节信息不全）
  ├─ Get笔记 API（需 GETNOTE_API_KEY）
  ├─ 或 Whisper.cpp 本地（large-v3）
  └─ 输出：完整逐字稿

[Step 3] 检测 NotebookLM 可用性
  └─ `notebooklm status` → 可用 → 走路径 A（生成 Audio Overview）
  └─ 不可用 → 降级走路径 B（直接 LLM 摘要）

### 路径 A：NotebookLM Audio Overview（推荐）

```
[Step A1] 写逐字稿为 .txt
  → 将转写稿或章节摘要写入 /tmp/podcast.txt

[Step A2] 上传 NotebookLM（Playwright 浏览器上传）
  node scripts/notebooklm-playwright.js upload-text "<节目名> EP<集数>" "<单集标题>" "<content>"

[Step A3] 生成 Audio Overview
  node scripts/notebooklm-playwright.js generate "<节目名> EP<集数>" audio [outputDir]
  # 脚本自动：打开笔记本 → 点击"音频概览" → 等待生成完成

[Step A4] 落地同上（飞书 / IMA）
```

### 路径 B：C 方案（降级 fallback）

```
直接跳到 Step 4：LLM 结构化摘要
```

[Step 4] 生成结构化摘要
  ├─ 按选定风格调用对应 prompt
  ├─ 每条要点带时间戳（mm:ss）
  └─ 输出：summary.md

[Step 5] 落地
  if 目标 == 飞书:
    → 调用 lark-master 创建 docx
    → 模板：标题 / 元数据卡 / 主旨 / 核心观点 / 金句 / 延伸 / 原始转写折叠
    → 归档到用户指定的播客笔记目录（首次使用通过 AskUserQuestion 询问 folder_token）
  if 目标 == IMA:
    → ima-skill:notes 写入
    → tags: 播客摘要, <节目名>
```

## 摘要 Prompt（要点提炼版）

```
你是一位高效的知识工作者，需要把这期播客转换成可执行笔记。

输入：完整逐字稿（已附时间戳）
输出格式：

## 一句话主旨
（不超过 50 字）

## 嘉宾 / 主播
- 姓名 - 身份 - 这期他们带来的独特视角

## 核心观点（按重要性排序）
1. [00:12:34] 观点标题：观点描述（80-120 字），原文金句「……」
2. ...
（5-10 条，每条必须带时间戳，便于回听）

## 金句摘录
> 「原文金句 1」 — 说话人，时间戳

## 延伸思考
- 这期跟哪类内容（书 / 文章 / 其他播客）形成对话？
- 我作为 [听众身份]，能在哪个场景应用？

要求：
- 时间戳必须真实，从转写中查找
- 不编造嘉宾未说的内容
- 中文输出，避免英式表达
```

## 降级方案

| 失败点 | 降级 |
|---|---|
| Get笔记 API 没配置 | 用 Whisper.cpp 本地转写（慢但免费） |
| 音频下载失败（小宇宙防盗链） | 让用户手动下载后传本地路径 |
| NotebookLM 失败 | 直接用 Gemini API 处理 transcript |

## 进阶用法

### 批量处理一档节目

```
把"晚点聊"近 5 期都转写并整理到飞书《晚点聊·季度精华》
```

AI 内部循环：抓 RSS 列表 → 取最近 5 个 episode_url → 各自走完整 pipeline → 汇总到一份飞书表格

### 跨集对比

```
对比"硅谷 101"近 3 期关于 OpenAI 的讨论，找出观点演进
```

## 输出物示例

```
~/Downloads/neirong-gongfang/podcast-summary/2026-05-20/
├── meta.json
├── transcript.json          # 完整逐字稿
├── transcript.txt           # 纯文本版（喂给 NotebookLM）
├── summary.md               # 结构化摘要
└── audio.m4a                # 原音频（缓存，可手动删）
```

## 🛡️ 诚实度契约

> 详见 `references/honesty-rules.md`

### ⚠️ 本场景最大风险

**章节时间戳路径下，AI 没听过原音频**，"核心观点"段落是基于章节标题的合理推测。**输出绝不能用"听过音频"的口吻写**。

### 完整度声明（必加在输出顶部）

```markdown
> **抓取完整度**: metadata-only（节目页 shownotes + 章节时间戳，未听原音频）
> **AI 演绎程度**: high（要点段落基于章节标题推断）
> ⚠️ 本摘要未听原音频。如需逐字稿，需走转写路径。
```

### 标注规则

- 章节标题 + 时间戳 + 嘉宾 + shownotes：直陈，标 *(原文)*
- 「核心观点」要点：基于章节标题的推测，每条带 *(基于章节标题推测)*
- 「金句」：除非来自 shownotes 明确引用，否则不要伪造
- "延伸思考" / "待办建议"：明确标 *(AI 建议)*

### 输出 schema 必带

```json
{
  "source_completeness": "metadata-only",
  "ai_inference_ratio": "high",
  "method": "WebFetch + LLM 摘要（无音频转写）",
  "warnings": [
    "未听原音频，要点基于章节标题推测",
    "金句仅采用 shownotes 中确实出现的"
  ]
}
```

### 升级到 low inference ratio 的方式

如果用户希望降低 AI 推断比例：
1. 走 Get笔记 / Whisper 转写路径，拿到逐字稿
2. ai_inference_ratio 降到 low/medium
