---
name: check-ai-crawler-access
description: Check which search and AI crawlers (GPTBot, ClaudeBot, PerplexityBot, CCBot, Google-Extended and more) a website's robots.txt allows. Use when someone asks why an AI assistant cannot see or cite a site.
---

# Check AI crawler access

Use the Why Won't AI MCP server to read a site's robots.txt the way 17 search and AI crawlers do.

## Connect

- MCP endpoint: `https://mcp.whywontai.com/` (Streamable HTTP, stateless, JSON responses)
- No API key is needed for `check_robots`. Without a key it is limited to 30 calls a day per IP address.

## Steps

1. Call the `check_robots` tool with the site URL. Add a page path to check one page instead of the home page.
2. For each crawler, read whether it is allowed and the robots.txt line that decides it.
3. Tell the user which crawlers are blocked and which line blocks them.

## Without MCP

People can use the same check in a browser at https://whywontai.com/ai-crawler-robots-txt-checker.

## Limits

A robots.txt allow does not prove that a crawler can read the page. A firewall, bot protection or a JavaScript-only page can still block it. Run a full scan to check that.
