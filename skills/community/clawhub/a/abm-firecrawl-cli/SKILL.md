---
name: firecrawl-cli
description: "When the user wants to scrape, crawl, or extract content from websites. Also use when the user mentions 'scrape site,' 'crawl website,' 'extract content,' 'web scraping,' 'site map,' 'get page content,' 'extract data from website,' 'autonomous extraction,' or 'structured extraction.' Covers all Firecrawl CLI commands: scrape (single page), crawl (entire site), crawl-status (check job), map (sitemap/URL discovery), search (search + scrape), agent (autonomous data gathering), and extract (structured LLM extraction). For company research via web search, see exa-company-research."
metadata:
  version: 1.0.0
---

# Firecrawl CLI

You help users scrape, crawl, and extract content from websites using the Firecrawl CLI tool. You select the right subcommand for the task and handle async operations like crawling.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing-context.md` exists (or `.claude/product-marketing-context.md` in older setups), read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Then determine:

1. **Target URL(s)** — What site or page to extract content from
2. **What content to extract** — Full page, specific data, all pages on a site
3. **Single page vs full site** — One URL (scrape) or many pages (crawl)
4. **Search first?** — Does the user need to find pages before extracting content

---

## Command Reference

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `scrape` | Extract content from a single page | Need content from one specific URL |
| `crawl` | Crawl an entire site (async) | Need content from multiple pages on a site |
| `crawl-status` | Check a crawl job's progress | After starting a crawl, to poll for results |
| `map` | Discover all URLs on a site | Need to see what pages exist before scraping |
| `search` | Search the web and scrape results | Need to find relevant pages AND extract content |
| `agent` | Autonomous web data gathering | Need AI to find and extract data across multiple sites |
| `extract` | Structured data extraction with LLMs | Need specific structured data from one or more URLs |

---

## Workflow by Use Case

### Scraping a Single Page

```bash
firecrawl.js scrape --url "https://example.com/page"
```

**When:** You need content from one specific page. Returns markdown by default.

**Options:**
- `--formats markdown,html` — Choose output format(s), comma-separated
- `--only-main-content false` — Include headers, footers, navs (default: main content only)
- `--dry-run` — Preview the API request without sending it

**Example — extract a blog post as markdown:**
```bash
firecrawl.js scrape --url "https://example.com/blog/post-title"
```

**Example — get full HTML including navigation:**
```bash
firecrawl.js scrape --url "https://example.com" --formats html --only-main-content false
```

### Crawling an Entire Site

```bash
firecrawl.js crawl --url "https://example.com" --limit 50
```

**When:** You need content from multiple pages across a site. This is an **async operation** — the CLI starts a crawl job and returns a job ID.

**Options:**
- `--limit N` — Maximum number of pages to crawl
- `--max-depth N` — Maximum link depth from the starting URL
- `--poll` — Automatically poll for completion instead of returning the job ID
- `--dry-run` — Preview the API request without sending it

**Workflow without --poll:**
1. Start the crawl: `firecrawl.js crawl --url "https://example.com" --limit 20`
2. Note the returned job ID
3. Check status: `firecrawl.js crawl-status --id "job-id-here"`
4. Repeat step 3 until complete

**Workflow with --poll (recommended):**
```bash
firecrawl.js crawl --url "https://example.com" --limit 20 --poll
```
The CLI handles polling automatically and returns all results when done.

### Checking Crawl Status

```bash
firecrawl.js crawl-status --id "job-id-here"
```

**When:** You started a crawl without `--poll` and need to check if it finished.

### Getting a Site Map

```bash
firecrawl.js map --url "https://example.com"
```

**When:** You need to discover all URLs on a site before deciding what to scrape. Good first step before targeted scraping.

**Options:**
- `--search "term"` — Filter URLs containing a search term
- `--limit N` — Maximum number of URLs to return
- `--dry-run` — Preview the API request without sending it

**Example — find all blog pages:**
```bash
firecrawl.js map --url "https://example.com" --search "blog"
```

### Searching and Scraping

```bash
firecrawl.js search --query "site:example.com pricing plans"
```

**When:** You need to find relevant pages AND extract their content in one step. Combines web search with content extraction.

**Options:**
- `--limit N` — Number of results to return
- `--country "us"` — Country code for localized results
- `--dry-run` — Preview the API request without sending it

**Example — find competitor pricing pages:**
```bash
firecrawl.js search --query "competitor.com pricing" --limit 5
```

### Autonomous Agent Extraction

```bash
firecrawl.js agent --prompt "Find pricing information for Acme Corp" --poll
```

**When:** You need the AI to autonomously search, navigate, and gather data. No URLs required -- just describe what you need.

**Options:**
- `--prompt "..."` -- Describe what data to find (required, max 10000 chars)
- `--url "..."` -- Optionally constrain to a specific URL
- `--urls "url1,url2"` -- Optionally constrain to multiple URLs
- `--max-credits N` -- Set spending limit (default: 2500)
- `--poll` -- Wait for results instead of returning job ID
- `--dry-run` -- Preview the API request without sending it

**Example -- find competitor pricing:**
```bash
firecrawl.js agent --prompt "Find pricing tiers and plans for competitor.com" --url "https://competitor.com" --poll
```

### Extracting Structured Data

```bash
firecrawl.js extract --urls "https://example.com/pricing" --prompt "Extract pricing tiers with plan names and prices" --poll
```

**When:** You need specific structured data extracted from URLs using LLMs. Supports wildcards for domain-wide extraction.

**Options:**
- `--urls "url1,url2"` -- URLs to extract from, comma-separated (required). Supports `/*` wildcards
- `--prompt "..."` -- Describe what data to extract
- `--schema '{"type":"object",...}'` -- JSON schema for structured output
- `--enable-web-search` -- Follow external links during extraction
- `--poll` -- Wait for results instead of returning job ID
- `--dry-run` -- Preview the API request without sending it

**Example -- extract product data from multiple pages:**
```bash
firecrawl.js extract --urls "https://example.com/products/*" --prompt "Extract product names, prices, and descriptions" --poll
```

---

## Choosing the Right Command

- **Need one page?** → `scrape`
- **Need the whole site?** → `crawl` with `--limit` and `--poll`
- **Need to discover URLs first?** → `map`, then `scrape` specific pages
- **Need search + content?** → `search`
- **Started a crawl and need results?** → `crawl-status`
- **Need AI to find data autonomously?** → `agent` with `--poll`
- **Need structured data from known URLs?** → `extract` with `--prompt` and `--poll`

**Common multi-step workflows:**

1. **Targeted extraction:** `map` → review URLs → `scrape` specific pages
2. **Full site dump:** `crawl --poll --limit 100`
3. **Research a topic:** `search` → review results → `scrape` for deeper content

---

## Output Format

Present extracted content with clear structure:

- **Source URL** — Always include the URL the content came from
- **Extraction method** — Note which command was used (scrape, crawl, search)
- **Content** — The extracted markdown/HTML content

For crawl results with multiple pages, organize by page with clear headers:

```
### Page 1: [title] (https://example.com/page-1)
[content]

### Page 2: [title] (https://example.com/page-2)
[content]
```

---

## Environment Setup

The Firecrawl CLI requires a `FIRECRAWL_API_KEY` environment variable. If the key is not set, the CLI will return an error. The user needs to:

1. Get an API key from [firecrawl.dev](https://firecrawl.dev)
2. Set it in their environment: `export FIRECRAWL_API_KEY="fc-..."`

Use `--dry-run` on any command to preview the API request without needing a key.

---

## Related Skills

- **exa-company-research** — For web search and company research (search-focused, not scraping)
- **seo-audit** — Uses Firecrawl for schema detection and technical SEO analysis
- **competitive-intelligence** — Combines Exa search + Firecrawl scraping for competitive analysis (Phase 4)
