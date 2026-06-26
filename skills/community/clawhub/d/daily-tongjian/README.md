# Daily Tongjian / 每日资治通鉴

**English**

A bilingual skill for reading **Zizhi Tongjian (资治通鉴)** progressively, one lecture at a time.
It is designed as a daily historical lecture experience with:
- progressive volume-by-volume reading (all 294 volumes)
- auto-tracked progress
- full lecture text by default
- generated scene art
- voice narration

**中文**

这是一个面向 **《资治通鉴》** 的双语讲史 skill，按“每日一讲”的方式逐卷推进。
默认特性包括：
- **逐卷推进**（294卷）
- **自动记录进度**
- **完整讲稿**（不是短摘要）
- **历史场景配图**
- **语音朗读**

## What it does

For each lecture, the skill is designed to generate:
1. **Full lecture text** — not a short summary
2. **Scene image** — based on the most vivid moment in the lecture
3. **Voice narration** — suitable for listening delivery

每一讲默认交付三件套：
1. **完整正文**
2. **配图**
3. **语音**

If the user has configured text, image, and voice, the skill should generate **all of them**, not just one.

## Why this skill exists

《资治通鉴》很长，也很容易被做成枯燥摘要。这个 skill 的目标不是“把历史压成短句”，而是把它做成：
- 每天能读的一讲
- 有叙事感
- 有点评
- 有画面
- 有声音

So the experience feels closer to a **daily historical lecture series** than a dry reference lookup.

## Delivery flow

Default order:
1. **Write the full lecture**
2. **Generate the image**
3. **Generate the voice**
4. **Advance progress**

默认顺序：
**正文 → 配图 → 语音 → 推进进度**

## Example images

### Lecture 1
![Daily Tongjian Lecture 1](./assets/lecture-1.jpg)

### Lecture 2
![Daily Tongjian Lecture 2](./assets/lecture-2.jpg)

## Core files

- `SKILL.md` — main workflow and delivery rules
- `references/structure.md` — lightweight historical structure map
- `references/style-guide.md` — lecture tone and formatting rules
- `scripts/progress.py` — progress tracking

## Triggers

- `资治通鉴`
- `通鉴`
- `daily tongjian`
- `今日通鉴`
- `继续读通鉴`
- `tongjian`

## Repository context

This skill currently lives in the `YumSkills` collection and is intended to be used as a narrative daily-history experience rather than a reference-only tool.
