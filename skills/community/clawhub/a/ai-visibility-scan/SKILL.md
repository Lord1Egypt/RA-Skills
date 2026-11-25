---
name: ai-visibility-scan
description: Run a Why Won't AI scan of a website and report its SEO, AEO and GEO score and issues. Use when someone asks why AI assistants or search engines do not mention or show their product.
---

# Run an AI visibility scan

The scan requests each page as Googlebot, Bingbot, GPTBot, ClaudeBot, PerplexityBot and CCBot, compares that with a rendered view and scores six categories.

## Connect

- MCP endpoint: `https://mcp.whywontai.com/` (Streamable HTTP)
- Send an API key as `Authorization: Bearer wwai_...`. The user creates the key in their whywontai.com dashboard under MCP & API. A free account works. Scans use the limits of the account's plan.

## Steps

1. Call `scan_site` with the site URL. Keep the returned scan ID.
2. Call `get_scan` with the scan ID. Set `wait_seconds` (up to 25) and call again until the status is complete.
3. Call `list_issues` to get every issue, most severe first. Filter by severity or category if the user asks.
4. Report the score, the most severe issues and the example URLs. Credit the Domain Rating as "Domain Rating by Ahrefs".

## Without a key

Only `check_robots` works without a key. A person can run a free scan at https://whywontai.com/ with no account.

## Limits

Do not promise rankings or AI mentions. A good score removes known blockers; it does not guarantee that an assistant will cite the site.
