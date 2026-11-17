# Five-layer audit framework

1. Crawlability and indexation: fetch status, robots directives, meta robots, sitemap availability, canonical intent, and `site:` visibility proxy.
2. Technical foundations: redirects, canonical consistency, hreflang, rendered JSON-LD validity, mobile metadata and URL hygiene.
3. On-page optimization: unique title, description, H1 hierarchy, target-keyword alignment and Open Graph metadata.
4. Content quality: thin/duplicate intent signals, useful main content, freshness and page-purpose match. Do not infer traffic.
5. Internal links and authority signals: internal link count, broken-link candidates and orphan risk from the sampled graph. Backlink authority remains external-only.

Continue lower layers after a critical Tier-1 finding, but never invent checks that could not run.
