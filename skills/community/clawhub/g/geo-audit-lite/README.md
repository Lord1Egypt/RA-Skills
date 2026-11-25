# geo-audit-lite

Offline AI-search readiness (GEO) audit for saved `page.html`, `robots.txt` and `llms.txt` files — checks whether ChatGPT, Perplexity, Claude and Google AI crawlers can reach, parse and cite a page. Zero network access, zero dependencies, Node 18+.

```bash
node scripts/audit.js --html page.html --robots robots.txt --llms llms.txt
```

JSON report on stdout. Exit `1` when any warn/fail is present (CI-gateable), `2` on usage/read error.

The full `geo-audit` skill ($39) adds live URL fetching and multi-engine citation tracking. See [SKILL.md](SKILL.md) for agent usage.
