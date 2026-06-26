---
name: dfseo
description: "SEO data from the terminal using DataForSEO APIs. Use when the user asks to check keyword rankings, analyze SERPs, run site audits, check backlink profiles, find keyword opportunities, compare competitors, do link gap analysis, check keyword difficulty or search volume, audit on-page SEO, or get Lighthouse scores. Triggers on: 'SEO', 'SERP', 'keyword research', 'backlinks', 'site audit', 'keyword difficulty', 'search volume', 'link building', 'competitor analysis', 'on-page SEO', 'Lighthouse', 'keyword ranking', 'referring domains', 'anchor text'."
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      bins:
        - dfseo
      env:
        - DATAFORSEO_LOGIN
        - DATAFORSEO_PASSWORD
    install:
      - id: pip
        kind: pip
        package: dfseo
        bins:
          - dfseo
        label: "Install dfseo CLI (pip)"
---

# dfseo-cli — SEO Data from Your Terminal

A CLI tool wrapping DataForSEO APIs. 43+ commands for SERP analysis, keyword research, site audits, and backlink analysis. All output is JSON by default (machine-readable). Add `--output table` for human-readable format.

## Authentication

Requires DataForSEO API credentials. Set them as environment variables:

```bash
export DATAFORSEO_LOGIN="your@email.com"
export DATAFORSEO_PASSWORD="your_api_password"
```

Or run `dfseo auth setup` for interactive configuration (saves to `~/.config/dfseo/config.toml`).

Verify with: `dfseo auth status`

## Quick Reference

### SERP Analysis

```bash
# Google SERP for any keyword + location
dfseo serp google "keyword" --location "Country" --language "Language"

# Compare Google vs Bing
dfseo serp compare "keyword" --engines google,bing

# YouTube results
dfseo serp youtube "keyword"

# SERP features only (featured snippets, PAA, etc.)
dfseo serp google "keyword" --features-only
```

### Keyword Research

```bash
# Volume, CPC, difficulty, search intent (up to 700 keywords)
dfseo keywords volume "kw1" "kw2" --location "Country" --include-serp-info

# Long-tail suggestions
dfseo keywords suggestions "seed keyword" --min-volume 100 --max-difficulty 40

# Semantically related keywords
dfseo keywords ideas "seed1" "seed2" --limit 100

# Bulk difficulty check (up to 1000)
dfseo keywords difficulty "kw1" "kw2" "kw3"
dfseo keywords difficulty --from-file keywords.txt

# Keywords a domain ranks for
dfseo keywords for-site "domain.com" --min-volume 50 --sort volume
```

### Site Audit

```bash
# Full audit (crawl + wait + summary)
dfseo site audit "domain.com" --max-pages 100

# Quick single-page check (uses Instant Pages API, no polling)
dfseo site instant "https://domain.com/page"

# Drill down after audit
dfseo site pages "$TASK_ID" --errors-only
dfseo site links "$TASK_ID" --type broken
dfseo site duplicates "$TASK_ID" --type title

# Lighthouse performance
dfseo site lighthouse "https://domain.com" --categories performance,seo
```

### Backlink Analysis

```bash
# Backlink profile summary
dfseo backlinks summary "domain.com"

# List backlinks (new, lost, broken)
dfseo backlinks list "domain.com" --dofollow-only --sort rank
dfseo backlinks list "domain.com" --status new
dfseo backlinks list "domain.com" --status lost

# Anchor text analysis
dfseo backlinks anchors "domain.com" --search "brand" --sort backlinks

# Link gap: who links to competitors but not to you
dfseo backlinks gap "your-site.com" "competitor1.com" "competitor2.com"

# Bulk rank comparison (up to 1000 domains)
dfseo backlinks bulk ranks "site1.com" "site2.com" "site3.com"
dfseo backlinks bulk ranks --from-file domains.txt

# Historical backlink data (since 2019)
dfseo backlinks history "domain.com" --from 2024-01 --to 2026-03
```

## Output Conventions

- **Default output: JSON on stdout** — always parseable, no decorative text
- **Errors and progress: stderr** — never mixed with results
- **`--output table`** — human-readable formatted tables
- **`--output csv`** — for spreadsheets and data pipelines
- **`-q` / `--quiet`** — suppress everything except the result
- **`--dry-run`** — show estimated cost without executing

Exit codes: 0 = success, 1 = error, 2 = auth failed, 3 = rate limited, 4 = bad params, 5 = insufficient funds.

## Common Patterns

### Keyword research workflow

```bash
# 1. Get seed keyword data
dfseo keywords volume "email hosting" --location "Italy" --language "Italian" --include-serp-info

# 2. Expand with suggestions
dfseo keywords suggestions "email hosting" --min-volume 50 --max-difficulty 40 --limit 50

# 3. Check difficulty for best candidates
dfseo keywords difficulty "email hosting professionale" "hosting email aziendale" --location "Italy"
```

### Competitor analysis workflow

```bash
# 1. Check competitor SERP presence
dfseo serp google "target keyword" --location "Italy" --depth 100

# 2. Find their keywords
dfseo keywords for-site "competitor.com" --location "Italy" --min-volume 100

# 3. Analyze their backlinks
dfseo backlinks summary "competitor.com"

# 4. Find link gap opportunities
dfseo backlinks gap "your-site.com" "competitor.com" --min-rank 200
```

### Site health check

```bash
# 1. Full audit
dfseo site audit "domain.com" --max-pages 200

# 2. Performance check
dfseo site lighthouse "https://domain.com"

# 3. Check for broken links
dfseo site links "$TASK_ID" --type broken
```

## Service References

For detailed command documentation, load the specific reference file:

- **SERP commands** — See <references/serp.md>
- **Keywords commands** — See <references/keywords.md>
- **Site Audit commands** — See <references/site.md>
- **Backlinks commands** — See <references/backlinks.md>

## Important Notes

- Site audits are async: `dfseo site audit` blocks until crawl completes by default. Use `dfseo site crawl` for non-blocking, then retrieve with task_id.
- `dfseo site instant` analyzes a single URL live with no polling.
- Google Ads endpoints (`keywords ads-volume`, `keywords ads-suggestions`) have a 12 req/min rate limit.
- Backlinks API requires a $100/month minimum DataForSEO commitment.
- The `--from-file` flag accepts text files with one item per line (# comments and blank lines ignored).
- All location/language defaults can be set globally via `dfseo config set location "Italy"`.
