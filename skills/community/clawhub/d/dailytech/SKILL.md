---
name: dailytech
description: "Daily AI & tech news in 60 seconds — LLM updates, product launches, startup funding, developer tools. Bilingual EN/CN visual card. Morning & evening push."
keywords:
  - 科技日报
  - 科技新闻
  - AI新闻
  - 技术日报
  - 今日科技
  - 最新科技
  - 创业新闻
  - 人工智能
  - 科技动态
  - 产品发布
  - daily tech
  - tech news
  - AI news
  - tech daily
  - startup news
  - product launch
  - latest tech
  - technology briefing
  - machine learning
  - artificial intelligence
metadata:
  openclaw:
    runtime:
      node: ">=18"
---

# Daily Tech / 科技日报

Generate a beautifully formatted daily tech news briefing focused on AI, startups, and technology.

## Workflow

1. **Search for news** — Use `web_search` to find today's top tech/AI stories. Run 3-4 searches:
   - `"AI news today [date]"`
   - `"tech startup news today"`
   - `"product launch technology today"`
   - `"China tech news today"` (for Asian audience relevance)
2. **Curate** — Select 5-6 most significant stories. Prioritize: AI/ML breakthroughs, major product launches, funding rounds > $50M, policy/regulation changes, notable acquisitions.
3. **Write summaries** — Each story: headline (EN + CN), 2-3 sentence summary (EN), 1-2 sentence summary (CN), source name, and a relevance tag.
4. **Generate the visual** — Create a single-file HTML artifact.

## Visual Design Requirements

Create a premium tech-media editorial layout:

- **Layout**: Magazine/newsletter style. Hero story at top (larger card), remaining stories in a 2-column grid below.
- **Typography**: Modern, techy but readable — (e.g., Space Grotesk or JetBrains Mono for headlines, Inter or IBM Plex Sans for body). Monospace accents for tags/categories.
- **Color scheme**: Dark mode default — near-black background (#0a0a0f), with accent colors: electric blue, neon green, or amber for highlights. Very "tech publication" feel.
- **News cards**: Each card has: category tag (AI / Startup / Product / Policy / China Tech), headline, summary, source badge, and a "relevance" indicator (🔥 hot, ⭐ notable, 📌 important).
- **Hero story**: Top story gets a larger card with more detailed summary.
- **Interactive**: Click any card to expand and show the full bilingual summary. Collapse on click again.
- **Stats bar**: At the top — "Today's Briefing: [date] | 6 stories | Reading time: ~3 min"
- **Animation**: Cards slide in from bottom on load with stagger. Category tags have a subtle glow effect.
- **Ad-ready zone**: `<div id="ad-slot-hero">` between hero and grid. `<div id="ad-slot-mid">` between 3rd and 4th story. `<div id="ad-slot-bottom">` at footer.
- **Footer**: "Powered by ClawCode"

## Content Guidelines

- Focus on stories that matter to builders and investors
- Include at least one China/Asia tech story
- Include at least one AI/ML specific story
- Avoid celebrity gossip disguised as tech news
- Source from credible outlets (TechCrunch, The Verge, Wired, 36Kr, etc.)

## Output

Save as `/mnt/user-data/outputs/daily-tech.html` and present to user.

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
