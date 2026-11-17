---
name: ClawSearch Ultra
slug: clawsearch-ultra
version: 1.0.1
description: "Federated web search across 10+ search engines (DuckDuckGo, Brave, Google, Bing), multi-language, news-aware, answer-first results."
metadata: {"clawdbot":{"emoji":"🔎","requires":{"bins":["node","curl"]}}}
---

# ClawSearch Ultra

Federated search skill and local fetching runtime for agents — built on Web Search Pro's
core, **enhanced with unique features**:

## 🆕 Unique features (not found in the original)

### Feature 1: Multi-language search
Search with automatic language detection and results in Danish, Arabic, Somali, English and more.
Use `--lang da` for Danish-filtered results:

```bash
node scripts/search.mjs "renten 2026 danmark" --lang da --json
node scripts/search.mjs "aqoonsi" --lang so --json   # somali
```

### Feature 2: News monitoring with alerts
Monitor a topic and get notified when NEW content appears (diff vs. last search):

```bash
node scripts/watch.mjs "BTC price" --interval 1h --notify telegram
node scripts/watch.mjs "Vantage spreads" --notify slack
```

### Feature 3: Answer-first with sources
Get a short answer + verified sources in one call (like Perplexity, but free baseline):

```bash
node scripts/answer.mjs "What is the DRT strategy?" --json
```

---

## Baseline search (inherited)

No API key required for baseline:

```bash
node scripts/search.mjs "OpenClaw docs" --json
node scripts/search.mjs "latest news" --type news --json
```

## Premium providers (optional)

```bash
export TAVILY_API_KEY=tvly-xxxxx      # best baseline upgrade
export EXA_API_KEY=exa-xxxxx
export BRAVE_API_KEY=xxxxx
export SERPER_API_KEY=xxxxx
export PERPLEXITY_API_KEY=xxxxx
export SEARXNG_INSTANCE_URL=https://searx.example.com
```

## Runtime contract

- `selectedProvider` — primary route
- `routingSummary` — compact routing explanation with confidence
- `federated.providersUsed` — providers that actually responded
- `federated.value` — gain from fanout (extra results, dedup savings)
- `cached` / `cache` — cache hit and TTL

## Full documentation
- Source: https://github.com/Zjianru/web-search-pro (based on v2.1, improved)
- News monitoring: `node scripts/watch.mjs --help`

## Feedback
- Helpful? → `clawhub star clawsearch-ultra`
---
