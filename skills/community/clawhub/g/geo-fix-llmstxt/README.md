# geo-fix-llmstxt

Generate specification-compliant `llms.txt` and `llms-full.txt` files for any website.

## What it does

1. **Discovers** your site structure via sitemap, navigation, and page crawling
2. **Categorizes** pages into logical sections (Docs, API, Blog, Products, etc.)
3. **Generates** `llms.txt` with structured links and descriptions
4. **Generates** `llms-full.txt` with embedded page content for direct LLM consumption
5. **Improves** existing llms.txt files by finding gaps, broken links, and missing pages

## Usage

```bash
# Generate from scratch
"Generate llms.txt for https://example.com"

# Improve existing
"Improve the llms.txt for https://example.com"

# Claude Code slash command
/geo-fix-llmstxt https://example.com
```

## Output

| File | Purpose |
|------|---------|
| `llms.txt` | Structured links and summaries for AI discovery |
| `llms-full.txt` | Full page content embedded for direct LLM consumption |

## Specification

Follows the [llmstxt.org](https://llmstxt.org/) proposed standard. See `references/llmstxt-spec.md` for the full specification reference.

## Installation

```bash
npx skills add Cognitic-Labs/geoskills --skill geo-fix-llmstxt
```
