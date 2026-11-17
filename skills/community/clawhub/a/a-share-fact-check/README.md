# a-share-fact-check · 投资内容体检

[中文文档 (Chinese)](README.zh-CN.md)

A Claude Skill that audits investment content — stock pitches, advisor ads, commentary, relayed earnings calls — against official disclosure and cross-validates it across independent sources. It is plain Markdown, so it runs in any harness that loads skill-style instructions.

> **Market scope.** A-shares (SSE / SZSE main boards, ChiNext, STAR, BSE) are fully supported — this is where the framework is actually exercised. NEEQ is supported for disclosure claims, but has no continuous market-data stream, so valuation claims are out of scope by construction. Hong Kong disclosure is retrievable via HKEXnews, but the caliber mapping for HK line items and the HK valuation series are not built yet, so HK claims are **honestly degraded to ⚠️ rather than guessed**. No other market is in scope.

---

**a-share-fact-check（投资内容体检）** 是一个面向中国上市公司的开源 Claude Skill。它把一篇已经存在的投资内容——荐股文、投顾获客广告、投资点评、公众号推文、雪球/小红书帖子、业绩说明会转述——拆成断言级单元，逐条对齐官方披露与交易所行情数据，并在多个独立来源之间交叉校验，输出一份「哪些为真 / 哪些对不上 / 哪些查无此据 / 哪些是纯话术」的核验报告。

它的方向与常见的金融 AI 相反：不从 ticker 生成研报，而是从内容审计断言。核验基准只取两条官方流——法定披露流（巨潮资讯网、沪深北交易所、港交所披露易、全国股转系统）与官方行情流（交易所成交数据）；第三方财经平台仅作线索定位，不作判真伪基准。取不到数据时按规则降级标注为「待核验」，不臆造数据，也不拼造来源链接。

边界是划死的：不预测股价、不做估值与建模、不给买卖结论。它只就公开信息的一致性做核验，判断权留给使用者，不构成投资建议。

---

## Installation

The runtime artifacts are `SKILL.md` plus the `references/`, `playbooks/`, `sources/`, and `tools/` directories. Install the folder wherever your harness expects skill directories:

```
git clone https://github.com/<owner>/a-share-fact-check.git /path/to/your/skills/a-share-fact-check
```

Or install the packaged bundle `a-share-fact-check.skill` through your client's skill installer.

### Optional dependencies

| Component | Purpose | Without it |
|---|---|---|
| [AKShare](https://github.com/akfamily/akshare) | Full-history PE/PB/PS/market-cap series; self-computed valuation percentiles | Percentile claims fall back to a search-derived range, explicitly marked "estimated, pending verification" |
| 企查查 MCP | Corporate registry, equity penetration, risk records | Equity-chain claims beyond the disclosed shareholder table are downgraded to ⚠️ |

Neither is required. The Skill degrades affected claims rather than filling the gap with guesses.

## Usage

Paste an article and ask for a check. The Skill triggers on content, not on a ticker.

```
Fact-check this article: [paste the full text]
```

```
这篇荐股文靠谱吗？[粘贴全文]
```

Give it the **whole article**. Picking out the "key claims" is the Skill's job, not yours — claim extraction and typing is step 2 of the pipeline.

### What counts as input

Anything already written that makes checkable assertions about a listed company. Stock pitches are the highest-frequency case, not the boundary.

| Input | Typical source | Triage |
|---|---|---|
| Stock pitch 荐股文 | WeChat public accounts, Xueqiu, Xiaohongshu, group forwards | A — full pipeline |
| Advisor lead-gen ad 投顾获客广告 | Persona + track record + funnel, target deliberately unnamed | B — funnel exposure, bait claims not checked one by one |
| Investment commentary 投资点评 | Community posts, newsletters, "why I'm holding X" | A |
| Relayed earnings call 业绩说明会转述 | Second-hand write-ups of management remarks | A, mostly ②′ relayed-forecast claims |
| Day-trader recap 游资复盘 | Post-hoc narratives of a run | A, montage-heavy — NE-1 / NE-4 fire often |
| Company promo / IR material 公司宣传稿 | Company-authored copy repeated as fact | A, discounted to P5–P6 rather than treated as disclosure |
| Screenshot 截图 | Any of the above, as an image | A — text is read from the image first |

What it is **not** for: "analyze this stock", "value it", "build me a model". Those are generation, not audit, and the Skill will say so instead of drifting into them.

## Overview

Most financial AI runs **company → research**: a ticker goes in, a report comes out. This Skill runs the opposite direction — **content → audit**: an article someone else already wrote goes in, a verdict on that article comes out.

The direction matters because it changes what can be reported. A generation tool has no way to say that a number *does not exist*: if it can't find the claimed "30亿 order backlog" in the annual report, it simply writes something else. An audit tool has to say so out loud. **"Not found in any official filing" is a first-class verdict here, not a footnote** — and in stock pitches it is often where the worst material hides.

The base model is the real baseline to beat. Anyone can paste the article into Claude and say "check this." What this Skill adds is not knowledge — it is **constraint**: a fixed source hierarchy, a closed verdict set, caliber and tolerance discipline, and a hard rule against fabricating source links. The constraints are the product.

### The core assumption

Hard data fabrication is rare. The lie is almost always in the assembly:

```
true A  +  true B  +  true C   ──▶   false D
```

Per-claim checking returns all-✅ on exactly these articles and misses the point entirely. So the pipeline runs a second, combination-level pass after per-claim verification, and the montage verdict goes into the main table — not into a note underneath it.

## How it works

```
Article
  → Triage        (A: verifiable pitch | B: lead-gen ad | Hybrid: A-primary + B-module)
  → Claim extraction & typing (5 label types)
  → Normalization (5-tuple Claim Schema; colloquial → GAAP-term mapping)
  → Route to 7 playbooks
  → Verification  (structured-first, three-state verdict)
  → Montage scan  (6 narrative-error types)
  → Report        (quick-read + per-claim table)
```

Triage runs first, deliberately. Running the full pipeline over a lead-gen ad audits the wrong target: it spends effort on whether the author started with 500k or 300k, when the harm of that article lies entirely in the funnel at the bottom. Checking the bait claims one by one also lends the ad the legitimacy of having been taken seriously.

### Claim types

Every sentence gets one of five labels. Only ① and the historical premises of ② enter the verification pipeline.

| Label | Type | Example | Handling |
|---|---|---|---|
| ① | Hard fact | "2024 revenue grew 45%" | Route to a playbook |
| ② | Forecast / stance | "we'll be number one next year" | Verify the historical premise only, never the future |
| ②′ | Relayed forecast | "the company cut FY26 guidance to 170m" | Verify **that the company said it**, not that it will come true |
| ③ | Opinion | "this company is incredible" | Not falsifiable; marked "no factual support" |
| ④ | Manipulation cue | "institutions are accumulating", "insider info" | Not verified; marked as a risk signal |

②′ is deliberately split into two layers. The fact layer ("the company issued this guidance") is checkable; the forecast layer ("the number will materialize") is not. A faithful relay gets `✅ (relay accurate) + 🔮 (company forecast, unresolved)`. An altered relay gets `❌`. The forecast number itself is never marked ✅ — that would be endorsing a prediction.

## Seven verification playbooks

Each playbook follows the same five-step contract (extract → normalize → retrieve → compare → adjudicate) and contains only what is specific to its claim type. Shared rules live in `references/`.

| # | Playbook | Claim types | Verified against | Type-specific discipline |
|---|---|---|---|---|
| 01 | Financial figures | Revenue, net profit (3 calibers), margins, leverage, cash flow, ROE/growth | Periodic reports (P1–P2) | Unstated net-profit caliber → check all three; derived metrics must carry their formula and inputs |
| 02 | Equity & control | Shareholding %, controller, major holders, stake changes | Latest "shareholders" section > change-of-interest filings > prospectus | Direct and indirect holdings both computed; a timestamp is mandatory — equity is dynamic |
| 03 | Use of proceeds & capacity | Fundraising purpose, capacity, expansion, projects under construction | Prospectus "use of proceeds" > periodic report progress table | The **status word** is the crux: "planned" reported as "operational" is the high-frequency error |
| 04 | Market share & position | Share, ranking, "industry leader", "outgrowing the sector" | Prospectus competition section (discounted) + trade-association data | Caliber triad (basis × scope × compiler) must align **before** any comparison; otherwise ⚠️, never a forced verdict |
| 05 | Policy existence | Cited policies, subsidies, regulations | Issuing ministry's official site | Checks **only** that the document exists, is correctly attributed, and is in force — never compliance or applicability |
| 06 | Manipulation cues | Urgency, privileged-info hints, herd cues, certainty language, vague authority | No external source; pattern recognition | New phrasings are folded in as variants of existing classes, not new classes — otherwise the library explodes |
| 07 | Valuation & market data | PE/PB/PS, dividend yield, market cap, price, "Nth percentile over 5 years" | Exchange market data; AKShare as the structured mirror | Percentiles are **self-computed** from the raw series, never taken from a vendor's ready-made number |

Playbook 07 splits compound claims across streams: PE = price ÷ EPS, so the price half is checked against the market stream and the EPS half against the disclosure stream, under playbook 01's caliber rules.

## Six montage patterns (with examples)

Per-claim verification is largely ineffective against these. Each cited fact stays ✅ on its own; a **separate claim is added** for the conclusion the assembly produces, and that claim is adjudicated on its own.

| # | Pattern | Signature | Example (from real pitches) |
|---|---|---|---|
| **NE-1** | Survivorship bias | Only winners cited; the many non-performers omitted | "Every Huawei move produces a multi-bagger" + five limit-up cases |
| **NE-2** | False causation | Correlation or coincidence dressed as an iron law | "Huawei acts → the stock rises"; "history proves it repeatedly" (n=3) |
| **NE-3** | Metric mixing | Figures across sources, currencies, base years, or calibers spliced into one paragraph | QYResearch (RMB / to 2032) + Frost & Sullivan (USD / to 2034) read as a single growth story |
| **NE-4** | Time-window manipulation | Periods compressed or shifted to manufacture continuity or a larger gain | "8x in 2022" when the run began in 2021; trough-to-peak measurement |
| **NE-5** | Entity substitution | Real data builds authority, then the conclusion jumps to an uncheckable or anonymous target | Thirty true facts → an anonymous "core supplier" |
| **NE-6** | Extrapolation from outliers | An extreme case implied to be reproducible; the 99% who failed are absent | "He turned 500k into billions — so can you" |

Adjudication rule, uniform across all six:

1. **Individual facts stay honest.** If the number checks out, it gets ✅. Real data is never punished.
2. **The conclusion gets its own row**, marked ⚠️ (assembly misleads: true cases ≠ valid rule). It escalates to ❌ only if a public counterexample directly falsifies it.
3. **The warning goes in the verdict column, not a note.** A reader scanning a column of ✅ reads "trustworthy."
4. The verdict sentence is always the same: **verifiable parts being true ≠ the article being true.**

### The anonymous-target cap

NE-5 usually co-fires with a structural rule. When the article's actual recommendation is never named — "a certain company", "the core of the core", "a key supplier" — attached to clues precise enough to be enticing but never precise enough to check, the hiding is not a defect. It is the product: free content builds trust with real facts, the anonymous target creates curiosity, the name sits behind the paywall.

Every anonymous clue is marked ⚠️ (subject unidentified) and **global credibility is capped, regardless of how precise the surrounding facts are.** The Skill will not guess the ticker for you. Inferring is not verifying.

## Full example

**Before** (excerpt, an industry-narrative pitch):

> Every big Huawei move mints a multi-bagger. 2021 HarmonyOS → a certain Runhe up nearly 5x; 2024 HiSilicon → a certain Huaqiang, 16 limit-ups in 17 days, **from 8 yuan to 48 yuan**…
>
> *[≈30 true data points follow: Atlas 950 specifications, hyperscaler orders, brokerage research excerpts]*
>
> One of them deserves to be called **the core of the core**: a key supplier to Huawei's supernode "neural network", earnings already up over 200%, covered by 35 institutions in a single month… The opportunity is right here. You decide.

**After** (excerpt, the health-check report):

> **⚡ Quick read**: Hybrid (A-primary, B-module) · One line: **verifiable parts being true ≠ the article being true.** The thirty surrounding facts hold up. The target it is actually selling you is never named.
>
> **Overall: ⚠️ partially unsupported** — anonymous-target cap triggered: the core recommendation is unnamed throughout; global credibility is capped regardless of the precision of surrounding facts.
>
> | # | Claim | Verification | Verdict |
> |---|---|---|---|
> | 4 | "Huaqiang from 8 to 48 yuan, 16 limit-ups in 17 days" | Actual high 41.55; **the 48 level does not exist in the price series** | ❌ Contradiction — a fabricated specific level. "Multi-bagger" is rhetoric; 48 yuan is falsifiable. |
> | ⑤-A | "Every Huawei move mints a multi-bagger" (5 cases) | Five winners cited; the non-performers omitted | ⚠️ NE-1 survivorship bias — true cases ≠ valid rule |
> | ⑤-C | 30 true data points → anonymous "core supplier" | The real data is the wrapper; the anonymous target is the product | ⚠️ NE-5 true facts → anonymous jump |
>
> The report notes that the anonymous clues **point strongly toward one specific connector supplier**, and states explicitly: *this is not a recommendation of that company; we verify whether the clues are real, the judgment is yours.*

Two things this example is meant to show. First, **❌ has a written threshold**: it is reserved for a fabricated, falsifiable data point. "16 limit-ups in 17 days" being loose, or a compressed timeline, would be ⚠️ — vagueness is not fabrication, and diluting ❌ costs it its weight. Second, a per-claim checker returns ✅ on rows 1–30 and hands back a clean bill of health for an article whose entire function is the funnel at the bottom.

## Verification discipline

The Skill's authority does not come from the model being smart. It comes from the harness denying the model several conveniences.

**Closed baseline.** Ground truth is only the official disclosure stream (CNINFO / exchanges / HKEXnews / NEEQ) and the official market-data stream (exchange trading data). Third-party financial portals are used for locating and leads, never as the arbiter of truth. The article under audit and the aggregators that reposted it are both part of "web consensus" — verifying a claim against the consensus it helped create is letting the suspect testify for himself. Market data is exempt from this: a closing price is an objective transaction fact, identical in every mirror.

**Ordered evidence, with early stopping.** P1 audited annual report > P2 interim/quarterly > P3 interim announcements > P4 prospectus > P5 investor-interaction replies > P6 company website > P7 third parties. Search top-down and **stop once P1–P4 answers it**. P5–P6 never produce a ✅ on their own — a company statement outside statutory disclosure is recorded as "the company has stated this", with the verdict staying ⚠️.

**Cross-validation, and conflicts are not forced.** A claim is not checked against one document and closed. Where a second independent source exists it is used: CNINFO against the exchange sites and the designated disclosure media; the disclosure stream against the market stream (a PE claim is decomposed and each half checked separately); a periodic report against the company's own investor-interaction replies; a registry MCP against the disclosed shareholder table.

When those sources disagree, the resolution is ordered rather than averaged. Different tiers → the higher tier wins, and the lower-tier contradiction is itself reported as a finding. Same tier, different dates → the latest filing, including restatements. Same tier, same date, still inconsistent — an annual report's body disagreeing with its own notes — → **no verdict is forced**; both figures are shown and the inconsistency is flagged. That case is a more valuable finding than either ✅ or ❌.

**Degrade, never fill.** Without AKShare, a percentile claim becomes a search-derived range, explicitly marked "estimated, requires self-computed series to confirm." Without the registry MCP, deep equity chains are ⚠️. The gap is reported as a gap.

**No invented links.** Only URLs actually fetched are cited. Announcement IDs are never reconstructed from a numbering pattern, and links are never reproduced from memory. When a source is known but was not retrieved in this environment, it is written as `[pending: source + locator]` — "CNINFO · Zijin FY2025 annual report · section X" — and the recheck is handed to the reader. A plausible-looking fabricated link is worse than no link: it manufactures false certainty in exactly the place the tool exists to remove it. This is the one rule that costs convenience by design.

## Data sources

Verification baselines, all free and login-free:

- **巨潮资讯网 CNINFO** — [cninfo.com.cn](http://www.cninfo.com.cn) — primary baseline; statutory disclosure across SSE / SZSE / BSE / HKEX / NEEQ
- **上交所 / 深交所 / 北交所** — [sse.com.cn](http://www.sse.com.cn) · [szse.cn](http://www.szse.cn) · [bse.cn](http://www.bse.cn) — redundant check, and the market data of record
- **HKEXnews 披露易** — [www1.hkexnews.hk](https://www1.hkexnews.hk) — Hong Kong baseline
- **全国中小企业股份转让系统** — [neeq.com.cn](http://www.neeq.com.cn) — NEEQ baseline
- **深交所互动易 / 上证 e 互动** — [irm.cninfo.com.cn](http://irm.cninfo.com.cn) · [sns.sseinfo.com](http://sns.sseinfo.com) — company statements (P5; never a ✅ on their own)
- **国家统计局 / 行业协会** — [stats.gov.cn](http://www.stats.gov.cn) — sector denominators, mounted on demand, never audited as standalone claims

Retrieval and cross-reference layers:

- Thanks to [AKShare](https://github.com/akfamily/akshare) for the programmatic market and financial data interface — used as the structured retrieval layer for valuation series. The exchanges remain the source of record.
- Thanks to 企查查 for the corporate registry MCP — used for leads only (P7); it never overrides a disclosed filing.

Full inventory with retrieval paths: [`sources/official-channels.md`](sources/official-channels.md).

## Repository structure

```
a-share-fact-check/
├── SKILL.md                       # Dispatch core: 3 scope laws + triage + 6-step pipeline + report templates
├── references/                    # 3 shared foundations — read these first
│   ├── normalization.md           # 5-tuple Claim Schema, colloquial→GAAP map, caliber & tolerance rules
│   ├── evidence-rules.md          # P1–P7 priority, conflict resolution, anti-fabrication link rule
│   └── narrative-errors.md        # NE-1 … NE-6 montage taxonomy
├── playbooks/                     # 7 playbooks, unified 5-step contract
│   ├── 01-financial-figures.md    ├── 05-policy-existence.md
│   ├── 02-equity-structure.md     ├── 06-red-flags.md
│   ├── 03-fundraising-capacity.md └── 07-valuation-market-data.md
│   └── 04-industry-position.md
├── sources/official-channels.md   # Source inventory + retrieval paths
└── tools/mcp.md                   # MCP configuration
```

## Status

The framework is derived from close reading of real stock pitches across several genres — valuation-driven pitches, industry-narrative pitches, advisor lead-gen ads. What has converged: entry triage, the claim typology, the three shared foundations, the seven playbooks, the montage layer, the anonymous-target cap.

**No benchmark evaluation has been run.** There is no measured precision or recall, no held-out corpus, and no comparison against an unconstrained base model. A batch survey and benchmark are the next milestone.

Items marked `TODO` in the source files — finalizing the error taxonomy, whether to split routing, expanding the manipulation-pattern library — are deliberately held open pending that survey rather than stacked up from single-article guesses.

## Contributing

The most useful contribution right now is **corpus**. Typical stock pitches, advisor ads, day-trader recaps — and especially any article this framework handles badly. Open an issue with the text and, if you have one, the verdict you think is correct. False positives matter as much as misses: a framework that flags everything is as useless as one that flags nothing.

## Disclaimer

This tool verifies the consistency of public information only. It does not predict prices, produce valuations, or issue buy/sell conclusions, and it does not constitute investment advice. Every verdict is a statement about an article, never about a security.

本工具仅就公开信息一致性进行核验，不构成任何投资建议。

## License

MIT-0
