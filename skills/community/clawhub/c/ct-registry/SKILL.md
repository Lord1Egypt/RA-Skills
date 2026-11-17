---
slug: ct-registry
displayName: Clinical Trial Registry Search / 临床试验注册检索专家
name: ct-registry
cn_name: 临床试验注册检索专家
version: 1.0.1
invocable: true
required_commands: [python]
summary: "跨源检索全球临床试验注册库（ClinicalTrials.gov、CDE/ChiCTR/ISRCTN/DRKS/WHO ICTRP、PubChem），归一化聚合分期/状态/申办方/时间线/竞品格局，产出 JSON / Markdown，用于立项查重、对照设计与竞品格局分析。"
license: MIT
description: "Cross-source search of global clinical-trial registries (ClinicalTrials.gov, CDE/ChiCTR/ISRCTN/DRKS/WHO ICTRP, PubChem), normalizes and aggregates phase/status/sponsor/timeline/competitor landscape into JSON/Markdown for trial planning, de-duplication, control-design benchmarking, and competitive intelligence. / 跨源检索全球临床试验注册库（ClinicalTrials.gov、CDE/ChiCTR/ISRCTN/DRKS/WHO ICTRP、PubChem），归一化聚合分期/状态/申办方/时间线/竞品格局，产出 JSON / Markdown，用于立项查重、对照设计与竞品格局分析。"
triggers:
  - "clinical trial registry search"
  - "临床试验注册库检索"
  - "查同类试验"
  - "竞品临床试验格局"
  - "ct-registry"
metadata:
  openclaw: { emoji: "🔍" }
  authors: ["medstatstar", "phoe-zip"]
  license: "MIT"
  tags: [clinical-trial, registry, ct-registry, ctgov, cde, public-data]
  homepage: "https://github.com/medstatstar/ct-registry"
permissions:
  scope: "user-space-only"
  network: "optional"
  network_note: "Public-retrieval sources (ClinicalTrials.gov v2, PubChem, China CDE/ChiCTR/ISRCTN/DRKS via a shared third-party endpoint); only public query terms + non-content request metadata egress. No confidential data input."
  filesystem: "read-only to its own files; writes report/Excel files to current working directory; download_docs.py can optionally write retrieved EU-CTR PDFs to a user-specified --out-dir"
  data: "no confidential data input; only public query terms plus non-content request metadata (query_origin machine-hash, skill_version, entry_point, user_language, demand_id) are transmitted"
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

- **English guide** → [README.md](https://github.com/medstatstar/ct-registry/blob/main/README.md) · **Chinese guide** → [README_zh-CN.md](https://github.com/medstatstar/ct-registry/blob/main/README_zh-CN.md)
- Bilingual auto-switch: the answer language follows the user's question language (English question → English answer, Chinese question → Chinese answer).

This skill responds in the user's current input language and auto-detects / switches accordingly. The runtime scripts embed a locale check so all user-facing prompts switch to Chinese on a `zh-*` locale and to English otherwise. Code comments and documentation are English-only.

The SKILL.md body, `references/*.md`, and `AGENTS.md` are English-only and agent-facing; runtime command prompts switch to Chinese / English by locale. For end-to-end walkthroughs and troubleshooting in your language, open the README above.

**Deliverable language (v1.0.1):** result files (`report.xlsx` / `report.md`) never inherit the *server* OS locale — the published workbench runs in an en_US container, which used to emit all-English workbooks. `--lang auto` resolves in this order: explicit `--lang` > `CT_REGISTRY_LANG` (workbench injects the current UI language) > skill-root `config.json language` > cover-title language (CJK → zh) > OS locale > zh. English users still get English via `--lang en` or by switching the workbench UI to EN. Raw registry values (titles, status enums, sponsor names) are never translated — only the interface chrome.

# Clinical Trial Registry Search

## Published Application

| Item | Value |
|---|---|
| Share link | `https://ct-registry.app.workbuddy.host/` |
| appId | `wbapp_39NhpDKvmNZ4AjTmsODgqH` |
| domainPrefix | `ct-registry` |
| Deploy metadata | `workbench/app.config.json` |
| Deployed as | http-service (`python app.py`, entry bootstraps `workbench/server.py`) |
| startCmd | `python app.py` |
| publishDir | `workbench/publish` |
| Payload | `workbench/publish/` (built by `workbench/publish-kit/build_publish.py`: `app.py` + `adapters/` + `scripts/` + `references/` + `workbench/`) |
| Publish infra | `workbench/publish-kit/` (`.wbapp_*.genie` marker + `install_genie.py` + `build_publish.py`) |

> **Re-publish rule (ct-base §13.5 Scheme B)**: always overwrite with the existing `appId` — the link must stay `https://ct-registry.app.workbuddy.host/`. Never `createNewApp`. Before deploy: 1. `python workbench/publish-kit/build_publish.py` — rebuild `workbench/publish/` from the skill tree (whitelist + prune, no bulk delete). 2. `python workbench/publish-kit/install_genie.py` — install the `.wbapp_*.genie` marker + `applications.yaml` into the **current workspace root** so `workbuddy_sites_deploy` can claim the appId (the marker's `localDir` is re-pinned to this machine's `publish` on every run). 3. Deploy with the existing `appId` (overwrite). After deploy, assert the returned `shareLink` equals the expected URL (§13.5 dirty-binding red line). Deploy registry, version anchors and the re-publish protocol → **`references/published_app.md`** (single source of truth; load it before any deploy / re-publish operation).

> Safe by default: preview, not execute.

## Purpose

Search global clinical-trial registries in one pass, normalize heterogeneous records into a unified schema, and aggregate them into an actionable landscape (phase / status / sponsor / timeline / competitor map) to support trial planning, de-duplication, control-design benchmarking, and competitive intelligence.

## Architecture

**Principle: the skill does not use a headless browser to scrape WAF-blocked registries over the network.** Chinese registries (CDE, ChiCTR) and WebForms portals (e.g. old ICTRP portal) block automated browsers via WAF fingerprint checks — a verified platform limitation, not a tooling gap. Where a registry has no clean HTTP API, retrieval is delegated to an external workflow (Tier 2) instead of the caller scraping: any needed browser automation runs **server-side inside the unified endpoint**, and a local **paste-mode** (`parse_cde.py`) parses user-pasted pages with **no egress**. The skill therefore uses two safe paths:

- **Tier 1 — direct-connect (pure HTTP, no browser):** `ClinicalTrials.gov v2` REST API (required); `EU CTR` legacy EudraCT search-result HTML parsed directly (`search_eu_ctr.py`, verified 2026-07-24); `PubChem` PUG-REST (drug → CID / targets, optional).
- **Tier 2 — external workflow service (Bearer token, POST JSON, no browser):** a third-party endpoint retrieves on our behalf and returns structured JSON. Shared client in `extsvc_client.py`; thin wrappers `search_cde_workflow.py` / `search_chictr.py` / `search_isrctn.py` / `search_drks.py` reuse it. **Only public query terms plus non-content request metadata are sent — no confidential data — compliant with the ct-base confidentiality red line.** Metadata = `query_origin` (stable machine-derived SHA-256 hash for abuse-limiting/attribution), `skill_version`, `entry_point`, `params.user_language`, `demand_id`; disclosed in README §Outbound data disclosure. CDE + ChiCTR + ISRCTN + DRKS + WHO ICTRP are served by one unified Coze endpoint `https://ct-search.coze.site/run` (WHO via `--source who`, CDE via `--source chinadrugtrials`), sharing one long-lived token.

**Bridge + de-duplication:** `aggregate.py` normalizes UTN/TRN/registry numbers + fuzzy matches + scans embedded registration numbers on the `raw` field (CT.gov canonical), so the ICTRP feed and our own bridging reinforce each other.

> Full CDE external-workflow detail (endpoints, token mechanism, four calling modes, payload contract, decision flow, agent interaction contract, parameter mapping) → **`CDE/cde_workflow.md`** (archived, local reference only).

## Data Sources

| Source | Tier | Access | Token |
|---|---|---|---|
| ClinicalTrials.gov v2 | Tier 1 (direct) | Official REST API (stable) | — |
| EU CTR (legacy EudraCT) | Tier 1 (direct) | Pure-HTTP HTML parse (`search_eu_ctr.py`) | — |
| PubChem | Tier 1 (direct) | PUG-REST | — |
| China CDE | Tier 2 (ext-svc) | Unified Coze endpoint `https://ct-search.coze.site/run` (`--source chinadrugtrials`) | Bearer (long-lived) |
| WHO ICTRP | Tier 2 (ext-svc) | Unified Coze endpoint (`--source who`); mirrors 14+ registries | Bearer (same token as CDE) |
| ChiCTR | Tier 2 (ext-svc) | Unified Coze endpoint (`--source chictr`) | Bearer (same token) |
| ISRCTN | Tier 2 (ext-svc) | Public API dead → unified Coze endpoint (`--source isrctn`) | Bearer (same token) |
| DRKS | Tier 2 (ext-svc) | JS/redirect-only → unified Coze endpoint (`--source drks`) | Bearer (same token) |

## External Open-Source Integrations (v0.13.0)

| Tool | Source | Purpose | Integration |
|---|---|---|---|
| **pytrials** | `pip install pytrials` | CT.gov batch-retrieval client: `ClinicalTrials().get_study_fields()` pulls fields in bulk and adapts to different endpoint response shapes | Optional API client, parallel to the existing CT.gov v2 REST API path |
| **Docling** | `pip install docling` | Regulatory-document structured parsing: `DocumentConverter().convert('protocol.pdf')` outputs hierarchical Markdown/JSON, preserving table structure and section levels | PDF-parsing enhancement layer shared by ct-protocol / ct-literature |

> WHO ICTRP is the meta-aggregator: when `--with-ictrp` is set it is PRIMARY and the national registries it covers (CT.gov, EU-CTR, ISRCTN, DRKS, ChiCTR) become FALLBACK-ONLY (skipped on WHO success). **CDE is ALWAYS independent** (`--with-cde` never skipped) because WHO's English-title matching misses Chinese trials.

## Features

- Search by disease / intervention / sponsor across sources → de-duplicate similar trials, find control designs.
- Unified normalization → heterogeneous cross-registry records into one schema.
- Aggregation analysis → phase / status distribution, top sponsors, timeline, competitor landscape.
- Drug → target mapping (PubChem) → mechanism & competitor target comparison.
- Structured output → JSON / Markdown / optional PNG; chained to `ct-pipeline` and `ct-protocol`.
- **Status track / diff (P0-A, local-only):** `--track` writes normalized results to `registry_snapshot.json`; `--diff <snapshotA> <snapshotB>` compares two `normalized.json` by NCT set and outputs `status_delta` (added / removed / status-changed / synonym-spelling-changed). Diff uses `STATUS_EIV` synonym normalization (RECRUITING≈ACTIVE_NOT_RECRUITING≈ONGOING in the same bucket, no false positives). Zero network.
- **pytrials enhanced mode (v0.13.0, opt-in):** uses pytrials as the official API client to batch-pull CT.gov fields, adding: ① indication-wise distribution heatmap of recruiting trials; ② same-indication endpoint-design comparison; ③ target-center historical project search. Complementary to the existing Tier 1 direct-connect path; pytrials offers a friendlier Python wrapper.
- **Tier-2 graceful fallback (P0-B, network only with --run):** WHO timeout/error auto-falls back to CDE + ClinicalTrials.gov for the report and sets `who_status=failed` (not hidden); CDE returning 0 records triggers one auto-retry (`--cde-retry` default 1, rate-limited by `--cde-retry-delay` default 2s); if still 0, marks `zero_hit_unverified`; all fallback paths disclose data flow in `report.md` (also writes `run_status.json`).
- **WHO Chinese-English keyword auto-translation (P0-C, 2026-09-07):** WHO ICTRP endpoint only accepts English (Chinese keywords reliably return 0; English hits normally). For any `source=who` search (including the ChiCTR→WHO fallback path where the keyword is Chinese), keyword / multi_keywords are auto-translated to English: curated term_map (`references/term_map.json`, bidirectional authoritative) first; dictionary-miss long-tail terms fall back to online translation (`kw_localize.online_translate`, MyMemory keyless); envelope labels `source=term_map/online` truthfully. Disable with `--no-kw-localize`. ⚠️ Online translation is unreliable for medical terms (tested `光生物调节`→`Photobioregulation`, WHO hit 0; correct term `photobiomodulation` hit 974) — **new domain terms MUST enter term_map (ct-base single source), do not rely on online fallback**.
- **ChiCTR WAF pure-Python crack (server-side node, 2026-09-07):** ChiCTR's Alibaba Cloud WAF `acw_sc__v2` can be cracked deterministically — challenge page inlines `var arg1='<40 hex>'`, algorithm = 40-bit position permutation table + fixed XOR key, solvable in pure Python (no Node/Playwright needed). Coze-side `chictr_search_node` rewritten to **HTTP-first** (`searchproj.html?title=<kw>&page=N` new param; old `searchContent=` is dead), Playwright as fallback only. ⚠️ This change is in Coze server-side source — **must be re-packaged and deployed to Coze console to take effect**; local `--source chictr` goes through the unified endpoint and auto-benefits from the node update.
- **WHO-COVERED 5-source auto WHO fallback (P0-D, 2026-09-07):** When a WHO-covered source is queried directly but that source's site is unreachable, auto-fallback to WHO ICTRP to retrieve that source's trials — no interruption, no empty hand. Layered: ① Unified-endpoint sources (ChiCTR/ISRCTN/DRKS, `search_ictrp.py`) detect `source_likely_down` then in-process switch to WHO, filter that source's records by `_SOURCE_ID_RE` and backfill (envelope `fallback_used=who_ictrp` / `<src>_records_via_who=N`); ② Tier-1 direct sources (CT.gov/EU-CTR, `ct_registry.py` orchestration) site-unreachable → `_tier1_who_backfill` auto-sends WHO search and merges into normalization — if WHO primary path already succeeded, the mirror already covers it, no duplicate request. CLI: `--no-fallback-who` disables auto-WHO-switch for unified-endpoint sources; Tier-1 fallback is on by default.
- **Research-layout vs disease-burden benchmarking (P1, intel push 2026-10-18):** reuses the JCE 2026 method to add an "are resources flowing to high-burden areas" analysis to registry search. Against trial counts aggregated by cause and GBD DALYs it computes three metrics — **log-log slope β** (β≈1 = resources scale linearly with burden; β<1 = high-burden areas under-funded), **misalignment ratio** (actual trial share vs burden share), and **share of zero-trial conditions** (number of causes with T=0 and their combined DALYs share). Script `scripts/burden_comparison.py` (pure-stdlib OLS; matplotlib optional for charts) + methodology `references/burden_benchmark.md`. GBD data is user-supplied; zero network calls.

## Requirements

- Python 3.10+ (Anaconda `C:\Tools\anaconda3\python.exe` recommended).
- Required: `requests`, `pandas`, `beautifulsoup4`, `lxml`.
- Optional: `matplotlib` (PNG); `playwright` (CDE local scrape — last resort only, WAF-blocked).
- Network: read-only public data. **CDE / WHO / ChiCTR / ISRCTN / DRKS require a Bearer token** (unified endpoint).

## Coze key (unified-endpoint credential)

All Tier-2 retrieval (CDE, WHO ICTRP, ChiCTR, ISRCTN, DRKS) is served by one unified endpoint `https://ct-search.coze.site/run`, which requires a Bearer token. That token is a **shared public credential** — a Coze workload-identity issued by the author, bound to the endpoint (not to any individual user), not a personal secret.

- **Where it lives:** embedded in `adapters/endpoint_token.py` as an XOR+base64 obfuscated blob (`EMBEDDED_SECRETS["coze_unified"]`). `.py` is on every publishing platform's allow-list, so it ships with the package and works out-of-the-box. (The blob used to live in `config/ictrp.dat`, but platforms like SkillHub silently strip `*.dat`, which broke the shipped skill — hence the move to `adapters/endpoint_token.py`.)
- **Resolution order (ct-base §5.236):** `CLI --token` > env `CT_REGISTRY_COZE_TOKEN` (legacy `ICTRP_WORKFLOW_TOKEN`; CDE standalone `CDE_WORKFLOW_TOKEN`) > embedded blob > legacy `.dat`. The embedded blob is the default; you normally never touch it.
- **Keep it as-is — do not replace it with your own token** unless the author issues a new one. To override (e.g. after a re-issue), pass `--token <JWT>` on the CLI or export `CT_REGISTRY_COZE_TOKEN`; never paste tokens into chat.
- **Obfuscated, not encrypted (ct-base §5.234):** the XOR+base64 encoding only hides the string from casual directory-listing / grep, not from a determined reader. Public shared credentials are allowed to ship with the package (§5.239/§5.243); private tokens must come from CLI/env only and are not persisted to disk.

## ⚠️ Safety

- Default SAFE PREVIEW: scripts only generate / display; network runs only with explicit `--run`.
- Reads public registry data ONLY — **zero confidential data or information input** (B-tier: ordinary input + public retrieval).
- CDE automatable path is the unified endpoint (one long-lived token shared with WHO ICTRP via `adapters/endpoint_token.py`); the legacy standalone `search_cde_workflow.py` is archived locally under `CDE/` (NOT shipped with the package — **RETIRED 2026-08-12**; `--cde-legacy` is now a no-op warning that auto-routes to the unified endpoint `search_ictrp.py --source chinadrugtrials`). Only public query terms plus non-content request metadata (`query_origin` machine-hash, `skill_version`, `entry_point`, `user_language`, `demand_id`) are sent; endpoint credential bundled in-package (shared public token, no user-side configuration; verified: HTTP 401 without it — the token ships with the skill); still disclose "data via third party". CDE paste-mode (Playwright / `parse_cde.py`) remains a no-egress fallback.
- **Unified-endpoint token** — all Tier-2 sources share one long-lived Bearer token, embedded in `adapters/endpoint_token.py` as a public shared credential (XOR+base64 obfuscated, not a personal secret). Full resolution order, override, and history → **Coze key** above. Never paste tokens into chat — provide via CLI(`--token`) / env `CT_REGISTRY_COZE_TOKEN` only.
- Output is for reference only, not a regulatory submission (CSR / filing must be generated per GCP separately).
- **Concurrency constraint (P1-7):** the quota counter `config/usage.json` and the output directory are shared files inside the skill directory; `usage_guard.py` serializes read/write via an advisory file lock. Run **one skill per session**; if multiple AI sessions call the same skill directory in parallel, they must rely on that lock to avoid shared-state races that could corrupt the counter or outputs.

## Search procedure

Execute in **forced order** (scope → translate → search). Full three-step procedure + the mandatory Keyword-System Confirmation Gate → **`references/search_procedure.md`**.

1. **Scope** — pick registries. WHO+CDE already covers CT.gov/EU-CTR/ChiCTR/ISRCTN/DRKS (two endpoints only); WHO and CDE are **separate calls** (shared `demand_id`), never one request.
2. **Keywords** — translate per source (English for CT.gov/WHO/PubChem; CDE needs Chinese, strip "类" suffix, e.g. use `drugs_name=列汀` not `DPP-4抑制剂`). > **🔤 CDE en→zh 翻译确认卡（0.5.02）**：端点直连路径的自动翻译映射随结果 JSON 的 `keyword_localization` 透出——凡遇 `ambiguous:true`（多候选）或 `fail_open`（英文未翻译）**必须停下向用户展示翻译确认卡并确认后重跑**；家族标准 → `ct-base/references/bilingual_retrieval.md` §5（模板 `ct-base/scripts/translation_gate.py`）；CDE 实例细则 → `references/search_procedure.md` §Translation Confirmation Card。
3. **Execute** — direct sources free & unmetered; external-workflow sources counted once per `demand_id` (currently free, daily cap). Then `normalize → aggregate → report` (Excel final artifact; PDFs never auto-downloaded).

> **⏱️ Retrieval time & data-volume guide** → **`docs/retrieval_guide.md`** (typical 10s–5min; partial-result-on-timeout; empirical record-throughput by keyword breadth).

## Errors

| Error | Cause | Fix |
|---|---|---|
| `URLError` on CT.gov | No network / proxy | Confirm clinicaltrials.gov reachable; set proxy |
| CDE/ChiCTR WAF "access blocked" | SafeDog WAF blocks browsers | Use external workflow (unified endpoint); fallback: assisted paste → local parse (no egress) |
| WHO/CDE 403 invalid token | Rare corrupted/revoked blob (token is long-lived, normally never 403s) | Re-issue via env `CT_REGISTRY_COZE_TOKEN` / `--token`, then re-run |
| ISRCTN 404 | Public API dead | Unified endpoint (`--source isrctn`) |
| DRKS unreachable | JS/redirect-only | Unified endpoint (`--source drks`) |
| EU CTR | Pure-HTTP HTML parse, no API/token | `search_eu_ctr.py` (verified 2026-07-24) |
| CDE HTTP 401 | Missing/malformed `Authorization` | Send `Authorization: Bearer <token>` (one space after Bearer) |
| CDE HTTP 500 `字段类型错误` | Field sent as `{"value":x}` or `project_list` as array | Use plain strings; `project_list` as JSON **string**/file |
| CDE `total_count:0` | Legitimate empty hit-set (fixed 2026-07-23) | Treat 0 as valid "no match"; retry transient timeout with `--timeout 300` |
| CDE read timed out | Slow large set / ~300 s cap | Transient — retry with default 300 s |

## Implementation

Entry script: `ct_registry.py` (cross-source orchestration, auto keyword-localization, parallel batch retrieval, quota guard) lives in `scripts/`. Outbound-calling per-source wrappers live in `adapters/` (the dedicated outbound directory per §16.9): `search_ctgov.py`, `search_eu_ctr.py`, `search_ictrp.py`, `search_chictr.py`, `search_isrctn.py`, `search_drks.py`, `search_cde.py`, `extsvc_client.py`, `enrich_pubchem.py`, `download_docs.py`, `fetch_eu_ctr_docs.py`. Pure-local compute stays in `scripts/`: `normalize.py`, `aggregate.py`, `report.py`, `export_xlsx.py`, `parse_cde.py` (no-egress paste-mode), `usage_guard.py`, `i18n.py`. The retired standalone CDE workflow is archived locally under `CDE/` (NOT shipped; **RETIRED 2026-08-12 — `--cde-legacy` is a no-op warning**).

- CDE external-workflow modes, payload contract, decision flow, parameter mapping → **`CDE/cde_workflow.md`** (archived, local reference only).
- Search procedure, scope rules, keyword gate → **`references/search_procedure.md`**.
- All CLI recipes, advanced-field inventory (WHO/CDE), detail/doc enrichment, resource-usage policy → **`references/cli_reference.md`**.

One-shot example:

```bash
# agent / non-interactive calls MUST add --no-expand (or --kw-en/--kw-zh / --kw-adopt),
# otherwise the Keyword-System Confirmation Gate stops unconditionally (sys.exit) with no output
python scripts/ct_registry.py --cond "NSCLC" --status RECRUITING --with-cde --no-expand --out-dir ./out --run
```

# Research-layout vs disease-burden benchmarking (P1): compare against GBD DALYs after aggregating results
python scripts/burden_comparison.py --trials out/normalized.json --dalys gbd_dalys.csv --out burden_comparison.json
# With charts (requires matplotlib); trials may also be passed directly as an aggregation dict
python scripts/burden_comparison.py --trials '{"diarrhea": 0, "breast_cancer": 120}' --dalys gbd_dalys.csv --chart burden_comparison.png

## Pipeline

- `ct-registry` → `ct-pipeline`: `normalized.json` consumed by the intelligence layer for competitor discovery & landscape.
- `ct-registry` → `ct-protocol`: similar-trial design benchmarking, aiding protocol writing.

See `references/units.md` for the atomic-task unit index.

## 4.1 Recruitment-Population Acceptability Dimension (P1 · JMIR 2026 AI digital-recruitment study)

> Source: JMIR Preprint 2026-10-11, *AI in Digital Recruitment for Cardiovascular Clinical Trials Among Black Adults* (10.2196/preprints.114103). When registry search / pooled analysis interprets "recruitment feasibility", it must include the target population's acceptability of, and barriers to, the recruitment approach — not only enrollment speed and coverage.

**Discipline (new dimension for recruitment-feasibility interpretation)**:

1. When results are used to assess recruitment feasibility for a trial or population, annotate the **population acceptability / perceived barriers / preferences** dimension in addition to registration counts and enrollment speed (where data are available).
2. For historically under-represented populations, distinguish the two layers "feasible at registry level" vs "acceptable at participant level"; do not substitute coverage for acceptability.
3. Aligns with `ct-eligibility` §7.1: recruitment-feasibility interpretation and screening-feasibility assessment share the same population-acceptability metric.

## Publishing (ct-base §16)

Shared assets are single-source in `ct-base` (§16.8) — never edit a shared file locally and ship it. Mandatory pre-publish gate `scripts/publish_preflight.py` (shared-sync check → secret scan → ClawHub audit → inject dry-run) + `publish_inject.py` self-contained packaging → GitHub → SkillHub → ClawHub. Full procedure → **`docs/publishing.md`**.


## Local Merge Addendum (this round)

Produced by skill-reloader semantic merge. The base is the remote full text captured at merge time and preserved line by line; the three indented lines below are remote baseline lines kept verbatim for traceability, while front-matter and body received same-address value replacements for this round of changes.

```text
    version: 0.14.5
    description: "Cross-source search of global clinical-trial registries (ClinicalTrials.gov, CDE/ChiCTR/ISRCTN/DRKS/WHO ICTRP, PubChem), normalizing and aggregating phase/status/sponsor/timeline/competitor landscape into JSON/Markdown for trial planning, de-duplication, control-design benchmarking, and competitive intelligence. / 跨源检索全球临床试验注册库（ClinicalTrials.gov、CDE/ChiCTR/ISRCTN/DRKS/WHO ICTRP、PubChem），归一化聚合分期/状态/申办方/时间线/竞品格局，产出 JSON / Markdown，用于立项查重、对照设计与竞品格局分析。"
    **Deliverable language (v0.14.5):** result files (`report.xlsx` / `report.md`) never inherit the *server* OS locale — the published workbench runs in an en_US container, which used to emit all-English workbooks. `--lang auto` resolves in this order: explicit `--lang` > `CT_REGISTRY_LANG` (workbench injects the current UI language) > skill-root `config.json language` > cover-title language (CJK → zh) > OS locale > zh. English users still get English via `--lang en` or by switching the workbench UI to EN. Raw registry values (titles, status enums, sponsor names) are never translated — only the interface chrome.
```
