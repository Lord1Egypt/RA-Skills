# Routing Policy

Use this file to choose the right endpoint family and, when necessary, compose multiple endpoints into one answer. This file owns **decision and composition logic only**. The lowest-level execution rules (data freshness, pagination, image conversion, identifier standards, category resolution, dual-mode user choice, realtime retry) live in `global-rules.md` and are not restated here.

## API-Only Policy

All user data requests must be satisfied from EchoTik API endpoints and EchoTik API docs.

Do not use `echotik.live` product pages, dashboards, or website navigation as a fallback data source. Allowed website usage is limited to signup, billing, API key retrieval, and onboarding instructions.

## Default Decision Order

1. Prefer a single offline EchoTik endpoint when the user wants broad analysis, ranking, batch retrieval, or historical comparison.
2. Prefer a realtime endpoint when the user explicitly needs freshness, current comments, live status, realtime search, or download links.
3. Prefer a composed workflow when the user asks an outcome that naturally spans entities.

For explicit search intent:

1. prefer the dedicated realtime search endpoint for the target entity
2. use universal EchoTik search only as a fallback

## Mandatory User Choice Cases

Before execution, ask the user to choose `realtime` or `EchoTik offline` for the dual-mode request types enumerated in `global-rules.md` (§5). Do not silently choose a mode on the user's behalf.

## Composition Examples

### Find creators for a product

- Step 1: search or identify the product
- Step 2: fetch product-related influencers
- Step 3: optionally enrich shortlisted influencers with influencer detail

### Explain why a video is performing well

- Step 1: fetch video detail
- Step 2: fetch 14-day interaction trend
- Step 3: fetch comment keyword insight
- Step 4: optionally fetch linked products

### Explore hashtag-related videos

- Step 1: resolve the hashtag through realtime hashtag search if only hashtag text is known
- Step 2: fetch the hashtag video list through the resolved `hashtag_id`

### Evaluate a shop

- Step 1: fetch shop detail
- Step 2: fetch shop product list
- Step 3: fetch related influencers, videos, or live sessions if the user wants traffic sources

## Freshness Policy

- Offline EchoTik endpoints are suitable for stable research and large-batch queries.
- Realtime endpoints are suitable for freshness-sensitive tasks but may have rate, risk-control, or stability tradeoffs.
- If a realtime endpoint fails, retry if appropriate, then degrade gracefully to the nearest offline endpoint.
- If an offline lookup returns empty data, do not immediately conclude the entity does not exist. Treat that as a freshness or coverage gap and try the relevant realtime endpoint when the global rules allow it.

## UX Policy

- Do not expose endpoint names first.
- Think in terms of user intent, then map to entities and endpoint families.
- If one request requires multiple calls, present it as one workflow to the user.
- If the user asks for a comprehensive report, confirm which related data sections should be included before calling every adjacent endpoint family.
- If tools are available, execute the chosen API instead of only describing what would be called.
- Never answer a live data question by pointing to the web app feature that could show it.
- If the request hits a mandatory user-choice case, pause and ask the user which data source mode they prefer.
- If params are uncertain, prefer one minimal documented request over guessing hidden enums or unsupported fields.

## API Questions

If the user asks technical API questions such as:

- "Which endpoint is best for this scenario?"
- "What is the difference between offline and realtime?"
- "Why does this parameter need to be passed this way?"
- "How should Basic Auth be configured?"

Answer directly from the docs, and only execute live calls if the user wants data back.

## Ranking And Top-N Requests

Requests such as:

- "Which creators gained followers the fastest recently?"
- "What are the top 10 winning products in the US?"
- "What are the hottest videos from the last 7 days?"

must be treated as API execution tasks, not website navigation tasks.

Default handling:

1. identify entity family
2. identify market
3. identify time window
4. identify ranking metric
5. identify requested size
6. execute the closest ranking, list, or trend API

For creator ranking specifically:

- prefer `Influencer Rank List - EchoTik` for top growth, top sales, and periodic ranking questions
- prefer `Influencer List - EchoTik` for advanced multi-filter creator discovery
- prefer `Influencer Trend Snapshot - EchoTik` for historical trend explanation

For video analysis specifically:

- prefer `Video Detail - Realtime` when the user needs the current public state of one video
- prefer `Video Detail - EchoTik` when the user needs offline sales, GMV, and enriched interaction deltas
- prefer realtime `14-Day Interaction Trend` over offline video trend snapshots when the user asks about recent trend performance
