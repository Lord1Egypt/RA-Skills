# Entrypoints

## Purpose

Use this file when defining stable A-share collection entry pages, cron priorities, and the default crawl path for the five target sites.

## Five Fixed Entrypoints

### 东方财富

- Primary: `https://so.eastmoney.com/`
- Secondary: `https://data.eastmoney.com/zjlx/dpzjlx.html`
- Secondary: `https://data.eastmoney.com/jgdy/`
- Role: public portal, search hub, data-center navigation, quasi-structured market pages
- Default mode: `fetch-first`, upgrade to `browser` for page truth and structured blocks

#### 东方财富子页面实测结论

- 公告大全 `https://data.eastmoney.com/notices/`: `已验证可用`; browser 可稳定看到列表页标题与表格壳，`web_fetch` 只能拿到很薄的正文文本，因此推荐 `browser-first`; 适合默认 cron，但更适合抓列表字段而不是正文全文
- 龙虎榜 `https://data.eastmoney.com/stock/lhb.html`: `已验证可用`; `web_fetch` 已能稳定抽到列表字段名与日期区块（如代码、名称、上榜次数、龙虎榜净买额、营业部维度字段），推荐 `fetch-first`; 适合默认 cron
- 融资融券 `https://data.eastmoney.com/rzrq/`: `可见但不稳定`; 页面可打开，但 `web_fetch` 多次只落到免责声明/页脚，说明首屏主要内容依赖前端渲染；推荐 `browser-first`; 不建议作为默认 cron 主入口，除非先补专门页面规则或替代源
- 机构调研 `https://data.eastmoney.com/jgdy/`: `可见但不稳定`; 页面可打开，但 `web_fetch` 主要返回免责声明，列表字段未稳定暴露；推荐 `browser-first`; 不建议默认 cron 直接依赖，除非用 browser 定向抓表格
- 研报 `https://data.eastmoney.com/report/`: `可见但不稳定`; browser 可见页面，`web_fetch` 仍以免责声明为主，评级/目标价/研究员等关键字段未在轻抓取中稳定出现；推荐 `browser-first`; 不适合默认 cron 作为轻量抓取源
- 财报/预告 `https://data.eastmoney.com/bbsj/`: `已验证可用`; browser 可见年报季报列表，`web_fetch` 能稳定抽到业绩报表/业绩预告字段名（营业总收入、净利润、公告日期、预告类型等），推荐 `fetch-first`; 适合默认 cron

### 财联社

- Primary: `https://www.cls.cn/telegraph`
- Secondary: `https://www.cls.cn/finance`
- Secondary: `https://www.cls.cn/depth?id=1003`
- Role: fast news, telegraph stream,盘中异动, A-share depth pages
- Default mode: `fetch-first`, upgrade to `browser` when structure or completeness matters

#### 财联社 telegraph -> detail 实测结论

- `https://www.cls.cn/telegraph` 已验证可稳定抓到列表层正文；`web_fetch` 可直接拿到时间、标题、正文、阅读数，`browser` 可看到列表卡片、`展开`、`评论(0)`、部分 `查看原文`
- 列表卡片里的 `评论(...)` 实际可映射到 `https://www.cls.cn/detail/<id>`；实测 `https://www.cls.cn/detail/2312340` 可正常打开，并能拿到标题与正文
- 但 `detail` 页对多数 telegraph 只是 canonical detail 页，并不天然意味着“比列表更长的正文”；实测样例中，`detail` 正文与列表基本等价，只多了关联话题等外围信息
- 部分公司/公告类 telegraph 还会出现 `查看原文`，实测可直链到上交所 PDF；这类链接是“原始出处二跳”，不是财联社自有长文正文
- 最小可行映射规则：默认先保留 telegraph 列表层；只有命中以下任一条件才做二跳：`列表正文被截断/需点展开`、需要稳定 canonical URL、需要判断是否有 `查看原文` 原始出处、需要补关联话题/标签
- 禁止把“存在 detail 链接”自动等同于“存在更完整正文”；若 `detail` 与列表正文等价，保留 `content_type=telegraph`，不要强行改写成长文 `news`
- 若 telegraph 无可用 `detail` 命中、无 `查看原文`、且列表已足够表达事实，则只保留列表记录即可

### 巨潮资讯

- Primary: `https://www.cninfo.com.cn/new/commonUrl/pageOfSearch?url=disclosure/list/search`
- Secondary: `https://list.cninfo.com.cn/`
- Role: formal disclosure, announcement verification, official confirmation layer
- Default mode: `browser-first` on disclosure/list/search pages
- Avoid: judging the site from homepage-only fetch results

#### 巨潮 PDF 二跳实测结论

- `browser` 在公告查询页可稳定看到列表表格，标题链接会落到 `https://www.cninfo.com.cn/new/disclosure/detail?...`
- 实测 `detail` 链接并不会先给 HTML 正文，而是直接 302 到 `https://static.cninfo.com.cn/finalpage/YYYY-MM-DD/<announcementId>.PDF`
- `web_fetch` 对该 PDF 直链拿到的主要是 PDF 二进制/对象流，不是可直接消费的正文摘要；浏览器打开 PDF 也只能看到 iframe/pdf viewer，`document.body.innerText` 基本为空
- 因而巨潮“二跳 PDF 抽取”默认不是轻量稳定链路；最小可行方案应以 `列表元数据 + 标题语义摘要` 为默认层，而不是默认追求 PDF 正文
- 值得二跳 PDF 抽取的场景：公告标题明显高价值（如回购、重组、业绩预告、处罚、终止上市风险、重大合同、药品批准等）、需要补关键金额/比例/对象/日期、或需验证财联社/东方财富转述是否与原公告一致
- 不值得二跳的场景：会议资料、法律意见书、H股市场公告、常规程序性文件、列表标题已足够表达事实、当前轮只是广覆盖 cron 扫描
- 默认降级：若无现成 PDF 文本提取能力，则保留 `code/name/title/date/detail-url/pdf-url(if known)` 元数据，并基于标题做保守摘要，明确“未下钻 PDF 正文”
- 若后续具备 PDF 文本能力，也应优先做“命中后少量二跳”，不要对整页公告列表批量全量下钻 PDF

### 韭研公社

- Primary: `https://www.jiuyangongshe.com/plan`
- Secondary: `https://www.jiuyangongshe.com/announcement`
- Secondary: `https://www.jiuyangongshe.com/timeline`
- Stable sub-routes: `https://www.jiuyangongshe.com/plan?pageType=search&stock_name=<股票名>` for stock-hit second hop, `https://www.jiuyangongshe.com/u/<user_id>` for author pages
- Role: topic logic, plan flow, event timeline, community heat
- Default mode: `browser-first`
- Login note: list pages are publicly readable in browser; stronger detail continuity depends on session state and should not be assumed in default cron

### 雪球

- Primary: `https://xueqiu.com/today`
- Secondary: search results like `https://xueqiu.com/k?q=中芯国际`
- Secondary: stock detail pages like `https://xueqiu.com/S/SH600000` and `https://xueqiu.com/S/SZ000001`
- Secondary: ranking pages under `https://xueqiu.com/hq/detail?...` and screener JSON such as `https://xueqiu.com/service/v5/stock/screener/quote/list?...`
- Avoid as fixed entrypoint: homepage shell `https://xueqiu.com/` and guessed `/7x24` or `/livenews` direct routes
- Role: market sentiment, hot-topic discovery, stock-level attention and quote snapshot
- Default mode: anonymous mixed (`browser-first` for rendered pages, `fetch-first` only for explicit JSON ranking APIs); with logged-in relay `browser-first`

## Verification Status

### 已验证

- 东方财富: search/data-center entry pages are publicly reachable and are suitable as the default stable layer
- 财联社: telegraph and A-share pages are publicly reachable and suitable for fast-event collection
- 巨潮资讯: disclosure/list/search pages are the correct verification target; homepage-only judgment is misleading
- 韭研公社: `plan` / `announcement` / `timeline` are usable as browser-first discovery entrypoints; `plan?pageType=search&stock_name=<股票名>` is a repeatable stock-hit page; no stable public post-detail permalink was confirmed from the list layer
- 雪球: stock detail pages and hot-topic views are usable only when access quality is sufficient; login state materially improves reliability

### 待补验证

- 巨潮资讯 deeper search/list result pages should be rechecked when building a production cron job
- 东方财富 subdomain-specific pages may differ in extraction quality and should be sampled before expansion
- 韭研公社 post body expansion works on some visible list cards without login, but deeper post/detail continuity still appears to depend on dynamic loading or session state and should be treated as non-default
- 财联社 some dense专题/深度 pages may need page-specific parsing rules

## Cron Scenario Priority

Use source priority by scenario, not by site prestige.

### 盘前摘要

1. 巨潮资讯
2. 东方财富
3. 财联社
4. 韭研公社
5. 雪球

Goal: overnight announcements, scheduled disclosures, pre-open catalysts, high-confidence factual setup.

### 盘中摘要（午间 / 尾盘）

1. 财联社
2. 东方财富
3. 巨潮资讯
4. 韭研公社
5. 雪球

Goal: event flow, sector rotation,异动 signals, then backfill official verification when needed.

### 盘后摘要

1. 巨潮资讯
2. 财联社
3. 东方财富
4. 韭研公社
5. 雪球

Goal: confirmed disclosures, post-close news, recap context, then add community interpretation as secondary material.

### 专题核查 / 个股核查

1. 巨潮资讯
2. 东方财富
3. 财联社
4. 雪球 stock detail
5. 韭研公社

Goal: verify facts first, then add market reaction and discussion.

## Xueqiu Subpage Rules

### `/today`

- Anonymous state: `browser` can usually render real feed cards, timestamps, and market snapshot modules; `web_fetch` often returns obfuscated anti-bot JavaScript instead of usable text
- Logged-in state: more complete and more repeatable than anonymous, but still treat as a community/discovery stream rather than a fact source
- Cron default: `yes`, but only as a low-weight sentiment/topic-discovery input and only through `browser-first`
- Best use: midday or post-close heat scan, hot posts, fast topic discovery, candidate stocks for secondary verification
- Not for: standalone factual cron output, exact full-feed coverage, or official-news substitution

### `7x24`

- Anonymous state: direct routes like `/7x24` and `/livenews` are not stable fixed entrypoints in testing; they commonly fall into 404, front-end reroute, or tab-only navigation behavior
- Logged-in state: the `7×24` tab reachable from `/today` may become usable inside a live session, but route stability is still weaker than `/today`
- Cron default: `no`
- Recommended use: manual trigger, low-frequency whitelist probe, or session-bound browser navigation from `/today` when the user explicitly wants Snowball fast-news flavor
- Safer default: use 财联社电报 as the cron default fast-news layer and treat 雪球 `7×24` as optional enrichment only

### `资讯`

- Anonymous state: do not assume a single stable public `资讯` landing page; homepage-like shells are noisy and route variants are easy to misjudge
- Logged-in state: can be explored interactively, but page identity and module composition vary enough that it should not be the default cron anchor
- Cron default: `no`
- Recommended use: manual exploration only, or per-session browser navigation after a clue already exists
- Safer default: use `/today` for broad discovery and stock/detail or search pages for scoped follow-up

### Search result pages

- Anonymous state: rendered search pages like `https://xueqiu.com/k?q=中芯国际` are materially usable in `browser`; they expose tabs, stock hits, and some discussion/QA snippets, while `web_fetch` usually yields only thin shell text
- Logged-in state: better continuity and likely deeper modules, but anonymous browser access is already sufficient for scoped discovery
- Cron default: `conditional`
- Recommended use: whitelist/targeted lookup for named stocks, concepts, or companies after another source or rule supplies the query term
- Not for: broad default cron crawling, because query choice drives coverage and can easily create unstable scope

### Ranking pages and list rules

- Anonymous state: rendered ranking/list pages under `/hq/detail?...` are more stable than homepage shells; explicit screener JSON APIs under `/service/v5/stock/screener/quote/list?...` can return structured anonymous data in testing
- Logged-in state: still preferred for browser continuity, but not required for the specific ranking/list probes that already work anonymously
- Cron default: `yes`, with scope control
- Recommended default rule: prefer direct ranking/list URLs or screener APIs for A-share leaderboards instead of scraping the homepage or guessing front-end tabs
- Recommended cron shape: whitelist a small set of stable list types (for example 涨幅榜 / 跌幅榜 / 成交额 / 龙虎榜相关公开榜单 where available) and poll at low frequency
- Not for: large fan-out crawling across many tab combinations, because route combinations are front-end driven and increase breakage risk

## Default Crawl Strategy

## 1. Start from the fixed entrypoint, not the homepage shell

- Prefer search/list/data/disclosure/telegraph/detail pages
- Avoid homepage-only judgments for 巨潮资讯 and noisy portal shells for 东方财富
- On 雪球, prefer `/today`, explicit search pages, stock detail pages, and direct ranking/list URLs over the homepage shell

## 2. Probe cheaply, then escalate

- Use `web_fetch` first on 东方财富 and 财联社
- Use `browser` first on 巨潮资讯 and 韭研公社
- On 雪球, use `browser` first for rendered pages and reserve `web_fetch` for known JSON endpoints like screener/ranking APIs

## 3. Separate site roles

- 巨潮资讯: official confirmation
- 东方财富: public aggregation and data navigation
- 财联社: fast event stream
- 韭研公社: topic logic and community clues
- 雪球: sentiment,热度, stock detail, and discussion

## 4. Keep extraction scoped

- Prefer list pages, search results, disclosure pages, telegraph streams, and stock detail pages
- For 韭研公社 default cron, stay on `plan`, `announcement`, `timeline`, and stock-hit pages like `plan?pageType=search&stock_name=<股票名>`
- Treat deeper community post/detail pages as second-hop only after a list item or stock hit is already judged worth expanding
- Do not over-collect deep community comment trees in default cron runs
- Escalate to deeper pages only when a clue needs confirmation or expansion

## 韭研公社 Page-Level Guidance

### Public list layer: default cron

- `plan`: good for low-frequency scans of stock heat, recent logic snippets, timestamps, and stance labels like `看好` / `谨慎`
- `announcement`: good for keyword-based clue collection and announcement-to-community linkage, but not as an official confirmation layer
- `timeline`: good for event-flow discovery and day-level topic changes
- `plan?pageType=search&stock_name=<股票名>`: best fixed second-level page for stock-specific expansion after another source or heat list hits a name

### Detail/body stability

- Public browser view can read the visible text already rendered in list cards, and some `展开` actions work without login
- This is only stable for the list-visible body segment, not for a confirmed standalone full-detail page
- A stable public permalink pattern for individual plan posts was not confirmed from the tested page DOM
- Therefore, treat visible list-card body as `partial` by default unless the full text is clearly present after expansion

### Login-only or login-preferred usage

- Logged-in sessions are the only safe way to assume repeatable access to deeper post bodies, user-history drilling, or any hidden/detail-only modules not exposed in the public list DOM
- If the task explicitly requires full正文 continuity across many posts, classify 韭研公社 as login-preferred rather than public-stable

### Cron policy

- Default cron: yes for `plan`, `announcement`, `timeline`, and low-frequency stock-hit pages
- Default cron frequency: low to moderate only; prefer a small number of list snapshots instead of wide or deep expansion
- Hit-driven second hop: yes for `plan?pageType=search&stock_name=<股票名>` after a stock is surfaced by heat lists, official news, or fast-news sources
- Deep post/detail expansion: no for default cron; use only when a clue is already important enough to verify or enrich

### Conservative downgrade

- If list pages render normally, keep 韭研公社 as `usable` for discovery and sentiment clues
- If only snippets are visible, mark the body as `partial` and keep it in `市场观点与情绪` or `待核实线索`
- If a stock-hit page stops rendering useful content, fall back to the top-level list pages and do not invent missing logic chains
- If full正文 is required but only snippets are reachable, declare 韭研公社 missing for full-detail coverage in this round and backfill with 财联社 / 东方财富 / 交易所公告 for factual confirmation

## 5. Report missing access honestly

- If a site is blocked, login-gated, or unstable, mark it as missing for this round
- Fall back to approved public alternatives rather than fabricating coverage
