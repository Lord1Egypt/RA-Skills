---
slug: ct-samplesize
displayName: Clinical Trial Sample Size / 临床试验样本量专家
name: ct-samplesize
cn_name: 临床试验样本量专家
version: 5.15.0
invocable: true
required_commands: [python]
summary: 为临床试验从业者提供的样本量与检验效能计算工具，覆盖 67 种检验，并提供 SVG 出版级别图形。自然语言驱动，默认回传完整 R 代码。
license: MIT
description: "Sample size and power calculation tool for clinical trial practitioners, covering 67 test types and returning publication-grade SVG figures. Natural-language driven; full reproducible R code is returned by default. / 为临床试验从业者提供的样本量与检验效能计算工具，覆盖 67 种检验，并提供 SVG 出版级别图形。自然语言驱动，默认回传完整 R 代码。"
triggers:
  - "clinical trial sample size"
  - "样本量计算"
  - "clinical trial power"
  - "检验效能计算"
  - "临床试验 设计"
  - "non-inferiority sample size"
  - "equivalence sample size"
  - "survival analysis sample size"
  - "adaptive design"
  - "group sequential design"
  - "Bayesian clinical trial"
  - "Wilcoxon rank-sum sample size"
  - "非参数检验 样本量"
  - "wilcoxon signed-rank"
  - "秩和检验 样本量"
metadata: { openclaw: { emoji: "📊" }, authors: ["medstatstar", "phoe-zip"], license: "MIT", tags: [clinical-trial, sample-size, power, coze, adaptive-design, bayesian, win-ratio, nonparametric, wilcoxon], homepage: "https://github.com/medstatstar/ct-samplesize" }
permissions:
  scope: "user-space-only"
  network: "required"
  network_note: "Requires remote Coze compute (CTSS_COZE_ENDPOINT; CTSS_COZE_MOCK=1 for demo); no local fallback. Only trial-design parameters (no patient data) + query_origin hostname-hash, skill_version, locale leave the machine; payloads PII-stripped."
  filesystem: "writes figures to CTSS_OUTPUT_DIR (default ./outputs) and optional curve PNGs; otherwise read-only"
  data: "no patient/external data leaves the boundary — only trial-design parameters plus hostname hash (query_origin), skill version (skill_version) and locale metadata are sent"
---
## Data Egress Guardrail (CT family standard · F33)

This skill may call external endpoints (Coze services, shared third-party search endpoints, public APIs or LLMs). **Internal confidential data must not leave the local domain.** Mandatory rules:

- **Never outbound**: patient-level records, unpublished protocols / CSRs / internal documents, personal identifiers or sponsor-confidential content — as query terms, attachments or prompt payload.
- **Allowed minimum**: public search terms and non-content metadata only (machine hash, skill version, entry point, language, request id). Results from public registries (ct.gov / CDE / FAERS / OpenAlex / PubMed, etc.) are processed locally.
- **Local first**: computation, de-identification, aggregation and reporting stay on this machine; confirm the payload carries no confidential field before any cloud call.
- **Visible disclosure**: workbench search forms must state the outbound endpoint and this boundary in visible text, not only in a hover tooltip.
- **Fail loud**: stop and tell the user if any rule cannot be guaranteed; never degrade silently.

Machine-checked by `ct-base/scripts/spec_lint.py` rule **F33**.

# Clinical Trial Sample Size

## Published Application

| Item | Value |
|---|---|
| Share link | `https://ct-samplesize.app.workbuddy.host/` |
| appId | `wbapp_9K1dei1PydVQ66YmawCD3C` |
| domainPrefix | `ct-samplesize` |
| Deploy metadata | `workbench/app.config.json` |
| Deployed as | Static site (`python -m http.server $PORT --bind 0.0.0.0`) |
| Payload | `WorkBuddy/2026-09-14-14-39-40/deploy_ctss/static/index.html` |

> **Re-publish rule**: always overwrite with the existing `appId` — the link must stay `https://ct-samplesize.app.workbuddy.host/`. Never `createNewApp`. After deploy, assert the returned `shareLink` equals the expected URL (see ct-base `references/workbench_ui.md` §13.0 dirty-binding red line). Last republished 2026-09-26 (feedback two-stage fix).

## Language

- **English guide** → [README.md](https://github.com/medstatstar/ct-samplesize/blob/main/README.md) · **中文指南** → [README_zh-CN.md](https://github.com/medstatstar/ct-samplesize/blob/main/README_zh-CN.md)
- Bilingual auto-switch: the answer language follows the user's question language (English question → English answer, Chinese question → Chinese answer).

## Purpose

This skill provides clinical trial researchers with an easy-to-use, comprehensive sample size & power calculation tool. **The default authoritative engine is a remote coze R compute service** (rpact / TrialSize / PowerTOST and 20+ other packages — running server-side, so your machine needs **no local R**), covering all 67 test types. Results come in Chinese or English per the OS language setting (prompt can force-switch). Reproducible R code is returned by default (coze returns it on every analysis).

---

## Features

| Capability | Description | Typical Scenario |
|:---|:---|:---|
| **① Sample size ⇄ Power (bidirectional)** | Solve n given target power, AND solve achievable power given fixed n. `--power` (forward) and `--nobs` (reverse) are mutually exclusive; covers all 67 types. | Sample size fixed, evaluate if power meets target |
| **② Power curve** | Given a sample-size sequence, batch-compute and plot the **Power curve** (x=sample size, y=power), with a target-power reference line. | Sample-size sensitivity analysis, protocol reporting |
| **③ Sample-size curve** | Given a power-target sequence, batch-compute and plot the **sample-size curve** (x=target power, y=required n). | Resource planning, feasibility assessment |
| **④ Deterministic NL pre-route (zero-LLM)** | `--nl "<natural language>"` runs a local zero-LLM deterministic detector that identifies `--test` and extracts params (power 80%→0.8, rate 70%→0.7, "enroll 30"→reverse-solve power, etc.), emitting a strong signal for the coze request; when confidence is low / params incomplete it prints a structured prompt and **never silently mis-params** — the local agent then asks the user for the missing test/params (≤2 rounds, then defaults); **raw NL text is never sent to coze** (the workbench is **deterministic-first** — `classify_test` + `param_aliases`, identical to conversation mode; the LLM fallback in `workbench/nl_llm.py` defaults to the family backend model resolved dynamically from the Feishu configtbl per ct-base §12 (packaged snapshot fallback LongCat-2.5;key via `load_llm_key()`: `LONGCAT_API_KEY` env > obfuscated `config/llm_key.py`; `CTSS_NL_ENDPOINT` overrides to any OpenAI-compatible model) and may only propose a test when rules fail — never override a rule-identified test; the coze compute endpoint has no NL/LLM path). Logic in `scripts/classify_test.py` + `scripts/param_aliases.py`; per-test contract baselines in `tests/coze_cases/` (fixture data), 67-test enumeration in `adapters/coze/coze_contract.md`. | User phrases it colloquially, e.g. "non-inferiority survival trial, NI margin 1.25…" |

- ②③ curve mode: list `"20,40,200"` or auto-seq `"20:20:200"` (start:step:stop); overlay multiple effect-size curves for sensitivity (continuous/survival solvers; proportion solvers plot the single p1/p2 series); returns the figure (SVG default per the ct-* uniform figure spec, PNG fallback) **plus the numeric series as machine-readable stats (x/y arrays)**. Full parameters & 67-test examples → `references/cli_examples.md`.
- **Specialized curve modes (`--effect_seq` / `--dist_plot` / `--power_time_seq` / `--heatmap`, added 2026-08-28):** effect-axis / H0–H1 overlap / follow-up-power / 2-D sensitivity scans for the 9 curve solvers; full parameters & 67-test examples → `references/cli_examples.md`.
- **★ Default figures (v5.6 + 2026-08-28):** when no figure is requested, the R engine auto-attaches the full set for the 9 curve solvers (curves + dist-overlap + heatmap) and the survival follow-up–power curve (`type` field + bilingual `caption`); all figure generation moved to the coze side — coze R (`coze_figure_layer.R`) is the primary plotter, `figure_kit.py` the coze-internal fallback, the local CLI a **thin client** consuming coze-returned `figures[]`. **Zero new R packages**. Opt out via any explicit figure flag / `--dry-run`; see [Default Figures (v5.6)](#default-figures-v56) and `references/default_figures.md`.

---

## Interaction — Triage first

Before answering, triage the request into the four-level difficulty **Simple / Middle / Complex / Vague**:
- **Simple** (test already named, params mostly given) → answer directly, **no menu**.
- **Middle** (single-point but deep — ICH guidance detail, statistical parameter, compliance gray zone, needs 3–4 points) → still answer **directly, no menu** (same path as Simple; mark `difficulty = "middle"` for a richer multi-point answer). When Simple vs Middle is unclear, prefer **Middle**.
- **Complex** (pick test type / design family / many params) → show the **routing menu** below (**the `## Quick Menu` is for the Complex branch only**).
- **Vague** ("not sure which test to use") → **bounded grill-me** (branch-by-branch probing), do **not** dump the menu. **Hard cap: ≤3 rounds** (on reaching the cap with the test still undecided, **converge with the accumulated question profile** — pick the best-fit test family and confirm). Each round ask 1–3 focused questions with a recommended default; accumulate confirmed fields into a **question profile**; when the test is locked, **echo a "needs portrait + recommended test + missing params" summary for confirmation** before computing. (This 3-round cap targets locking the test; the global missing-parameter cap is **2 rounds then use defaults** — different dimensions, no conflict.)

**Routing gate (audit follow-up — avoid accidental remote compute):** a **remote coze compute** (data leaves the machine) happens **only** when the user's intent is explicitly a sample-size / power / curve **calculation**. General consulting — "help me figure out my trial design", methodology questions, ICH guidance, "what test should I use" — must be answered **locally without sending anything**, and may use the menu / grill-me flow. Do not fire a coze request on vague or advisory phrasing; ask for the calculation intent first.

## Cross-turn Continuity (mandatory)

> **Runtime is stateless.** The coze R engine re-supplies `test`+`params` each call and never persists prior fields. Semantic drift (effect/α/power/n silently changing) = highest-risk failure for a stateless remote.

**Hard rules** (full rules below (Cross-turn Continuity); minimal unit = `{test, effect, alpha, power, solve, side, sd}`, `—` = not-yet-known):
1. **Echo a `## 当前分析设定：` block after every calculation (mandatory):** `## 当前分析设定： test=ttest_ind | effect(d)=0.5 | alpha=0.05 | power=0.8 | solve=n | side=two | sd=1.0 | n=— | ratio=—`. No field omitted (`—` placeholder). `solve=n` solves n given power; `solve=power` reverses; `side=two/one_greater/one_less`.
2. **On follow-up, change only the changed fields:** read the most recent `## 当前分析设定：` block, override only the changed field, inherit the rest verbatim, then send to coze.
3. **Deterministic merge (default path, not optional):** every follow-up **MUST run** `merge_spec.py` for a lossless merge, then send the merged spec to coze — never assemble params from LLM memory alone. `echo '{"prev":{...},"cur":{"power":0.9}}' | python scripts/merge_spec.py` (dev: `scripts/merge_spec.py`). If `missing_required` is non-empty, clarify first. (The `compute` payload also carries `resolved_spec`, a full snapshot — additive, landed.)

> Red line: ct-samplesize's coze is a **stateless remote compute**; continuity MUST be solved locally — the remote cannot help unless you actively send history. `merge_spec.py` is the local **deterministic merger** (code-fixed, LLM-executed), not a fragile classifier — upholds family red line 4.

## Batch-call governance (v5.7, must-read)
Mandatory constraints (curve-already-contains-single-point; batch-grid-submit; trim-envelope via `build_params`) + Feishu-backend evidence + outbound envelope guard + local `--batch-file` → `references/batch_calls.md`.

## Request-level log aggregation (v5.15, must-read)
**One user request → as few Feishu rows as possible.** Wrap one user demand in `request_scope()` (CLI `main()` does this automatically); all coze sub-calls then share `request_id`, and the coze `feishu_save` node merges them by `update_records` into one row (`call_count` / `calls[]` / `statuses`). Prefer `call_paired()` (n + achieved power in one POST) and `call_grid()`/`call_batch()` (parameter sweep in one POST) over N serial calls. `call()` also de-duplicates identical successful signatures within 60 s locally (no POST, no new row) and rejects out-of-domain params before any network round-trip. Old clients without `request_id` keep the legacy one-POST-one-row behaviour. Contract: one generated artifact per deploy unit — local client reads `config/log_contract.json`, workbench reads its own `workbench/publish/config/log_contract.json`, coze runtime imports the baked-in constant module `src/graphs/nodes/log_contract_data.py` (no path probing, no defensive duplicates; regenerate all via `scripts/build_log_contract.py`). Capability discovery: `scripts/route_intent.py`. Details → `references/request_log_aggregation.md`.

## Quick Menu — two-level routing (level-1 only here; level-2 in `references/menu.md`)

> Authoritative layered menu: [`references/menu.md`](references/menu.md) · CLI examples & bidirectional solve: [`references/cli_examples.md`](references/cli_examples.md) · Operation SOP: [`references/operation_sop.md`](references/operation_sop.md).
>
> **Two-level routing rule (per Type-Compute, do NOT dump the full test list):** on a Complex request, first show **only this level-1 summary** (7 endpoint categories + high-frequency design families). After the user picks a category, go to `references/menu.md` **Part 1** for that category and show the **level-2 sub-list** (the specific `--test` options). Never present all ~67 tests in one screen.

**Level 1 — endpoint categories:**
- ① **Continuous** (means) · ② **Binary / Proportions** (rates, OR/RR, NI/BE) · ③ **Count / Rates** (Poisson) · ④ **Survival / Time-to-event** (logrank, HR, one-sample) · ⑤ **Diagnostic / Method comparison** (ROC, Bland-Altman) · ⑥ **Special / Advanced designs** (group-sequential, adaptive, Bayesian, MAMS, win-ratio, cluster …)

**Level 1 — high-frequency design-family entries** (non-exclusive; full list in `references/menu.md` Part 2): Group-Sequential · Adaptive · Equivalence / Non-inferiority / BE · Bayesian · Dose-escalation · MAMS · Historical control · Vaccine · Win-statistics · Cluster / Multiple endpoints

> ③ **Can't decide?** → say "explain the differences between these choices in detail", and I'll clarify the clinical/statistical meaning before you choose. (Family-standard wording, verbatim.)

> The menu is a *navigation aid*, not a strict taxonomy: the same test is reachable from multiple categories (e.g. `gsd_survival` from both ④ Survival and the Group-Sequential index). Still unsure where to start? Use **Part 0** in `references/menu.md` — find your test by *research question*, no jargon needed.

**Advanced:** `--test adaptive_simulate` empirically validates adaptive / group-sequential designs (power, type I error, expected N) — full guide → [`references/adaptive_simulator.md`](references/adaptive_simulator.md). `--verify` (default OFF) re-simulates an **analytic** solution with an **independent** Monte-Carlo engine (checks empirical power ±2 pp / type-I error ±0.5 pp; takes only the n as input, so a wrongly-derived n is caught) — supports `ttest_* / proportion_two / survival(log-rank) / group_sequential / adaptive_reestimate`; reports MC 95% CI, returns `INCONCLUSIVE` rather than a false PASS. Pure local, no network. `--audit` (added 2026-09-29, planning layer) grades every design assumption **known / weak / unknown / missing** (with fabrication-signature heuristics + `--evidence-source` promotion), maps the test into 7 design-logic families with self-consistency checks, and emits **fallback/contingency plans** per weakest assumption; exits without computing; complements (not replaces) `--show-assumptions`. Pure local (`scripts/hypothesis_audit.py`). `--mcid Δ --sd S [--mcid-source …]` (J1) is a clinically-worded alias of the Δ/sd conversion channel (d = MCID/SD, echo + audit linkage); `--justify` (J2) appends an **IRB/SAP-ready bilingual justification paragraph** — hidden by default: the paragraph text renders software as `R <ver> + rpact/TrialSize <ver>` (versions from the result envelope; no cloud/local wording; unknown versions render as fill-in placeholders), and after a successful single computation the CLI prints a one-line offer — **when you see that offer, ask the user whether they want the document paragraph; generate it only on their yes (re-run with `--justify`)**. Skeleton = CONSORT-SPIRIT Item14/DELTA2 Box4 + CDE《样本量估计指导原则(试行)》2024-12-23; placeholders must be filled by the investigator — anti fake-precision. Details → [`references/justification_templates.md`](references/justification_templates.md). Pure local (`scripts/justify_text.py`).

---

## Requirements

| Requirement | Details |
|:---|:---|
| **coze compute endpoint** | **Production default.** Set `CTSS_COZE_ENDPOINT` (or `COZE_ENDPOINT`) to the coze R service; covers all 67 tests. For a no-network demo, set `CTSS_COZE_MOCK=1`. |
| **Python** | ≥ 3.8, **stdlib only** (argparse / json / urllib). The v5 refactor removed the local pure-Python fallback and all third-party compute deps (statsmodels / numpy / scipy are no longer required). No local R required. |
| **R (dev / optional)** | **Not shipped in the published skill.** The coze R engine source is maintained in the coze-synced backend directory (excluded from the publish package). The legacy local-R backend and R templates are kept for offline dev / contribution only — **the v5 `select_backend` no longer routes to them**; they are not part of the published skill. |

---

## ⚠️ Safety

- **No local R / shell is ever executed.** The published skill never runs R or a shell on your machine. The default engine is the remote **coze** compute service: only trial-design parameters (never patient data) are sent, and results come back as numbers + optional figures — inherently safe (stateless compute, no local code execution).
- **SAFE PREVIEW is the default for inspection.** `--dry-run` prints the exact request envelope (test, params, mode) that *would* be sent to coze, without sending anything. `--show-code` reveals the coze request JSON (the R source coze used is included in every result by default). The legacy `--yes` gate applies only to the optional local-R dev backend (offline dev only).
- **First-use outbound disclosure (audit follow-up):** even though the public coze endpoint is pre-whitelisted (never prompts), the assistant MUST state on first outbound use in a session — in one line: "This will send your trial-design parameters plus a hostname hash (query_origin), your skill version (skill_version) and locale to the cloud service https://ct-samplesize.coze.site/run for computation — proceed?" (localized zh version in `references/security_model.md`). Custom endpoints still trigger the one-time AUTH-BLOCK confirmation. **Output for reference only; validate before regulatory submissions.**

### Security model (transparent disclosure)

> Full disclosure table (remote compute / server-side R / output / network / outbound gate / filesystem), upload confidentiality, and the natural-language outbound guidance → [`references/security_model.md`](references/security_model.md). Key guarantees: no local R/shell; SAFE PREVIEW default; only trial-design parameters ever leave the machine.

---

## User-Uploaded Documents

This skill is **parameter-driven** (design params via CLI / natural language). When the user uploads a document (protocol / SAP / design brief as `.docx` / `.pptx` / `.pdf` / `.doc`), **convert it to md/text first**, then extract the design parameters — the coze endpoint is a plain-text JSON contract and does **not** accept attachments. Converter: shared **`scripts/office_to_md.py`** (stdlib-only, single parser for docx+pptx):

| Uploaded format | Handling |
|---|---|
| `.docx` / `.pptx` | `python scripts/office_to_md.py <file>` → md (pptx sectioned by `### Slide N`) |
| `.pdf` / `.doc` / scanned | env `pdf` skill (OCR prompt) / word-reader / text-version prompt — never hand-write a parser |

**🔔 User notice before ANY conversion (show this exact notice first):**
> ⚠️ Every uploaded document is converted to **md** for processing; **PPT conversion tends to lose substantial information** (images, layout, animations, charts, and other non-text elements). We recommend you **convert to md and review the content yourself** before asking, so key details are not lost.

**Confidentiality:** the skill does **not** judge data confidentiality — the document is converted as-is; **only the extracted design parameters** (test, effect, α, power, n …) are ever sent to coze; the raw document md is used **locally for parameter extraction only** and never forwarded. If the user requires data-not-leaving, guide them to keep computation fully local (extract params and compute manually, or use the offline dev backend) — never send document content to coze.

---

## Implementation

**Bidirectional solve:** `--power` (default) solves required `n` given target power; `--nobs N` reverses to achievable power given fixed `n` (mutually exclusive, `--nobs` wins). Default = **SAFE PREVIEW**: `--dry-run` prints the coze request envelope without sending; `--show-code` reveals it (and, with `CTSS_RETURN_R_CODE=1`, the R source coze used); no `--yes` needed for coze (stateless remote compute). Full CLI examples (all 67 tests, reverse-solve, curve mode) → `references/cli_examples.md`; data format → `references/data_format_guide.md`.

**Common params:** `--side one|two` (default `two`, test direction); `--sd FLOAT` (optional, auto-computes Cohen's d = Δ/sd; omitted ⇒ `--effect` is d directly).

**Curve mode:** `--n_seq`/`--power_seq`/`--plot_effects`/`--effect_seq`/`--dist_plot`/`--power_time_seq`/`--heatmap` — see Features. **11 tests support curves** (`.curve_solvers`: ttest_ind/paired/one, anova, proportion_one/two, survival, equivalence, be_tost, wilcoxon, wilcoxon_signed_rank); `--dist_plot` covers `ttest*/proportion*/survival`; `--power_time_seq` survival-only; others return "curve not supported".

> **Architecture & security:** orchestration (`scripts/samplesize_power.py`) contains **no R code**; `ComputeBackend` (`scripts/compute_backend.py`) routes to `CozeBackend` (default authoritative, server-side R) — the only backend in v5. All R logic lives in the coze-synced, publish-excluded backend directory. Every user string reaching server-side R is validated against a strict allowlist. History → `CHANGELOG.md`.

### Workbench

A local web UI covering the full flow "input → results → figure-option control → follow-up questions": `workbench/` (backend `server.py` is a stdlib-only `http.server`, frontend `workbench.html` is a single zero-dependency file). The form schema is reflected at runtime from argparse + `_contract_index.json` (67 tests / 210 CLI params, zero-maintenance); follow-up questions reuse the deterministic merge (`merge_spec`). Launch defaults to the **live coze endpoint** (not MOCK — MOCK returns fake results). On Windows hosts with a stale system `HTTP(S)_PROXY` in the registry, strip the proxy env (`HTTPS_PROXY= HTTP_PROXY= ... NO_PROXY=*`) or urllib cannot reach coze. See `workbench/README.md` for the exact launch command and endpoints.

**Standard inspection process (mandatory release gate):** any change to `workbench.html` / `server.py` / `form_schema.py` / `tokens.css` / `wb-list.css` / `wb-list.js`, and **every** `build_publish.py` / `install_genie.py` run, must pass the 5-layer automated suite (`workbench/autotest/`, 110 cases, ~70s) first — **all layers green (0 failed / 0 error) is the publish criterion**. The suite covers static contract, backend API, in-browser behavior, end-to-end flow, and layout/a11y; it does **not** enter the workbench publish bundle (whitelist-built). Canonical spec → `references/workbench_qa.md` (zh: `references/workbench_qa_zh-CN.md`).

---

## Figure Output & Rendering

All figures follow the **uniform SVG spec shared across the ct-* family** (same pipeline as `meta-analysis`). The coze endpoint emits all figures; the conversation stream does **NOT** inline SVGs — presentation is delegated to the local HTML aggregated report (`render_html_report`, stats + SVGs + R script). No hand-redraw. Details → [`references/rendering_rules.md`](references/rendering_rules.md). **Default Figures (v5.6):** every method produces ≥1 figure, all on the coze side (8 default kinds, effect ±20 % sensitivity band, zero new R packages). The local allocation-ratio filter (v5.7.1) shows `alloc_suite` only when `--ratio != 1`. Full spec → [`references/default_figures.md`](references/default_figures.md).

---

## Formulas, Reports & Errors

**Formulas:** `references/formulas.md` (all 67 types, incl. independent t / Schoenfeld survival / Cox-with-covariate / Cluster DEFF) | **Full functions:** `references/extended_functions.md` | **Common error:** coze endpoint not configured → set `CTSS_COZE_ENDPOINT` (real) or `CTSS_COZE_MOCK=1` (demo)

---

## External-Control / RWD-Augmented Designs · Distributional Balancing (2026-10-19)

> Maps to the 2026-10-19 intelligence round (P2 improvement; evidence: Zern Ke, Cui M, Moran G, Cabrera J. *Distributional Balancing with Machine Learning for Clinical Trial Augmentation Using Real-World Data*. arXiv:2609.23524, 2026-09-20 — see the `ct-base/references/qc_independence_pharmasug2026.md` family).

- **When to use**: covariate balance from randomized assignment is hard to achieve due to recruitment cost / dropout, and control patients must be borrowed from an external real-world database (RWD) — external control-arm trials, mixed control, RWD-augmented control.
- **DBML three-step method**: ① a variational autoencoder (VAE) flags **RWD units that are outliers relative to the treated-arm distribution**; ② the remaining units are **reweighted** so the candidate-control distribution matches the treated-arm distribution (matching distributions, not unit pairs); ③ sample the control arm by weight. Empirically covariate balance beats matching- and weighting-class baselines.
- **Reporting obligation (hard requirement on ct-samplesize output)**: when an RWD-augmented control is used, besides the sample-size statement you **must report covariate-balance metrics** (e.g. the SMD distribution / max standardized mean difference). Reporting only "borrowed N RWD controls = nominal sample size" is forbidden — unquantified balance means the design is undefined.
- **Relation to existing capability**: Bayesian external-control single-arm inference (reliability under transportability violation, Stat Med 2026, DOI `10.1002/sim.70748`) can serve as the inference layer after DBML sampling; this item only registers the method and reporting discipline — the engine is unchanged.

---

## ct-base §22 Alignment — AI-Generated Asset Governance (2026-10-19 intelligence round)

ct-samplesize's AI-generated assets = **SVG statistical figures** (coze `coze_figure_layer.R`) + **reproducible R code** returned on every analysis. Applicable ct-base §22 obligations and current status:

- **§22.1 P0·a "ambiguity → stop" HITL gate**: enforced — the deterministic NL pre-route (`classify_test` + `param_aliases`) never silently mis-params; low-confidence paths ask the user (≤2 rounds), raw NL text is never sent to coze (see Capability ④).
- **§22.2 P0·b deterministic generation + fixed seed**: planned — coze R plotting should pin a fixed seed for byte-identical SVG across runs; not yet enforced at the engine layer.
- **§22.3 P1·a three-layer compliance + LINEAGE + reproducibility**: partially met — every analysis returns full reproducible R code (LINEAGE by construction); output-figure lineage not yet separately logged.
- **§22.18 P1·i spec AI-readiness Gate**: planned — no formal six-item readiness gate before figure/code generation; acknowledged as a compute-only skill but should be documented.
- **§22.19 P0·f "reading the answer = leak" veto**: N/A by design — ct-samplesize generates from user-supplied design parameters only; it never references an answer/target dataset (no synthetic-ADSL reverse-derivation path exists).
- Engine-layer hardening (§22.10–§22.17 independent-QC family) tracked as planned in CHANGELOG; this section is the normative-layer alignment only.

---

- **Upstream (context)**: `ct-registry` (via `ct-pipeline` public-intel orchestration) · **Downstream**: `ct-protocol` (protocol skeleton) → `ct-ecrf` (CRF + SDTM mapping spec) · **Same category (design)**: `ct-protocol` / `ct-ecrf` / `ct-eligibility` · **Public-intel (Tier B)**: `ct-pipeline` (dispatches `ct-registry` / `ct-safety` / `ct-literature`)
