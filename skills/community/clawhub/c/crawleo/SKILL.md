---
name: crawleo
description: Use when OpenClaw needs Crawleo-powered web search, Google Search SERP data, Google Maps place data, URL crawling/content extraction, or headful browser crawling through the Crawleo REST API.
user-invocable: true
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": [], "env": ["CRAWLEO_API_KEY"] },
        "primaryEnv": "CRAWLEO_API_KEY",
      },
  }
---

# Crawleo OpenClaw Skill

Use this skill when OpenClaw needs Crawleo-powered live web search, Google Search SERP data, Google Maps place data, URL crawling/content extraction, or headful browser crawling for protected and highly dynamic sites.

## Current Implementation Status

This repository now includes offline-tested Crawleo REST wrapper helpers for all five documented endpoints. Live Crawleo calls require `CRAWLEO_API_KEY`; user-facing examples and optional live verification are expanded in later slices. Do not claim live behavior was verified unless an explicitly enabled live test has run.

## Source of Truth

Use `contracts/crawleo-endpoints.json` as the machine-readable endpoint contract, `contracts/crawleo-endpoints.md` as the human-readable contract, and `contracts/coverage-checklist.md` as the endpoint-to-wrapper/test/example coverage checklist. These files cover:

- `/search` mapped to MCP tool `search_web`
- `/google-search` mapped to MCP tool `google_search`
- `/google-maps` mapped to MCP tool `google_maps`
- `/crawl` mapped to MCP tool `crawl_web`
- `/headful-browser` mapped to MCP tool `headful_browser`

Crawleo endpoint-specific docs take precedence over the local OpenAPI snapshot when sources conflict. If a default, limit, response field, error table, or parameter is unclear, write `not specified in Crawleo docs` rather than inventing behavior.

## Authentication and Secret Handling

Live Crawleo REST calls require `CRAWLEO_API_KEY`. OpenClaw understands this skill's `primaryEnv` metadata and should ask the user to provide `CRAWLEO_API_KEY` when it is missing. Do not attempt live Crawleo calls until that environment variable is available.

Send the key with Crawleo's documented `x-api-key` header by default. Crawleo also documents `Authorization: Bearer YOUR_API_KEY` as an alternate authentication style.

Create a client with `createCrawleoClient({ apiKey: process.env.CRAWLEO_API_KEY })`, then call `client.search`, `client.googleSearch`, `client.googleMaps`, `client.crawl`, or `client.headfulBrowser` with endpoint parameters from `contracts/crawleo-endpoints.json`.

Never print, echo, log, persist, or include API key values in errors, examples, test output, or debug output.

## Offline-First Behavior

Default commands, examples, and tests must be offline-safe. They must not call `https://api.crawleo.dev`, require `CRAWLEO_API_KEY`, or consume Crawleo credits unless explicitly marked as live tests.

Live tests must require both:

1. `CRAWLEO_API_KEY`
2. `CRAWLEO_ENABLE_LIVE_TESTS=1`

Run optional live verification with:

```bash
CRAWLEO_API_KEY=... CRAWLEO_ENABLE_LIVE_TESTS=1 npm run test:live
```

Without both variables, the live test skips safely and exits 0.

## Endpoint Use Guidance

- Use `/search` / `search_web` for Bing-powered web search with optional auto-crawling and content extraction for LLM/RAG workflows.
- Use `/google-search` / `google_search` for Google SERP data, including web, news, images, places, shopping, knowledge graph, People Also Ask, related searches, and answer boxes.
- Use `/google-maps` / `google_maps` for structured place/business/landmark data from Google Maps.
- Use `/crawl` / `crawl_web` for direct URL crawling and content extraction. Try this before headful browser to reduce credit usage.
- Use `/headful-browser` / `headful_browser` only when standard crawling is blocked or a headed browser/screenshot path is required. Crawleo docs say this costs 50 credits per URL and failed requests cost 0 credits.

## Verification

Run offline verification with:

```bash
npm test
npm run verify:contracts
npm run verify:examples
npm run verify:scaffold
```

At this stage, `npm run verify:scaffold` proves the self-contained package files exist, point to the Crawleo contract inventory, and export the runtime wrapper surface. Later slices add richer examples, documentation, and optional live-test gating.
