# epic-novel-writer — Epic Novel Writing Full Workflow

> An AI-driven creative writing SKILL for long-form serialized novels, covering the entire lifecycle from world-building and character design to chapter planning, writing, version archiving, and HTML guide generation.

**Adapted Length: Medium (100-250k words) → Long (250-600k words) → Super Long (600k-1.5m words)**
> 💡 **Proven Benchmark**: Used to generate **420,000 words** (300 chapters, 10 volumes), validating global chapter numbering, anti-collapse settings system, and HTML guide generation for super-long-form novels.

---

## 🚀 Why This SKILL?

The hardest part of writing a novel isn't "starting" — it's **surviving 300 chapters without things falling apart**. This SKILL solves the most painful problems of long-form writing:

### 1. File Names = Chapter Numbers, Never Get Lost
```
chapter-001.md → Chapter 1
chapter-150.md → Chapter 150 (regardless of which volume)
chapter-300.md → Chapter 300
```
**Restarting from 1 in every volume** is every long-form writer's nightmare. We use **global continuous numbering** — file name IS chapter number, open the folder and you know where you are.

> **文件编号 = 章编号**：`chapter-001.md` 就是第 1 章，`chapter-300.md` 就是第 300 章。不管在哪一卷，文件名直接告诉你章节号。打开文件夹就知道写到哪了。

### 2. One-Click Professional Archive
From `references/archive-template.md`, an 8-step flow auto-generates:
- ✅ **Full-text merged version** (md + txt dual format)
- ✅ **Character profile JSON** (char_data.json with name, role, growth arc, first appearance)
- ✅ **HTML guide page** (dark theme, responsive layout, character card grid, continuous chapter links)
- ✅ **Plain text table of contents** (chapter numbers + hyperlinks)

> **一键专业存档**：8 步流程自动生成全文合并版（md+txt）、人物画像 JSON、HTML 导引页（暗色主题 + 人物卡网格 + 连续章节链接）、纯文本目录。

### 3. Anti-Collapse Settings System
- **World-building template** (`world-setting-template.md`) — geography, history, power system, core conflicts
- **Character card template** (`character-card-template.md`) — personality, background, ability growth arcs, appearance tracking
- **Chapter blueprint template** (`chapter-blueprint-template.md`) — scene settings, plot outlines, foreshadowing/clue tracking, skill usage records

> **防崩设定体系**：三个模板分别覆盖世界观、角色卡、章纲。章纲模板追踪每章伏笔、线索、技能调用，确保剧情不偏离。

### 4. Read-Only Archives, Free Editing
All editing happens in `在编辑稿/` (Work-in-Progress), archive versions (v1/v2/v3…) are **read-only**,可随时对比、回溯、反向合并。

> **只读存档**：所有编辑在 `在编辑稿/` 完成，存档版本（v1/v2/v3…）只读，随时对比、回溯、反向合并。

---

## 📋 Contents

| File | Purpose |
|------|---------|
| `SKILL.md` | Core rules, workflow, naming conventions, archive process guide |
| `references/archive-template.md` | 8-step archive flow (directory structure + command examples + checklists) |
| `references/world-setting-template.md` | World-building template (geography/history/power system/rhythm planning) |
| `references/character-card-template.md` | Character card template (personality/background/ability growth/appearance tracking) |
| `references/chapter-blueprint-template.md` | Chapter blueprint template (scene/plot/foreshadowing/skill usage) |

---

## 🔧 Quick Start

### 1. Initialize Project

```bash
mkdir -p "我的小说/在编辑稿/{01-story-premise,02-world-setting,03-outline,04-chapters,05-references}"
```

### 2. Fill Core Settings

Copy templates from `references/`:
```bash
cp references/world-setting-template.md 在编辑稿/02-world-setting.md
cp references/character-card-template.md 在编辑稿/references/characters/主角.md
```

### 3. Start Writing Chapter 1

```bash
cp references/chapter-blueprint-template.md 在编辑稿/03-outline/chapter-001-blueprint.md
# Fill blueprint, then create chapter-001.md in 04-chapters/
```

### 4. Archive

When the user says "存档" (archive):
```bash
# Read references/archive-template.md and execute the 8-step flow
```

---

## 📐 Project Structure

```
MyNovel/
├── 在编辑稿/              ← 所有编辑在此 (all editing happens here)
│   ├── 01-story-premise.md     # 故事设定 (story premise)
│   ├── 02-world-setting.md     # 世界观 (world-building)
│   ├── 03-chapters-written.md  # 章节状态 (chapter status)
│   ├── 03-outline/             # 大纲 (outlines)
│   ├── 04-chapters/            # 正文 (manuscript, chapter-001.md ~ chapter-XXX.md)
│   ├── 05-reports/             # 过程报告 (process reports)
│   └── references/             # 参考文档 (reference docs)
├── MyNovel_v1/               ← 存档（只读） (archive, read-only)
├── MyNovel_v2/               ← 存档（只读） (archive, read-only)
└── ……
```

---

## ⚠️ Core Rules

1. **All editing in `在编辑稿/`**, don't touch archive directories
2. **Archive versions are read-only**, for comparison, tracking
3. **Global continuous numbering**: `chapter-001.md` = Chapter 1, doesn't reset per volume
4. **Archive must generate**: Character profile JSON + HTML guide page

> **核心规则**：所有编辑在 `在编辑稿/` 完成；存档只读；文件名=章编号=全局连续；存档必含人物画像 JSON 和 HTML 导引页。

---

## 📏 Suitable Length

| Length | Chapters | Word Count | Fit |
|--------|----------|------------|-----|
| Medium (中篇) | 30-80 chapters | 100k-250k words | ✅ Perfect fit |
| Long (长篇) | 80-200 chapters | 250k-600k words | ✅ Ideal match |
| Super Long (超长篇) | 200-500 chapters | 600k-1.5m words | ✅ Fully capable |

> 💡 **实测标杆 (Proven Benchmark)**: 已用于生成 **420,000 字**（300 章，10 卷）

**Estimation Reference (篇幅估算参考)**: ~4,000 words/chapter, ~10 chapters/volume (~40,000 words/volume). Given total word count, reverse-calculate chapters and volumes.

---

## 🏷️ Use Cases

- Long-form serialized novels (100+ chapters)
- Web novels / light novels / fantasy / sci-fi
- AI-assisted writing (LLM generation + human polishing)
- Multi-person collaboration (each works in `在编辑稿/`, archives regularly)
- Complex world-building, many characters

---

## 📦 Installation

```bash
clawhub install epic-novel-writer
```

## 🔄 Update

```bash
clawhub update epic-novel-writer
```

## 📄 License

BSD 3-Clause License

Copyright (c) 2026, sunshinejnjn@github

---

> 用结构化流程对抗长篇写作的混沌。从第 1 章到第 300 章，每一步都有据可查。
> **Structure the chaos of long-form writing. Every chapter, every step, traceable.**
