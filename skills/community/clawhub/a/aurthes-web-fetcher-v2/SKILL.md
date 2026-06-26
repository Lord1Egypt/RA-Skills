---
name: web-fetcher
version: 1.2.0
description: Fetch web pages and extract readable content for AI use. Use when reading, summarizing, or crawling a specific URL or small set of URLs. Prefer low-friction URL-to-Markdown services first, then fall back to browser-based retrieval, search snippets, or cached/indexed copies when sites are protected by Cloudflare or similar bot checks.
---

# Web Fetcher

Fetch readable web content with a reliability-first fallback chain.

## Core rule

Do **not** promise direct access to every site. Some sites use Cloudflare, login walls, bot detection, or legal restrictions. In those cases, switch to the next fallback instead of insisting the first method should work.

## Preferred fetch order

### 1) Direct readable fetch

Try lightweight conversion services first:

1. **r.jina.ai**
   ```
   https://r.jina.ai/http://example.com
   ```

2. **markdown.new**
   ```
   https://markdown.new/https://example.com
   ```

3. **defuddle**
   ```
   https://defuddle.md/https://example.com
   ```

For deterministic retries, use the bundled script:

```bash
python {baseDir}/scripts/fetch_url.py "https://example.com/article"
```

The script returns JSON with:
- chosen method
- attempt history
- blocked/thin-content detection
- final content when successful

Use these when the user wants article text, page summaries, or structured extraction from normal public pages.

### 2) Detect failure modes early

Treat the fetch as failed or unreliable if you see signs like:

- `Just a moment...`
- `Performing security verification`
- `Enable JavaScript and cookies`
- CAPTCHA / challenge pages
- login wall instead of target content
- obvious truncation / missing article body

When this happens, **stop treating the result as the page content**.

### 3) Browser fallback for protected sites

For sites blocked behind Cloudflare or requiring real browser execution:

- Prefer a real browser session via OpenClaw browser tools when available.
- If the user is using the Chrome relay/extension, ask them to attach the tab and then inspect the live rendered page.
- Snapshot the page and extract only the needed fields.

Use browser fallback for:
- JS-heavy pages
- Cloudflare-protected pages
- sites that render key content after load
- pages where the direct markdown services return verification screens

### 4) Search / indexed fallback

If direct fetch and browser fetch are not available or still fail:

- search for the exact page / journal / article title
- use search snippets, publisher mirror pages, cached summaries, or secondary sources
- prefer official publisher pages when search can surface the needed field
- clearly label data as secondary-source derived if it was not read directly from the target page

This is often enough for metadata tasks like:
- editor-in-chief names
- journal impact factors
- publication frequency
- ISSN
- institutional affiliations

### 5) Partial-completion mode

If a site is inconsistent, return a mixed result instead of stalling:

- fill the rows that can be verified directly
- mark blocked / unresolved rows clearly
- explain what failed and which fallback was used

## Practical extraction strategy

### For one page

1. Try `r.jina.ai`
2. If blocked, try `markdown.new`
3. If blocked, try `defuddle`
4. If still blocked, use browser tools
5. If browser unavailable, use search/indexed fallback
6. Report confidence level

### For many similar pages

1. Fetch the index/list page first
2. Extract all target URLs or codes
3. Process pages in batches
4. Record success/failure per row
5. Retry only failures with stronger fallback methods
6. Deliver the best complete table possible

## Output guidance

When extracting structured data, prefer columns like:

- source URL
- extraction method (`direct`, `browser`, `search`, `secondary`)
- confidence (`high`, `medium`, `low`)
- note for blocked/unverified rows

## Examples

- User: "Read this article" → direct fetch first
- User: "What does this page say?" → direct fetch, then browser fallback if blocked
- User: "Crawl this journal site" → index page first, then batched extraction with fallback chain
- User: "Cloudflare blocked it" → switch to browser or search fallback, do not keep retrying the same failed method
