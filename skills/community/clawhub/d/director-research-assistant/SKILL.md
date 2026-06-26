---
name: research-assistant
description: Conduct web research on any topic, summarize findings, and create structured reports. Use when user wants to (1) research a topic online, (2) get summaries of articles or documents, (3) create a report on a subject, (4) compare options or alternatives, (5) gather competitive intelligence, or (6) find recent news/trends on a topic.
---

# Research Assistant

Conduct thorough web research and create actionable reports.

## Workflow

### 1. Gather Information
Use web_search (Perplexity) for comprehensive results:
```
Search query: <topic> + "2024" or "latest" for recent info
```

### 2. Extract Key Sources
- Fetch top 3-5 URLs using web_fetch
- Extract main points from each source
- Note publication dates and credibility

### 3. Synthesize Findings
- Identify common themes
- Note conflicting information
- Find statistics and data points

### 4. Structure Report
Create organized output with:
1. **Executive Summary** - 2-3 sentence overview
2. **Key Findings** - Numbered list of main discoveries
3. **Details** - Expanded explanation of each finding
4. **Sources** - Links to references
5. **Next Steps** - Recommended actions (if applicable)

## Research Types

### Competitive Analysis
```
Focus: Competitor features, pricing, market position
Output: Comparison table + recommendations
```

### Technology Research
```
Focus: Capabilities, limitations, adoption, alternatives
Output: Technical overview + decision matrix
```

### Market Research
```
Focus: Size, growth, trends, key players
Output: Statistics + trend analysis
```

### News/Trends
```
Focus: Recent developments, emerging patterns
Output: Timeline + impact assessment
```

## Best Practices

- **Cite sources** - Always include links
- **Date everything** - "As of [date]..."
- **Distinguish fact from opinion** - Use "reportedly" for unconfirmed
- **Quantify when possible** - Numbers > adjectives
- **Flag gaps** - Note when information is limited

## Output Example

```
# Research: AI Coding Assistants (April 2026)

## Summary
The AI coding assistant market has matured with 3 dominant players...

## Key Findings
1. GitHub Copilot leads with 2M+ paid subscribers
2. Cursor. AI gained 500K users in 6 months
3. New entrants focus on enterprise compliance

## Sources
- [TechCrunch](link) - March 2026
- [Andreessen Horowitz](link) - February 2026

## Recommendations
- For individuals: Start with free Cursor tier
- For enterprises: Evaluate GitHub Copilot Business
```
