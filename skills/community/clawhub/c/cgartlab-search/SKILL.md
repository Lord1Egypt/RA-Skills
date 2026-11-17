---
name: cgartlab-search
description: 'Unified multi-backend internet search. Backends: Brave/Exa (web & deep research), Context7 (library/framework/API docs), Zhihu OpenAPI global search (中文全网), Tencent News (official CLI: 新闻搜索 + 热点榜), plus key-less web_fetch backends — Bing RSS (general web search), 腾讯新闻热榜 and 虎扑足球 (news/体育/足球), Stack Overflow, GitHub, Hacker News (developer sources). Use whenever the user needs information from the internet — searching the web, researching a topic, looking up docs, finding news or current events (including 足球比赛新闻), investigating anything — in Chinese or English, even when they don''t explicitly say "search". Activate on 查一下/搜一下/调研/全面了解/最新动态/新闻/足球赛况/知乎上怎么看/look up/research/how do I use X/what''s new. Do not activate for purely local tasks (reading/editing local files, running local commands) unless external sources are needed.'
license: CC-BY-NC-SA-4.0
compatibility: HTTP call capability — a shell with curl, or the harness native WebFetch/web_fetch tool (GET-only; all key-less backends work through it).
metadata:
  version: "0.1.1"
  date: "2026-10-23"
  reference: "https://github.com/cgartlab/cgartlab-search"
---

# cgartlab-search — unified search

Route a query to the best backend(s), call each via the transport your environment
supports, normalize the results, and answer the user with a cited Markdown summary.

## When to use

Any external-information need: web search, deep research, library/API docs, news, sports
news, Chinese knowledge. If the answer must come from the internet (not the user's local
files or your training knowledge), use this skill.

## Step 1 — route

Read `references/routing.md` for the full table (curl column vs DSH/web_fetch column).
Quick guide:

| Intent | backend(s) |
|---|---|
| general web / facts / "查一下" | **bing** (brave in curl harnesses) |
| 行情 / 价格 / 走势 (market data) | **bing** (keyword-rewritten query) → direct-fetch data site (routing.md market two-step) |
| library/framework/API docs | **context7** |
| dev Q&A / errors | **so** (+ hn) |
| codebase / tool finding | **github** |
| latest / hot news | **tencent** (热点榜) or **qqnews** (+ bing) |
| 中文新闻 / 中文全网 | **tencent** (新闻搜索) + **zhihu** (全网中文) |
| 足球 / 体育 news | **hupu** (+ bing, qqnews) |
| deep research / broad | **bing + context7 + hn** (add exa+brave with curl) |
| 知乎 / Chinese knowledge | **zhihu** (official Global Search API — indexes the whole web, strong on 中文) |

## Step 2 — call

Open `references/backends.md` and follow the recipe for each chosen backend. Transport:

- **Shell with network** (Claude Code, Codex, terminal) → use the **curl** recipes (all
  backends), or run `scripts/search.mjs <backends> "<query>" --limit 5` (Node 18+, zero
  deps, emits normalized JSON). `scripts/search.sh` is the curl+python variant (it probes
  `$PYTHON`/`python3`/`python`); prefer `search.mjs` wherever Node exists.
- **No shell network (DSH)** → use your harness's **WebFetch/web_fetch** tool on the GET
  URLs in `backends.md`. Check its host-reachability list first; skip unreachable hosts
  with an `errors` entry.

Keys only matter for brave/exa/tencent/zhihu: env vars (`BRAVE_SEARCH_API_KEY`, ...) or
`secrets.json` next to SKILL.md. Key-less backends need nothing.

## Step 3 — normalize + answer

Merge into the normalized shape (see `backends.md`), dedupe by URL, then write the answer:

```markdown
## Docs (Context7)
- **<title>** — <one-line>. [source](url)
  <key excerpt>

## Web / Q&A (bing / so / github / hn)
- **<title>** — <snippet>. [link](url)

## News (qqnews / hupu / bing)
- **<title>** (<date>, <source>) — [link](url)
```

If a backend errored or was unreachable, add one line, e.g. "Brave/Exa 在本环境不可达，已用
bing 替代" or "知乎未配置，已用 bing site:zhihu.com 替代". Never fabricate results for a
failed backend.

## Degradation

Missing keys, anti-bot 403s, and blocked hosts are normal — record in `errors` and
continue. Only if ALL chosen backends fail, say so plainly and suggest checking
keys / network / backend configuration.

## Backend status (verified 2026-10-20)

- **Live & key-less (curl + web_fetch)**: bing, context7, qqnews, hupu, so, github, hn.
- **curl-only (keyed)**: brave, exa — unreachable from DSH's sandboxed egress.
- **Live (keyed)**: `zhihu` (official OpenAPI global search, HTTP) and `tencent`
  (official `tencent-news-cli` binary — needs a local install, not just a key).