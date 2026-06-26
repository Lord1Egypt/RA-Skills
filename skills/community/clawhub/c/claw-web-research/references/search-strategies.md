# Search Strategies for Web Research

## Query Construction Rules

### Primary Strategy
1. Start broad, narrow gradually
2. Use natural language queries (self-hosted SearXNG supports this)
3. Vary phrasing across 3-5 search variants
4. Include year constraints when recency matters

### Query Patterns

| Scenario | Pattern | Example |
|----------|---------|---------|
| Market size | `"<industry>" market size 2025 OR 2026` | `"AI agents" market size 2025` |
| Competitor analysis | `"company" vs "competitor" comparison` | `"OpenClaw" vs "OpenHands" comparison` |
| Technical specs | `"<product>" features limitations` | `"web scraping API" limitations` |
| Pricing research | `"<service>" pricing plans` | `"freelance platform" pricing 2025` |
| Trends | `"<topic>" trends 2025 OR 2026` | `"AI automation" trends 2025` |
| Expert opinion | `"<topic>" expert analysis site:.edu OR site:.org` | `"open source agents" analysis site:.edu` |

### Search Categories to Use
- `general` — default broad search
- `news` — recent developments
- `science` — academic/research sources
- `it` — technical topics

### When to Use web_fetch vs web_search
- **web_search first** — get overview, identify relevant sources
- **web_fetch second** — extract detailed content from top 3-5 results
- **Limit:** max 10 results per search, max 10000 chars per fetch

## Avoiding Common Pitfalls

1. Don't trust first result — check 3+ sources
2. Check publication dates (especially for fast-moving topics)
3. Look for primary sources (not just summaries of summaries)
4. Flag sponsored/paid content
5. Note when sources are conflicting or outdated
