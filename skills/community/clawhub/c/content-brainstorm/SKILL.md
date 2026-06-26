---
name: content-brainstorm
version: 1.0.0
description: "Social media content ideation engine. Generates a 7-day topic plan with titles, angles, SEO keywords, and trend scores for any niche and platform."
author: ai-agent-store
license: MIT
platforms:
  - openclaw
  - cursor
  - claude-code
  - codex-cli
tags:
  - content
  - social-media
  - brainstorm
  - marketing
  - chinese
price: 9
---

# Content Brainstorm — 自媒体选题策划

Generate a complete weekly content calendar for Chinese social media platforms.

## When to Activate

Trigger when the user mentions: 选题, content planning, what to write, 灵感枯竭, brainstorm, topic ideas, 内容规划.

## Workflow

1. **Gather context:**
   - Niche / vertical (e.g., personal growth, AI tech, food, fashion)
   - Target platform (小红书 / 知乎 / 公众号 / 抖音 / Twitter)
   - Account positioning (one-sentence description)
   - Hot-topic preference (chase trends vs. evergreen)

2. **Generate a 7-day plan using the 3:3:1 ratio:**
   - 3 trend-chasing topics
   - 3 evergreen topics
   - 1 opinion / controversial topic

3. **For each topic include:**
   - Title (platform-native style)
   - Angle / hook
   - Target SEO keywords
   - Estimated virality: ⭐⭐⭐⭐⭐ scale
   - Reference competitor content
   - Estimated creation time

4. **Title style by platform:**
   - 小红书: emoji + numbers + keywords
   - 知乎: question format
   - 公众号: suspense / curiosity gap
   - 抖音: hook-first, colloquial

## Output Format

```
## Weekly Content Plan ({date range})

### Day 1 - {weekday}
**Title:** {title}
**Angle:** {hook / angle}
**Keywords:** {SEO keywords}
**Virality:** ⭐⭐⭐⭐ / High
**Reference:** {competitor example}
**Est. time:** {hours}

---
(repeat × 7)
```

## Research Strategy
- Use web_search to check current trending topics
- Analyze platform-specific trending hashtags
- Reverse-engineer competitor account topics
- Cross-reference with user's past high-performing content (if available)

## Guidelines
- Never plagiarize — reference angles only
- Flag time-sensitive topics (must publish same day)
- Mark evergreen topics as "can prepare ahead"
