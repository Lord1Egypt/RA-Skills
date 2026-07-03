---
name: book-to-skills
slug: book-to-skills
displayName: "电子书拆解成技能包"
version: "1.0.0"
description: "This skill should be used when the user provides an electronic book (PDF, EPUB, TXT, MD) and wants to automatically extract knowledge, analyze structure, and generate multiple WorkBuddy skills. Trigger phrases: 拆解这本书, 从这本书提取技能, 把这本书变成技能, 生成技能包, book to skills. Supports three modes: Knowledge Base, Action Guide, Hybrid."
xiaping_trigger: ["拆解这本书", "从这本书提取技能", "把电子书变成技能", "生成技能包", "book to skills", "extract skills from book", "电子书拆解", "把书变成技能"]
xiaping_category: ["效率工具", "学习教育", "知识管理"]
xiaping_tags: ["电子书", "PDF", "EPUB", "知识库", "技能生成", "学习方法", "知识提取", "Skill Builder"]
agent_created: true
---

# Book to Skills — 电子书智能拆解器

## Overview

输入一本电子书，自动完成格式识别 → 文本提取 → 结构分析 → 知识点拆解 → 生成多个可直接使用的 WorkBuddy 技能包。支持 PDF、EPUB、TXT、Markdown 四种输入格式，三种输出模式（知识库式 / 行动指南式 / 混合式），生成的技能包直接安装到本地 `~/.workbuddy/skills/`，立即可用。

## Workflow Decision Tree

```
User provides a book file
    ↓
Step 1: Format Detection & Text Extraction
    ↓
Step 2: Book Analysis (structure + core concepts + methodologies)
    ↓
Step 3: User Chooses Output Mode (knowledge / action / hybrid)
    ↓
Step 4: Generate Skills (multiple skill packages)
    ↓
Step 5: Install & Deliver (zip + installed locally)
```

## Step 1: Format Detection & Text Extraction

### 1.1 Auto-detect Format

Use file extension and magic bytes to determine format:

| Extension | Format | Extraction Method |
|-----------|--------|-------------------|
| `.pdf` | PDF | `pdfplumber` library |
| `.epub` | EPUB | `ebooklib` library |
| `.txt` | Plain Text | Direct read |
| `.md` | Markdown | Direct read |

### 1.2 Text Extraction Commands

**PDF extraction** (use managed Python):

```bash
# Install pdfplumber if needed
python3 -m pip install pdfplumber -q

# Extract text to file
python3 scripts/extract_pdf.py "<input.pdf>" "<output.txt>"
```

**EPUB extraction**:

```bash
# Install ebooklib if needed
python3 -m pip install ebooklib beautifulsoup4 -q

# Extract text to file
python3 scripts/extract_epub.py "<input.epub>" "<output.txt>"
```

**TXT/MD**: Read directly with the Read tool.

### 1.3 Output

Extracted text is saved to a temporary file: `/tmp/book_to_skills_extracted.txt`

## Step 2: Book Analysis

Load the extracted text and perform structured analysis. The analysis must be thorough — read the full text, not just the first few pages.

### 2.1 Analysis Dimensions

Produce a structured analysis covering:

1. **书籍元信息**: 书名、作者、出版信息、主题领域
2. **章节结构**: 目录层级（章→节→小节），每章的核心主题
3. **核心概念清单**: 每个核心概念用 1-2 句话概括
4. **可落地方法论**: 识别书中明确的操作步骤、框架、checklist
5. **知识产品化信号**: 哪些内容可以变成课程/星球帖/公众号文章（关联知识产品化探测器）
6. **技能拆分建议**: 建议生成几个 skill，每个 skill 的主题和边界

### 2.2 Analysis Output Format

输出一份 `书籍分析报告.md`，结构如下：

```markdown
# 《书名》分析报告

## 📖 书籍元信息
- 书名：
- 作者：
- 主题领域：
- 核心主张（一句话）：

## 📑 章节结构
1. 第1章：xxx（核心主题）
   - 小节1：xxx
   - 小节2：xxx
2. ...

## 🧠 核心概念清单
| # | 概念 | 一句话概括 | 可技能化 |
|---|------|-----------|---------|
| 1 | xxx  | xxx       | ✅/❌    |

## 🔧 可落地方法论
| # | 方法论名称 | 步骤数 | 适用场景 | 可行动化 |
|---|-----------|-------|---------|---------|
| 1 | xxx       | N步   | xxx     | ✅/❌    |

## 💡 知识产品化信号
- 课程素材：
- 星球帖：
- 公众号：
- 选题关联：

## 🎯 技能拆分建议
建议生成 N 个 skill：
1. `{book-slug}-knowledge` — 知识库 skill（覆盖全书知识点）
2. `{book-slug}-{method-1}` — 行动 skill（{方法论名称}）
3. ...

---
```

## Step 3: User Chooses Output Mode

After presenting the analysis report, ask the user to choose one of three modes:

```
请选择技能生成模式：

A) 📚 知识库式 — 生成1个综合知识库 skill，包含全书的 references 文档
B) ⚡ 行动指南式 — 为每个可落地方法论生成独立 action skill
C) 🔀 混合式（推荐） — 1个知识库 skill + N个行动 skill

你选哪个？
```

Do NOT proceed to Step 4 until the user responds with A, B, or C.

## Step 4: Generate Skills

### 4.1 Skill Naming Convention

All generated skills use the prefix derived from the book name:
- English book → slugify the title (e.g. `atomic-habits-`)
- Chinese book → pinyin abbreviation or English translation (e.g. `yuanzi-xiguan-`)

Ask the user to confirm the prefix if ambiguous.

### 4.2 Knowledge Base Skill (知识库式)

When mode is A or C, generate one knowledge base skill:

```
{book-slug}-knowledge/
├── SKILL.md           # 知识库 skill 元信息 + 使用指引
└── references/
    ├── overview.md    # 全书概览 + 核心主张
    ├── concepts.md    # 核心概念详解
    ├── quotes.md      # 可引用金句
    └── structure.md   # 章节结构 + 各章要点
```

**SKILL.md template for knowledge skill**:

```markdown
---
name: {book-slug}-knowledge
description: >
  Knowledge base for the book "{Book Title}". This skill should be used when the user wants to
  reference, query, or review concepts, quotes, and methodologies from this book. Trigger phrases
  include: "{book title}", "{author}", "{key concepts from the book}".
agent_created: true
---

# {Book Title} — 知识库

## Overview

This is a knowledge base skill for 《{Book Title}》by {Author}.

## How to Use

When the user mentions this book, its author, or its core concepts:
1. Load the relevant reference file(s) from `references/`
2. Provide accurate, book-grounded answers
3. When the user asks for quotes, load `references/quotes.md`
4. When the user asks about specific concepts, load `references/concepts.md`

## Reference Files

- `references/overview.md` — Book overview and core thesis
- `references/concepts.md` — All core concepts with detailed explanations
- `references/quotes.md` — Memorable quotes organized by topic
- `references/structure.md` — Chapter-by-chapter breakdown
```

### 4.3 Action Guide Skills (行动指南式)

When mode is B or C, generate one action skill per methodology:

```
{book-slug}-{method-slug}/
├── SKILL.md           # 行动 skill 元信息 + 步骤指引
└── scripts/
    └── checklist.py   # (optional) 可执行的 checklist 脚本
```

**SKILL.md template for action skill**:

```markdown
---
name: {book-slug}-{method-slug}
description: >
  Action guide for "{Method Name}" from the book "{Book Title}". This skill should be used when
  the user wants to apply this methodology in practice. Trigger phrases include: "{method name}",
  "{related keywords}", "{book title} method".
agent_created: true
---

# {Method Name} — 行动指南

> 来源：《{Book Title}》by {Author}

## Overview

{1-2 sentence description of the method}

## Prerequisites

- {prerequisite 1}
- {prerequisite 2}

## Step-by-Step Guide

### Step 1: {Step Name}

{Detailed instructions}

### Step 2: {Step Name}

{Detailed instructions}

...

## Checklist

- [ ] Step 1 completed
- [ ] Step 2 completed
...

## Common Pitfalls

1. **{Pitfall}**: {Description + how to avoid}
2. ...

## Related Concepts

- From the same book: {concept 1}, {concept 2}
- See also: `{book-slug}-knowledge` skill for full book reference
```

### 4.4 Quality Requirements

Each generated skill must:
- Have complete YAML frontmatter with specific `name` and `description`
- Include `agent_created: true` flag
- Have a clear trigger description (when to use)
- Reference bundled resources correctly
- Be immediately usable after installation

## Step 5: Install & Deliver

### 5.1 Create Output Directory

```bash
mkdir -p ~/workbuddy-output/{YYYY-MM-DD}-book-to-skills/{book-slug}/
```

### 5.2 Install Skills Locally

For each generated skill, create the directory under `~/.workbuddy/skills/`:

```bash
mkdir -p ~/.workbuddy/skills/{skill-name}/
```

Write all files (SKILL.md + references/scripts/assets) to the skill directory.

### 5.3 Generate Index Document

Create `技能索引.md` listing all generated skills with descriptions:

```markdown
# 《{Book Title}》技能包索引

生成日期：{YYYY-MM-DD}
技能总数：{N}

## 技能列表

| # | 技能名称 | 类型 | 描述 | 触发词 |
|---|---------|------|------|--------|
| 1 | {name} | 知识库 | {desc} | {triggers} |
| 2 | {name} | 行动指南 | {desc} | {triggers} |
...

## 使用示例

- 想查这本书的某个概念 → 直接说概念名，会自动触发知识库 skill
- 想执行某个方法论 → 说方法名，会自动触发行动 skill
- 想引用书中的金句 → 说"帮我找 {书名} 里关于 {主题} 的金句"
```

### 5.4 Package Skills (Optional)

If the user wants distributable zip files:

```bash
python3 path/to/skill-creator/scripts/package_skill.py \
  ~/.workbuddy/skills/{skill-name} \
  ~/workbuddy-output/{YYYY-MM-DD}-book-to-skills/{book-slug}/
```

### 5.5 Final Delivery

Present to the user:
1. Analysis report (书籍分析报告.md)
2. Skill index (技能索引.md)
3. Confirmation that all skills are installed and ready to use

## Bundled Scripts

### scripts/extract_pdf.py

Python script for extracting text from PDF files using pdfplumber. Execute this script when the input is a PDF file.

### scripts/extract_epub.py

Python script for extracting text from EPUB files using ebooklib. Execute this script when the input is an EPUB file.

## Interaction with Other Skills

This skill naturally integrates with:
- **知识产品化探测器** — Book analysis feeds directly into productization signals
- **多平台选题素材雷达** — Extracted concepts can become content ideas
- **概念讲解** — Individual concepts can be expanded into educational content
- **写公众号** / **短视频脚本创作** — Book insights can become content pieces

## 引流信息

> 🔔 如果这个技能对你有帮助，欢迎关注我的公众号「桂皮AI实战」，获取更多 AI 效率工具和实战教程。
> 
> 加入知识星球「AI超级个体变现」，与 500+ AI 实战玩家一起交流变现心得。
> 
> 作者：桂皮 | GitHub: [guipi888](https://github.com/guipi888)

---

## 📝 版本迭代记录

| 版本 | 日期 | 更新内容摘要 | 操作人 |
|------|------|------------|--------|
| v1.0 | 2026-06-22 | 创建技能，支持 PDF/EPUB/TXT/MD 四种格式，三种输出模式 | Kyle |
