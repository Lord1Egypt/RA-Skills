---
name: ai-hot-news-workbench
description: Daily AI intelligence briefing workflow for finding the hottest global and China-region artificial intelligence news, product launches, model releases, research, funding, policy updates, and industry moves, then sending a concise Chinese briefing to the user's Codex workbench. Use when the user asks for AI hotspot monitoring, daily AI news, China AI updates, AI briefings, scheduled AI information collection, or workbench delivery of AI trends.
---

# AI Hot News Workbench

## Overview

Use this skill to produce a daily 09:00 AI hotspot briefing for the Codex workbench. The workflow gathers current global and China-region AI information, ranks it by impact and freshness, and returns a Chinese briefing that can be posted directly to the workbench.

## Quick Start

1. Get current candidates from live sources. Prefer the bundled collector:

```bash
python scripts/collect_ai_hot_news.py --hours 24 --region all --limit 40 --output /tmp/ai-hot-news.json
```

2. If the local Python certificate store is broken, fix the certificate store first. For a one-off local debug run only, use `--insecure` and state that TLS verification was disabled.
3. If network access is unavailable, browse the web manually and follow `references/source_policy.md`.
4. Deduplicate stories by underlying event, not by headline.
5. Select 6-10 top items and produce the workbench message in Chinese.
6. Include source links and publication times when available.

## Source Policy

Read `references/source_policy.md` when choosing sources, scoring hotness, or handling conflicting reports. Use primary sources first, then reputable technology and business media, then curated feeds for discovery.

## Ranking Rules

Score each candidate on these factors:

- Freshness: published or materially updated in the last 24 hours.
- Impact: affects many AI users, developers, enterprises, regulators, or investors.
- Novelty: new model, product, benchmark, policy, partnership, incident, or research result.
- Source strength: official announcements and primary documents outrank commentary.
- Cross-source confirmation: multiple independent sources raise confidence.

Prefer a balanced final set across:

- model and product launches
- frontier AI research
- developer platform changes
- major business, funding, and partnership news
- regulation, safety, copyright, and geopolitical updates
- notable incidents, outages, or security issues
- China-region model releases, AI apps, chips, cloud services, regulation, financing, and open-source ecosystem moves

If credible China-region candidates are available, include at least 2 China-region items in the final briefing. "China-region" means Chinese companies, products, policy, research groups, chips/cloud infrastructure, applications, financing, open-source models, or domestic market moves. A Chinese-language article about a foreign company does not count unless it has clear China-market relevance. If there are fewer than 2 credible China-region items, add a short note under "中国区动态" explaining that no more high-confidence items were found in the current window.

## Workbench Output Format

Return one concise Chinese message:

```markdown
# 今日 AI 热点简报（YYYY-MM-DD 09:00）

## 重点结论
- ...
- ...
- ...

## 热点排行
1. **标题**（来源，时间）
   - 为什么重要：...
   - 关键事实：...
   - 链接：...

## 中国区动态
- ...
- ...

## 值得跟进
- ...
```

Keep each item brief. Do not paste long article text. If a fact is uncertain, label it as "待确认" and explain what source would confirm it.

## Automation Prompt

For a scheduled Codex automation, use this prompt:

```text
Use $ai-hot-news-workbench to collect the hottest global and China-region AI information from the last 24 hours and send a concise Chinese briefing to the workbench. Include 6-10 ranked items with at least 2 China-region items when credible sources are available, plus source links and publication times. Highlight what changed, why it matters, and what to follow next.
```

The schedule belongs to the Codex automation system, not inside this skill. Configure it for 09:00 in the user's local timezone.
