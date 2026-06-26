---
name: exa-search
description: "Neural web search, similar-page discovery, and URL content fetching via the Exa AI search engine. USE WHEN: user asks to search the web, find articles/repos/papers on a topic, look up recent news, find pages similar to a URL, or fetch page contents for a known URL. NOT FOR: fetching tweets (use fxtwitter), downloading videos (use yt-dlp), scraping JS-heavy or anti-bot sites (use scrapling), querying APIs directly, or searching local files/repos (use rg/find)."
homepage: https://github.com/Prompt-Surfer/exa-search-rust
metadata: {"openclaw":{"emoji":"🔍","requires":{"env":["EXA_API_KEY"],"bins":["bash","cargo"]},"primaryEnv":"EXA_API_KEY","install":[{"id":"build","kind":"script","label":"Build Rust binary","run":"bash install.sh"}]}}
---

# exa-search skill

Use this skill to search the web, find similar pages, or fetch page contents via the [Exa AI](https://exa.ai) search engine — fast, neural, and certificate-aware.

The skill invokes a native Rust binary (`bin/exa-search`) via Bash. Run `install.sh` once to build it.

---

## When to Use / When NOT to Use

✅ **USE when:**
- Searching the web for articles, documentation, repos, papers, tools, people, companies
- Finding recent news or announcements (use `livecrawl: "fallback"` or `"always"` for recency)
- Fetching full text of a known URL without browser automation
- Finding pages similar to a reference URL (competitor analysis, alternative tools)
- Any web lookup that isn't a specific tweet or video

❌ **NOT FOR:**
- Fetching tweets/X posts → use `fxtwitter` skill (Exa can't fetch tweet URLs)
- Downloading video/audio → use `yt-dlp`
- Scraping dynamic or Cloudflare-protected pages → use `scrapling`
- Local file/code search → use `rg`, `find`, or `grep`
- Querying structured APIs (GitHub, weather, etc.) → use their dedicated skills
- When the query is already a direct URL with known content → prefer `get_contents` action

---

## Prerequisites

- `EXA_API_KEY` set in `~/.openclaw/workspace/.env` (get one at [exa.ai](https://exa.ai))
- Rust installed (`rustup`) — only needed for the one-time build
- `bin/exa-search` binary present (run `bash install.sh` to build)

---

## Actions

### 1. Search

```bash
echo '{"query":"your query here","num_results":5}' \
  | EXA_API_KEY=$(grep -E "^EXA_API_KEY=" ~/.openclaw/workspace/.env | cut -d= -f2 | tr -d '"') \
  ~/.openclaw/workspace/skills/exa-search/bin/exa-search
```

**Full params:**

```json
{
  "query": "rust async programming",
  "num_results": 5,
  "type": "neural",
  "livecrawl": "never",
  "include_domains": ["github.com", "docs.rs"],
  "exclude_domains": ["reddit.com"],
  "start_published_date": "2025-01-01",
  "end_published_date": "2026-12-31",
  "category": "research paper",
  "use_autoprompt": true,
  "text": { "max_characters": 2000 },
  "highlights": { "num_sentences": 3, "highlights_per_url": 2 },
  "summary": { "query": "key takeaways" }
}
```

**`type` options:** `auto` (default) · `neural` · `keyword`

**`livecrawl` options:**
- `"never"` — fastest (~300-600ms), pure cached index. Best for reference material, docs, courses.
- `"fallback"` — use cache, crawl live if not cached. Good default.
- `"preferred"` — prefer live crawl. Slower but fresher.
- `"always"` — always crawl live. For breaking news or rapidly-changing pages.

---

### 2. Find Similar

Find pages similar to a given URL:

```bash
echo '{"action":"find_similar","url":"https://example.com","num_results":5}' \
  | EXA_API_KEY=$(grep -E "^EXA_API_KEY=" ~/.openclaw/workspace/.env | cut -d= -f2 | tr -d '"') \
  ~/.openclaw/workspace/skills/exa-search/bin/exa-search
```

**Params:** same contents options as search (`text`, `highlights`, `summary`, `livecrawl`)

---

### 3. Get Contents

Fetch full contents for one or more URLs:

```bash
echo '{"action":"get_contents","urls":["https://example.com","https://other.com"],"text":{"max_characters":1000}}' \
  | EXA_API_KEY=$(grep -E "^EXA_API_KEY=" ~/.openclaw/workspace/.env | cut -d= -f2 | tr -d '"') \
  ~/.openclaw/workspace/skills/exa-search/bin/exa-search
```

---

## Output format

All actions return JSON on stdout:

```json
{
  "ok": true,
  "action": "search",
  "results": [
    {
      "url": "https://...",
      "title": "...",
      "score": 0.87,
      "author": "...",
      "published_date": "2026-01-15",
      "image": "https://...",
      "favicon": "https://...",
      "text": "...",
      "highlights": ["..."],
      "summary": "..."
    }
  ],
  "formatted": "## [Title](url)\n..."
}
```

On error:
```json
{ "ok": false, "error": "..." }
```

The `formatted` field is ready-to-use markdown — you can send it directly to the user.

---

## Speed reference (same query, 3 runs)

| Mode | Avg | Peak |
|---|---|---|
| `livecrawl: "never"` (instant) | ~440ms | **308ms** |
| Default (no livecrawl) | ~927ms | 629ms |

~18.7× faster than Exa MCP at peak.

---

## Helper: load API key

```bash
EXA_API_KEY=$(grep -E "^EXA_API_KEY=" ~/.openclaw/workspace/.env | cut -d= -f2 | tr -d '"')
```

Or export once at the top of a longer workflow:

```bash
export EXA_API_KEY=$(grep -E "^EXA_API_KEY=" ~/.openclaw/workspace/.env | cut -d= -f2 | tr -d '"')
echo '{"query":"..."}' | ~/.openclaw/workspace/skills/exa-search/bin/exa-search
```

---

## Invocation pattern

```bash
EXA_API_KEY=$(grep -E "^EXA_API_KEY=" ~/.openclaw/workspace/.env | cut -d= -f2 | tr -d '"')
echo '{"query":"...","num_results":5,"livecrawl":"never"}' \
  | EXA_API_KEY="$EXA_API_KEY" ~/.openclaw/workspace/skills/exa-search/bin/exa-search
```

The `formatted` field in the output is ready-to-use markdown — send it directly to the user.

---

## Mode selection (be deliberate, every search)

| Situation | `livecrawl` | `type` |
|---|---|---|
| Docs, tutorials, courses, reference material | `"never"` | `"neural"` |
| General research — people, tools, concepts, companies | `"never"` | `"neural"` |
| Exact function names, error messages, package names | `"never"` | `"keyword"` |
| Recent releases, changelogs, GitHub repos | `"fallback"` | `"auto"` |
| News or announcements from the last 1-2 weeks | `"fallback"` | `"neural"` |
| Breaking news, live prices, today's events | `"always"` | `"neural"` |
| Unsure | `"fallback"` | `"auto"` |

**Default when in doubt:** `livecrawl: "never"`, `type: "neural"` — fastest, works for 80% of searches.

---

## When to use each action

**`search`** (default) — use for any information retrieval from a query string.

**`find_similar`** — use when you have a URL and want more like it: related articles, alternative tools, similar repos, competing products.
```bash
echo '{"action":"find_similar","url":"https://...","num_results":5,"livecrawl":"never"}' | EXA_API_KEY="$EXA_API_KEY" ...
```

**`get_contents`** — use when you have a specific URL and need its full text: docs pages, blog posts, GitHub READMEs, papers. Faster than `search` when the URL is already known.
```bash
echo '{"action":"get_contents","urls":["https://..."],"text":{"max_characters":3000}}' | EXA_API_KEY="$EXA_API_KEY" ...
```

---

## Enrich results for research tasks

When writing reports, summaries, or comparing multiple results — request highlights or summary per result:

```json
{
  "query": "...",
  "num_results": 5,
  "highlights": { "num_sentences": 3, "highlights_per_url": 2 },
  "summary": { "query": "key takeaways for a developer" }
}
```

Note: highlights/summary add latency (~200-500ms extra). Only use when you actually need them.
