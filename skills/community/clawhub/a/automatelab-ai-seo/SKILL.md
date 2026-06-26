---
name: ai-seo
description: Use when the user wants to audit a URL for AI citation eligibility, check why AI systems don't cite their pages, score AI Overview or citation worthiness, generate or validate an llms.txt file, rewrite content for AEO/GEO, extract named entities, or diff two page versions for SEO regressions. No API keys required.
version: 0.5.0
license: MIT
homepage: https://github.com/AutomateLab-tech/ai-seo-mcp
compatibility:
  hosts:
    - claude-code
    - cursor
    - claude-desktop
    - windsurf
    - vscode
    - zed
    - continue
    - cline
    - jetbrains
    - warp
metadata:
  npm: "@automatelab/ai-seo-mcp"
  mcpName: io.github.AutomateLab-tech/ai-seo-mcp
---

# ai-seo

Pairs with the `@automatelab/ai-seo-mcp` server (14 tools). Audits why AI systems do or do not cite a page — structured answer extraction, schema completeness, crawler access, `llms.txt`, canonical hygiene — and generates fixes.

## When to use which tool

**Start here:** `audit_page` composes all 14 checks in one call and returns a ranked list of citation-blockers with specific fixes. Use it as the default entry point.

**Drill into a specific dimension:**

| Tool | Use when |
|---|---|
| `audit_schema` | User asks about structured data, JSON-LD, or schema.org coverage |
| `audit_canonical` | Checking canonical URL, `og:url`, `hreflang`, or noindex traps |
| `check_robots` | Verifying GPTBot / ClaudeBot / PerplexityBot / OAI-SearchBot are allowed |
| `check_sitemap` | Checking `lastmod` freshness signals and sitemap coverage |
| `check_technical` | Core Web Vitals signals, crawl accessibility, redirect chains |
| `score_ai_overview_eligibility` | "Will this page appear in Google AI Overviews?" |
| `score_citation_worthiness` | Cross-engine citation probability score |
| `generate_llms_txt` | Create an `llms.txt` for the site |
| `validate_llms_txt` | Validate an existing `llms.txt` against the spec |
| `rewrite_for_aeo` | Rewrite a page section for Answer Engine Optimization |
| `rewrite_for_geo` | Rewrite a page section for Generative Engine Optimization |
| `extract_entities` | Check named entity density and `sameAs` coverage |
| `diff_pages` | Compare two versions of a page for SEO regressions |

## Default workflow

```
User: "Audit https://example.com/my-post"
→ audit_page(url)          # full citation-blocker report
→ Read findings, prioritize by severity
→ For fixable issues, call the specific tool (e.g. rewrite_for_aeo) or draft inline edits
```

## Server setup

Add to your MCP config:

**Claude Code** (`.claude/mcp.json`):
```json
{
  "mcpServers": {
    "ai-seo": {
      "command": "npx",
      "args": ["-y", "@automatelab/ai-seo-mcp"]
    }
  }
}
```

**Claude Desktop** (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "ai-seo": {
      "command": "npx",
      "args": ["-y", "@automatelab/ai-seo-mcp"]
    }
  }
}
```

Requires Node 20+. No API keys needed — all checks are read-only HTTP fetches against the target URL.

---

Developed by [AutomateLab](https://automatelab.tech). Source: [github.com/AutomateLab-tech/ai-seo-mcp](https://github.com/AutomateLab-tech/ai-seo-mcp).
