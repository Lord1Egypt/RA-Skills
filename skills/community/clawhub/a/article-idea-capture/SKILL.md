---
name: article-idea-capture
description: Record公众号文章灵感、选题、半成品观点，并持续整理成可写的大纲或初稿。Use when the user says they have an article idea, topic, inspiration,选题, 钩子, 标题想法, or wants to save a thought for later writing. Also use when the user wants to append to the ongoing idea pool, rank saved ideas, or expand one saved idea into an outline or draft.
---

# Article Idea Capture

Maintain the user's ongoing article idea pool with low friction.

## Default storage

Primary sink:
- Feishu doc: `加十的公众号灵感池`
- URL: `https://www.feishu.cn/docx/BwAFdeJZdoEeeWxfbkbcZVpWnOe`

If Feishu doc tools are unavailable in the current tool surface, fall back to a local markdown file under the workspace and clearly say it was stored locally instead of Feishu.

## Core rule

Optimize for **capture first, refinement later**.

When the user drops a raw idea, do not force a full article structure immediately unless they ask for it.

## Capture workflow

### 1. If the user gives a raw idea
Turn it into a compact idea card with these fields:

- **题目方向**
- **核心观点**
- **为什么值得写**
- **适合谁看**
- **可延展角度**
- **可能标题**

Keep it concise and useful. Do not over-polish.

### 2. Append to the idea pool
Prefer appending to the Feishu idea pool doc.

Append under a new section like:

`### 灵感 N：<short title>`

Then include the six fields above.

### 3. Confirm what was stored
Reply briefly with:
- it was recorded
- the short title used
- whether it went to Feishu doc or local fallback

## Expansion workflow

When the user wants to continue an existing idea, support these next steps:

- pick the best 3 ideas
- cluster ideas by theme
- expand one idea into an outline
- write a first draft
- generate title options
- split one big idea into a series

## Writing style

- Keep the capture lightweight
- Prefer practical article angles over abstract slogans
- Preserve the user's original insight even when cleaning wording
- Do not flatten everything into generic AI-blog phrasing

## Fallback local storage

If Feishu doc append is unavailable, store in:
- `/Users/shiyi/.openclaw/workspace/research/article-idea-pool.md`

Append only; do not overwrite existing entries.
