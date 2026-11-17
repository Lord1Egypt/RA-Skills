# Backend reference — cgartlab-search

Per-backend API contracts, recipes, response parsing, and normalization rules. Read the
section(s) for the backend(s) you routed to.

## Transport: curl vs WebFetch

This skill is harness-agnostic. Pick the transport your environment supports:

- **curl via your shell tool** — preferred in normal harnesses (Claude Code, Codex, opencode,
  terminal). Works for ALL backends.
- **native WebFetch / web_fetch tool** — GET-only, cannot set custom headers. In DSH's
  sandboxed shell this is the ONLY network path (shell has zero outbound network). Every
  key-less public GET backend below works through it.

### Host reachability via DSH web_fetch (verified 2026-10-01)

- REACHABLE (use these): `cn.bing.com`, `r.inews.qq.com`, `news.qq.com`,
  `soccer.hupu.com`, `sports.sina.com.cn`, `feed.mix.sina.com.cn`,
  `api.stackexchange.com`, `api.github.com`, `hn.algolia.com`, `context7.com`, `exa.ai`,
  `www.cngold.org`, `www.huilvbiao.com` (finance/market data; verified 2026-10-01)
- REACHABLE BUT JS-TRUNCATED (returns title/empty body — useless for content):
  `www.24k99.com` (homepage title only), `www.baidu.com` (HTTP 200, empty body). Prefer
  static-HTML sites when direct-fetching.
- NOT reachable (GFW-like egress): `api.search.brave.com`, `feeds.bbci.co.uk`,
  `www.theguardian.com`, `news.google.com`, `api.duckduckgo.com`, `rsshub.app`,
  `en.wikipedia.org` (DNS resolves to a non-public IP), `www.bing.com` (302 to
  cn.bing.com; web_fetch does not follow cross-origin redirects),
  `www.zhihu.com` API (HTTP 403 anti-bot).
- Rules: always use `cn.bing.com`, never `www.bing.com`. Prefer mainland-reachable hosts.
  If a host fails: drop that backend, record it in `errors`, continue the rest. If EVERY
  host fails with the SAME error (esp. `resolves to a non-public IP address`, including
  stable context7.com) it is an environment-level DNS/proxy outage — stop and report it
  instead of churning backends. This map is environment-specific — in an unrestricted
  harness, curl covers everything anyway.

## Secrets (keyed backends only)

Load order: environment variables, then `secrets.json` next to SKILL.md.

| Env var | secrets.json field |
|---|---|
| BRAVE_SEARCH_API_KEY | brave_api_key |
| EXA_API_KEY | exa_api_key |
| CONTEXT7_API_KEY | context7_api_key |
| ZHIHU_API_KEY | zhihu_api_key |

Key-less backends (bing, context7, qqnews, hupu, so, github, hn) need NO secrets.
Never hardcode keys into requests you log or into git. `secrets.json` is gitignored.

> **`tencent` is the exception**: its key is owned by the `tencent-news-cli` binary
> (`tencent-news-cli apikey-set`), not by `secrets.json`. The `TENCENT_NEWS_KEY` /
> `tencent_news_key` slots are unused — set the key through the CLI instead.

## Runtime prerequisites for the two scripts

| Script | Needs | Notes |
|---|---|---|
| `scripts/search.mjs` | Node 18+ | zero dependencies; only `tencent` shells out |
| `scripts/search.sh` | `curl` + a real Python | probes `$PYTHON` → `python3` → `python` |

Two Windows gotchas this repo already handles — keep them when editing:

- **`python3` may be a Store alias stub.** On Windows, `python3` can resolve to
  `.../WindowsApps/python3` which exits 0 and prints nothing, so every parser silently
  returns empty JSON. `search.sh` therefore *verifies real output*
  (`"$cand" -c 'print(1)'` must equal `1`) instead of trusting the command name.
  The same applies to the one-liner recipes below: if `python3` misbehaves, use `python`.
- **Native tools cannot read MSYS-style paths.** Passing `/d/repo/secrets.json` to a
  Windows Python raises `FileNotFoundError`; `search.sh` pipes the file through
  **stdin** instead. Do not reintroduce `python3 - "$path"` there.

## Normalized output

Produce (or have `scripts/search.mjs` emit) this shape, then write the user-facing summary:

```json
{"query":"...","backends":["bing","hupu"],
 "results":[{"backend":"bing","type":"web","title":"...","url":"...","snippet":"...","score":0.9,"published":"...","source":"..."}],
 "errors":[{"backend":"zhihu","error":"not configured"}]}
```

`type` values: web | news | docs | qa | repo | community | knowledge.

---

# A. Key-less backends (work via both curl and web_fetch)

## bing — general web search (RSS)  (verified)

Use for general web lookups, facts, fast answers, and query-specific news. The workhorse
backend for DSH.

```
GET https://cn.bing.com/search?q=<urlenc>&format=rss
```

- Returns RSS 2.0 XML, ~10 `<item>`s: `title`, `link`, `description`, `pubDate`.
- **Query rewriting matters (verified)**: relevance collapses on long natural-language
  queries with time phrases — `过去一周黄金价格走势` returned dictionary entries for "过去"
  with zero gold results; `现货黄金 上周 走势 回顾` drifted to "现货是什么" definitions.
  Rewrite to keywords first: keep head nouns + one time keyword ("黄金 本周 走势"). Then
  rank by `pubDate`, not just position. Also try the **tight compound** (verified:
  `昆明地震` hit 10/10 while `昆明 地震 新闻` returned only generic city pages — juxtapose
  place/event terms, drop generic suffixes like 新闻/资讯).
- Freshness: `filters=ex1%3a%22ez1%22` (24h) and `ex1%3a%22ez2%22` (week) only BIAS toward
  recency — old items still leak through (verified: a 2025-08 item passed the 24h filter).
  Always filter client-side against the requested window. For "latest/hot news" prefer
  qqnews/hupu.
- Numbers/data queries (行情/价格/销量, e.g. 黄金价格走势, 比亚迪销量): portals rarely carry
  the figures (verified: `比亚迪 销量 最新` → official/portal pages, zero sales numbers) —
  apply the two-step (routing.md): direct-fetch `www.cngold.org` (快讯+quote pages, numbers
  in HTML) or `www.huilvbiao.com/gold` (static tables). If step-2 shows placeholders (`--`),
  the number is often already in the RSS description (verified: 现货白银 60.62 in snippet).
- Zhihu fallback in DSH: append ` site:zhihu.com` + use the compound query form. Notes
  (verified): `site:` is only loosely honored — zhihu hits come back MIXED with general
  results, so filter client-side for `zhihu.com` before citing. Worse, conversational
  Chinese queries collapse to head-term definitions regardless of form (2026-10-01: both
  `产品经理 转行 AI site:zhihu.com` and its compound variant returned "什么是产品"
  definitions, zero on-topic hits) — if results are generic-definition pages the fallback
  MISSED: say so and degrade (exa/brave in curl harness); never cite off-topic pages to
  appear complete.

curl:
```bash
curl -sS --compressed "https://cn.bing.com/search?q=$(python3 -c 'import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))' "$QUERY")&format=rss"
```
web_fetch (DSH): fetch the same URL directly; the tool returns the XML as text.

Normalize: `{"backend":"bing","type":"web","title":title,"url":link,"snippet":description,"published":pubDate}`

## context7 — library/framework/API documentation  (verified, WebFetch-usable)

Search libraries (public):
```
GET https://context7.com/api/v1/search?query=<urlenc>
```
→ `{"results":[{"id":"/reactjs/react.dev","title":"React","verified":true,"score":280.8,...}]}`.
Pick top `verified:true` / highest `score`; note its `id`. If the top hit is a source repo
with sparse docs (low `totalTokens`/`totalSnippets`) or a `/llmstxt` duplicate, prefer the
`/websites/...` docs mirror instead (verified: vue `/vuejs/vue` had 118 snippets vs
`/websites/vuejs` 2142; pydantic's repo is rich at 2446 snippets so the repo won fine).

Fetch docs (public). URL-encode the id (drop leading `/`, inner `/` → `%2F`):
```
GET https://context7.com/api/v1/<id-encoded>?tokens=<N>&topic=<optional>
```
e.g. `/reactjs/react.dev` → `https://context7.com/api/v1/reactjs%2Freact.dev?tokens=4000&topic=hooks`
Returns markdown text directly (not JSON). `tokens` caps length (~4000 typical).

Normalize: `{"backend":"context7","type":"docs","library":id,"title":title,"url":"https://context7.com/"+id,"content":"<markdown>"}`

## qqnews — 腾讯新闻热榜 (Chinese news hot list)  (verified)

Use for "最新新闻 / 热点 / what's the news" — a live top-trending list, NOT query-filtered.
For query-specific Chinese news use bing instead.

```
GET https://r.inews.qq.com/gw/event/hot_ranking_list?page_size=<N>
```

- Response JSON: `ret:0`, `idlist[0].newslist[]`. Per item use ONLY:
  `title`, `url` (view.inews.qq.com/a/...), `time` ("2026-09-30 18:58:48"), `timestamp`,
  `abstract`, `readCount`, `commentNum`, `card.chlname` (source).
- The first list entry is a banner without `url` — skip items lacking `url`.
- The payload is very verbose (share metadata) — keep `page_size` <= 10 and ignore all
  other fields.
- **Absence proves nothing** (verified: a M4.3 Kunming quake ~20h old was NOT in the top-6
  during National Day rotation). Never treat "not in hot list" as evidence an event didn't
  happen — event verification always needs a query-specific search (bing).

Normalize: `{"backend":"qqnews","type":"news","title":title,"url":url,"snippet":abstract (300 chars),"published":time,"source":card.chlname}`

## hupu — 虎扑足球 news list  (verified)

Use for 足球/体育 news specifically — fresh headlines with links, several per hour.

```
GET https://soccer.hupu.com/
```

- web_fetch returns markdown: headlines are links `[title](https://bbs.hupu.com/<id>.html)`.
  Parse those directly — most reliable path.
- curl/raw HTML: extract anchors matching `https://bbs.hupu.com/\d+\.html`, strip nested
  tags (there is often an `<img>` inside the anchor), keep text >= 8 chars, dedupe by URL.
- Related boards as alternates: `https://bbs.hupu.com/482` (国际足球资讯),
  `https://bbs.hupu.com/china-soccer` (中国足球).
- The page is long (nav + several sections + forums); surface only the top ~10 headlines —
  the freshest items are the first list plus the 热门推荐 block (marked "N小时前").

Normalize: `{"backend":"hupu","type":"news","title":title,"url":url,"snippet":""}`

## so — Stack Overflow / Stack Exchange Q&A  (verified)

Use for "how do I fix / how to use" developer questions (complements context7).

```
GET https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=relevance&q=<urlenc>&site=stackoverflow&pagesize=<N>
```

- No key needed (quota 300/day unauth; response has `quota_remaining`).
- `items[]`: `title` (may contain HTML entities — decode), `link`, `score`, `is_answered`,
  `view_count`, `creation_date` (unix seconds), `tags[]`.
- To fetch an answer body later: `/2.3/answers/{ids}?site=stackoverflow&filter=withbody`.

Normalize: `{"backend":"so","type":"qa","title":title,"url":link,"snippet":"[tags] answered/unanswered · score N","score":score,"published":ISO(creation_date)}`

## github — repository search  (verified)

Use for finding codebases / tools / library alternatives.

```
GET https://api.github.com/search/repositories?q=<urlenc>&sort=stars&per_page=<N>
```

- No key: ~10 search req/min (HTTP 403 on limit → record error, continue).
- `items[]`: `full_name`, `html_url`, `description`, `stargazers_count`, `language`,
  `pushed_at`.

Normalize: `{"backend":"github","type":"repo","title":full_name,"url":html_url,"snippet":description,"score":stargazers_count,"published":pushed_at}`

## hn — Hacker News (Algolia)  (verified)

Use for tech community discussion / opinions / recent dev-world signal.

```
GET https://hn.algolia.com/api/v1/search?query=<urlenc>&hitsPerPage=<N>
```

- `hits[]`: `title`, `url` (may be null — fall back to `https://news.ycombinator.com/item?id={objectID}`),
  `points`, `num_comments`, `created_at`.

Normalize: `{"backend":"hn","type":"community","title":title,"url":url,"snippet":"N points · M comments","published":created_at}`

---

# B. Keyed backends (curl, or web_fetch only if key-less)

## brave — general web / facts / news  (curl only; header auth)

```
GET https://api.search.brave.com/res/v1/web/search?q=<urlenc>&count=<N>
GET https://api.search.brave.com/res/v1/news/search?q=<urlenc>&count=<N>
```
Headers: `X-Subscription-Token: <BRAVE_SEARCH_API_KEY>`, `Accept: application/json`; use `--compressed`.

```bash
curl -sS --compressed "https://api.search.brave.com/res/v1/web/search?q=<enc>&count=5" \
  -H "X-Subscription-Token: $BRAVE_SEARCH_API_KEY" -H "Accept: application/json"
```
Response: `{"web":{"results":[{title,url,description,age}]},"news":{...}}`
Normalize: `{"backend":"brave","type":"web|news","title","url","snippet":description,"published":age}`
In DSH: unreachable (host blocked + header auth) — record `{"backend":"brave","error":"unreachable in this environment"}` and use bing.

## exa — deep research / semantic  (curl only; POST + header)

```
POST https://api.exa.ai/search   body: {"query":"...","numResults":N,"type":"auto","contents":{"text":true,"maxCharacters":1000}}
POST https://api.exa.ai/contents body: {"ids":["url1"],"text":true}
POST https://api.exa.ai/answer   body: {"query":"..."}  → {"answer","citations"}
```
Headers: `x-api-key: <EXA_API_KEY>`, `Content-Type: application/json`.
Response: `{"results":[{title,url,score,publishedDate,text}]}`
Normalize: `{"backend":"exa","type":"web","title","url","snippet":text[:300],"score","published":publishedDate}`
In DSH: unreachable (POST + host) — degrade to bing + hn.

## tencent — 腾讯新闻 (official CLI)  (verified 2026-10-20)

Tencent's official **`tencent-news-cli`** — a Go binary, *not* an HTTP API. It prints
human-readable text and has **no `--json` / `--format` flag** (verified v1.0.17), so the
adapter parses its text output.

Official skill package: https://mat1.gtimg.com/qqcdn/qqnews/cli/hub/tencent-news.zip

### Install

```powershell
# Windows
irm https://mat1.gtimg.com/qqcdn/qqnews/cli/hub/tencent-news/setup.ps1 | iex
```

```bash
# macOS / Linux
curl -fsSL https://mat1.gtimg.com/qqcdn/qqnews/cli/hub/tencent-news/setup.sh | sh
```

Installs to `~/.tencent-news-cli/bin/tencent-news-cli[.exe]`.

> **Known installer bug (Windows, verified)**: `setup.ps1` fails with
> `No matching checksum found for windows-amd64/tencent-news-cli.exe` because its
> checksum loop sees the whole `checksums.txt` as **one string** (`$checksumContent.Count -eq 1`)
> instead of 5 lines, so the per-line regex never matches. Manual install:
> download `.../hub/windows-amd64/tencent-news-cli.exe`, compare against the SHA-256 in
> `.../hub/checksums.txt`, then place it at `~/.tencent-news-cli/bin/tencent-news-cli.exe`.
> Invoking `setup.ps1` via `pwsh` (not `powershell`) is what triggers this.

### API key

The key lives in the **CLI's own config**, never in this skill:

```bash
tencent-news-cli apikey-set <KEY>    # Windows: writes HKCU\Environment
tencent-news-cli apikey-get
```

Because it is persisted (registry on Windows, shell RC on macOS/Linux), a terminal that was
already open will not see it — set `TENCENT_NEWS_APIKEY` in the current process, or open a new
one. The adapter does **not** read `secrets.json` for this backend.

### Commands used

| Intent | Command |
|---|---|
| keyword news search | `search <关键词> --limit N` |
| trending / hot list | `hot --limit N` |

Both accept only `--limit` (plus the global `--caller`). Adapter mapping:

- non-empty query → `search <query>` — **always**; `--news` does *not* switch to the hot
  list, because every tencent result is already `type=news` and dropping a keyword
  returns unrelated headlines
- empty query → `hot` (热点榜) — the only case the CLI runs without keywords
- `--limit` clamped to 1-50 locally
- binary resolution: `TENCENT_NEWS_CLI_PATH` → `tencent-news-cli` on `PATH` →
  `~/.tencent-news-cli/bin/tencent-news-cli[.exe]`. The installer does **not** add itself
  to `PATH`, so a PATH-only lookup reports "not found" on a perfectly working install.

### Output text shape (this is what gets parsed)

```
【腾讯新闻 - 搜索「AI 芯片」】 2026-10-20 21:37

1. 标题：...
   摘要: ...
   来源: ...
   发布时间: 2026-10-20 10:26:12
   链接: https://view.inews.qq.com/a/...

共 2 条搜索结果，还有更多结果
```

Note the **title line carries the `N. ` ordinal** while every other field is indented —
a regex anchored on `^\s*标题` will not match. No-results output is the single line
`未找到与「...」相关的新闻` (exit 0); the adapter maps that to an empty result set.

### Failure modes (all detected from CLI text, since exit codes are unreliable)

| CLI text | Adapter error |
|---|---|
| binary missing at every candidate path | `tencent-news-cli not found (tried: <paths>) — install ...` |
| `未设置 API Key` / `not set` | `API key not configured — run: tencent-news-cli apikey-set <KEY>` |
| `API Key 无效` / `401` / `403` | `API key invalid or unauthorized` |


## zhihu — 知乎 OpenAPI global search  (verified 2026-10-20)

Zhihu's official **Global Search** endpoint. It searches the **whole public web**, not just
zhihu.com — so it is a general web backend with a China-mainland index, not a
"zhihu.com-only" one. Useful for Chinese-language topics and 知乎 discussion threads.

Official skill package: https://developer.zhihu.com/download/global_search_skills.zip
(SKILL.md v2.0.0 + `scripts/global-search.py`, Python stdlib only.)

```
GET https://developer.zhihu.com/api/v1/content/global_search
Authorization: Bearer $ZHIHU_API_KEY
X-Request-Timestamp: <unix seconds>
```

Query params (PascalCase, note the shift from the camelCase used elsewhere):

| Param | Required | Notes |
|---|---|---|
| `Query` | yes | search terms |
| `Count` | no | default 10, **server-clamped to 1-20** |
| `Filter` | no | advanced filter expression, e.g. `host=="36kr.com"` |
| `SearchDB` | no | `all` (default) / `realtime` / `static` |

Response is `{"Code":0,"Message":"success","Data":{"HasMore":bool,"SearchHashId":str,"Items":[...]}}`.
`Code` is `0` on success; a bad key returns `Code: 20001, Message: "Authorization failed"`.
Each item carries `Title`, `Url`, `ContentText`, `ContentType`, `ContentID`, `AuthorName`,
`AuthorBadge`, `VoteUpCount`, `CommentCount`, `EditTime` (unix seconds), `AuthorityLevel`,
`RankingScore`.

Adapter notes:

- `--news` maps to `SearchDB=realtime`; otherwise the API default (`all`) is used.
- `--limit` is clamped locally to 1-20 to match the server, so the reported count stays honest.
- `published` is derived from `EditTime` (seconds → ISO 8601); it is **edit time, not publish time**.
- `score` is `RankingScore` (relevance-ish, not a vote score).
- `AuthorName` / `ContentType` are frequently empty for plain web pages — only 知乎-native
  items tend to populate them. Do not assume they are present.

If `ZHIHU_API_KEY` is absent: the adapter returns `{"error":"missing key"}`. Fallback for
zhihu-intent queries remains bing RSS with `site:zhihu.com` — best-effort only; gate
citations on topical relevance and report honestly when it misses (see bing section).
