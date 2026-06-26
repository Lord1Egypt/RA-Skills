# eBay Tooling Ecosystem — Landscape Research

**Researched:** 2026-03-24  
**Purpose:** Understand what already exists in the eBay developer/CLI/AI tool space before building further features in ebay-agent. Identify gaps, opportunities to build on existing work, and signal from real-world usage patterns.

---

## Summary

The eBay open-source tooling space is surprisingly sparse for a platform this large. There is no dominant, well-maintained CLI tool for eBay research. The Python SDK landscape is fragmented and mostly unmaintained. The MCP/AI-agent layer is brand new and thin. **ebay-agent fills a genuine gap**, but there are several specific projects worth understanding for code reuse and inspiration.

---

## 1. Python API Wrappers (Library Layer)

### `ebay_rest` — matecsaj/ebay_rest ⭐ ~200
**Best current option for programmatic access.**

- Full Python 3 wrapper for all of eBay's REST APIs (`buy_browse_search`, inventory, selling, fulfillment, etc.)
- Uses Python generators for paged results — avoids loading all 10k records into memory
- Handles OAuth automatically, with browser automation via Playwright for user tokens
- Threading safe; multiprocessing untested
- Install: `pip install ebay_rest` or `pip install ebay_rest[complete]`
- Config via `ebay_rest.json` file; refresh tokens can be reused to skip browser auth

**Relevance to ebay-agent:**
This is the most complete API wrapper available. Our current code hits the Browse API directly via `httpx`. We could swap the auth/request layer to use `ebay_rest` instead, gaining access to all 100+ API methods without writing wrapper code. Particularly relevant if we want to add seller data, inventory APIs, or fulfillment endpoints later.

**Repo:** https://github.com/matecsaj/ebay_rest  
**Verdict:** Worth depending on as a foundation for future expansion. Not worth replacing our current Browse API calls today since they're working well, but keep as an option.

---

### `ebaysdk-python` — timotheus/ebaysdk-python ⭐ ~500
**The old standard — largely unmaintained.**

- Wraps eBay's legacy XML-based APIs (Finding, Shopping, Trading)
- Last meaningful activity: 2021–2022
- The Finding API it wraps is being deprecated in favor of Browse API
- Still widely referenced in blog posts and older projects

**Relevance to ebay-agent:**  
Mostly irrelevant for new development. Our Browse API + Marketplace Insights approach is already the right move. Mentioned here because it still shows up in search results and docs — don't get sidetracked by it.

---

### `python-ebay` — roopeshvaddepally/python-ebay
**Archived / abandoned.**

- Very old (2012-era), wraps legacy APIs
- Not maintained, not installable via pip in modern Python
- Ignore

---

### `ebay-oauth-python-client` — eBay (official)
**Official OAuth helper from eBay.**

- Handles the OAuth 2.0 flow for getting application and user access tokens
- YAML/JSON config file
- Lightweight — only handles auth, not API calls
- Useful if we ever need user-scoped tokens (e.g., for selling features, watchlist access)

**Repo:** https://github.com/eBay/ebay-oauth-python-client  
**Verdict:** Worth knowing about if we ever add seller-side features that require user OAuth.

---

## 2. CLI / Terminal Tools

### `ebay-selling-tool-cli` — adrain-cb
**The only real CLI predecessor found.**

- Python CLI designed for eBay sellers
- Very basic: prompts for App ID, searches for items
- Minimal feature set, no scoring/relevance/valuation logic
- Not maintained

**Relevance:**  
Shows there's genuine demand for a Python-based CLI for eBay. Also confirms the space is empty — this project never got traction. **ebay-agent is already a much better version of what this attempted.**

---

### `ebSear` — asherAgs
**Scraper-based search CLI using web scraping (not API).**

- `getSearchPage` and `getItem` methods
- Web scraping approach (not API-based)
- Risk: eBay actively blocks scrapers with CAPTCHAs

**Verdict:** Wrong approach. API-based (what we do) is more reliable and ToS-compliant. Avoid.

---

### `ebayMarketAnalyzer` — driscoll42 ⭐ ~200
**Interesting — price analysis from sold listings.**

- Originally scraped eBay sold data automatically; now requires manual XML export
- Computes median, mean, trends, scatter plots from sold item data
- Exports to Excel; generates price-over-time charts with trendlines
- Was used to analyze the PS5/GPU scalping market in 2020–2021 (got significant attention)
- **Now requires manual XML export because eBay added CAPTCHAs to block automated scraping**

**Key insight from this project:** Sold listing analysis is hugely valuable (it's the core of our `value` command), but scraping is a dead end. Our use of the Marketplace Insights API with Browse API fallback is the right approach and avoids the CAPTCHA problem entirely. The author explicitly recommends **Terapeak** for commercial use — which is interesting competitive context.

**Repo:** https://github.com/driscoll42/ebayMarketAnalyzer

---

## 3. MCP (Model Context Protocol) Servers

This is the newest and most strategically relevant category. MCP is how AI assistants (Claude, Cursor, etc.) connect to external tools.

### `ebay-mcp` — YosefHayim ⭐ growing fast
**Most comprehensive eBay MCP server — 325 tools, Sell API focus.**

- TypeScript / Node.js (`npm install -g ebay-mcp`)
- 325 tools covering: inventory management, order fulfillment, marketing campaigns, analytics, developer tools
- Sell API focused — designed for sellers managing listings, not buyers researching prices
- Requires OAuth setup; npm-based install
- Very recent (March 2026 — same week as our QA)

**Relevance:**  
This is the emerging competitor in the AI-native space. It's focused on seller operations (managing eBay stores), not buyer research / deal hunting. **We are targeting a different use case**: research, valuation, and deal evaluation from the buyer/researcher perspective, accessible via CLI and OpenClaw. Still worth watching — if they add buyer-side research tools, that's direct competition.

**Repo:** https://github.com/YosefHayim/ebay-mcp

---

### `ebay-mcp-server` — hanku4u
**Small, homelab-focused MCP server.**

- Python / FastMCP framework
- Focus: homelab equipment deal hunting (servers, networking gear, RAM)
- Features: search with filters, price tracking, deal monitoring
- Early stage, small community, explicitly built for personal use

**Key quote from README:** "Created by @hanku4u with AI assistance from RockLobster 🦞"

**Relevance:**  
This is the closest existing project to ebay-agent in spirit — a personal, CLI/AI-integrated eBay research tool. Key differences: (1) MCP protocol vs standalone CLI, (2) homelab niche vs general, (3) Python/FastMCP vs Python/argparse. Their "price tracking" feature is essentially our planned `watch` command. Worth reading their implementation for ideas.

**Repo:** https://github.com/hanku4u/ebay-mcp-server  
**Glama listing:** https://glama.ai/mcp/servers/@hanku4u/ebay-mcp-server

---

## 4. Commercial / SaaS Competitors

These are not open source but are important market context.

### Terapeak (built into eBay Seller Hub)
- eBay's own research tool, free for sellers
- Goes back further in historical data than the API
- Best source for actual sell-through rate, competition density, average price by date
- Limitation: requires eBay seller account; no API/CLI access; web UI only

### ZIK Analytics ($30–100/mo)
- Product research for eBay dropshippers and resellers
- "Unlimited searches" vs Terapeak's limits
- Competitor analysis, keyword research, trending products
- Target user: eBay resellers/dropshippers

### MarkSight (free tier available)
- Positioned as a Terapeak alternative
- Aggregated eBay market data

### Other SaaS tools: 3Dsellers, Pexda, AutoDS
- Mostly dropshipping-focused automation tools
- Not direct competitors to our research/CLI use case

**Takeaway:** The commercial tools are all web UIs targeting eBay sellers/dropshippers. None of them are CLI-first, agent-friendly, or designed for buyers and researchers. This is the open gap we're in.

---

## 5. Interesting Niche Projects

### LabGopher (labgopher.com)
- Web app that aggregates eBay listings specifically for homelab/server gear
- Shows deals on rack servers, switches, RAM, etc. sorted by value
- Uses eBay API under the hood; not open source
- Has a cult following in the homelab community (r/homelab, r/homelabsales)

**Relevance:**  
LabGopher is a great example of "narrow niche + eBay API = beloved product." They built something deeply useful by going vertical into one category. Inspiration: a `--category homelab` or `--category photo-gear` mode in ebay-agent could attract niche communities the same way.

---

### `ebay-price-tracker` — mohammed-ysn
- Simple program that tracks eBay product prices over time
- SQLite-based persistence
- Basic alerting

**Relevance:**  
This is a simpler version of our planned `watch` command. Worth reading to understand the storage patterns people use. They use SQLite; we're planning JSON. For v1 JSON is fine, but SQLite makes more sense at scale (multiple watches, deduplication history, trend data).

---

### PricePoint — sburl
- Python tool for Amazon + eBay + Facebook Marketplace arbitrage research
- Compares prices across platforms to find arbitrage opportunities
- Interesting cross-platform angle: "is this cheaper to buy on eBay and sell on Amazon (or vice versa)?"

**Relevance:**  
This validates the multi-platform comparison feature idea. A `compare-amazon` command in ebay-agent would be genuinely useful and hasn't been done well in an open-source CLI yet.

---

## 6. TypeScript / Node.js Ecosystem

### `ebay-api` — hendt ⭐ ~500, active
**Best maintained TypeScript eBay client.**

- Full REST + legacy API coverage
- TypeScript, works in Node and browser
- Updated March 2026 (very active)
- Better TypeScript support than any Python equivalent

**Relevance:**  
If ebay-agent ever moves to TypeScript (e.g., to publish as an npm ClawHub skill), this would be the API layer to use. For now we're Python-first, so this is informational. But the activity level here vs. the Python side suggests the TS/Node ecosystem is more active for eBay development.

---

## Key Gaps in the Ecosystem (Our Opportunities)

| Gap | Our Position |
|---|---|
| No good Python CLI for eBay research | ebay-agent fills this |
| No deal-rating tool (great/good/fair/overpriced) | `deal` command is unique |
| No `watch` command / price alert CLI | Planned v0.7.0 — nobody has done this well open source |
| No relevance filtering (accessories) | Our `relevance.py` is unique |
| No multi-platform price comparison | Opportunity: `compare-amazon` |
| No OpenClaw/AI agent integration | Our core differentiator |
| No vertical/category-specific modes | Opportunity: homelab, photo gear, etc. |

---

## Lessons for ebay-agent Development

**1. Don't scrape — use the API.**  
Every scraper project (ebSear, ebayMarketAnalyzer) eventually got killed by CAPTCHAs. Our API-first approach is the right one. The Browse API + Marketplace Insights combo we have is solid.

**2. The `ebay_rest` library is worth knowing.**  
If we want to add seller-side features (listing creation, inventory management), `ebay_rest` would save significant auth and API wrapper code. We don't need it today, but it's the right dependency for seller features.

**3. SQLite for the `watch` command, not JSON.**  
The price tracker community consistently uses SQLite for persistence. It handles deduplication, history, and concurrent reads better than a flat JSON file. Use it from the start for `watch`.

**4. MCP is the next platform.**  
`ebay-mcp` (YosefHayim) just shipped 325 tools for the Sell API in MCP format. The buyer/research side in MCP is uncovered. We should eventually publish an `ebay-agent` MCP server that wraps our existing `search`, `value`, `deal`, and `watch` commands — making them available directly to Claude Desktop, Cursor, etc. FastMCP (Python) makes this fast to build.

**5. Niche community = sticky product.**  
LabGopher proves that going vertical (homelab gear) builds a loyal user base. We could add category-specific modes (homelab, camera gear, vinyl, sneakers) that attract passionate communities. Each community has its own pricing signals and condition language.

**6. Cross-platform comparison is a wide-open gap.**  
Nobody has built a clean CLI that says "should I buy this on eBay or Amazon?" PricePoint tried but is rough. This could be a high-value feature.

---

## Recommended Next Steps (in priority order)

1. **`watch` command** — Use SQLite for state, support `add/list/check/remove`. Design for cron integration. (v0.7.0)
2. **MCP server wrapper** — Wrap existing commands as MCP tools using FastMCP. Unlocks Claude Desktop / Cursor integration. (v0.8.0)
3. **`compare-amazon` command** — Cross-platform price comparison. (v0.8-0.9)
4. **Category modes** — `--category homelab`, `--category camera-gear`, with tuned relevance filters and condition vocabulary. (v1.0+)
5. **Consider `ebay_rest` for seller features** — If we build listing creation or seller analytics, use this library instead of rolling our own.

---

*Research by Bob / EagerBots — March 2026*
