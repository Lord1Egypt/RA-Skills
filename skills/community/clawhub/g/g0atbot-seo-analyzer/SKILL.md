# SEO Analyzer Skill

Analyze websites and pages for SEO factors - free alternative to paid tools like Ahrefs, SEMrush.

## What It Does

- **Page SEO Analysis**: Analyze any URL for meta tags, headings, content structure
- **Keyword Suggestions**: Research keywords based on topics
- **Competitor Analysis**: Compare SEO metrics between pages
- **Site Audits**: Check for common SEO issues
- **Ranking Checks**: Look up how pages rank for keywords (via search)

## Usage

```
/seo-analyze <url> - Full page analysis
/seo-keywords <topic> - Get keyword ideas
/seo-compare <url1> vs <url2> - Compare two pages
/seo-audit <url> - Check for technical issues
```

## Tools Used

- `web_fetch` - Fetch page content for analysis
- `web_search` - Search for rankings and keywords
- `browser` - For dynamic pages that need JS rendering

## Requirements

- Brave Search API (for keyword/ranking data)
- Can analyze most static pages directly
- Uses browser for SPA/dynamic sites

## Output Format

Provides:
- Meta title & description (with optimization suggestions)
- Heading hierarchy (H1-H6)
- Word count & readability
- Internal/external links
- Images (alt text check)
- Technical issues found
- Keyword opportunities

## Paid Tools Replaced

- Ahrefs ($99-999/mo)
- SEMrush ($119-449/mo)
- Moz Pro ($99/mo)
- Ubersuggest ($29-199/mo)

This skill covers 80% of basic SEO analysis for free.
