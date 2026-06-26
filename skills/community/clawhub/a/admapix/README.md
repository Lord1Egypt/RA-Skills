# AdMapix — Ad & App Intelligence Data Layer

[中文文档](README_CN.md)

AdMapix is a **data layer** over the AdMapix read API. It turns natural-language requests into single API calls and returns **raw structured JSON** — ad creatives, app/product info, rankings, download & revenue estimates, ad distribution, and market metadata. Your agent (Claude Code, Codex, …) decides which endpoints to call, chains them as needed, and does any analysis itself. No hosted research, no generated pages — just clean data you can compose.

## What you can pull

- **Creative search** — ad creatives by keyword, advertiser, app, region, media channel, creative type (image / video / playable), industry, and date range, sorted by newest, most impressions, or longest running. Each record carries the creative assets, advertiser/app, first/last seen, and impression estimates.
- **Apps / products / companies** — unified product & company search, full app detail, developer detail, app profile, similar apps, and the SDKs a package uses.
- **Rankings** — App Store / Google Play store ranks (free / paid / grossing) and generic ranking lists, by country and category.
- **Downloads & revenue** — download and revenue estimates over time, by detail and by country *(third-party estimates, not official figures)*.
- **Ad distribution** — where and how an app advertises: countries, media placements, and creative formats.
- **Market** — market-level search and aggregation across industries, advertisers, and channels.
- **Metadata** — `filter-options` returns every filter dimension (countries, media channels, ad types, devices, industries / `tradeLevel`, product models, …) so your agent can discover valid codes and build precise queries.

Per-endpoint parameters and response fields live in [`references/`](references); natural-language → code mappings (creative type, industry, country groups, date ranges, sorting, page size) are in [`references/param-mappings.md`](references/param-mappings.md).

## Install

```bash
npx clawhub install admapix
```

## Setup

1. Register at [www.admapix.com](https://www.admapix.com) and create an API Key.
2. Configure it with one of:

OpenClaw / ClawHub:

```bash
openclaw config set skills.entries.admapix.apiKey "<your-key>"
```

Generic shell environment:

```bash
export ADMAPIX_API_KEY="<your-key>"
```

Keep the key in your host's secret store — never paste it into chat, logs, or generated output.

## Usage Examples

Ask your agent for data; it picks the endpoint(s) and returns raw results.

| Data | Example prompts |
|------|----------------|
| Creative search | "Search video ads for puzzle games", "Find casual-game creatives running in Southeast Asia", "Most-impression finance creatives in the US" |
| App / product data | "Get Temu's app detail", "Who develops TikTok?", "What SDKs does this app use?", "Find apps similar to CapCut" |
| Rankings | "US App Store free chart top 10", "Top-grossing games in Japan", "Google Play tools ranking" |
| Downloads & revenue | "Temu's download estimates for the last 30 days", "SHEIN revenue by country" *(estimates)* |
| Ad distribution | "Which countries does Temu advertise in?", "What ad channels does this game use?" |
| Market | "Game-ad market data for Southeast Asia", "Top advertisers in the finance industry" |
| Metadata | "List the available industries / countries / media channels" (via filter-options) |

Supports **English** and **Chinese** inputs.

## How it works — a composable data layer

This skill is deliberately thin:

1. **One call per request.** Each skill action maps to a single AdMapix read endpoint and returns that endpoint's raw JSON — no rewriting, summarizing, or ranking.
2. **The agent composes.** Multi-step questions ("downloads for Temu", "SDKs of 放置少女") are resolved by the calling agent: it first looks up the entity (e.g. `unified-product-search`), then fetches the metric (e.g. `download-detail` / `sdk-detail`). The endpoint catalog in `SKILL.md` plus the reference docs make these chains explicit.
3. **Metadata is first-class.** `filter-options` exposes every filter dimension, so the agent builds exact queries (right country codes, industry IDs, media channels) instead of guessing.
4. **Analysis stays with you.** Comparisons, trends, and recommendations are produced by your agent from the raw data — the skill never runs hosted "deep research" or generates HTML / H5 pages.

The result is predictable and auditable: you always see the underlying data, and the intelligence lives in the agent you control.

> ⚠️ Download and revenue figures are third-party **estimates**, not official app-store data.

## Links

- Website: [www.admapix.com](https://www.admapix.com)
- API: [api.admapix.com](https://api.admapix.com)
- GitHub: [github.com/fly0pants/admapix](https://github.com/fly0pants/admapix)

---

Built by [Miaozhisheng](https://www.admapix.com)
