# Web Scraping Reference

Complete reference for web scraping operations via `bdata scrape`.

## Command Syntax

```bash
bdata scrape <url> [options]
```

## All Options

| Flag | Description | Default |
|------|-------------|---------|
| `-f, --format <fmt>` | Output format: `markdown`, `html`, `screenshot`, `json` | `markdown` |
| `--country <code>` | ISO country code for geo-targeting | *(none)* |
| `--zone <name>` | Web Unlocker zone name | stored default |
| `--mobile` | Use a mobile user agent | *(off)* |
| `--async` | Submit async, return a snapshot ID | *(off)* |
| `-o, --output <path>` | Write output to file | stdout |
| `--json` | Force JSON output | *(off)* |
| `--pretty` | Pretty-print JSON output | *(off)* |
| `-k, --api-key <key>` | Override API key | stored default |
| `--timing` | Show request timing info | *(off)* |

## Output Formats

### Markdown (default)
Clean, readable markdown extracted from the page. Best for reading content, documentation, articles.

```bash
bdata scrape https://docs.example.com/getting-started
```

### HTML
Raw HTML source. Best for debugging, custom parsing, or when you need the exact DOM structure.

```bash
bdata scrape https://example.com -f html
```

### JSON
Structured JSON representation of the page. Best for programmatic processing.

```bash
bdata scrape https://example.com -f json
```

### Screenshot
PNG screenshot of the rendered page. Best for visual verification, design comparison, evidence capture.

```bash
bdata scrape https://example.com -f screenshot -o page.png
```

## What Gets Handled Automatically

Every `bdata scrape` request automatically:
- **Rotates proxies** — residential IPs from 195+ countries
- **Renders JavaScript** — SPAs, React, Vue, Angular all work
- **Solves CAPTCHAs** — reCAPTCHA, hCaptcha, Cloudflare, etc.
- **Bypasses bot detection** — fingerprint rotation, header management
- **Retries on failure** — intelligent retry with different configurations
- **Returns clean output** — noise (nav, ads, cookie banners) stripped in markdown mode

## Scraping Patterns

### Read Documentation
```bash
# JS-rendered docs (Docusaurus, GitBook, Nextra)
bdata scrape https://docs.example.com/api-reference

# GitHub READMEs
bdata scrape https://github.com/org/repo
```

### Read News / Articles
```bash
# News articles (bypasses soft paywalls)
bdata scrape https://techcrunch.com/2026/03/23/article-slug

# Blog posts
bdata scrape https://blog.example.com/post-title
```

### Geo-Targeted Browsing
```bash
# See US prices on Amazon
bdata scrape https://amazon.com/dp/B09V3KXJPB --country us

# See UK version of a site
bdata scrape https://example.co.uk --country gb

# See Japanese version
bdata scrape https://example.com --country jp
```

### Mobile vs Desktop
```bash
# Desktop (default)
bdata scrape https://example.com

# Mobile user agent
bdata scrape https://example.com --mobile
```

### Capture Visual Evidence
```bash
# Full-page screenshot
bdata scrape https://competitor.com/pricing -f screenshot -o pricing.png

# Screenshot for design comparison
bdata scrape https://example.com -f screenshot -o current-design.png
```

### Async for Heavy Pages
```bash
# Submit async
bdata scrape https://heavy-page.com --async
# Returns: snapshot_id: s_abc123

# Check status
bdata status s_abc123 --wait
```

### Batch Scraping (shell)
```bash
# Scrape multiple URLs from a file
cat urls.txt | xargs -I{} bdata scrape {} -o "output/{}.md"

# Parallel scraping (5 concurrent)
cat urls.txt | xargs -P5 -I{} bdata scrape {} --json -o "output/{}.json"
```

### Pipe to Tools
```bash
# Pipe to markdown viewer
bdata scrape https://docs.example.com | glow -

# Pipe to less for paging
bdata scrape https://long-page.com | less

# Pipe HTML to a parser
bdata scrape https://example.com -f html | python3 parse.py
```

## When to Use Scrape vs Pipelines

| Scenario | Use |
|----------|-----|
| Read any arbitrary webpage | `bdata scrape` |
| Get structured data from a known platform (Amazon, LinkedIn, etc.) | `bdata pipelines` |
| Read documentation or articles | `bdata scrape` |
| Extract product details from Amazon | `bdata pipelines amazon_product` |
| Take a screenshot | `bdata scrape -f screenshot` |
| Get raw HTML for custom parsing | `bdata scrape -f html` |

**Rule**: If a pipeline extractor exists for the target platform, always prefer `bdata pipelines` — it returns structured, typed JSON without parsing. Use `bdata scrape` for everything else.

## Tips

- **Markdown is the best default for agents** — clean, readable, no HTML noise.
- **Use `-o` for screenshots** — screenshots write binary data; always specify an output file.
- **Geo-targeting affects content** — prices, availability, language, and even page layout change by country.
- **Async for reliability** — if a page is slow or complex, `--async` prevents timeouts.
- **Combine with `--json`** — when piping to other tools, JSON is more reliable than markdown.
