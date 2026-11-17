# Capabilities & Reference Detail (ct-literature)

> Extracted verbatim from `SKILL.md` (2026-09-27, line-budget refactor — SKILL.md ≤ 200 lines per ct-base §16.1 / F02). No content removed; SKILL.md keeps one-line pointers here. Load this file when you need the full source / feature / output / invocation detail.

## Positioning within the ct- library

The four A-tier public-intel skills (non-confidential input, `network=public-retrieval`) are complementary:

| Skill | Answers | Object retrieved | Source family |
|---|---|---|---|
| `ct-registry` | What trials are registered / ongoing / completed? | Trial-registry metadata | Registry libraries |
| `ct-literature` | What evidence has been *published*? | Publications | Literature libraries |
| `ct-safety` | Is a drug–event over-reported (signal)? | FAERS cases | Adverse-event databases |
| `ct-pipeline` | Aggregate the above into a strategic intel brief | Consumes the three JSONs | Public-intel layer |

**Boundaries:** `ct-registry` never fetches paper full-text/abstracts; `ct-literature` never fetches registry structured metadata. `ct-literature --safety` surfaces *published* safety literature — **qualitative**, must NOT replace `ct-safety`'s FAERS disproportionality. Not sure which skill? Route via `ct-advisor`; full competitive-intel picture → `ct-pipeline` directly (§15).

## Data Sources (detail)

| Source | Access | Status | Role |
|---|---|---|---|
| OpenAlex | Public REST; free key recommended (100k/day via `.env` auto-load) — keyless capped 100/day since 2026-02-13 | Required (primary) | Broad coverage + citation counts |
| Europe PMC | Public REST (MEDLINE / PubMed Central), no key, MeSH-indexed | **Default ON** (`--no-with-europepmc`) | Biomedical precision + MeSH |
| PubMed / MEDLINE | NCBI E-utilities (`esearch` + `efetch`/`esummary`), no key (3 req/s) or `NCBI_API_KEY` (10 req/s); polite pool via `CT_LIT_NCBI_EMAIL` | **Off by default** — `--with-pubmed`, or auto-enabled by the Europe PMC fallback | Independent lane covering PubMed/MEDLINE **and** CDSR (`Cochrane Database Syst Rev[ta]`); Europe PMC outage backup |
| Cochrane (CDSR) | Via Europe PMC journal filter **or** the PubMed lane's `[ta]` tag | Opt-in `--cochrane` | Cochrane Database of Systematic Reviews only |
| Semantic Scholar | Public Graph API, no key, rate-limited (429) | **Opt-in only** `--with-semantic-scholar` (not part of default sources; requires key to be useful) | Citation-aware ranking; skipped when no key |
| bioRxiv / medRxiv | Via Europe PMC `SRC:PPR` + publisher filter | **Default ON** (`--no-with-biorxiv` / `--no-with-medrxiv`) | Preprints (Tier P) |
| arXiv | Public Atom API, no key | Optional `--with-arxiv` | Methodology breadth |
| PROSPERO | Public REST (CRD York); public POST search (self-made `prospero-auth-token`, no login) since v1.7.2 | Optional `--with-prospero` (keyless works; `--prospero-token` GET leg kept as unverified fallback) | Duplication-avoidance / protocol discovery |

> All are public bibliographic APIs — no WAF. The **default data sources are OpenAlex (primary) + Europe PMC (on by default) + bioRxiv/medRxiv (on by default)**; everything else (arXiv, Cochrane, PROSPERO, Semantic Scholar, PubMed) are opt-in.
>
> **PubMed lane & the Europe PMC fallback (v1.7.0).** Europe PMC is the only source that natively covers *both* PubMed/MEDLINE and Cochrane CDSR in one query. If it is rate-limited or unreachable, OpenAlex still covers part of PubMed (it carries `ids.pubmed`) but **Cochrane coverage drops to zero** — OpenAlex has no CDSR filter. The NCBI E-utilities lane is independent of Europe PMC, so `--pubmed-fallback` (default ON) auto-enables it when the Europe PMC leg fails (exception or 0 hits), restoring both halves. Trigger requires Europe PMC to be enabled and PubMed not explicitly mounted (no double-fetch). State is recorded in `meta.pubmed` (`explicit`/`fallback_enabled`/`ran`/`trigger`) and in the evidence-log ledger (`status="fallback"` on the PubMed entry, with the reason). `--sources PubMed` selects the NCBI lane directly (before v1.7.0 `pubmed` aliased to `europepmc`; use `EuropePMC` for that leg). OpenAlex keyless = 100 credits/day since 2026-02-13; a free key lifts to 100k/day (`--openalex-key` / env `OPENALEX_API_KEY` / skill `.env` auto-load; key never printed). Semantic Scholar is an explicit opt-in source (`--with-semantic-scholar` + key) and is **not considered in the default pipeline**.
>
> **PROSPERO public search (v1.7.2, 2026-11-03):** the reverse-ported POST path (`https://www.crd.york.ac.uk/PROSPERO/api/search`, JSON body + a self-made `prospero-auth-token` header) works **without login or key**; real-network validation returned 1479 hits for `efficacy AND pd 1 AND inhibitors AND advanced`, matching the meta-analysis baseline. The former GET + token leg remains only as an unverified downgrade path. `--raw-query` bypasses the internal query builder when a caller already has a tuned query. Honest-degradation notes: ES-backend timeout envelopes are detected as errors (never reported as 0 hits); a failed POST falls back to GET if a token is present.

## Clinical guideline sources (`--with-guidelines`, opt-in · LOCAL corpus)

Guidelines are **version-pinned** reference standards — at analysis time we read a **pre-built LOCAL corpus**, never "fetch latest" per run.

> **Corpus boundary (audit note 2026-09-07):** every entry is a manually curated, version-pinned pointer to an organisation-issued document, but the builder's 12+ sources also surface reviews / consensus / adherence analyses and AI-in-medicine commentary. Such items are kept as background pointers only and are **not** authoritative clinical guidance — always resolve the linked source before relying on it; a `retrieved:false` pointer is an honest placeholder, never a fabricated citation.

> **🔒 Data-protection split.** The skill tree ships **pointer-only** (`references/guidelines/guidelines_index.json`: org/title/URL/version — publish-safe). **Full-text documents are NEVER written into the skill** — they live in the author's self-controlled Coze KB (or an EXTERNAL local cache `~/.workbuddy/ct-guideline-docs`, opt-in via `--download`, off by default); ct-advisor consults that KB for native guideline Q&A.

- **Author / build-time** (network): `python adapters/build_guidelines.py --topic <topic> --run` aggregates 12+ sources → `guidelines_index.json` (96 curated entries, schema v1). SAFE PREVIEW: omit `--run` (dry-run, no network/write).
- **Analysis-time** (zero network): `--with-guidelines` on the main pipeline → `adapters/guideline_corpus.load()` reads the local index → `guidelines.json` + `guidelines` block in `.merged.json`.

| Tier | Sources | How it got into the corpus |
|---|---|---|
| `api` | OpenAlex, Europe PMC, GIN, WHO IRIS | fetched by the builder (OA-PDF download attempted) |
| `api` (key-gated) | NICE¹, MAGICapp, TRIP² | fetched if a key configured; else skipped |
| `portal`→`api` | CPIC | genuine fetch via free keyless PostgREST API (`api.cpicpgx.org/v1`) |
| `portal` pointer | NCCN, ADA, AHA, SIGN, CMA | best-effort public-portal scrape → graceful fallback to honest pointer (`retrieved:false`), never fabricated |

**Build-time portal fetch (`adapters/portal_fetch.py`):** every fetcher is wrapped so it never raises — failed fetch degrades to the honest pointer, so the corpus is always honest (build once, read many). Each record carries `access` (`api`/`portal`) + `retrieved`; `guideline_corpus.load()` filters by topic/org and returns `corpus_missing` (with the builder command) if the index is absent. ¹ NICE REST auth undocumented (like PROSPERO) — skip until a token works. ² TRIP requires a commercial key.

## Features (full catalogue)

| Capability | Source | Typical scenario |
|---|---|---|
| Topic / drug / disease search | All | Build the published-evidence base |
| Review-type filter | All | `systematic-review` / `meta-analysis` / `rct` / `case-report` |
| **Cochrane retrieval (focus)** | Europe PMC | `--cochrane` → restrict to the Cochrane Database of Systematic Reviews (verified journal filter, shared with meta-analysis) |
| Year-range filter | All | Focus on recent evidence |
| Safety / CSM tagging | All | Every work is flagged `is_safety` (amber-highlighted in the Works sheet) when its title/abstract mentions AE / PV / toxicity — useful for quick scanning. **The standalone Safety-Related sheet is opt-in** (`--safety`); a plain search does NOT emit it by default. |
| Multi-source merge + dedupe | normalize | One unified list, DOI/title de-duped, provenance kept |
| Citation ranking | OpenAlex / S2 | Most influential works |
| MeSH terms | Europe PMC | Biomedical concept indexing |
| Concepts / Keywords / Funders | OpenAlex | Topic classification + COI signals |
| PubMed/PMC ID, OA full-text URL, complete abstract | All | Direct links + full evidence preservation |
| Structured output | — | JSON + Markdown + Excel workbook (`excel_style`). Default sheets: README → Overview → Works → Evidence Log. `Safety-Related` sheet appears **only with `--safety`**. |
| Chained invocation | — | → `ct-pipeline` / `ct-protocol` / `ct-csr` |
| Resilient fetch (retry + backoff) | All | Honors `Retry-After`; OpenAlex Bearer via key |
| Safe link rendering | All | `_normalize_link()` sanitises every hyperlink |
| Citations + BibTeX/RIS | All | `--citation-style` (apa/nature/vancouver/ieee/gb7714) + `--export-bib` |
| PRISMA screening funnel | All | `--prisma` deterministic rule screen → SVG funnel in HTML |
| **Doc-type exclusion** | All | 双向类型甄别（`doc_type_filter`，移植自 meta-analysis 实证规则）：① 只要原创研究 → `--original-only`（排除 review/guideline/protocol，unknown 放行）；② **反向模式** → `--only-type review` / `--only-type guideline,protocol` 等（只保留指定类型，unknown 也排除）。判别依据：标题/摘要信号 + pubType 元数据；PRISMA 漏斗记录 `non-original-type:*` / `type-not-required:*`。也可单独用 `scripts/doc_type_filter.py`（`--exclude-non-original` / `--only TYPES`，支持 `--use-pdfs` PDF 级兜底）。甄别异常一律放行，绝不阻断检索流程 |
| Relevance scoring | All | `--rank relevance` → `relevance_score` (title .6 + abstract .4) |
| Obsidian / Zotero integration | All | `--obsidian` notes + MOC; `--zotero` CSV/RIS |
| **P0 · Citation verification** | All | Anti-hallucination (§17.1). `--verify {all\|top\|none}`; source-aware skip; DOI cross-checked via doi.org; title/author consistency vs Crossref/Europe PMC/OpenAlex; flags `verified/bot_blocked/mismatch/unresolved/...` |
| **P1 · DOI audit** | All | `--verify-dois` (opt-in, needs `--run`): writes additive `doi_verified` / `doi_mismatch` onto every work and emits `doi_mismatch.md` — a human-review list isolating the real-but-wrong / hallucinated-DOI case (Crossref title+author fuzzy match). Standalone: `scripts/verify_dois.py --in .merged.json --run` |
| **P0 · Evidence provenance log** | All | `evidence_log.json/.md` + workbook sheet + HTML block: query→source→hits→retrieved_at→verification rate |
| **P1 · PROSPERO registry** | Review register | `--with-prospero` (opt-in, **keyless** since v1.7.2) — public POST search; `--raw-query` bypass for tuned queries; GET+token leg unverified |
| **G · Guideline corpus** | Guideline orgs | `--with-guidelines` → local pointer corpus (see above) |
| **P0 · 结构化 PICO 概念** | topic/干预/对照/结局 | `--concept TYPE=VALUE`（可重复，TYPE∈{condition,population,intervention,comparator,outcome,endpoint,study_design,biomarker,drug,indication}）：概念 AND 拼入检索式、独立成轴；MeSH 精确归一化 + `mapping_status` 审计（exact_label/synonym/unmapped_literal，模糊匹配拒绝、未命中保留原词） |
| **P0 · 检索深度预算** | resource control | `--depth quick\|standard\|deep`：决定每源上限与弱化结果救援开关（**非证据质量评级**）；不传则沿用 `--max` 旧语义 |
| **P0 · 证据维度分轨** | safety vs efficacy | 合并后每篇打 `evidence_dimension`（=`safety` 若 `is_safety`，否则 `general`）；`--safety` 触发独立 safety lane，安全性信号不被疗效文献稀释 |
| **P1 · 四态审计 ledger** | provenance | `evidence_log` 新增 `status∈{ok,empty,error,skipped}` + `coverage∈{healthy,partial,empty,critical_gap}`；被显式关闭的源记 `skipped`（not_run）、缺口诚实呈现、**不归零** |
| **P1 · lane 规划视图** | dry-run | SAFE PREVIEW 直接打印 lane 规划（purpose / 源 / evidence_dimension / 备注），跑前可审查 |
| **P1 · 弱化结果救援** | recall rescue | `standard`/`deep` 且合并唯一文献 < 5 且概念曾收窄检索式时，放宽至主题级回补一轮（单次、非致命；无新增记 skipped） |

## Unified work schema

```
{ source, id, title, authors, year, publication_date, publication, journal_iso,
  type, study_type, cited_by_count, url, open_access_url,
  pmid, pmcid, doi, abstract_snippet, mesh, concepts, keywords, funders,
  language, is_retracted, is_safety, is_preprint, volume, issue, page,
  affiliations, sources }
```

## Output (full detail)

**Standard deliverables = HTML + Excel only.** Present `lit_report.html` to the user as the result, and remind them of the optional add-ons below (the report itself shows a "还能做什么 / Options" strip with these hints).

- Per-source payloads: `openalex.json` / `europepmc.json` / `semantic_scholar.json` / `biorxiv.json` / `medrxiv.json` / `arxiv.json` (enabled only)
- `lit_report.xlsx` — Excel delivery (`excel_style`; `--no-xlsx` to skip): Overview → Literature master → Safety-related, KPI cards, charts, `is_safety` amber highlighting. **The complete result — user can keep filtering / pivoting on top of it.**
- `lit_report.html` — self-contained HTML report (inline CSS, offline; `--no-html` to skip); inline-SVG PRISMA funnel when `--prisma`. **Default deliverable to open.**
- **On-demand citation formats** (default OFF — ask the user or use `--export-bib`): `references.bib` / `references.ris` / `references_<style>.md` (Zotero RIS / BibTeX / APA etc.). OA-PDF downloads are likewise on request: `--download-pdf` attempts **ALL** records that carry an OA URL or DOI (batched, legal OA sources only); users may instead ask for specific DOI / PMID(s) or the top-N works. The PDF local-path column in `lit_report.xlsx` is written back automatically by `PdfDownloader` when constructed with `xlsx_out` (the main `--download-pdf` flow and any standalone driver that passes `xlsx_out` both benefit); you no longer need to call `update_xlsx_pdf_paths.py` separately. **Server-side supplement chain**: when the A-path direct links all fail, the coze endpoint runs a supplement chain — Unpaywall best-OA → Europe PMC PMC-OA → PPR preprints (bioRxiv/medRxiv, author-verified) — before the (off) browser fallback; the local skill only calls, it no longer implements multi-channel download algorithms. **Concurrency (2026-09-19 fix)**: local resolve/download and Coze decode now run **in parallel** — the Coze decode thread is started *before* the local download phase and each returned sub-batch pipes its links straight into the concurrent downloader, so a locally-resolved direct link starts downloading immediately instead of waiting for Coze to finish the whole round (the docstring previously claimed this overlap but the code serialized it). The "local download failed → Coze retry" pass is gated on `_local_phase_done` so it still runs after the main batches. The workbench's `coze_resolve.py --pipeline` (default) implements the same three-way overlap (local probe ‖ Coze ‖ download) and starts downloading the moment a single link resolves; `--no-pipeline` restores the old serial phases for comparison.
- **⚠️ PDF 下载后结果面板规则**：`--download-pdf` 及任何直驱 `PdfDownloader` 的脚本，下载完成后结果面板**只呈现标准产物 `lit_report.html` / `lit_report.xlsx`**，绝不逐个打开 / 列出 PDF 文件（数十个 PDF 同时打开会卡死 UI）。下载反馈仅用纯文本告知用户共同保存目录 `out_dir/pdfs/`，由用户自行打开所需 PDF。
- `obsidian/` (`--obsidian`) — per-paper notes + `Literature MOC.md`; `zotero.csv` / `zotero.ris` (`--zotero`)
- `.merged.json` gains additive `prisma` + per-work `relevance_score` / `prisma_included` blocks

See `sop.md` for the full command catalogue.

## Implementation (invocation cookbook)

```bash
# Primary: OpenAlex only (no key)
python scripts/ct_literature.py --topic "osimertinib" --review-type systematic-review --year-from 2018 --safety --run --out-dir ./out

# Add Europe PMC (default ON) + Semantic Scholar (may 429 -> skipped)
python scripts/ct_literature.py --topic "osimertinib" --with-europepmc --with-semantic-scholar --run --out-dir ./out

# Cochrane-only retrieval (focus on the Cochrane Database of Systematic Reviews)
python scripts/ct_literature.py --topic "NSCLC" --cochrane --with-europepmc --run --out-dir ./out

# Clinical guidelines: build once (network), read many (zero network)
python adapters/build_guidelines.py --topic "diabetes" --run          # author/build-time; omit --run = SAFE PREVIEW
python scripts/ct_literature.py --topic "2型糖尿病" --with-guidelines --run --out-dir ./out

# Source subset (--sources): comma-separated, OVERRIDES the --with-* / --cochrane defaults.
# A source is enabled iff listed. Consumed by meta-analysis A1's "检索范围" revision.
# Names: OpenAlex, EuropePMC, PubMed, bioRxiv, medRxiv, SemanticScholar, arXiv, PROSPERO, Guidelines, Cochrane
# (OpenAlex is the pipeline base and cannot be disabled.)
python scripts/ct_literature.py --topic "osimertinib" --sources "OpenAlex,EuropePMC" --run --out-dir ./out
python scripts/ct_literature.py --topic "osimertinib"            # preview (no --run) prints the resolved source list

# ── v1.7.0 PubMed lane (NCBI E-utilities) ──────────────────────────────────────
# Explicit: mount the independent NCBI lane (PubMed/MEDLINE + Cochrane CDSR)
python scripts/ct_literature.py --topic "osimertinib" --with-pubmed --cochrane --run --out-dir ./out
# Fallback (default ON): Europe PMC unreachable/rate-limited -> NCBI lane takes over.
# Simulate an outage to see it: --no-with-europepmc disables the leg entirely (no fallback),
# so keep Europe PMC enabled and let it fail, or just read meta.pubmed in .merged.json.
python scripts/ct_literature.py --topic "osimertinib" --cochrane --run --out-dir ./out
# Opt out of the automatic fallback
python scripts/ct_literature.py --topic "osimertinib" --no-pubmed-fallback --run --out-dir ./out

# ── v1.6.3 local-source imports (opt-in, no network) ──────────────────────────
# H: read-only Zotero local library (local API, no key, MCP-free)
python adapters/zotero_import.py --list                              # collection paths
python adapters/zotero_import.py --collection "肿瘤/NSCLC" --out zotero.json
python scripts/ct_literature.py --topic "NSCLC" --run --out-dir ./out --zotero-import "肿瘤/NSCLC"

# I: user-exported Chinese-database files (RIS/JSON) — import, never crawl
python adapters/cn_ref_normalizer.py --in cnki_export.ris --out cn.json
python scripts/ct_literature.py --topic "NSCLC" --run --out-dir ./out \
    --merge-cn cnki_export.ris --merge-cn wanfang_2024.ris
# I: China regulatory evidence lane (CDE/NMPA)
python scripts/ct_literature.py --topic "NSCLC" --run --out-dir ./out \
    --with-guidelines --guidelines-region china

# G: paragraph-level anchors (needs local PDFs in <out-dir>/pdfs)
python scripts/ct_literature.py --topic "NSCLC" --run --out-dir ./out --download-pdf --anchor
python adapters/anchor_injector.py --in ./out/.merged.json --pdf-dir ./out/pdfs --out anchored.json
```

### OpenAlex API key (recommended since 2026-02-13)

Keyless is capped at 100 credits/day; a free key lifts to 100k/day. **Zero-friction:** drop the key into the skill's `.env` (copy from `.env.example`) — no extra flag needed. `http_utils.load_openalex_key()` auto-resolves: env `OPENALEX_API_KEY` → skill-root `.env` → `scripts/.env` (key value never printed). Explicit provision also works (`--openalex-key`). Application steps, quota, troubleshooting → `openalex_key.md`.

## Changelog

### v1.6.3 (2026-11-02) — 本地增量源与段落级溯源（G/H/I）
- **新增** `--anchor` 段落级锚点：Block ID `{doc_hash}:{page}-{block_index}`，provenance 由 DOI 级下钻到 `{block_id, page, quote_excerpt}`；无 PDF → `pdf_missing`，扫描版 → `no_text`，绝不伪造。
- **新增** `--zotero-import "<集合路径>"`：Zotero 官方本地 API 只读导入（无 key、MCP-free）；集合歧义显式报错；子附件/笔记不重复计数；本地回环请求绕过系统代理（修 502 假故障）。
- **新增** `--merge-cn <RIS|JSON>`（可重复）+ `--guidelines-region china|global|both`：中文库走「用户合法导出→导入」，不爬取；CJK 题名（繁简/全半角/标点）归一致同键；不支持格式显式报错。region 支持**机构名兜底推断**（CMA/CDE/NMPA/NHC/CACA/CSCO → china），因既有语料 96 条全无 `region` 字段；同时修既有缺陷：中文主题对指南语料恒 0 命中，改为按检索式候选词重试。
- **约束**：三项全部 opt-in、纯本地、不触碰 Coze 检索层；不传新参数行为与 v1.6.2 一致。导入留痕落 `meta.imports`。
- **验证**：`tests/test_g_h_i_upgrades.py` 15 项通过；既有 28 项回归全绿；ctqa W0 24 PASS；实跑 `--run --local --max 6 --merge-cn --anchor` 端到端通过。

### v1.2.0 (2026-09-30) — 检索结构模型（借鉴「组小学」专家，P0/P1）
- **新增** 结构化 PICO 概念 `--concept TYPE=VALUE`（可重复）：概念 AND 拼入检索式、干预/对照/结局独立成轴；MeSH 精确归一化 + `mapping_status` 审计。
- **新增** 检索深度预算 `--depth quick|standard|deep`：决定每源上限与弱化结果救援开关。
- **新增** 证据维度分轨：合并后每篇打 `evidence_dimension`（safety/general）；`--safety` 触发独立 safety lane。
- **新增** 四态审计 ledger + coverage 判定：`status∈{ok,empty,error,skipped}` + `coverage∈{healthy,partial,empty,critical_gap}`；关闭源记 skipped、不归零。
- **新增** SAFE PREVIEW 打印 lane 规划视图；`standard`/`deep` 下合并集偏薄触发弱化结果救援（单次、非致命）。
- **约束**：全部 additive、向后兼容；不引入组小学的 7 场景全量 / first-class trial·drug·target 对象 / 靶点基因变异实体（越 ct-literature 临床文献边界，与 ct-registry / ct-safety 分工冲突）。
- **验证**：SAFE PREVIEW + `evidence_log.build_log` 单元验证通过；一次本地最小化 live run 端到端通过（concepts 入审计、coverage=healthy、disabled 源 skipped）。
