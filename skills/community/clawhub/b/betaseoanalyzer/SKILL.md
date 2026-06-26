---
name: seo-analyzer
description: Analyzes websites for SEO opportunities. Generates keyword ideas, checks on-page SEO factors, and provides actionable optimization recommendations.
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      bins: [python3]
    always: false
---

# SEO Analyzer

Automated SEO analysis and optimization recommendations.

## Features

- **Meta Tag Analysis**: Checks title, description, keywords, Open Graph tags
- **Content Length**: Word count vs industry benchmark
- **Heading Structure**: H1/H2/H3 hierarchy analysis
- **Mobile Readiness**: Viewport and mobile-friendly signals
- **Keyword Density**: Target keyword frequency analysis
- **Link Analysis**: Internal vs external link count
- **Page Speed Signals**: Resource count and loading signals

## Usage

```bash
python3 seo.py --url https://example.com --keyword "trading bots"
python3 seo.py --url https://example.com --keyword "AI agents" --depth full
```

## Output Format

```
SEO ANALYSIS: https://example.com
================================

TITLE TAG
- Current: "Example Site"
- Length: 45 chars (ideal: 50-60)
- Recommendation: Add target keyword

META DESCRIPTION
- Current: "..." (120 chars)
- Missing keyword "trading bots"
- Add primary keyword within first 100 chars

HEADINGS
- H1 tags found: 1
- H2 tags found: 5
- Structure: OK / Needs H1 / Add H2 subheadings

CONTENT
- Word count: 850 words
- Industry benchmark: 1500+ words
- Recommendation: Expand by 600+ words

KEYWORD DENSITY
- "trading bots": 0.3% (ideal: 1-2%)
- "AI": 1.2% (good)
- Add "trading bots" 3-5 more times

TECHNICAL
- Mobile friendly: YES
- Viewport set: YES
- HTTPS: YES

OVERALL SCORE: 72/100
Priority fixes:
1. Expand content to 1500+ words
2. Add "trading bots" to title
3. Add meta description with keyword
```

## Example Workflow

1. Run analysis: `python3 seo.py --url <target>`
2. Review score and priority fixes
3. Implement title/meta updates
4. Expand content based on recommendations
5. Re-run after 2 weeks to measure improvement

## Notes

- Requires: python3, urllib (stdlib)
- No API keys needed for basic analysis
- For production use, add Google Search Console API integration
- MIT-0 License
