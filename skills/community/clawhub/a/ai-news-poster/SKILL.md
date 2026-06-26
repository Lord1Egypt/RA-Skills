---
name: ai-news-poster
description: Generate fixed-template daily AI news posters from five news items. Use when the user asks to create a poster, social card, or image summary for "today's AI news", "5 AI news", "AI headlines", "每日AI资讯", or "AI新闻海报", including Chinese or bilingual output.
---

# AI News Poster

Create one fixed-style poster from exactly 5 AI news items.

## When to use this skill

Use this skill when the user wants:
- A daily AI news poster
- A fixed template visual for 5 AI headlines
- A Chinese or bilingual social poster summarizing AI updates

If the user asks for a long-form report, article, PPT, or spreadsheet, do not use this skill.

## Input contract

Before generating the poster, normalize input into this structure:

```json
{
  "date": "YYYY-MM-DD",
  "title": "今日AI资讯速览",
  "news": [
    {"headline": "新闻1标题", "summary": "一句话摘要（18-32字）", "source": "来源", "tag": "模型/产品/融资/政策/研究"},
    {"headline": "新闻2标题", "summary": "一句话摘要（18-32字）", "source": "来源", "tag": "模型/产品/融资/政策/研究"},
    {"headline": "新闻3标题", "summary": "一句话摘要（18-32字）", "source": "来源", "tag": "模型/产品/融资/政策/研究"},
    {"headline": "新闻4标题", "summary": "一句话摘要（18-32字）", "source": "来源", "tag": "模型/产品/融资/政策/研究"},
    {"headline": "新闻5标题", "summary": "一句话摘要（18-32字）", "source": "来源", "tag": "模型/产品/融资/政策/研究"}
  ],
  "footer": "数据来源: 公开新闻整理",
  "brand": "你的品牌名"
}
```

Rules:
- Always use exactly 5 news items.
- If more than 5 are provided, keep the most important 5 and explain filtering in one sentence.
- If fewer than 5 are provided, ask for missing items.
- Remove hype and keep each summary factual.

## Fixed poster template (must follow)

### Canvas
- Size: 1080 x 1350 (4:5)
- Background: deep navy gradient (`#0B1020` to `#121A33`)
- Safe margin: 64px on all sides

### Typography
- Main title: 72px bold, white
- Date subtitle: 32px medium, `#A9B4D0`
- News headline: 38px semibold, white
- News summary: 28px regular, `#D6DEFF`
- Meta line (tag + source): 24px medium, `#8FA2D8`
- Footer: 22px regular, `#93A0C3`

### Layout
1. Top block:
   - Main title (`今日AI资讯速览`)
   - Date line (`YYYY-MM-DD`)
2. Body block:
   - 5 cards in a single vertical column, evenly spaced
   - Each card includes:
     - Index badge (`01` to `05`)
     - Headline (single line preferred, max 24 Chinese chars)
     - Summary (1 line, max 32 Chinese chars)
     - Meta line: `#tag  |  source`
3. Bottom block:
   - Left: footer text
   - Right: brand mark text

### Visual style
- Card background: translucent white 8%-10%
- Card border: 1px `#2B3C73`
- Corner radius: 18px
- Use one accent color for badges: `#6AA8FF`
- Keep high contrast; avoid decorative clutter

## Generation workflow

1. Validate and normalize 5 news items.
2. Rewrite each summary to one concise sentence (18-32 Chinese chars).
3. Build poster JSON following the input contract.
4. Generate one final poster image using:
   - `python scripts/render.py <input.json> <output.png>`
5. If needed, install dependency once:
   - `python -m pip install pillow`
6. Self-check before final output:
   - Exactly 5 items
   - No overflow/cropping
   - Typography hierarchy is clear
   - Source shown for all items

## Utility scripts

- Renderer: `scripts/render.py`
- Sample input: `examples/input.sample.json`

Quick start:
- `python scripts/render.py examples/input.sample.json output/today-ai-news.png`

Manual copy flow (fallback when script is unavailable):
- Build poster copy using the exact order:
   - Title -> Date -> News01..News05 -> Footer -> Brand
- Render one final poster image in 1080x1350.

## Poster text template

Use this content skeleton before rendering:

```text
[TITLE] 今日AI资讯速览
[DATE] 2026-02-28

[01] {headline}
{summary}
#{tag} | {source}

[02] {headline}
{summary}
#{tag} | {source}

[03] {headline}
{summary}
#{tag} | {source}

[04] {headline}
{summary}
#{tag} | {source}

[05] {headline}
{summary}
#{tag} | {source}

[FOOTER] 数据来源: 公开新闻整理
[BRAND] {brand}
```

## Output requirements

- Primary output: one poster image file (`.png`)
- Optional companion output: the normalized JSON used for rendering
- Keep output deterministic: same input should produce same layout structure

## Example trigger prompts

- "把今天 5 条 AI 新闻做成固定模版海报"
- "按我们日更样式生成一张 AI 资讯图，给小红书发"
- "Use today's five AI headlines and make a poster card"
