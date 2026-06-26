---
name: daily-quote
description: "Daily curated quote from philosophers, leaders, and thinkers — with author context and why it resonates today. Bilingual EN/CN shareable visual card."
keywords:
  - 每日金句
  - 今日金句
  - 名言
  - 励志
  - 鸡汤
  - 早安语录
  - 每日名言
  - 人生格言
  - daily quote
  - quote of the day
  - motivational quote
  - morning motivation
  - inspirational quote
  - wisdom
  - daily inspiration
metadata:
  openclaw:
    runtime:
      node: ">=18"
---

# Daily Quote / 每日金句

Generate a beautiful daily inspirational quote card with bilingual (Chinese + English) presentation.

## Workflow

1. **Get today's date** — Use the current date to seed the quote selection.
2. **Search for a quote** — Use `web_search` to find an inspiring, thought-provoking quote. Search for quotes related to today's date, or a rotating theme (Monday=courage, Tuesday=wisdom, Wednesday=creativity, Thursday=perseverance, Friday=joy, Saturday=love, Sunday=reflection). Query example: `"inspirational quote [theme] famous"`.
3. **Select and translate** — Pick ONE powerful quote. Provide both English original and Chinese translation. Include the author name and brief context (1 line).
4. **Generate the visual card** — Create a single-file HTML artifact (saved to `/mnt/user-data/outputs/daily-quote.html`) with:

## Visual Design Requirements

Create a stunning, full-viewport quote card. Each day should feel different:

- **Layout**: Centered quote with generous whitespace. Author below. Date at top-right corner.
- **Typography**: Use a distinctive serif or display font from Google Fonts (rotate between: Playfair Display, Cormorant Garamond, DM Serif Display, Libre Baskerville). Body text in a clean sans-serif.
- **Background**: Rotating aesthetic — use CSS gradients, subtle patterns, or mesh gradients. Avoid plain white. Examples: warm sunset gradient, deep ocean tones, forest green to black, golden hour warmth.
- **Bilingual display**: English quote prominent, Chinese translation below in slightly smaller size with a different weight.
- **Micro-interactions**: Subtle fade-in animation on load. Quote text should animate in with a gentle reveal.
- **Ad-ready zone**: Include a tasteful, empty `<div id="ad-slot-bottom" style="...">` at the bottom of the card (min-height 90px, centered, with a subtle dashed border in dev mode). This is the future ad placement area.
- **Footer**: Small "Powered by ClawCode" text at the very bottom.

## Content Tone

- Prefer quotes from diverse sources: Eastern and Western philosophers, scientists, writers, leaders
- Avoid overly cliché quotes (no "be the change you wish to see" etc.)
- Each quote should genuinely make someone pause and think

## Output

Save as `/mnt/user-data/outputs/daily-quote.html` and present to user.

---

## 推送管理

```bash
# 开启每日推送（早晚各一次）
node scripts/push-toggle.js on <userId>

# 自定义时间和渠道
node scripts/push-toggle.js on <userId> --morning 08:00 --evening 20:00 --channel feishu

# 关闭推送
node scripts/push-toggle.js off <userId>

# 查看推送状态
node scripts/push-toggle.js status <userId>
```

支持渠道：`telegram` / `feishu` / `slack` / `discord`
