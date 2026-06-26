---
name: research-agent
description: "Deep research on any topic with structured report generation. Use when: (1) user asks for research, analysis, or investigation, (2) need competitive analysis, market research, or technology landscape, (3) user wants a comprehensive report on a topic. Outputs structured markdown reports with citations, key findings, and actionable insights."
---

# Research Agent

Conduct deep research and generate structured reports.

## Workflow

### 1. Scope Definition
- Clarify the research question
- Identify key aspects to investigate
- Set boundaries (time, depth, focus areas)

### 2. Multi-Source Research
Gather data from diverse sources:

```bash
# Web search (DuckDuckGo)
curl -s "https://api.duckduckgo.com/?q=QUERY&format=json" | jq '.RelatedTopics[:5]'

# GitHub (repos, stars, activity)
gh search repos "TOPIC" --limit 20 --json name,description,stargazersCount,url

# News/Tech (Hacker News, TechCrunch)
curl -s "https://hacker-news.firebaseio.com/v0/topstories.json" | jq '.[:10]'

# NPM packages
npm search PACKAGE --json 2>/dev/null | jq '.[0:5]'
```

### 3. Analysis & Synthesis
- Cross-reference findings across sources
- Identify patterns, trends, gaps
- Extract key statistics and quotes
- Note contradictions or debates

### 4. Report Generation
Use the standard report structure from `references/report-template.md`.

## Report Structure

Every research report follows this format:

```markdown
# [Topic] Research Report

**Date:** YYYY-MM-DD
**Researcher:** Clawie (AI Research Agent)
**Sources:** X sources analyzed

---

## Executive Summary
[2-3 paragraph overview with key findings]

## Key Findings

### Finding 1: [Title]
[Evidence, data, sources]

### Finding 2: [Title]
[Evidence, data, sources]

## Market/Technology Landscape
[Competitors, alternatives, ecosystem]

## Trends & Predictions
[Where things are heading]

## Gaps & Opportunities
[What's missing, underserved areas]

## Recommendations
[Actionable next steps]

## Sources
[Numbered list of all sources with URLs]

## Methodology
[Brief note on research approach]
```

## Quality Standards

- **Minimum sources:** 20+ for comprehensive reports
- **Citations:** Every claim backed by source
- **Objectivity:** Present multiple perspectives
- **Actionability:** End with clear recommendations

## Quick Commands

```bash
# Check trending GitHub repos for a topic
gh search repos "ai agent" --sort stars --limit 30 --json name,description,stargazersCount,url,updatedAt

# Get recent articles from a domain
curl -sL "https://DOMAIN.com/feed" | grep -oP '<title>.*</title>' | head -20

# Check npm package popularity
npm view PACKAGE version time.created time.modified
```

## Tips

- Start broad, then narrow down
- Verify claims across multiple sources
- Prioritize primary sources (official docs, papers) over secondary (blogs, news)
- Note publication dates for recency
- Flag uncertain or unverified information