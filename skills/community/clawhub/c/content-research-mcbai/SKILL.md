---
name: content-research
description: Research and discover trending content sources for any topic using web search. Use this skill whenever the user wants to find articles, news, blog posts, or trending content about a specific topic for content creation, LinkedIn posts, social media writing, or content curation. Also trigger when the user mentions "research topic", "find articles about", "trending news", "content sources", "search for content", or wants to gather data/sources before writing posts.
---

# Content Research Skill

## Installation

```bash
npx clawhub@latest install content-research-mcbai
```

Search the web for trending articles, news, and content sources on any topic. This skill powers the MCB AI content research pipeline — finding, filtering, scoring, and organizing source material for content creation.

## Search Strategy: Brave + Tavily Dual-Engine

This skill uses TWO search providers in parallel for maximum coverage:

- **Brave Search** — via `web_search` tool (built-in OpenClaw tool)
- **Tavily** — via direct API call using `TAVILY_API_KEY` from `~/.openclaw/.env`

### Tavily API Call

```
POST https://api.tavily.com/search
Headers: Content-Type: application/json
Body:
{
  "api_key": "<TAVILY_API_KEY>",
  "query": "<query>",
  "search_depth": "advanced",
  "include_answer": false,
  "include_raw_content": false,
  "max_results": 10,
  "topic": "news"   // use "general" for non-news searches
}
```

Run Tavily via `exec` with PowerShell:
```powershell
$body = @{
  api_key = $env:TAVILY_API_KEY
  query = "<query>"
  search_depth = "advanced"
  include_answer = $false
  include_raw_content = $false
  max_results = 10
  topic = "news"
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://api.tavily.com/search" -Method Post -ContentType "application/json" -Body $body
```

### Fallback Logic

- Run Brave (`web_search`) and Tavily in parallel
- If Brave fails → use Tavily results only
- If Tavily fails → use Brave results only
- If both succeed → merge and deduplicate by URL

## When to Use

- User wants to research a topic before writing content
- User needs to find recent articles, news, or data about a subject
- User wants to discover trending content sources for LinkedIn/social media
- User needs to curate sources for a toplist, POV, case study, or how-to post

## Core Workflow

### Step 1: Understand the Research Request

Extract from the user's message:
1. **Topic** — the subject to research (required)
2. **Source filter** — where to search (default: all sources)
   - `all` — All web sources
   - `news` — News publications only
   - `linkedin` — LinkedIn posts/articles (append `site:linkedin.com`)
   - `youtube` — YouTube videos (append `site:youtube.com`)
   - `blogs` — Blog posts and articles (append `blog OR article OR guide`)
3. **Freshness** — how recent (default: past month for web, past week for news)
4. **Count** — how many results to return (default: 10-15)

If the user doesn't specify these, use sensible defaults and mention what you chose.

### Step 2: Execute Dual Search (Brave + Tavily)

Run BOTH providers. Each provider runs TWO queries when possible.

#### Brave Search (web_search tool)

**Query 1 — Web:**
```
Query: {topic} {source_filter_query}
count: 10
freshness: month
```

**Query 2 — News:**
```
Query: {topic} news
count: 10
freshness: week
```

#### Tavily Search (exec PowerShell)

**Query 1 — General:**
```powershell
$env:TAVILY_API_KEY = (Get-Content "$env:USERPROFILE\.openclaw\.env" | Select-String "TAVILY_API_KEY" | ForEach-Object { $_ -replace "TAVILY_API_KEY=", "" })

$body = @{
  api_key = $env:TAVILY_API_KEY.Trim()
  query = "{topic}"
  search_depth = "advanced"
  include_answer = $false
  include_raw_content = $false
  max_results = 10
  topic = "general"
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://api.tavily.com/search" -Method Post -ContentType "application/json" -Body $body
```

**Query 2 — News:**
```powershell
# Same as above but topic = "news"
```

### Step 3: Merge and Deduplicate

1. Collect all results from Brave (web + news) and Tavily (general + news)
2. **Deduplicate** by URL — keep one copy per URL, prefer Tavily version (richer content)
3. **Sort** by relevance:
   - News articles first (most time-sensitive)
   - Then by freshness (most recent first)
4. **Limit** to requested count (default 15)
5. **Label source engine** in metadata: `[Brave]` or `[Tavily]`

### Step 4: Process and Organize Results

For each result, extract and structure:

```
Article:
  - Title: [article title]
  - Source: [publication/website name]
  - URL: [full URL]
  - Date: [relative date, e.g. "2 hours ago", "3 days ago"]
  - Summary: [description/snippet from search]
  - Type: [News / Blog / Report / Video / LinkedIn]
  - Tag: [auto-detected tag, see Tag Rules below]
  - Engine: [Brave / Tavily / Both]
```

#### Source Name Extraction
Clean the hostname to a readable name:
- Remove `www.` prefix
- Remove `.com`, `.org`, `.net`, `.io`, `.co` suffixes
- Map known domains: techcrunch → TechCrunch, crunchbase → Crunchbase, forbes → Forbes, bloomberg → Bloomberg, reuters → Reuters, etc.

#### Auto-Tag Rules
Scan title + summary and apply the FIRST matching tag:

| Tag | Pattern Keywords |
|-----|-----------------|
| Funding | fund, raise, round, series A-C, seed, valuation, invest, VC, venture |
| AI | ai, artificial intelligence, machine learning, LLM, GPT, Claude, OpenAI |
| SaaS | saas, software as a service, subscription, ARR, MRR |
| Tools | tool, platform, app, software, stack, framework |
| Trends | trend, report, survey, data, statistic, forecast, prediction |
| Startup | startup, founder, launch, accelerator, incubator, YC |
| Growth | growth, marketing, GTM, acquisition, retention, conversion |

### Step 5: Present Results

Present the organized results in a clear, scannable format:

```
## Research Results: "{topic}"
Found {N} articles from {sources_count} sources
Sources: Brave ({brave_count}) + Tavily ({tavily_count}) → merged {total} unique

### 📰 News
1. **{title}** — {source} ({date}) [{engine}]
   {summary}
   🏷️ {tag} | 🔗 {url}

### 📝 Articles & Blogs
2. **{title}** — {source} ({date}) [{engine}]
   {summary}
   🏷️ {tag} | 🔗 {url}

...
```

Then ask the user which articles they want to use for content creation. If the user wants to proceed to writing, hand off to the `content-writer` skill with the selected articles.

## Output Format

Always provide results as a numbered list with:
- Clear title
- Source name and date
- Engine label [Brave] or [Tavily]
- Brief summary (1-2 lines)
- Auto-detected tag
- Source URL

## Tips for Better Research

- For funding/startup topics: search for specific company names + "funding" or "series"
- For trend pieces: include year/quarter in the search (e.g., "AI trends Q1 2026")
- For competitive analysis: search for specific company + "vs" or "alternative"
- For LinkedIn content: recent news performs best (past 1-2 weeks)
- Combine multiple source types for richer content
- Tavily `search_depth: "advanced"` digs deeper — use for complex topics
- If one engine returns fewer results than expected, note it in the summary

## Integration with Content Writer

After research, the user typically selects articles and moves to writing. Pass the selected articles to the content-writer skill in this format:

```json
{
  "articles": [
    {
      "title": "Article title",
      "source": "Publication name",
      "url": "https://...",
      "date": "2 days ago",
      "summary": "Brief description",
      "tag": "AI",
      "engine": "Tavily"
    }
  ]
}
```

See `references/source-filters.md` for detailed source filter configurations.


