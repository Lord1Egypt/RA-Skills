# Risks

## Purpose

Use this file when designing resilient collection, deciding whether to trust extracted content, and defining downgrade behavior for recurring A-share workflows.

## P0 Risks

P0 means the output would be materially wrong, fabricated, or operationally unsafe if not handled.

### Anti-bot or login wall misread as content

- Typical signal: `web_fetch` returns obfuscated JavaScript, disclaimer text, or empty shell; browser shows login gate or degraded view
- Common sites: 雪球, sometimes dynamic community/detail pages
- Risk: fake confidence that the site is publicly usable
- Mitigation: mark as `restricted` or `not-usable`; require logged-in relay or approved fallback source

### Homepage-only judgment on sites that require inner pages

- Typical signal: homepage fetch looks empty, noisy, or disclaimer-heavy while list/search/disclosure pages contain real content
- Common sites: 巨潮资讯, 东方财富
- Risk: false negative on site usability, leading to missed official facts
- Mitigation: test the fixed entrypoints in `references/entrypoints.md`; do not use homepage-only verdicts for production decisions
- Eastmoney-specific note: even on validated inner pages, `web_fetch` may still return disclaimer-heavy shells on `jgdy`/`rzrq`/`report`, so page reachability and field extractability must be judged separately

### Community opinion presented as confirmed fact

- Typical signal: emotionally loaded claims, causal narratives, target-price language, reposted screenshots, no primary source link
- Common sites: 韭研公社, 雪球
- Risk: summary mixes rumor and fact, creating false certainty
- Mitigation: assign `source_tier=T3`, use `opinion_risk`, and move the item into `市场观点与情绪` or `待核实线索` unless independently confirmed

### Silent data loss in cron collection

- Typical signal: one or more priority sites fail, but the final summary still reads complete
- Risk: hidden blind spots and overconfident downstream decisions
- Mitigation: always output `本轮缺失站点`; record what failed and what fallback source was used

## P1 Risks

P1 means the summary is directionally useful but may lose precision, coverage, or ranking quality.

### Partial extraction treated as full extraction

- Typical signal: readable text exists, but only snippets, headers, or incomplete body content are present
- Common sites: 韭研公社 list cards, some community/detail modules, 财联社 telegraph cards with `展开`, 巨潮 PDF only exposing metadata but no body text
- Risk: missing qualifiers, timestamps, or issuer names
- Mitigation: downgrade `credibility`, set `fact_status=partially-confirmed`, use `body_coverage`, and escalate to browser or alternate source if the item matters

### Login-dependent detail body assumed to be public-stable

- Typical signal: list page text is readable, but full正文 continuity, deeper expansion, or standalone detail routing cannot be reproduced without session state
- Common sites: 韭研公社, 雪球
- Risk: cron design overcommits to a page depth that only works intermittently or only when logged in
- Mitigation: keep default cron at the public list/search layer; require logged-in browser access before treating deep detail extraction as repeatable

### Dynamic routes or page variants break stable entrypoints

- Typical signal: same URL returns different modules by session state, region, or time; browser-visible content differs from fetched text
- Common sites: 雪球, some portal or专题 pages
- Risk: cron instability and non-repeatable coverage
- Mitigation: prefer fixed list/search/detail pages; maintain verified entrypoint lists; mark unstable pages as non-default
- Xueqiu-specific note: do not treat guessed direct routes like `/7x24` or `/livenews` as cron-safe just because a `7×24` tab appears inside another rendered page

### Telegraph detail over-promotion

- Typical signal: 财联社 telegraph 列表项带 `评论(...)`/detail 链接，于是被误判为一定存在更完整详情正文
- Risk: 把短电报错误提升为长文报道，或在 detail 正文与列表等价时重复记两条事实
- Mitigation: only create `detail_url` after actual hit; compare detail body with list body; if equivalent, keep one telegraph fact record and do not promote content type

### Duplicate event inflation

- Typical signal: multiple portals and reposts repeat the same announcement or telegraph, making one event seem larger than it is
- Risk: false perception of breadth or urgency
- Mitigation: apply `dedup_key`; merge same-event reports while keeping source provenance

### Time ambiguity across pages

- Typical signal: only date is present, or page displays local time without context, or repost time differs from original event time
- Risk: wrong market-session labeling and wrong chronology
- Mitigation: normalize to Asia/Shanghai; preserve uncertainty; avoid inventing exact timestamps

### Wrong ticker mapping

- Typical signal: company names are ambiguous, same abbreviation maps to multiple issuers, or article mentions peer companies
- Risk: event is attached to the wrong stock
- Mitigation: keep ticker blank when ambiguous; require unambiguous evidence before mapping

## P2 Risks

P2 means lower-severity quality issues that still deserve discipline in production workflows.

### Noisy portal content crowds out signal

- Typical signal: homepages, ad-heavy pages, or broad search pages contain large amounts of irrelevant text
- Risk: lower quality summaries and wasted crawl budget
- Mitigation: prefer targeted list/data/disclosure pages; cap per-site collection scope
- Xueqiu-specific note: homepage-style `资讯`/portal shells should not be the default cron anchor when `/today`, search, stock detail, or direct ranking/list pages can express the same intent more deterministically

### Over-collection of community chatter

- Typical signal: many low-value discussion posts with similar wording or repeated sentiment fragments
- Risk: sentiment section overwhelms factual section
- Mitigation: keep only representative signals; use `cron_keep=false` by default for weak chatter

### PDF binary mistaken as extracted body

- Typical signal: 巨潮 `detail` 跳转到 `finalpage/...PDF`, 但抓到的是 `%PDF-1.7`、对象流、加密脚本或 pdf viewer 壳
- Risk: binary/object-stream noise is summarized as if it were正文, causing fabricated key points
- Mitigation: treat as `metadata-only` unless usable human-readable text is actually recovered; prefer title-level summary and mark `未下钻PDF正文`

### Source-tier drift in manual summarization

- Typical signal: final prose no longer distinguishes T1/T2/T3 material
- Risk: readers cannot tell what is official, reported, or speculative
- Mitigation: include `来源层级说明` in the final output and preserve field-level metadata throughout normalization

### Fallback source sprawl

- Typical signal: too many substitute sites are pulled in ad hoc, reducing consistency
- Risk: workflow becomes hard to maintain and compare across cron runs
- Mitigation: use the approved fallback order only; note deviations explicitly

## Downgrade Strategy

Apply the first matching downgrade that protects correctness.

1. If login wall or anti-bot blocks meaningful extraction, mark `restricted`
2. If only shell or disclaimer text is returned, switch to browser or a fixed inner entrypoint
3. If browser still cannot reveal usable public content, mark the site missing for this round
4. If a 财联社 telegraph has only list body and no verified richer detail, keep it as `telegraph` with `body_coverage=list-full|partial`
5. If a 巨潮 detail resolves to PDF but no usable正文 is recovered, keep only metadata and title-derived summary; do not claim PDF body extraction
6. If the clue is community-only, keep it as T3 and do not promote it to confirmed fact
7. If a factual claim matters but remains unconfirmed, move it into `待核实线索`
8. If a priority site is missing, use approved public fallback sources and state the substitution

## Final Summary Safety Checks

Before delivering a production summary, verify all of the following:

- confirmed facts are traceable to T1 or well-supported T2 sources
- community sentiment is separated from confirmed facts
- unverified or conflicting claims are labeled explicitly
- missing sites and degraded access are disclosed
- no buy/sell recommendation language is introduced by the summarizer
