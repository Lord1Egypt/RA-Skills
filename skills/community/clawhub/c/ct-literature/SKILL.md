---
slug: ct-literature
name: ct-literature
displayName: Clinical Trial Literature Search / 临床试验文献检索专家
cn_name: 临床试验文献检索专家
version: 1.7.10
invocable: true
summary: 全数据源覆盖检索医学领域学术文献（OpenAlex + Europe PMC/MeSH + NCBI PubMed/MEDLINE + bioRxiv/medRxiv 预印本 + arXiv 方法学广度），归一化合并去重，可产出 CSM 安全性定性子集，协助提供 OA 文献 PDF 下载。集成 Docling PDF 结构化解析。
license: MIT
description: "Search medical-domain scholarly literature with full data-source coverage (OpenAlex + Europe PMC/MeSH + NCBI PubMed/MEDLINE + bioRxiv/medRxiv preprints + arXiv methodology breadth), normalize, merge, and de-duplicate the results, produce a qualitative CSM safety-literature subset, and assist in providing open-access (OA) full-text PDF downloads. Integrated Docling PDF structured parsing. / 全数据源覆盖检索医学领域学术文献（OpenAlex + Europe PMC/MeSH + NCBI PubMed/MEDLINE + bioRxiv/medRxiv 预印本 + arXiv 方法学广度），归一化合并去重，可产出 CSM 安全性定性子集，协助提供 OA 文献 PDF 下载。集成 Docling PDF 结构化解析。"
triggers:
  - "systematic literature search"
  - "系统文献检索"
  - "文献证据基础"
  - "已发表安全性文献 / CSM"
  - "cross-database literature search"
  - "跨数据库 文献检索"
  - "Embase Cochrane Web of Science"
  - "多数据库 系统综述"
  - "ct-literature"
  - "追溯某篇论文的引用 / 被引"
  - "X 的前后向文献 / 引文网络扩展"
  - "citation expand / snowball from <DOI/PMID/题名>"
  - "引导式检索剧本 / 读→扩→链"
required_commands: [python]
metadata:
  openclaw: { emoji: "📚" }
  authors: ["medstatstar", "phoe-zip"]
  tags: [clinical-trial, literature, evidence, systematic-review, csm, openalex, pubmed, public-data]
  homepage: "https://github.com/medstatstar/ct-literature"
  pdf_parsing: "Docling (primary) / PyMuPDF / PdfPlumber (fallback)"
permissions:
  scope: "user-space-only"
  network: "optional"
  network_note: "Reads only public bibliographic sources (OpenAlex, Europe PMC, Semantic Scholar, arXiv), keyless; Europe PMC + bioRxiv/medRxiv on by default, arXiv opt-in. No confidential input; opt-in bug reports send only an 11-key sanitized envelope."
  filesystem: "read-only to its own files; writes report files only to the current working directory"
  data: "no confidential data input; no external transmission of user data"
---
## Data Egress Guardrail (CT family standard · F33)

This skill may call external endpoints (Coze services, shared third-party search endpoints, public APIs or LLMs). **Internal confidential data must not leave the local domain.** Mandatory rules:

- **Never outbound**: patient-level records, unpublished protocols / CSRs / internal documents, personal identifiers or sponsor-confidential content — as query terms, attachments or prompt payload.
- **Allowed minimum**: public search terms and non-content metadata only (machine hash, skill version, entry point, language, request id). Results from public registries (ct.gov / CDE / FAERS / OpenAlex / PubMed, etc.) are processed locally.
- **Local first**: computation, de-identification, aggregation and reporting stay on this machine; confirm the payload carries no confidential field before any cloud call.
- **Visible disclosure**: workbench search forms must state the outbound endpoint and this boundary in visible text, not only in a hover tooltip.
- **Fail loud**: stop and tell the user if any rule cannot be guaranteed; never degrade silently.

Machine-checked by `ct-base/scripts/spec_lint.py` rule **F33**.

## Language

- **English guide** → [README.md](https://github.com/medstatstar/ct-literature/blob/main/README.md) · **Chinese guide** → [README_zh-CN.md](https://github.com/medstatstar/ct-literature/blob/main/README_zh-CN.md)
- Bilingual auto-switch: the answer language follows the user's question language (English question → English answer, Chinese question → Chinese answer).

## Purpose

Retrieve **published scholarly literature** (peer-reviewed papers, systematic reviews, conference abstracts, preprints) about a drug / disease / method, normalize heterogeneous records from multiple public bibliographic sources into one de-duplicated evidence base, and surface the evidence landscape plus a **CSM (cumulative safety monitoring)** qualitative subset. Supports trial-planning background, protocol / CSR introductions, and published-safety literature checks.

## Positioning within the ct- library

Four complementary public-intel skills: `ct-registry` (registered trials) · **`ct-literature` (published evidence)** · `ct-safety` (FAERS signals) · `ct-pipeline` (aggregate intel brief).
**Boundaries:** the safety lane here is *qualitative* published-safety literature — never a substitute for `ct-safety`'s FAERS disproportionality. Unsure which skill? Route via `ct-advisor` (§15). Full four-skill matrix + boundary detail → [references/capabilities.md](references/capabilities.md).
**Pipeline position:** `ct-registry` landscape hypotheses seed a search here; the assembled evidence base then feeds `ct-pipeline` (intel evidence dimension) and supplies background for `ct-protocol` / `ct-csr`, while the safety subset corroborates `ct-safety` qualitatively.

## Data Sources

**Default lane**: OpenAlex (primary) + Europe PMC + bioRxiv/medRxiv preprints. **Opt-in**: arXiv, Cochrane CDSR (via the Europe PMC journal filter), Semantic Scholar, PROSPERO.
**PubMed lane**: an independent direct-to-NCBI channel covering both PubMed/MEDLINE and Cochrane CDSR. Off by default because Europe PMC already covers both; **automatic fallback is on** — when the Europe PMC leg fails (exception or zero hits) the PubMed lane takes over, restoring PubMed *and* Cochrane coverage. Lane state and the fallback reason are recorded in the evidence log.
**Local imports (no network)**: a local Zotero collection, and files the user exported from Chinese databases (CNKI / WanFang / SinoMed). These are imports, not retrieval — they join the same dedupe / verification / PRISMA pipeline.
**Clinical guideline corpus**: a version-pinned, pointer-only local corpus, built once and then read offline; full texts are never shipped inside the skill, and a failed fetch degrades to a "not retrieved" pointer rather than a fabricated citation.
**Recency caveat**: the publication-date window is pushed down into every source query and clipped again after merging; the online channel applies the same window but can still truncate the newest items at the result cap, so a hard recency guarantee requires the local engine.
Per-source access, role and status table → [references/capabilities.md](references/capabilities.md).

## Capabilities

- **Search & filters**: topic / drug / disease search; review-type, publication-year and month-level recency filters; relevance ranking; document-type inclusion and exclusion.
- **Evidence assembly**: multi-source merge, dedupe, citation ranking, MeSH / concept / funder normalization, PRISMA funnel.
- **Safety subset**: qualitative CSM tagging over published safety literature.
- **Structured concepts**: PICO-style condition / population / intervention / comparator / outcome axes, MeSH-normalized, with any unmapped term kept literal rather than invented.
- **Citation-network expansion from one seed paper**: start from a DOI, a PMID or a free-text title, and expand one hop backward (its references) and forward (works citing it); the seed itself is returned and tagged as such.
- **Local-source enrichment**: paragraph-level provenance anchors over already-downloaded PDFs, Zotero import, and Chinese-database import with cross-database CJK dedupe.
- **Batch retrieval**: a list of topics in one spec file, run sequentially with aggregated results, a format check, a call-quota gate and checkpoint resume; the quota gate estimates the run first and aborts **before any network call** when the estimate exceeds the daily safe threshold unless the user explicitly confirms.
- **Deliverables & add-ons**: HTML + Excel reports; on demand citations (BibTeX / RIS / styled), open-access PDF download, Obsidian notes, Zotero export.
- **Anti-hallucination**: citation verification, DOI audit, and an evidence provenance log.
- **Honest source accounting**: every source is logged as ok / empty / error / skipped, the run returns a coverage verdict (healthy / partial / empty / critical gap), disabled sources are recorded as skipped rather than zeroed, and a primary-source failure is flagged as a critical gap with an explicit warning against extrapolation; a narrowed query that returns too few unique works triggers one broader rescue run (single-shot, non-fatal) instead of a thin result set.
- **PDF structured parsing**: table- and hierarchy-preserving conversion (Docling primary, PyMuPDF / PdfPlumber fallback) for table-dense protocol, CSR and open-access full-text PDFs before any downstream reuse.
- **Meta-analysis topic evaluation**: early fatal-defect gates plus six-dimension scoring, offline and decoupled from retrieval.

Exact command syntax and the full parameter table → [references/sop.md](references/sop.md); the complete capability / parameter matrix → [references/capabilities.md](references/capabilities.md).

## Outputs

**Standard deliverables = HTML + Excel only** — present `lit_report.html`; `lit_report.xlsx` keeps the complete filterable result. On-demand add-ons: citations, open-access PDF download, Obsidian notes, Zotero exports. After a PDF download, point users at the output folder rather than opening or listing individual files.
Full output catalogue, sheet layout, server-side supplement chain and concurrency notes → [references/capabilities.md](references/capabilities.md).

## Published Application

The workbench is published as a Python HTTP service at `https://ct-literature.app.workbuddy.host/` (appId `wbapp_WuOPnJ4caJ32GTquNlR7vc`, deploy bundle `workbench/publish-dist/`, workspace-independent). Re-publishing is always an **overwrite of the same appId**, never a new app, and the returned `shareLink` must be asserted against the expected domain — a mis-bound bundle path silently serves another app.

Full registry table and re-publishing protocol → [references/published_app.md](references/published_app.md) — load it before any deploy or re-publish operation.

## ⚠️ Safety

- **Safe preview by default**: the pipeline only generates and displays a plan; network requests run only after the user explicitly confirms execution.
- Reads **public publications only** — no confidential research or subject data is ever an input.
- The safety lane is **qualitative** — never feed it into FAERS disproportionality; it only corroborates `ct-safety` qualitatively.
- Output is for reference / background only, not a regulatory submission.

## Dialogue — Triage-First (mandatory)

Every natural-language turn MUST start at Step 0 triage — never skipped, never jump straight to execution (§6.2 + [references/search_menu.md](references/search_menu.md)). Four buckets: **Simple** (topic + at least two parameters → preview) · **Complex** (menu → keyword gate → preview → run) · **Vague** (grill-me, at most two rounds, then re-triage) · **Middle** (answer directly).
**Red lines:** never skip triage; never decide for the user (the Complex menu keeps the "explain the differences" entry); the keyword-system confirmation gate is mandatory whenever search terms are parseable.
**Cross-turn continuity (high-risk, mode A):** the query spec lives only in the thread — after every run append a "current search spec" echo line carrying topic, review type, year, safety, sources, maximum results and verification state (never omit fields); follow-ups override only the changed fields and are re-merged by default; remote calls are stateless, so continuity is local-only.
Full triage tables, echo / merge rules and the execution flow → [references/dialogue.md](references/dialogue.md) — load it when executing a dialogue round.

## AI-Generated Asset Governance (ct-base §22)

> This skill is bound by `ct-base/BASE.md` §22 (AI-generated asset governance). It produces search / synthesis output, not SDTM / ADaM / TLF / CSR assets; three obligations apply and all three are implemented: the RAG three-column to-verify checklist (question / source location / basis, derived from the real run ledger, zero fabrication), shadow-mode promotion thresholds (guardrail-only for this skill's LLM normalisation / translation / labelling layer), and layered verification (deterministic layer versus LLM layer disclosed separately, never blended into one headline accuracy). **Red line:** search / synthesis conclusions must never omit provenance, and uncovered items must be listed explicitly rather than assuming the search was complete (§22.16 + §17.1). Full obligation table → [references/gov22_obligations_zh.md](references/gov22_obligations_zh.md).

## Where to Look

- Capabilities, parameters, per-source tables, output catalogue → [references/capabilities.md](references/capabilities.md)
- Command examples and the parameter table → [references/sop.md](references/sop.md)
- Batch spec format and quota / resume rules → [references/batch_spec.md](references/batch_spec.md)
- Triage tables, echo / merge rules → [references/dialogue.md](references/dialogue.md) · keyword gate → [references/search_menu.md](references/search_menu.md)
- Multi-database import contract → [references/multi-db-search.md](references/multi-db-search.md)
- Meta-analysis topic-evaluation rubric → [references/meta_topic_rubric.md](references/meta_topic_rubric.md)
- Error handling → [references/errors.md](references/errors.md) · maintenance and change notes → [references/maintenance.md](references/maintenance.md) · published application and re-publishing protocol → [references/published_app.md](references/published_app.md)
