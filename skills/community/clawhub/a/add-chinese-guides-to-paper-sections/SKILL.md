---
name: add-chinese-guides-to-paper-sections
description: |
  Generate a Chinese guided-reading edition for an academic paper from a user-provided
  paper PDF, URL, text excerpt, abstract, or LaTeX source. Use when the user wants a
  Chinese guide version of a paper: section-by-section guide, key concepts, equations,
  figure/table reading notes, claims and evidence, questions, and a reading path.
  This public skill produces a reviewable guide document and stays in a reading-and-writing workflow.
---

# Add Chinese Guides to Paper Sections

This public skill turns an academic paper into a Chinese guided-reading edition. The output is a standalone guide that helps a reader enter the paper section by section, understand the main claims, and know what to watch for before reading each part.

The guide should be useful even when the user only has a PDF, URL, abstract, pasted text, or local LaTeX. Prefer a readable Markdown guide, optionally with an HTML version if the user asks.

## Quick Start

Use this skill when the user asks for:

- "把这篇论文做成中文导读版"
- "给这篇论文做一个中文阅读包"
- "我想看这篇 paper 的中文导读版本"
- "Generate a Chinese guided-reading edition for this paper"
- "Explain this paper section by section in Chinese"
- A paper PDF, paper URL, arXiv/OpenReview/conference URL, abstract, pasted paper text, or local LaTeX source

Do not use this for a plain one-paragraph summary unless the user asks for a guided paper version, reading path, section-by-section guide, or Chinese paper-reading scaffold.

If only a title is provided, identify what information is missing and ask for a PDF, URL, abstract, or pasted text. If a URL or uploaded file is provided, read only the paper content needed for the guide.

## Output Contract

Create or report these artifacts when possible:

```text
paper-guide.zh.md
paper-guide.zh.html
guide-report.md
failure-notes.md
```

Use `paper-guide.zh.md` as the default deliverable. Create HTML only when helpful or requested. If the input is too partial, produce a partial guide and explain what was missing.

## Workflow

1. Classify the input: uploaded PDF, URL, abstract, pasted text, local `.tex`, or partial excerpt.
2. Extract or read enough paper content to identify the paper's title, authors if available, abstract, section headings, key methods, experiments, and conclusion.
3. Build a paper map:
   - paper goal and research question
   - section list and each section's role
   - key concepts and notation
   - main method or model
   - main evidence and results
   - limitations or assumptions
4. Write `paper-guide.zh.md` in Chinese with the structure below.
5. Keep the guide specific to the paper. Avoid generic filler.
6. If only partial paper content is available, label the guide as partial and avoid pretending you saw the full paper.
7. Write `guide-report.md` with input coverage, assumptions, and missing parts.

## Guide Structure

Use this structure unless the user asks for a different format:

```markdown
# 《Paper Title》中文导读版

## 1. 一句话定位
用 1-2 句说明这篇论文到底在解决什么问题。

## 2. 阅读路线
给出建议阅读顺序、哪些段落/图/表最关键、哪些部分可以略读。

## 3. 论文地图
按 section 列出每一节的功能：问题、方法、证据、结论。

## 4. 分节导读
### Section Name
- 读前问题：
- 这一节在全篇中的作用：
- 关键概念/公式/图表：
- 读完应能回答：

## 5. 核心概念表
术语 | 中文解释 | 在论文中的作用

## 6. 公式、图和表怎么看
解释关键公式、figure/table 的阅读方式和它们支撑的论点。

## 7. 主张与证据
Claim | Evidence | 可信度/注意事项

## 8. 局限与批判性问题
列出假设、边界条件、实验限制、可能反例。

## 9. 复习问题
给出 8-12 个中文问题，帮助读者检查理解。
```

## Section Guide Standard

Each section guide should contain 2-4 Chinese Q&A items. Good questions target:

- What problem is this section solving?
- What method, assumption, or model is being introduced?
- What result or evidence matters most?
- Why does this section matter for the paper's overall claim?

Keep the guide specific. Avoid generic filler like "本文主要介绍了" unless followed by concrete method, evidence, or contribution.

## Quality Checks

Review the guide before delivering:

- Does the guide name the paper's actual problem, method, and evidence?
- Does each section guide help the reader know what to watch for before reading?
- Are equations, figures, and tables explained in the paper's own context?
- Are uncertainties labeled when the input was partial?
- Are claims and limitations separated clearly?
- Is the output a guide, not a full translation or reproduction of the paper?

## Hard Rules

- Do not present a full translation of copyrighted paper text unless the user owns it and explicitly asks.
- Keep direct quotations short and necessary.
- Do not claim to have read sections that were not available.
- Stay in a reading-and-writing workflow; do not run paper code or project toolchains as part of this public skill.
- Do not request or log credentials.
- If the user asks for a typeset PDF workflow, explain that this public skill creates a guided-reading document; a separate trusted workflow is needed for that delivery format.
- Be honest about partial results, missing sections, broken PDFs, or unreadable content.
