# Capability Units

> Schema: Input / Output / Dependencies / AI autonomy / Composition interface
> Designed per ct-base `BASE.md` §6. AI autonomy: 🟢 fully automatic (default execute) / 🟨 semi-automatic (confirmation required) / ⬜ assistive. (🟡 = confirm only on a specific trigger, e.g. detail >100 items.)

---

## U1: search_ctgov / CT.gov search

- Input: search criteria (disease `cond` / intervention `intr` / sponsor `sponsor` / status `status`, at least one required)
- Output: `{"source":"CTGOV","records":[raw study]}` JSON
- Depends on: none (entry)
- AI autonomy: 🟨 semi-automatic (confirm query criteria)
- Composition interface: → U6

## U2: External-workflow & China sources (CDE / ChiCTR / ISRCTN / DRKS / WHO ICTRP)

> Architecture (2026-07-24, revised 2026-08-13): **The skill's own direct-retrieval scripts avoid browser automation (Tier 1 is pure HTTP).** However, browser use DOES occur in two places, so "no browser" is not a blanket guarantee: (a) the **unified third-party endpoint (Tier 2) performs Playwright/headless-Chromium server-side** on our behalf — that automation runs at the vendor, not locally; (b) the **CDE paste-mode local fallback (`parse_cde.py`) uses Playwright locally** when the user pastes a CDE page. Chinese registries (CDE, ChiCTR) and WebForms portals uniformly block *automated* browsers via WAF fingerprint checks, which is why direct browser scraping from this skill is avoided in favour of the workflow. Sources split into two tiers:
> - **Tier 1 (direct, pure HTTP):** CT.gov v2 REST API, EU CTR legacy EudraCT HTML parse
>   (`search_eu_ctr.py`), PubChem PUG-REST. No token, no browser.
> - **Tier 2 (external workflow, Bearer token):** a third-party endpoint retrieves on our behalf
>   and returns JSON. Shared client `extsvc_client.py`; thin wrappers `CDE/search_cde_workflow.py` (archived) /
>   `search_chictr.py` / `search_isrctn.py` / `search_drks.py` reuse it. **Only public query
>   terms leave the environment** — compliant with the ct-base red line.
> - **WHO ICTRP is a Tier-2 external service (re-added 2026-07-27).** Its portal is an ASP.NET
>   WebForms mirror with no clean API, but a dedicated external workflow now exposes a clean JSON
>   API (`source="who"`) — reachable without a browser. One call mirrors 14+ primary registries
>   (jRCT, DRKS, ANZCTR, ISRCTN, CTRI, …), expanding coverage. Its bridge + de-dup value is
>   reinforced (not replaced) by `aggregate.py` (UTN/TRN normalization + fuzzy matching + raw
>   scan, CT.gov canonical). See **U2c**.

### U2a: search_cde / China CDE (药物临床试验登记与信息公示平台)

> SafeDog WAF blocks even headless Chrome (verified). The **recommended automatable path**
> is the external workflow via the **unified endpoint** `search_ictrp.py --source chinadrugtrials`
> (`ct-search.coze.site/run`). The legacy standalone `CDE/search_cde_workflow.py` (original spec
> `ct-searchcde.coze.site/run`, archived under `CDE/`, NOT shipped) is **RETIRED 2026-08-12**
> (an alternative `h2ybbswdjq.coze.site/run` also existed): sends only public query terms, returns JSON. Paste-mode local
> parse stays a no-egress fallback. Egress note: only public query terms leave
> the environment; no confidential subject / protocol / CRF data — compliant with the ct-base red
> line.
>
> Auth (verified 2026-07-22 with a live token):
> - HTTP 401 = missing / malformed `Authorization` header (needs exactly `Bearer <token>`).
> - HTTP 403 = token rejected (corrupted / revoked / invalid) — **re-issue only if it recurs**; the
>   localized token is long-lived and normally never 403s. Token *type* is not the blocker.
> - HTTP 500 = payload schema error: a search field sent as `{"value": x}` (must be a plain
>   string) or Need-B `project_list` sent as a JSON array (must be a JSON **string**).
>
> **Workflow-side status (updated 2026-07-23):**
> - **Need A search: FIXED & VERIFIED** — `keyword=678` (2026-07-23) returned HTTP 200 with
>   `total_count=56`; the earlier "0 results" issue is resolved on the workflow side.
> - **Need B detail browser: FIXED & VERIFIED** — a live client call (2026-07-23,
>   `mode=detail` on 3 real project_ids) returned HTTP 200, `error_msg=None`, and **full detail
>   data (50+ fields per record)**. The prior "无法启动浏览器" failure is resolved; Playwright
>   Chromium is confirmed working.
> - **Coze gateway 503** (2026-07-22) was transient and recovered; the token is **localized and
>   long-lived (does NOT expire)** — no freshness concern. Only a rare 403 (corrupted/revoked blob)
>   warrants a `--store-token` re-store.

> **Mode routing (4 calling modes, all VERIFIED 2026-07-23):** `search` (default keyword OR
> advanced field-filtered), `combined` (keyword global search + advanced filters), `multi_keyword`
> (space-separated AND of keywords; endpoint echoes them back as `keywords`), and `detail`
> (project list → parallel detail fetch). Search-field shape: all 11 fields are **plain strings**;
> OMIT unused; `drugs_type` / `trial_status` use the enum values. `is_advanced_search` is auto-set in
> `search` mode when a filter field is present; ignored by `combined` / `multi_keyword`.

#### U2a-1: CDE list search (Need A — keyword / advanced → project list)
- Input: `mode="search"` (REQUIRED) + free-text `keyword` (default) **or** structured filters
  (`reg_no` / `indication` / `case_no` / `drugs_name` / `drugs_type` / `appliers` /
  `communities` / `researchers` / `agencies` / `trial_status`). All 11 fields are **plain
  strings** (the contract labels them "object", but the endpoint requires plain strings —
  verified by the 2026-07-23 `keyword=678` -> 56-record success). **OMIT unused fields** — never
  send `""`. Enum constraints: `drugs_type` ∈ {中药/天然药物/化学药物/生物制品};
  `trial_status` ∈ {进行中/尚未招募/招募中/招募完成/已完成/主动暂停/主动终止/IEC/IRB暂停/
  IEC/IRB终止/责令暂停/责令终止} (11 values, full).
  Advanced-search form: `https://www.chinadrugtrials.org.cn/clinicaltrials.prosearch.dhtml?pro=y`.
- Output: `{"source":"CDE","need":"search","total_count":N,"records":[trials],"project_list_raw":"<json string>"}`
  JSON. `project_list_raw` is preserved so it can be fed verbatim into U2a-2.   An `error_msg`
  (string) field is present when the workflow reports a failure.

  Example (advanced multi-filter — VERIFIED contract shape; empty fields are OMITTED by the
  script, not sent as `""`):
  ```json
  {
    "mode": "search",
    "indication": "非小细胞肺癌",
    "drugs_name": "帕博利珠单抗",
    "drugs_type": "化学药物",
    "appliers": "默沙东",
    "researchers": "张三",
    "trial_status": "进行中"
  }
  ```
- Depends on: none (entry)
- AI autonomy: 🟢 automatic (default execute) — auto-map from the user's words and run `--run` directly; report the result.
- Composition interface: → U6 (or → U2a-2 to fetch details)

#### U2a-2: CDE parallel detail fetch (Need B — project list → details)
- Input: `mode="detail"` + `project_list` = **STRING-typed field** (JSON serialized as a string,
  not a bare object/array in the body). The string CONTENT accepts two forms, both auto-parsed
  for `project_id`:
  1. Search response's `project_list` **verbatim** (preferred) — wrapped object string
     `{"total_count":N,"total_pages":M,"projects":[{project_id,...}]}`; the script extracts this
     automatically when you pass `--project-list <U2a-1 output file>`.
  2. Plain array string `[{project_id,...}, ...]` (hand-written also works).
  The node parses each object's `project_id` and fetches 8-thread parallel.

  Example (detail — `project_list` is a STRING; content may be a plain array or the search
  wrapped object):
  ```json
  {
    "mode": "detail",
    "project_list": "[{\"project_id\":\"1f60c09c-87ca-4747-a4f1-394a8b2e6d3b\",\"登记号\":\"CTR20250068\",\"药物名称\":\"XXX\",\"适应症\":\"YYY\",\"试验状态\":\"进行中\",\"试验通俗题目\":\"ZZZ\"}]"
  }
  ```
- Output: `{"source":"CDE","need":"detail","records":[trial details],"scraped_data_json":"<json string>"}` JSON.
- Depends on: none (entry); typically fed by U2a-1's list.
- AI autonomy: 🟢 automatic (default execute) — run by default; **confirm with the user ONLY if the
  project list has >100 items** (8-thread parallel fetch is time-consuming). For ≤100 items, no
  confirmation needed.
- Composition interface: → U6

#### U2a-3: CDE combined list search (keyword + advanced filters)
- Input: `mode="combined"` + `keyword` (global substring on reg-no + drug name) **and** any
  advanced filter field(s) (`reg_no` / `indication` / `case_no` / `drugs_name` / `drugs_type` /
  `appliers` / `communities` / `researchers` / `agencies` / `trial_status`). `is_advanced_search`
  is ignored (combined always applies the filters). All fields plain strings; OMIT unused; enum
  constraints as in U2a-1.
- Output: same shape as U2a-1 (`total_count` / `total_pages` / `records` / `project_list_raw`),
  consumable directly by U6 or chained into U2a-2 for detail.
- Example (VERIFIED 2026-07-23: keyword=678 + trial_status=已完成 → 29 records):
  ```json
  {
    "mode": "combined",
    "keyword": "678",
    "trial_status": "已完成"
  }
  ```
- Depends on: none (entry)
- AI autonomy: 🟢 automatic (default execute) — auto-map from the user's words and run `--run` directly; report the result.
- Composition interface: → U6 (or → U2a-2 to fetch details)

#### U2a-4: CDE multi_keyword list search (space-separated AND)
- Input: `mode="multi_keyword"` + `multi_keywords` (space-separated string, e.g. `"高血压 糖尿病"`).
  The workflow full-searches the first term, then intersects with the rest (logical AND). The
  endpoint echoes the supplied list back as `keywords` and returns `keyword_stats` (per-keyword
  `{total_results, total_pages}` — VERIFIED 2026-07-23 fix, previously always null) in the response.
- Output: same shape as U2a-1, plus `keywords` (the supplied list) surfaced when present.
  Consumable directly by U6 or chained into U2a-2 for detail.
- Example (VERIFIED 2026-07-23: 高血压 糖尿病 → 166; 阿司匹林 高血压 已完成 → 28; BMI 肥胖 → 17):
  ```json
  {
    "mode": "multi_keyword",
    "multi_keywords": "高血压 糖尿病"
  }
  ```
- Depends on: none (entry)
- AI autonomy: 🟢 automatic (default execute).
- Composition interface: → U6 (or → U2a-2 to fetch details)

### U2b: search_chictr / China ChiCTR
- Input: Chinese drug name / disease / registration number (`--q`)
- Output: `{"source":"CHICTR","records":[trials]}` JSON
- Depends on: none (entry)
- AI autonomy: 🟨 semi-automatic (confirm); preview-only by default (no network)
- Composition interface: → U6
- Note: WAF blocks headless browsers → **Tier-2 external workflow** (`search_chictr.py` →
  `search_ictrp.py --source chictr`, unified Coze endpoint `https://ct-search.coze.site/run`,
  shared ICTRP token, v0.3.30+ 已接管). Leans toward investigator-initiated trials,
  cross-validates CDE. No PLACEHOLDER; no Playwright.

## U2c: search_ictrp / WHO ICTRP (Tier 2, external workflow)

- Input: condition keyword / advanced WHO fields (`who_condition`, `who_intervention`,
  `who_sponsor`, `who_country`, `who_phase`, `who_recruitment_status`, booleans for
  COVID-19 / with-results / rare-diseases / gene-editing); mode `search` / `combined` /
  `multi_keyword` / `detail`.
- Output: `{"source":"ICTRP","records":[trials]}` JSON (project_list parsed from a JSON string).
- Depends on: none (entry).
- AI autonomy: 🟨 semi-automatic (confirm).
- Composition interface: → U6.
- Note: WHO ICTRP portal is WebForms (no clean API) → routed through the consolidated Coze
  external-workflow endpoint `https://ct-search.coze.site/run` (`source="who"`), Bearer token.
  Re-added 2026-07-27. One call mirrors 14+ registries (jRCT / DRKS / ANZCTR / ISRCTN / CTRI /
  TCTR / PACTR / IRCT / SLCTR / …) that we do NOT directly connect to — the cheapest way to widen
  coverage. Records feed `aggregate.py`, which bridges on embedded registration numbers (NCT /
  JPRN / CTRI / …) found in the `raw` field. The localized Coze workload-identity JWT is
  **long-lived (does NOT expire)** and normally never 403s; only a rare 403 (corrupted/revoked blob)
  warrants re-issue via `search_ictrp.py --store-token "<new-jwt>"`.
- **`who_phase` caveat (verified 2026-07-30):** `--who-phase` IS honored server-side (live test:
  `Olverembatinib` keyword-only → 41; `+who_phase "Phase 1,Phase 2"` → 2). But the WHO portal's
  Phases dropdown filters on a *normalized* phase field that **under-captures combined/numeric
  phases** (the full I/II set still returned only 2, vs ~19 true I/II from detail-derived phases).
  So `--who-phase` is a **coarse narrowing only**; the authoritative I/II gate is the post-hoc
  detail-phase filter in `normalize.py` → `phase`. Never drop records solely on `who_phase` exclusion.

## U3: search_eu_ctr / EU CTR search (Tier 1, direct)

- Input: keyword `--q` (EudraCT search); optional `--max`
- Output: `{"source":"EUCTR","records":[trials]}` JSON
- Depends on: none (entry)
- AI autonomy: 🟢 automatic (default execute; pure HTTP, no token)
- Composition interface: → U6
- Note: **Tier-1 direct-connect** — parses the legacy EudraCT search-result HTML directly
  (`search_eu_ctr.py`, no browser). Verified 2026-07-24: 20 hits parse cleanly (EudraCT no. /
  title / condition / sponsor / start date). The new EU CTIS `retrieve/{ct_number}` API is
  retrieve-by-number only (no search) and is out of scope for keyword search.

## U4: search_isrctn / ISRCTN search (Tier 2, external workflow)

- Input: keyword `--q`
- Output: `{"source":"ISRCTN","records":[trials]}` JSON
- Depends on: none (entry)
- AI autonomy: 🟨 semi-automatic (confirm); preview-only by default (no network)
- Composition interface: → U6
- Note: 🔴 Public search API is dead (all `/api/query*` endpoints 404, tested 2026-07-20) →
  **Tier-2 external workflow** (`search_isrctn.py` → `search_ictrp.py --source isrctn`, unified
  Coze endpoint `https://ct-search.coze.site/run`, shared ICTRP token, v0.3.30+ 已接管). No
  PLACEHOLDER; no Playwright.

## U4b: search_drks / DRKS (German registry, Tier 2, external workflow)

- Input: keyword `--q`
- Output: `{"source":"DRKS","records":[trials]}` JSON
- Depends on: none (entry)
- AI autonomy: 🟨 semi-automatic (confirm); preview-only by default (no network)
- Composition interface: → U6
- Note: DRKS search is JS/redirect-only (form action missing, POST 307, OAI timeout) →
  unreachable by pure HTTP → **Tier-2 external workflow** (`search_drks.py` →
  `search_ictrp.py --source drks`, unified Coze endpoint `https://ct-search.coze.site/run`,
  shared ICTRP token, v0.3.30+ 已接管). No PLACEHOLDER; no Playwright.

## U5: enrich_pubchem / drug→target mapping

- Input: drug name list `drug`
- Output: `{"source":"PUBCHEM","records":[{drug, cid, props, targets}]}` JSON
- Depends on: none (entry / assistive)
- AI autonomy: ⬜ assistive
- Composition interface: → U6 / U7
- Note: Optional. PUG-REST fetches CID / properties / target genes.

## U2f: detail & document enrichment (post-fetch, pre-normalize)

> Runs only when `ct_registry.py --with-detail` is set. Two independent enrichments, both
> graceful (failure → records keep `documents: []` and list-level summary fields):

### U2f-1: CDE structured detail (Need B — project_list → 65-field detail)
- Input: CDE **list** output (`cde.json`) carrying `project_list_raw` / `project_id`s.
- Mechanism: `CDE/search_cde_workflow.py mode=detail --project-list <list>` (parallel 8-thread
  fetch of full records). `ct_registry.py` swaps the `--cde` path to `cde_detail.json` when
  detail succeeds, so U6 `norm_cde` consumes **detail shape** (sponsor / phase / 入排标准 /
  终点指标 / 实际入组总人数 all populated; `&nbsp;` HTML entities cleaned via `_clean()`).
- Output: `cde_detail.json` (detail-shaped records).
- **Caveat (verified against `cde_detail.json`): CDE detail returns ZERO attachment/PDF URLs** —
  the protocol ("方案") appears as structured **text** (试验方案编号 / 入选标准 / 排除标准 /
  试验药 / 对照药 / 主要终点指标 / 实际入组总人数), NOT a downloadable file. So CDE PDF
  auto-download is **impossible** via automation (SafeDog WAF); only the public detail page is
  reachable, and `report.py` prints a manual-download note for every CDE record.
- AI autonomy: 🟡 confirm-gated on **>100 items** (detail fetch is slow; skip with a warning
  above that threshold).

### U2f-2: EU-CTR document links (CTIS retrieve API)
- Input: EU-CTR list output (`euctr.json`) carrying `ctNumber`s.
- Mechanism: `fetch_eu_ctr_docs.py --run` recursively scans the CTIS `retrieve/{ctNumber}`
  response and extracts `{title, type, url}` document entries into each record's `documents`.
- Output: `euctr_docs.json` (records with `documents` populated where the CTIS API exposes
  download URLs). `ct_registry.py` swaps `--euctr` to this file on success.
- Caveat: best-effort; legacy EudraCT numbers may need mapping to CTIS numbers, some documents
  may be redacted or behind auth. Degrades gracefully to `documents: []`.

### U2f-3: confirm-gated document download (utility, not a fetch unit)
- Tool: `download_docs.py`. By default it **PREVIEWs** every downloadable link found across
  normalized records (`documents` entries). Actual download requires `--yes` (explicit user
  confirmation) → writes files into `--out-dir` with retries, skipping existing files.
- Invoked by `ct_registry.py --download-docs` (the flag itself is the confirmation gate).
- AI autonomy: 🟨 semi-automatic — listing is automatic, downloading is confirmation-gated.
- Composition interface: consumes U6-normalized `documents`; NOT chained into U7.

## U6: normalize / unified normalization

- Input: raw JSON from each source in U1–U2f, U3, U4, U5 (any or all)
- Output: unified trial schema list `[{source, registry_id, title, status, phase, conditions, interventions, sponsor, dates, countries, enrollment, drug, url, documents}]`
  — `url` is the registry homepage/detail link; `documents` is a list of `{title, type, url}`
  (default `[]`; populated by U2f-2 for EU-CTR, always empty for CDE).
- Depends on: U1, U2, U3, U4, U5, U2f (any or all)
- AI autonomy: ⬛ fully automatic
- Composition interface: → U7

## U7: aggregate / analytical aggregation

- Input: U6 normalized list
- Output: aggregation structure `{phase_dist, status_dist, top_sponsors, timeline, competitor_map}`
- Depends on: U6
- AI autonomy: ⬛ fully automatic
- Composition interface: → U8

## U8: report / report output

- Input: U7 aggregation result
- Output: Markdown report (primary) + JSON (optional) + PNG charts (optional, matplotlib)
- Depends on: U7
- AI autonomy: 🟨 semi-automatic (confirm output format)
- Composition interface: → `ct-pipeline` / `ct-protocol` (chained call)

## U9: ct_registry / cross-source orchestrator

- Input: CT.gov criteria (`cond`/`intr`/`sponsor`/`status`, at least one) + optional `--with-cde`
  (CDE `--cde-keyword` / `--cde-multi-keywords` / `--cde-mode` / advanced field flags) + optional
  `--with-pubchem` (`--drug`).
- Output: `out-dir/{ctgov,cde,normalized,agg,agg_full,report}.json|md` — a **single merged
  landscape** across all enabled sources.
- Depends on: U1 (CT.gov) + U2a (CDE, opt-in via `--with-cde`) + U5 (PubChem, opt-in) → U6 → U7 → U8.
- AI autonomy: 🟢 automatic when actually run (default = preview-only); CDE retrieval failure
  degrades gracefully to CT.gov-only (no crash).
- Note (2026-07-23): the top-level one-shot entry point that makes "cross-source" real. `--with-cde`
  invokes `CDE/search_cde_workflow.py` (external workflow, archived) and folds the CDE result into the SAME
  unified schema as CT.gov via U6, so both land in one landscape. Verified: CT.gov 20 + CDE 2057
  → 2077 normalized records in one `status` distribution.

---

## Pipeline

```
input → [U1 ∥ U2a ∥ U2b ∥ U2c ∥ U3 ∥ U4 ∥ U4b] → U5(optional) → U6 → U7 → U8 → output
                                               └─→ ct-pipeline / ct-protocol
```

> The symbol `∥` means multi-source parallel fetching. CT.gov (U1) is the default required
> Tier-1 direct source; EU CTR (U3) and PubChem (U5) are Tier-1 direct; CDE (U2a) / ChiCTR
> (U2b) / WHO ICTRP (U2c) / ISRCTN (U4) / DRKS (U4b) are Tier-2 external-workflow sources
> (Bearer token, no browser). WHO ICTRP (U2c) mirrors 14+ registries per call, so it is the
> cheapest way to widen the landscape; its bridge/de-dup role is reinforced by U6
> (`aggregate.py`).
