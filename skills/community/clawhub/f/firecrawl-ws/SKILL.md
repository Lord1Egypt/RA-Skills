---
name: firecrawl
description: AI-native web scraping, crawling, domain mapping, and structured extraction. Use for converting websites into LLM-ready Markdown, scraping pages with dynamic JS/actions, crawling full domains, or extracting schema-based structured JSON.
---

# Firecrawl Skill

This skill extends Manus with the capability to search, scrape, crawl, and extract structured data from any website using **Firecrawl** [1] [2].

*   **Author:** Simon-Pierre Boucher
*   **Target Audience:** AI Engineers, Agent Developers, Data Engineers, Web Scraping Engineers

---

## 1. Core Workflows

### 1.1 Scraping a Single URL (`/scrape`)
Use when you need the text content, Markdown, HTML, or screenshots of a specific webpage [2].
1.  Initialize the Firecrawl client with your API key [1].
2.  Specify output `formats` (e.g., `["markdown"]` or `["markdown", "screenshot"]`) [2].
3.  Apply custom browser actions (e.g., click, wait, write) if the page has dynamic content or requires interaction [2].
4.  Optionally filter the DOM using `includeTags` or `excludeTags` [2].

### 1.2 Crawling a Domain (`/crawl`)
Use when you need to discover and scrape all pages under a specific domain or path recursively [1] [2].
1.  Start an asynchronous crawl job by specifying the starting `url` [2].
2.  Set depth limits (`maxDepth`) and page limits (`limit`) to control token and credit usage [2].
3.  Configure `scrapeOptions` to ensure each crawled page is parsed with the correct format (e.g., Markdown only) [2].
4.  Poll the crawl status using the `jobId` until completed [2].

### 1.3 Mapping a Domain (`/map`)
Use when you need to quickly discover all URLs belonging to a domain without scraping page content [1] [2].
1.  Provide the base `url` [2].
2.  Optionally provide a `search` filter to only return URLs matching a specific keyword or path [2].
3.  Set `includeSubdomains` to `true` if you need sub-domain discovery [2].

### 1.4 Structured Extraction (`/extract`)
Use when you need to parse raw web pages and extract structured JSON data conforming to a specific schema [3].
1.  Provide an array of `urls` and a natural language extraction `prompt` [3].
2.  Define the target schema using a **JSON Schema**, **Pydantic model** (Python), or **Zod schema** (TypeScript) [3].
3.  Run the extraction to retrieve guaranteed, type-safe JSON [3].

---

## 2. Resource Guides

For comprehensive API parameters, SDK code templates, and configuration options, read the following reference files:
*   **API Reference & SDK Snippets:** Read `references/api_reference.md` for complete endpoint request/response schemas, Python SDK templates, and TypeScript/Zod snippets.
*   **Self-Hosting & Docker:** Read `references/self_hosting.md` for production-ready Docker Compose configurations, environment variables, and scaling guidelines.

---

## 3. Best Practices & Anti-Patterns

### 3.1 Best Practices
*   **Always use `onlyMainContent: true`** to strip out navigation bars, headers, and footers. This dramatically reduces downstream LLM token costs and keeps context windows clean [2].
*   **Leverage `/map` before `/crawl`** if you only need to discover pages or filter specific URLs to scrape. Mapping is significantly faster and cheaper than full crawls [1] [2].
*   **Implement exponential backoff with jitter** when handling rate limits (`429`) or transient server errors (`5xx`) to ensure scraping resiliency [4].
*   **Set explicit CPU and RAM limits** on your containers if self-hosting to prevent headless Chromium from consuming all host system resources [5].

### 3.2 Anti-Patterns
*   **Do not use hard-coded `waitFor` delays** when scraping dynamic content. Instead, use selector-based waits (e.g., `{"type": "wait", "selector": "#loaded-element"}`) to minimize request latency [2].
*   **Do not run synchronous crawls.** Crawling is an inherently long-running process; always use the asynchronous `/crawl` endpoint and poll for results or use webhooks [2].
*   **Do not reuse browser sessions across unrelated scraping tasks** if security isolation is required. Firecrawl relies on ephemeral containers to prevent session contamination [5].

---

## References
[1] Firecrawl Homepage, "The API to search, scrape, and interact with the web at scale." URL: https://github.com/firecrawl/firecrawl  
[2] Firecrawl Documentation, "Advanced Scraping Guide." URL: https://docs.firecrawl.dev/advanced-scraping-guide  
[3] Firecrawl Documentation, "Agent Endpoint." URL: https://docs.firecrawl.dev/features/agent  
[4] Firecrawl Documentation, "Rate Limits." URL: https://docs.firecrawl.dev/rate-limits  
[5] Firecrawl GitHub Repository, "Self-hosting Firecrawl Guide." URL: https://raw.githubusercontent.com/firecrawl/firecrawl/main/SELF_HOST.md
