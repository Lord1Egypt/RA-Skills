# Routing strategy — cgartlab-search

Pick backend(s) by the user's PRIMARY intent. Multi-select (comma-separated) for broad
fan-out. Two columns: the curl recipe (any shell-networked harness) and the web_fetch
recipe (DSH / restricted-egress environments).

| Intent / signal | curl harness | DSH (web_fetch) |
|---|---|---|
| general web, facts, fast answer | brave | **bing** |
| library/framework/API docs, "how do I use X" | context7 | **context7** |
| dev how-to / error fixes (Q&A) | brave, exa | **so** (+ hn) |
| find a codebase / tool / alternative | brave | **github** |
| deep research / best content / opinion | exa, brave | **bing** (multi-angle queries) + **hn** |
| latest / hot news (全站热点) | tencent*, brave --news | **qqnews** (+ bing) |
| query-specific news ("X 最新消息") | brave --news | **bing** (append 新闻/最新) |
| 足球 / 体育 news | brave --news | **hupu** (+ bing, qqnews) |
| Chinese knowledge / opinion (知乎上怎么看) | zhihu*, exa | **bing best-effort**: `site:zhihu.com` + compound query; **gate on topical relevance — if results collapse to generic definitions, report the fallback missed** (then exa/brave) |
| broad "全面调研 / 全面了解 X" | exa,brave,context7 | **bing,context7,hn** |

(* = endpoint/key still pending; degrade as noted below.)

Rules of thumb:
- Language does not decide intent — a Chinese question about a JS library still goes to
  context7, not zhihu.
- "最新/热榜/新闻" → news backends first; "查一下X" (lookup) → bing; docs intent → context7.
- When unsure between bing and a specialist: bing for generic, specialist (hupu/so/github/
  hn/qqnews) when the domain matches — specialist sources are fresher and better scoped.
- **Rewrite long time-phrase queries to keywords before bing** (verified: "过去一周黄金价格
  走势" returned dictionary entries for "过去" and zero gold results). Keep head nouns + one
  time keyword — "黄金 本周 走势", "黄金价格 最新 走势 国际金价"; drop filler time words.
- **Retry with the tight compound form when the spaced form misses** (verified: `昆明地震`
  → 10/10 on-topic quake reports; `昆明 地震 新闻` → zero quake hits, only generic city
  pages). Juxtapose place/event terms without spaces and drop generic suffixes
  (新闻/资讯/文章) — they dilute RSS relevance instead of sharpening it. When one form
  misses, the other is the immediate second attempt.
- **Numbers/data queries (行情/价格/销量/榜单) = two-step pattern**: (1) keyword-form bing
  query to locate data sites; (2) direct-fetch 1–2 site pages for the actual figures —
  portal pages usually LACK them (verified: `比亚迪 销量 最新` → BYD official/baike/stock
  portals, zero sales figures). Verified targets (2026-10-01): `www.cngold.org` (快讯流 +
  quote pages carry numbers in HTML), `www.huilvbiao.com/gold` (static brand/recycle tables
  — but its /silver page showed JS placeholders `--`). If step-2 returns placeholders/empty,
  the number is often already in the bing RSS description (verified: 现货白银 60.62 quote
  appeared in snippet) — use it or switch to a cngold quote page. JS-only bodies → prefer
  static-HTML sites.
- Fan-out only for genuinely broad research; otherwise single backend to save time/tokens.
- Unreachable/unconfigured backends: record in `errors`, continue. NEVER fabricate results
  for a failed backend — say plainly what was and wasn't reachable.
- Fault scope decides the response: ONE host failing → skip that backend, continue; EVERY
  host failing with the SAME error (esp. `resolves to a non-public IP address`, including
  known-stable context7.com) → environment-level DNS/proxy outage — stop, report it, tell
  the user to check proxy/DNS; churning through more backends proves nothing.

Examples:
- "React 19 的 use() hook 怎么用？" -> context7 (topic=use)
- "最近 AI 搜索引擎有什么新动态？" -> qqnews + bing("AI 搜索引擎 新闻")
- "搜搜最新足球比赛新闻" -> hupu + bing("足球 新闻") + qqnews
- "TypeError: x is not a function 怎么修" -> so (+ bing)
- "全面调研一下 Bun JS runtime" -> bing,context7,hn (+ exa,brave in curl harness)
- "知乎上大家怎么看 Rust 后端落地？" -> zhihu if configured, else bing(`Rust 后端 site:zhihu.com`)
- "过去一周黄金价格走势" -> rewrite -> bing("黄金 本周 走势") -> direct-fetch www.cngold.org
  + www.huilvbiao.com/gold for actual quotes (market two-step)
- "比亚迪最新销量数据" -> bing("比亚迪 销量 最新") -> portals lack the figure -> direct-fetch
  a data page or quote the RSS-snippet number (numbers two-step)

Output: merge results, dedupe by URL, keep source attribution (`backend`), write a cited
Markdown summary grouped by type (Docs / Q&A / Web / News), always with source links.