---
name: daily-history
description: "Today in history — 3–5 major events on this date with context and lasting impact. Bilingual EN/CN timeline card. Daily morning push."
keywords:
  - 历史上的今天
  - 今天发生了什么
  - 历史事件
  - 大事记
  - 历史
  - on this day
  - today in history
  - this day in history
  - historical events today
  - history timeline
  - world history
  - China history
metadata:
  openclaw:
    runtime:
      node: ">=18"
---

# Today in History / 历史上的今天

Generate a beautiful visual timeline of significant historical events that happened on today's date.

## Workflow

1. **Get today's date** — Determine the month and day.
2. **Search for events** — Use `web_search` to find 5-6 notable events that happened on this date across different centuries and categories. Query: `"on this day [month] [day] history events"`. Try to cover: science/tech, politics, culture, sports, and notable births/deaths.
3. **Curate and translate** — Select the 5 most interesting/diverse events. Write each as a concise 1-2 sentence description in both English and Chinese.
4. **Generate the visual** — Create a single-file HTML artifact.

## Visual Design Requirements

Create a vertical timeline layout, full-viewport:

- **Layout**: Vertical timeline with alternating left-right event cards. Timeline line runs down the center. Year markers on the timeline.
- **Typography**: Use a distinguished font pair — a bold condensed display font for years (e.g., Oswald, Bebas Neue) and an elegant body font for descriptions (e.g., Source Serif Pro, Lora).
- **Color scheme**: Deep, rich palette — think aged paper tones, or a modern editorial look with dark backgrounds and gold/amber accents. Rotate themes.
- **Event cards**: Each card has: Year (large), Event title (bold), Description (EN + CN), and a category icon (emoji: 🔬 science, 🏛️ politics, 🎨 culture, ⚽ sports, 👤 people).
- **Animation**: Cards should fade and slide in on load with staggered delays. Timeline line draws itself downward.
- **Header**: "历史上的今天 / Today in History" with today's full date (e.g., "April 2 / 4月2日").
- **Ad-ready zone**: `<div id="ad-slot-middle">` between 3rd and 4th event (min-height 90px, centered). `<div id="ad-slot-bottom">` at page bottom.
- **Footer**: "Powered by ClawCode" at bottom.

## Content Guidelines

- Mix different centuries — don't cluster in one era
- Include at least one event relevant to China or Asia
- Include at least one science/technology event
- Keep descriptions concise but vivid — make history feel alive

## Output

Save as `/mnt/user-data/outputs/daily-history.html` and present to user.

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
