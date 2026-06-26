---
name: ai-news-researcher
description: Researches latest AI news, summarizes 5 top stories with sources.
---

# AI News Researcher Skill

## Tools
- browser: Search and read news sites
- file: Save markdown reports
- email: Optional delivery (configure if needed)

## Instructions
1. Search "latest AI news" on Google/news sites.
2. Read 5+ recent articles (prioritize reputable: TechCrunch, VentureBeat, arXiv).
3. Extract key facts, trends, impacts.
4. Summarize in Markdown: bullets per story + links.
5. Save as ~/clawd/reports/ai-news-$(date +%Y%m%d).md
