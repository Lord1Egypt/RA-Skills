# Fields

## Purpose

Use this file when normalizing cross-site A-share collection output, especially for formal summaries, recurring cron jobs, and any downstream merge or dedup step.

## Unified Record Schema

Use one normalized item per fact, event, disclosure, article, post, or clue.

```json
{
  "title": "",
  "summary": "",
  "source_site": "",
  "source_name": "",
  "source_url": "",
  "source_tier": "",
  "credibility": "",
  "content_type": "",
  "published_at": "",
  "captured_at": "",
  "market_session": "",
  "tickers": [],
  "company_names": [],
  "sector_tags": [],
  "event_tags": [],
  "region": "CN",
  "opinion_risk": "",
  "cron_keep": false,
  "dedup_key": "",
  "fact_status": "",
  "body_coverage": "",
  "detail_url": "",
  "origin_url": "",
  "pdf_url": "",
  "evidence_note": "",
  "raw_excerpt": ""
}
```

## Field Definitions

- `title`: source title or concise normalized headline
- `summary`: one- to three-line distilled content; do not add investment advice
- `source_site`: canonical site id, such as `cninfo`, `eastmoney`, `cls`, `jiuyangongshe`, `xueqiu`
- `source_name`: human-readable source name, such as `巨潮资讯` or `财联社`
- `source_url`: direct page URL used for this record
- `source_tier`: source quality tier used for ranking and output explanation
- `credibility`: confidence level of the record after source + content judgment
- `content_type`: normalized content class
- `published_at`: source publication time in ISO-like local form
- `captured_at`: actual crawl time in ISO-like local form
- `market_session`: `pre`, `mid-am`, `mid-pm`, `post`, `offhours`, or `unknown`
- `tickers`: normalized A-share codes only, such as `SZ300476`, `SH601872`
- `company_names`: normalized issuer names when available
- `sector_tags`: sectors, styles, themes, industries
- `event_tags`: normalized event labels such as `earnings`, `announcement`, `capital-flow`, `policy`, `rumor`, `telegraph`
- `opinion_risk`: degree of subjective interpretation or rumor contamination
- `cron_keep`: whether the item is worth retaining in recurring summary memory
- `dedup_key`: deterministic key for same-event merging
- `fact_status`: `confirmed`, `partially-confirmed`, `market-claim`, `unverified`, or `conflicting`
- `body_coverage`: `full`, `partial`, `list-full`, `metadata-only`, or `unavailable`
- `detail_url`: second-hop detail page actually used for this record, if any
- `origin_url`: upstream original source URL when the media page points to exchange/regulator/company original text
- `pdf_url`: direct PDF URL when the record resolves to a PDF announcement
- `evidence_note`: short note on why the status was assigned
- `raw_excerpt`: short direct excerpt for auditability

## Source Tier Standard

### `T1`

Use for official or near-official factual sources.

- 巨潮资讯
- 上交所 / 深交所
- regulator / ministry / statistical bureau sources
- company disclosures and exchange-confirmed materials

### `T2`

Use for strong public financial media or data-navigation sources with generally high utility but not primary legal disclosure.

- 财联社
- 东方财富 data/search/news pages
- major securities media used as fallback public confirmation

### `T3`

Use for community, discussion, plan, or sentiment-oriented sources.

- 韭研公社
- 雪球 posts, hot streams, discussion threads
- other non-official social or forum-style material

## Credibility Standard

### `high`

- direct disclosure or official statement
- same fact confirmed by multiple independent high-quality sources
- structured data page with clear attribution

### `medium`

- reputable media report without direct primary document in hand
- partial but coherent confirmation from public sources
- browser-visible content that appears real but still lacks primary backing

### `low`

- community claim, rumor, forwarded screenshot, or weakly sourced opinion
- single-source claim from discussion boards
- anti-bot-limited or partial extraction with missing context

## Opinion Risk Standard

### `low`

- mostly factual, source-attributed, limited interpretation

### `medium`

- contains analyst framing, community interpretation, or causal inference

### `high`

- speculative, rumor-like, emotionally loaded, or strongly directional commentary

## Content Type Standard

Use one primary type per record.

- `announcement`: formal disclosure or filing
- `news`: standard article or straight news report
- `telegraph`: short fast-news item
- `data-page`: structured or semi-structured market data page
- `research`: research note, brokerage summary, strategy text
- `community-post`: social/community post or discussion item
- `timeline`: time-ordered event/feed item
- `topic-board`: sector/theme aggregation page
- `stock-detail`: individual stock detail page
- `policy`: policy or macro/regulatory release
- `rumor`: unverified market chatter or claim

## Cron Keep Standard

Set `cron_keep=true` only when the item is likely to matter after the current round.

Keep by default:

- official announcements and disclosures
- high-impact policy and macro releases
- material earnings / forecast / restructuring / punishment / halt-resume events
- repeated intraday catalysts that shaped market direction
- strong consensus signals seen across multiple sources

Do not keep by default:

- low-signal community chatter
- duplicate telegraphs with no new facts
- routine portal noise
- weak sentiment fragments that do not change understanding

## Time Normalization

- Normalize all times to Asia/Shanghai
- Use `YYYY-MM-DD HH:MM:SS+08:00` when exact time is available
- If only date is available, use `YYYY-MM-DD` and leave session as `unknown` unless context is explicit
- Preserve uncertainty in `evidence_note`; do not invent missing minute/second precision
- `captured_at` should reflect actual crawl time, not rewritten source time

## Ticker and Company Normalization

- Normalize A-share tickers as `SH600000`, `SZ000001`, `BJ430047`
- Preserve multiple tickers if the item is cross-company
- Do not mix index codes and stock codes in the same field unless clearly needed
- If a source gives only company name, infer ticker only when unambiguous
- When ambiguity remains, keep company name and leave ticker blank

## Body Coverage Rules

### 财联社 telegraph

- 列表正文已完整可读时，设 `body_coverage=list-full`
- 列表出现 `展开` 且未二跳确认完整正文时，设 `body_coverage=partial`
- 若二跳到 `https://www.cls.cn/detail/<id>` 后正文与列表等价，仍保留 `content_type=telegraph`，并把 `detail_url` 填上，不要改写成深度长文
- 若存在 `查看原文` 并命中交易所/公告原文链接，可将该链接记入 `origin_url`; 只有真的使用原文内容时，才把事实层确认升级到对应原始来源
- 无法命中 detail 或没有必要二跳时，`source_url` 保持 telegraph 列表页，`detail_url` 留空

### 巨潮资讯 announcement/PDF

- 列表页可读到代码、简称、标题、日期时，至少可设 `body_coverage=metadata-only`
- `detail` 链接若直接跳转 PDF，但当前轮未抽到可用正文，不要把 PDF 当作 `full`; 仍记 `body_coverage=metadata-only` 或 `unavailable`
- 只有拿到可复制文本、可解析正文片段、或可靠人工核对到关键段落时，才可升级到 `partial` 或 `full`
- 基于公告标题生成的保守一句话摘要，应在 `evidence_note` 说明 `title-derived`; 不要伪装成来自 PDF 正文的摘要

## Dedup Rules

Build `dedup_key` from the most stable combination available.

Preferred order:

1. normalized source URL when the page is unique and canonical
2. `content_type + normalized title + published_at + primary ticker`
3. `event tag + issuer + event date + key numeric attribute`

Dedup guidelines:

- merge reposts of the same disclosure or fast-news event
- keep separate records when later items materially update the fact set
- keep official disclosure and community reaction as separate records, but link them conceptually in the final summary
- if two sources disagree, do not force dedup; mark `fact_status=conflicting`

## Fact Classification Rules

- `confirmed`: supported by T1 source or multiple reliable sources
- `partially-confirmed`: key point is supported, but some details remain incomplete
- `market-claim`: widely circulated market statement without primary confirmation
- `unverified`: single weak clue with insufficient support
- `conflicting`: sources disagree on material facts

## Output Discipline

- Facts and sentiment must be separable from the raw records
- Community content must carry `T3` and a non-`low` `opinion_risk` unless it is merely relaying a confirmed fact
- Never upgrade a T3 community post to `high` credibility without independent confirmation
- Final summaries should consume these fields rather than freehand mixing fact and opinion
