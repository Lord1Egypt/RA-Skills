---
slug: ct-safety
displayName: Clinical Trial Safety Signal / 临床试验安全信号专家
name: ct-safety
cn_name: 临床试验安全信号专家
version: 1.0.1
invocable: true
required_commands: [python]
summary: "基于 FDA FAERS 筛查药物-事件安全信号，计算 disproportionality（PRR / ROR / IC / EBGM，含 95% CI）与安全信号评分（0–100，T1–T4）。数据源：FDA FAERS、FDA 标签、中国 NMPA 药物警戒通报、DailyMed 说明书、RxClass MED-RT、openFDA 召回执法、香港 ADR 警报。"
license: MIT
description: "Screen drug–event safety signals via disproportionality analysis (PRR / ROR / IC / EBGM with 95% CIs) on FDA FAERS, with Safety Signal Score (0–100, T1–T4). Sources: FDA FAERS, FDA Label, China NMPA PV bulletins, DailyMed SPL, RxClass MED-RT, openFDA enforcement recalls, Hong Kong ADR Alerts. / 基于 FDA FAERS 筛查药物-事件安全信号，计算 disproportionality（PRR / ROR / IC / EBGM，含 95% CI）与安全信号评分（0–100，T1–T4）。数据源：FDA FAERS、FDA 标签、中国 NMPA 药物警戒通报、DailyMed 说明书、RxClass MED-RT、openFDA 召回执法、香港 ADR 警报。"
triggers:
  - "FAERS safety signal"
  - "安全性信号分析"
  - "药物不良反应信号"
  - "disproportionality analysis"
  - "ct-safety"
  - "compare drug X vs Y adverse events"
  - "FAERS safety comparison"
  - "active-comparator disproportionality"
  - "多药安全性对比"
  - "药物类别头对头安全性比较"
metadata:
  openclaw: { emoji: "🛡️" }
  authors: ["medstatstar", "phoe-zip"]
  license: "MIT"
  tags: [clinical-trial, safety, faers, pharmacovigilance, signal-detection]
  homepage: "https://github.com/medstatstar/ct-safety"
permissions:
  scope: "user-space-only"
  network: "public-retrieval"
  network_note: "Reads only public sources (FDA FAERS/openFDA, DailyMed, RxClass MED-RT, openFDA recalls, optional China/HK PV); keyless. All retrieval OUTBOUND to ct-search.coze.site (thin local client); No local fallback path since v0.9.9. No confidential input."
  filesystem: "read-only to its own files; writes outputs ONLY to the user-specified --out-dir (default cwd). No system-path or hidden logging; logs under --out-dir; FAERS raw not persisted unless saved."
  data: "no confidential data input; only public query keywords + public results cross the boundary. No confidential user data transmitted."
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

- **English guide** → [README.md](https://github.com/medstatstar/ct-safety/blob/main/README.md) · **中文指南** → [README_zh-CN.md](https://github.com/medstatstar/ct-safety/blob/main/README_zh-CN.md)
- This skill responds in the user's input language and auto-switches; runtime prompts switch by locale. Bilingual walkthroughs live in the READMEs.

## Cross-turn Continuity (required)

Family standard: `ct-base/references/continuity.md` (pattern A). Echo the block below after every analysis; on a follow-up (changed `event` / different comparator drug / different measure), read the most recent block in the conversation and override **only the changed fields** — never rely on LLM memory alone:

```
## Current retrieval settings: drug=… | event=… | comparator=… | measure=PRR | source=FAERS
```

# Clinical Trial Safety Signal

## Published Application

Workbench app: `https://ct-safety.app.workbuddy.host/` (appId `wbapp_GyOm0cdJ1qHoaQxlFZOVwl`) — deployment registry / version anchors / re-publish protocol / post-deploy smoke list in `references/published_app.md` (**single source of truth**; load before any deploy; always overwrite the existing appId, never `createNewApp`).

> Safe by default: **overview-first**. Step 1 (overview) runs automatically; Step 2 (detailed retrieval) runs ONLY after the user explicitly confirms.
>
> **What counts as explicit confirmation.** Any unambiguous go-ahead — e.g. "yes, run the detail" / "确认，跑详情", or **`skip preview and run` / `跳过预览，直接跑`**. The last one is a *confirmation phrasing*, not a bypass: it means "the overview is enough, run Step 2 now". All Step-2 guardrails apply identically (no heavy download before confirmation, outputs confined to `--out-dir`, no confidential input). Conversely, a generic remark in passing conversation is **not** consent — the go-ahead must be an instruction that explicitly asks for the detail step to run.

## Disclaimer & Intended Use

- **Audience.** This skill is intended for **pharmacovigilance / clinical-trial methodologists and drug-safety professionals**. It is a methodologic signal-screening aid, not end-user health software.
- **Not a clinical or regulatory decision tool.** All outputs are **statistical disproportionality signals** computed from *spontaneous* adverse-event reports (FDA FAERS), which are subject to reporting bias, under-reporting, and confounding. A signal **does NOT establish causation** and **MUST NOT** be used to start, stop, or change any medication, or to make clinical or regulatory decisions. Always corroborate with RCTs, product labels, and qualified clinical/regulatory judgment (ICH E2 family).
- **Data flow (transparent).** Reads ONLY public sources (keyless); writes outputs SOLELY to the user-specified `--out-dir`; no system-path or hidden logging; FAERS raw responses not persisted unless explicitly saved. Zero confidential data input (see the Data Egress Guardrail above).

## Purpose

Run pharmacovigilance disproportionality analysis on FDA FAERS public adverse-event data to surface potential drug–event safety signals (PRR / ROR / IC / EBGM), supporting clinical-trial safety surveillance and label / signal screening. Optional China official PV bulletins (cdr-adr.org.cn) provide qualitative corroboration only. For *published* safety literature context (reviews / PV papers), chain to **`ct-literature --safety`** — it returns a qualitative CSM subset that corroborates signals but must not enter the FAERS 2×2.

## Data Sources

Two categories — **quantitative** (2×2 disproportionality) and **corroborative** (qualitative labeled-vs-unlabeled judgement). The latter does not feed PRR/ROR (would distort the 2×2); it informs signal prioritization per ICH E2C / CIOMS VIII (labeled = known risk → downgrade; unlabeled = potential new signal → upgrade).

| Category | Source | Access | Status |
|---|---|---|---|
| Quantitative | FDA FAERS (`drug/event.json`) | Thin local client (Coze unified endpoint `ct-search.coze.site`). `query_total` / `fetch_case_reports` always local-direct (structured state cannot round-trip through Coze) | Required (A-tier) |
| Quantitative | **MAUDE device adverse events (`device/event.json`)** — `--device` | Same thin-client single-egress via Coze (`source='maude'`). Device dimension defaults to `device.brand_name`, adverse-event dimension to `event_type`, date dimension to `date_received`; 2×2 & disproportionality reused unchanged | Optional (maude channel on the unified endpoint verified working 2026-11-08) |
| Quantitative | FDA Label (`drug/label.json`) | Thin local client (Coze unified endpoint). `check_event` local-only | Optional `--with-fda-label` |
| Corroborative | DailyMed SPL · RxClass MED-RT · openFDA Enforcement | Thin local client (Coze unified endpoint) | Optional `corroborative_sources.py` |
| Qualitative | cdr-adr.org.cn | Thin local client (Coze `nmpa_pv` node; local keeps keyword expansion + evidence grading + cache) | Optional `--with-cn-pv` |
| Qualitative (CN add-on) | drugoffice.gov.hk (HK ADR Alerts) | Thin local client (Coze `hk_pv` node) | Coze node written; after deployment |

## Methods

Four disproportionality measures on the drug–event 2×2 table (plus multiple-testing and corroboration layers):

- **PRR** — signal if PRR ≥ 2 **and** χ² ≥ 4.
- **ROR** — signal if lower 95% CI > 1.
- **IC** (UMC/VigiBase Information Component) — signal if lower 95% CI > 0.
- **EBGM** (FDA MGPS Bayesian shrinkage) — signal if EB05 ≥ 2.
- **Corroboration layers** — BH-FDR q-value over top-N / benchmarks; PT→SOC MedDRA grouping; Haldane-Anscombe continuity (+0.5/cell; `a==0` → conservative null); aROR (`--compare-drugs`); temporal anomaly CUSUM / rolling-Z / changepoint (`--trend`); Safety Signal Score 0–100 + T1–T4 (`--with-fda-label`); Naranjo (`--with-causality`, qualitative only — never fed into PRR/ROR/IC/EBGM).

Full formulas, thresholds, EBGM/MGPS math, FDR, aROR, trend, and score/tier weighting: `references/methods.md`.

## Features

| Capability | Flag / Source |
|---|---|
| Drug–event signal detection (PRR/ROR/IC/EBGM) + multi-method cross-judgement | FAERS |
| **Device adverse-event signal detection (same 2×2/PRR/ROR/IC/EBGM pipeline)** | MAUDE via `--device` (Coze `source='maude'`, dimension `device.brand_name` / `event_type` / `date_received`; **maude channel verified working on the unified endpoint, 2026-11-08**) |
| Statistical guards (BH-FDR · PT→SOC · sparse-2×2 `--validate-controls`) | — |
| HTML + XLSX core deliverables (JSON/MD backup) | — |
| China official PV bulletins (qualitative only) | `--with-cn-pv` |
| Labeled / unlabeled corroboration | `corroborative_sources.py` |
| Temporal anomaly · multi-drug aROR · score 0–100 + T1–T4 | `--trend` · `--compare-drugs` · `--with-fda-label` |
| Naranjo causality · MedDRA coding · prioritization · PSUR | `--with-causality` · `--code-verbatim` · `--prioritize` · `--psur` |
| Case-level de-duplication (L1 collapse / L2 flag-only) | `--case-level` |
| Non-ASCII drug-name auto-translate | `--drug 阿司匹林` → `aspirin` |
| Chained invocation | `ct-protocol` · `ct-registry` · `ct-literature --safety` |

Full capability table with scenarios and boundaries: `references/ADVANCED.md`.

## Requirements

- Python 3.10+ (Anaconda recommended). Required: `requests`. Optional: `matplotlib` (PNG charts).
- Network: read-only FAERS public API. An openFDA key is optional (raises quota only) — see below.

## ⚠️ Safety

- Network: retrieval (present / `--out-xlsx`) runs lightweight openFDA `count` facet queries (seconds, no case download); **case-level download requires explicit `--run`** (throttled by HARD_CAP=10000). Reads FAERS public reports ONLY — **zero confidential data or information input** (A-tier, `network=public-retrieval`).
- China PV bulletins are **qualitative narrative** — NO per-drug-event counts; must **NOT** feed disproportionality; only corroborate a FAERS signal.
- FAERS re-ingests the same case as follow-up versions and via multiple reporters. Case-level de-duplication fixes the **individual-case listing** only; disproportionality counts come from openFDA **aggregate** endpoints and therefore still carry duplicate-reporting bias. Never claim a signal is "de-duplicated".
- Signal detection is for screening, not causal conclusion; regulatory submission (DSUR / PBRER / label change) must be assessed per GCP / ICH E2 separately.

## Workflow

Two-step, overview-first (**present summary in context, Excel on demand**):
1. **Step 1 — Overview (automatic):** `fetch_reports.py --drug X` sends 8 `count` facets, prints the summary to context in seconds, caches `faers_summary_cache.json`. No confirmation needed.
2. **Step 2 — Detail (only after explicit confirm):** `--out-xlsx` builds the summary Excel from cache; `--run` downloads individual case reports (HARD_CAP 10000) for age/country stats. Signal detection via `ct_safety.py`.

`scripts/overview.py` is deprecated (merged into Step 1). Full workflow, caching, `--parallel`, XLSX layout: `references/fetch_pipeline.md`.

### One-shot signal report (`ct_safety.py`) — two core deliverables

`ct_safety.py --drug X --event Y --run` writes into `--out-dir` and prints a "Core Deliverables" block:

- **`faers_report.html`** — visual report (open in browser preview). **Core ①.**
- **`faers_report.xlsx`** — ALL raw data (counts, 2×2, four measures, optional Label/CN-PV/Score). **Core ②; audit every number here.** (`faers_report.md` / `*.json` are backups only.)

### Progressive analysis layers

An extension of the overview-first design: every layer below is an **opt-in flag** (nothing runs by default — each layer adds openFDA query volume). Stack layers according to the question you need answered. All layers degrade gracefully (a single-layer failure never breaks the main report).

| Layer | Question it answers | Flag | Network cost (relative to L0) | Report section |
|---|---|---|---|---|
| **L0 Standard** | Does this (drug, event) pair show a signal? | (default, no flag) | 1 × 2×2 count | Core ①② |
| **L1 Grading** | How strong is the signal? Which one first? | `--with-fda-label` | +1 label query | Safety Signal Score 0–100 + T1–T4 |
| **L2 Trend** | Is it **new** or long-standing? Worsening lately? | `--trend` | +N monthly pages (rate-limit sensitive) | Time-trend anomalies (CUSUM / rolling-Z / changepoint) |
| **L3 Comparison** | Is it **this drug** or a class-wide effect? | `--compare-drugs FOCAL REF1 REF2` (needs ≥2 drugs) | +(1+M) counts | Multi-drug comparison · aROR (95% CI + sparse correction) |
| **L4 Confirmation** | Any time/dose relationship? Worth escalating? | `--verify-signal` (needs `--case-level` for full depth) | +quarterly series (reuses L2 if already run); cases billed separately | Signal verification workflow (temporal CUSUM/Poisson + dose-response / dechallenge) |

Typical combinations:
- **Quick screen**: `--drug X --event Y` (L0)
- **Routine monitoring**: `--drug X --event Y --with-fda-label` (L0+L1)
- **New-signal investigation**: `--drug X --event Y --trend --with-fda-label` (L0+L1+L2 — answers "is this a Weber effect?")
- **Class-effect triage**: `--drug X --event Y --compare-drugs X Y Z --with-fda-label` (L0+L1+L3 — answers "is the whole class like this?")
- **Deep confirmation**: L0–L3 all on + `--verify-signal --case-level 200` (add `--psur` for a PSUR draft)

> The L3 aROR is an **aggregate-level** adjusted reporting ratio from FAERS (the openFDA count API exposes no case-level covariates); true covariate adjustment needs `--case-level` case pulls followed by `adjust_ror.py`'s `logistic_irls`. An L2 changepoint may reflect reporting-behaviour shifts (media attention, regulatory alerts) rather than causality — conclusions from all three layers must be read together with RCT evidence and the label.

## API Key (openFDA) — optional, self-configured

The skill runs **without a key**; a free key only raises quota. Provide via CLI `--api-key`, env `OPENFDA_API_KEY` (recommended), or skill-root `.env` (git-ignored; plaintext or `obf:` XOR+base64 per ct-base §5) — never paste keys into chat or shipped files. Details: `references/openfda_api_key.md`.

## Errors

Brief; full table in `references/errors.md`.

- **429 / rate-limited** — exceed openFDA quota; fix: `--api-key` or lower frequency.
- **Persistent 404 on multi-word PT** — not indexed; swap to standard PT; `total()` auto-downgrades 404→`.exact`.
- **`--max > 10000`** — clamped to HARD_CAP 10000 (API-return-order first N, selection bias).
- **Outbound Coze rejected / unreachable** — endpoint not allow-listed / token invalid / `safety_rest_node` undeployed; check Coze deployment status and config.json `auto_approve_endpoints`.

## Comparative Study Design Mode

For "compare X vs Y" / "within-class head-to-head" / "active-comparator" requests, switch to the comparative track (single-drug default otherwise). Steps: ① data prep (`faers-data-prep.md`) → ② study style + 4 workloads (`faers-comparative-design.md`) → ③ metrics / comparators / robustness (`faers-method-library.md`) → ④ evidence tiers + claim boundaries (`evidence-hierarchy.md`).

**Hard rules:** never run disproportionality on unprepared raw counts; present all four configurations then recommend one; label every result `[Tier 1]` signal / `[Tier 2]` comparative / `[Tier 3]` robustness; Tier-4 claims (incidence, causality, benefit–risk, prescribing) forbidden without external data; flag weak comparator indication overlap.

## Pipeline

- `ct-safety` → `ct-protocol`: signals feed the safety monitoring plan.
- `ct-safety` → `ct-registry`: control-trial safety-design benchmarking (CDE trials).
- CN-PV is an in-skill qualitative add-on, not a chain target. Units: `references/units.md`. Changelog: `CHANGELOG.md`.
