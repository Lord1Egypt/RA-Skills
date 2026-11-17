# Answer-engine readiness — https://example.com

**Score 30.0/100 · grade F** · geo-scan 1.2.0 · 2026-10-19 22:09 CEST · 5 requests

| axis | score | status | evidence |
|---|---|---|---|
| Crawler access (robots.txt) | 20.0/20 | open | robots.txt HTTP 404 = no restrictions (RFC 9309) · 8/8 search/retrieval agents may fetch the root · training crawlers blocked (not scored): none |
| Machine readability | 0.0/15 | thin | no usable sitemap (https://example.com/sitemap.xml: HTTP 404; https://example.com/wp-sitemap.xml: HTTP 404) |
| Snippet permissions | 10.0/10 | ok | 1/1 pages may be indexed and quoted (meta robots, X-Robots-Tag) |
| Page structure | 0.0/25 | thin | 0/1 pages carry article-level schema.org markup · 0/1 have exactly one <h1> · median word count 25 |
| Quotability | 0.0/20 | thin | 0 definitional phrases, 0 hard figures, tables on 0/1 pages · English phrase lists only |
| Freshness | 0.0/10 | thin | no machine-readable dates found |

## Actions

- **high** — Publish sitemap.xml with an accurate <lastmod> on every URL and list it in robots.txt with a Sitemap: line.
- **medium** — Add JSON-LD that matches the visible content (Article/BlogPosting with author and dateModified, BreadcrumbList); keep exactly one <h1> per page. Use FAQPage only on pages that really are FAQs.
- **medium** — Add a 40-60 word definitional answer plus one hard figure or comparison table near the top of each page — that is the block engines quote.
- **medium** — Refresh or retire stale pages and expose an honest dateModified.
- **low** — Optional: llms.txt is a proposal with no confirmed consumer among the major engines (Google says it does not use it). Publish one only if it is cheap to maintain.

## Pages

| url | words | h1 | schema | figures | quotes | robots directives |
|---|---|---|---|---|---|---|
| https://example.com | 25 | 0 | — | 0 | 0 | — |

_Weights are geo-scan's judgement, not validated against observed citations. CDN/WAF bot blocking and JS rendering are invisible to this tool._
