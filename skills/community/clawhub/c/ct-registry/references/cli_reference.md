# Implementation — CLI reference

> **English-only agent-facing reference.** SKILL.md keeps only the overview; all CLI recipes,
> advanced-field tables, and runtime behaviour live here.

## Direct-connect sources

```bash
# 1) CT.gov search (required, official API)
python scripts/search_ctgov.py --cond "non-small cell lung cancer" --status RECRUITING --max 50 --out ctgov.json

# 2) CDE — external workflow (ARCHIVED LEGACY path; third-party; Bearer token required)
#    NOTE: the standalone CDE endpoint is retired. Production uses the unified endpoint
#    (search_ictrp.py --source chinadrugtrials). This workflow is preserved only under CDE/
#    for local reference only (the `--cde-legacy` switch is now a no-op warning that auto-routes to the unified endpoint). NOT shipped with the package.
#    Need A · default keyword search -> project list  (mode=search is auto-set)
python CDE/search_cde_workflow.py --keyword "奥希替尼" --run --out cde_list.json
#    Need A · advanced search (structured filters; drugs_type / trial_status use the enum values)
python CDE/search_cde_workflow.py --drugs-name "帕博利珠单抗" --indication "非小细胞肺癌" --drugs-type "化学药物" --appliers "默沙东" --trial-status "进行中" --run --out cde_list.json
#    Need A · combined (keyword global search + advanced filter; is_advanced_search ignored)
python CDE/search_cde_workflow.py --mode combined --keyword "678" --trial-status "已完成" --run --out cde_list.json
#    Need A · multi_keyword (space-separated AND; endpoint echoes keywords back)
python CDE/search_cde_workflow.py --mode multi_keyword --multi-keywords "高血压 糖尿病" --run --out cde_list.json
#    Need B · parallel detail fetch (auto-run by default; confirm ONLY if project list >100 items)
#    Pass the search-output FILE (its project_list is reused) or a JSON STRING of {project_id,...} objects
python CDE/search_cde_workflow.py --project-list cde_list.json --run --out cde_detail.json
#    Preview only (default, no network): prints the exact payload + request
python CDE/search_cde_workflow.py --keyword "奥希替尼"

# 2-alt) CDE FALLBACK paths (NOT the external workflow above)
#   - 3rd-party commercial API (opt-in, data via 3rd party):
python scripts/search_cde.py --api-key "<dxy-key>" --drug "奥希替尼" --run --out cde_api.json
#   - local Playwright scrape: VERIFIED blocked by SafeDog WAF (2026-07-20); keep only as a
#     last resort. (search_cde.py, no --api-key)
python scripts/search_cde.py --drug "奥希替尼" --run --out cde_scrape.json   # likely WAF-blocked

# 2b) ChiCTR — WHO-covered national registry (no public API). Served by the UNIFIED
#     Coze endpoint (source=chictr) — the wrapper now delegates to search_ictrp.py,
#     sharing the ICTRP token; no separate endpoint to provision.
python scripts/search_chictr.py --q "肺癌" --run --out chictr.json
# 2c) ISRCTN — WHO-covered national registry (public search API dead, all /api/query* 404).
#     Served by the UNIFIED Coze endpoint (source=isrctn); wrapper delegates to
#     search_ictrp.py, sharing the ICTRP token.
python scripts/search_isrctn.py --q "cancer" --run --out isrctn.json
# 2d) DRKS — WHO-covered national registry (search is JS/redirect-only, unreachable by pure HTTP).
#     Served by the UNIFIED Coze endpoint (source=drks); wrapper delegates to
#     search_ictrp.py, sharing the ICTRP token.
python scripts/search_drks.py --q "diabetes" --run --out drks.json
#     (WHO ICTRP is a Tier-2 external service via search_ictrp.py; its bridge/de-dup role is
#      reinforced by aggregate.py. Pass --with-ictrp to include it.)
# 3) EU CTR — Tier-1 pure-HTTP HTML parse (no browser, no token). Verified 2026-07-24.
python scripts/search_eu_ctr.py --q "cancer" --run --out euctr.json

# 4) PubChem drug -> target (auto direct-connect)
python scripts/enrich_pubchem.py --drug "osimertinib" --targets --out pubchem.json

# 5) Normalize (multi-source -> unified schema; merge only actually-usable sources)
python scripts/normalize.py --ctgov ctgov.json --cde cde.json --chictr chictr.json \
    --euctr euctr.json --isrctn isrctn.json --drks drks.json --out normalized.json

# 6) Aggregate + report
python scripts/aggregate.py --in normalized.json --out agg.json
python scripts/report.py --in agg.json --out report.md --png report.png

# 6b) (optional) Clinical-friendly multi-sheet Excel — ONE .xlsx, clickable links,
#     frozen header + autofilter, cover-style README, status colour-coding.
#    Method A · CLI (default auto = follow OS language):
python scripts/export_xlsx.py --in normalized.json --out report.xlsx \
    --title "Asciminib 2023-2026"
#    Method B · direct function call:
#     from export_xlsx import export_workbook, prepare_dists
#     recs = json.load(open("normalized.json", encoding="utf-8"))
#     export_workbook(recs, "report.xlsx", title="奥雷巴替尼 I/II 期 (2020 至今)", lang="zh")
#   · export_workbook(recs, out_path, *, title="", meta=None, lang="auto") is the only public entry;
#     recs accepts both list and {"records": [...]} dict.
#   · prepare_dists(recs) is a pure-data step (no IO), callable standalone to precompute/inspect.
#   · lang: "auto"(=OS locale) / "zh" / "en"; CDE Chinese status/indication raw values kept verbatim.
#
# Sheets produced (4): 说明 / 检索结果概要 / 试验总表 / 原始明细
#   - Language (v0.3.25): UI framework labels switch via ct-base shared i18n xlsx.* keys by --lang
#     (single source); raw data values (CDE Chinese status, Chinese indication, etc.) never translated.
#   - 说明 = cover-ified (xlsxwriter, migrated from openpyxl at v0.3.20): deep-blue banner title +
#     rich-text subtitle + 4 KPI cards (total trials/WHO/CDE/year span) + search-overview info card +
#     field dictionary + yellow "data limitations" note; standard header/footer (&C title / &P page + &D date).
#   - 检索结果概要 = workbook sheet 2: 9 stacked zones (phase/status/source/indication/country-region/
#     timeline/sponsor/sample-size stats + interval histogram/phase×status matrix). Distribution blocks
#     (1-7): LEFT data table + RIGHT native chart (bar/pie/line, all data-labelled); chart height hard
#     floor 20 rows (400px), auto-grows by data rows; pie stays square; percentage column DataBar.
#     Sample-size block (8): A:B two-col KPI + interval histogram; cross block (9): wide 3-colour-scale
#      matrix, table only.
#   - 试验总表 = no banner (header on top, frozen first row); status column colour-coded
#     (green=recruiting/blue=ongoing/yellow=not-yet/light-blue=completed/red=withdrawn·terminated/grey=pending·unknown),
#     clickable homepage links, auto-filter.
#   - 原始明细 = plain table snapshot (no banner).
#   Style: shared theme palette, deep-blue white header, zebra rows, real percentages, count colour-scale + data bars.
```

## One-shot & cross-source orchestration

```bash
# One-shot orchestration (CT.gov + PubChem + aggregate + report):
python scripts/ct_registry.py --cond "NSCLC" --status RECRUITING --with-pubchem --out-dir ./out

# Cross-source: CT.gov + CDE merged into the SAME landscape (external workflow auto-invoked,
# then normalized alongside CT.gov; CDE failure degrades gracefully to CT.gov-only):
python scripts/ct_registry.py --cond "NSCLC" --status RECRUITING --with-cde --out-dir ./out --run
# Full landscape: Tier-1 (CT.gov + EU-CTR) + Tier-2 (CDE + ChiCTR + ISRCTN + DRKS + WHO ICTRP)
python scripts/ct_registry.py --cond "NSCLC" --status RECRUITING \
    --with-euctr --with-cde --with-chictr --with-isrctn --with-drks --with-ictrp \
    --out-dir ./out --run
# Per-source keyword override (localized term when default derivation misses):
python scripts/ct_registry.py --cond "NSCLC" --status RECRUITING \
    --with-isrctn --isrctn-keyword "non-small cell lung cancer" --run
```

### Keyword localization (two-phase)

`ct_registry.py` auto-localizes the search keyword to each source's expected language — type ONE keyword only.

- **Phase 1 — terminology first:** every switch consults `ct-base/references/term_map.json` (~190 curated
  terms) **plus** the extended drug-class / specific-drug maps in `ct-base/scripts/kw_localize.py`
  (`_CLASS_EN2ZH`, `_DRUG_EN2ZH` — e.g. `sartan→沙坦`, `valsartan→缬沙坦`, `ARB→沙坦类`). All three maps
  are merged into **both** translation directions inside `localize()`.
- **Phase 2 — confirm-on-miss (foreign sources):** if a **CT.gov / PubChem** keyword is NOT in the map (and
  is in the wrong language), the run **stops** and prints a suggested English translation — it does NOT
  silently search CT.gov with Chinese. Confirm by rewriting the arg in English, or re-running with
  `--confirm-cond` / `--confirm-intr` / `--confirm-drug` carrying the agreed translation.
  (Add `--auto-confirm` only for known-safe automation that may tolerate missed hits.)
- **CDE (domestic China)** expects Chinese; an English keyword is auto-translated to Chinese via the extended
  maps above (so `sartan`→`沙坦` hits 788 instead of 10). **Only if a keyword truly cannot be resolved to
  Chinese** does the run render the **keyword-matching MENU** (`kw_localize.kw_match_candidates` →
  `render_kw_menu`) and stop for the user to pick an interpretation — it no longer silently searches CDE with
  English text. **CDE search uses silent fallback (updated 2026-08-11):** the orchestrator first runs the
  Chinese keyword against CDE; if it returns 0 records AND a valid English translation exists, it automatically
  re-runs with the English keyword and merges the two result sets. This replaces the previous default
  bilingual parallel (which always fired both zh+en concurrently). Disable silent fallback with
  `--no-cde-bilingual`.
- **Non-standard / category keywords → MENU, not trial-and-error:** when a term is a drug *class* (e.g.
  `sartan`) or misses the map, `kw_match_candidates()` offers `as_is` / `translate` / `class_suffix`
  (→ 沙坦, CDE wins) / `enumerate` (→ specific ARB names, WHO wins) / `structured` (WHO fields). See
  `references/keyword_match.md` for the empirical matching rules + probe data.
- Explicit `--cde-*` args always win. Extend coverage in `ct-base/references/term_map.json` or the embedded
  maps in `ct-base/scripts/kw_localize.py`.

### Common search recipes (v0.3.31)

WHO (`--source who`) and CDE (`--source chinadrugtrials`) share the same unified endpoint, orchestrated by
`ct_registry.py` in **Batch-1 concurrency**. All commands need `--run` to go online (preview is offline by
default); the shared endpoint daily cap is 1000 (per demand_id, WHO+CDE merged counts once).

1. **Full WHO+CDE parallel (most common default):** covers zh+en dual registries; WHO exact EN match, CDE auto-translated ZH + bilingual.
   ```bash
   ct_registry.py --with-ictrp --with-cde --cond "Type 2 Diabetes" \
     --intr "DPP-4 inhibitor" --min-year 2023 --run
   ```
2. **WHO structured combined (most precise narrowing):** `search_ictrp.py --source who --mode combined`, multi-field intersect.
   ```bash
   search_ictrp.py --source who --mode combined \
     --who-condition "lung cancer" --who-intervention "pembrolizumab" \
     --who-phase "Phase 3" --who-recruitment-status Recruiting \
     --who-date-start 01/01/2023 --who-date-end 31/12/2025 --run
   ```
3. **CDE advanced field search (Chinese registry precise):** `--cde-keyword` must be Chinese; `--cde-trial-status` enum value exact (`进行中`, not "正在进行").
   ```bash
   ct_registry.py --with-cde --cde-keyword 沙坦 --cde-trial-status 进行中 \
     --cde-drugs-type 化学药物 --min-year 2023 --run
   ```
4. **Multi-keyword AND narrowing (both sources):**
   ```bash
   search_ictrp.py --source who --multi-keywords "diabetes DPP-4 inhibitor" --run
   ct_registry.py --with-cde --cde-multi-keywords "高血压 沙坦" --run
   ```
5. **Year + status double filter (trend/in-study screen):**
   ```bash
   ct_registry.py --with-ictrp --with-cde --cond 肝功能不全 --since-years 3 --status 招募中 --run
   ```
6. **Detail enhancement (precise phase/sponsor):** `--with-detail` makes CDE pull 65 fields, WHO go detail; phase uses normalized value.
   ```bash
   ct_registry.py --with-ictrp --with-cde --cond 列汀 --with-detail --run
   ```
7. **WHO-down fallback:** on WHO failure auto-concurrent EU-CTR + ISRCTN + DRKS + ChiCTR (+ CDE if needed).
   ```bash
   ct_registry.py --with-ictrp --with-cde --cond cancer --fallback-covered --run
   ```

> Usage: daily = combo 1; precise = combos 2/3 structured fields; narrow volume = combo 4 (multi-keyword AND)
> + combo 5 (year/status); precise phase = combo 6; WHO unreachable = combo 7.

### Parallel retrieval (v0.3.29 → v0.3.30)

`ct_registry.py` runs independent network sources inside `ThreadPoolExecutor` batches:
- **Batch-1** = **WHO ICTRP + CDE-zh** — different endpoints / separate subprocesses → dispatched concurrently. If CDE-zh returns 0 records AND a valid English translation exists, the orchestrator auto-runs CDE-en and merges (silent fallback, updated 2026-08-11). Wall-clock drops from "serial sum" to "max of the two".
- **Batch-2 (fallback / cover, v0.3.30)** = **EU-CTR (pure HTTP) + ISRCTN / DRKS / ChiCTR (unified endpoint, source=isrctn/drks/chictr)** — WHO-covered national registries: skipped when WHO succeeds, run independently + aggregated when opted in (`--with-<src>`) or when WHO fails + `--fallback-covered` is set.
- Serial only where a source depends on another (e.g. CDE detail-fetch needs the project list).
- Quota charged **exactly once per demand** even under concurrency: parent calls `_ensure_quota_checked(demand_id)` once (sets `CT_DEMAND_CHECKED=1`); child subprocesses see the flag and skip their own `usage_guard.check()`.

> Verified 2026-07-23: `normalize.py` consumes the CDE workflow output directly (`source:"CDE"` + `records`),
> so CT.gov (20) + CDE (2057) merge into one 2077-record landscape. CDE **list** search returns only summary
> fields; `sponsor` / `phase` populated only by **detail** mode, so list aggregation may show them as `Unknown`.

### Advanced search — WHO & CDE parameter inventory (v0.3.14)

When the prompt contains a parameter combination (e.g. drug + phase, condition + sponsor + country + year),
prefer building a structured/advanced search payload over a bare keyword search.

**WHO ICTRP advanced fields → CLI (`search_ictrp.py --source who`)**
| WHO AdvSearch field | CLI flag | Notes / accepted values |
|---|---|---|
| Title (public/scientific/abbr) | `--who-title` (+ `--who-title-operator` None/NOT) | AND/OR/NOT combinable |
| Condition / Health problem | `--who-condition` | overrides `--q` |
| Intervention / Treatment | `--who-intervention` (alias `--intr`; `--who-intervention-operator` AND/OR/NOT) | |
| Recruitment status | `--who-recruitment-status` (or `--status`→Recruiting) | `Recruiting` / `ALL` |
| Primary sponsor | `--who-sponsor` (alias `--sponsor`) | full/partial/abbr name |
| Recruiting country | `--who-country` | comma-separated ISO/names |
| **Phases** | `--who-phase` | **comma-separated**, e.g. `Phase 1,Phase 2,Phase 1/Phase 2,Early Phase 1` |
| Date of registration | `--who-date-start` / `--who-date-end` (DD/MM/YYYY) | also `--since-years` in orchestrator |
| Study type | (via `--who-condition`+keyword) | |
| With results / COVID-19 / Rare disease / Gene editing | `--who-with-results` / `--who-covid19` / `--who-rare-diseases` / `--who-gene-editing` (bool) | |
| Secondary ID (e.g. ISRCTN no.) | `--who-secondary-id` | |

- **Mode rule:** if any structured field (other than `--q`) is supplied, `search_ictrp.py` auto-selects
  `mode=combined`; `--mode multi_keyword` for space-separated AND terms. Plain `--q` only → `mode=search`.

**CDE advanced fields → CLI (`search_ictrp.py --source chinadrugtrials`)**
| CDE AdvSearch field | CLI flag | Enum / notes |
|---|---|---|
| 登记号 | `--reg-no` | |
| 适应症 | `--indication` | |
| 试验方案编号 | `--case-no` | |
| 药物名称 | `--drugs-name` | |
| 药物类型 | `--drugs-type` | `中药`/`天然药物`/`化学药物`/`生物制品` |
| 申请人 / 申办者 | `--appliers` | |
| 伦理委员会 | `--communities` | |
| 主要研究者 | `--researchers` | |
| 临床参加机构 | `--agencies` | |
| **试验状态** | `--trial-status` | 11 values: 进行中/尚未招募/招募中/招募完成/已完成/主动暂停/主动终止/IEC·IRB暂停/IEC/IRB终止/责令暂停/责令终止 |
| ⚠️ 分期 (phase) | — | **CDE AdvSearch has NO phase filter**; phase only post-filter after detail normalization (`norm_cde` fills `试验分期`) |

- **Mode rule:** any advanced field (other than `--q`) auto-sets `is_advanced_search=True`. Orchestrator
  flags: `--cde-indication` / `--cde-drugs-name` / `--cde-drugs-type` / `--cde-appliers` / `--cde-trial-status` (+ `--cde-mode combined`).

**⚠️ `who_phase` caveat — verified 2026-07-30 (do NOT use as sole phase filter):** a live test on
`Olverembatinib` proved `--who-phase` **is honored server-side** (keyword-only → 41; `+who_phase "Phase 1,Phase 2"` → 2).
**BUT** the WHO portal's Phases dropdown filters on a *normalized* phase field that **under-captures
combined/numeric phases**: the same query with the full I/II set still returned 2, whereas detail-derived
phases show ~19 true I/II trials. **Therefore:** (1) `who_phase` may be sent as a **coarse narrowing** to
reduce fetch volume, but (2) **always re-validate phase on detail-normalized records** (`normalize.py` →
`phase`); the post-hoc detail-phase filter is the **authoritative** I/II gate. CDE phase is *always*
detail-post-filter only (no server-side phase field exists).

### Structured detail + document links (v0.3.0)

1. **Structured detail auto-fill (`--with-detail`).** After the normal list search:
   - CDE runs `mode=detail` (65 fields/record) and the orchestrator swaps the CDE input to `cde_detail.json`,
     so `sponsor` / `phase` / eligibility / endpoints / actual enrollment are populated (previously `Unknown`).
     `&nbsp;` HTML entities are cleaned.
   - EU-CTR runs `fetch_eu_ctr_docs.py` against the CTIS `retrieve/{ctNumber}` API, extracting
     `{title, type, url}` **document links** into each record's `documents` list.
   - Both enrichments are graceful: failure degrades to `documents: []` / list-level summary.
2. **Homepage links in every record.** The unified schema carries a `url` field (registry homepage / detail
   page). `report.py` renders it as a `[首页](url)` link for **every** primary record.
3. **Confirm-gated PDF download (`--download-docs`).** Only EU-CTR currently exposes downloadable document
   URLs (CDE detail returns **zero** attachment URLs; SafeDog WAF blocks automated file download). By default
   `download_docs.py` only **lists** links; `--download-docs` (or `--yes`) is the explicit confirmation gate.
   - **v0.3.13 generic doc-enrich entry `enrich_docs.py` (for WHO mirror libs):** WHO ICTRP-mirrored CT.gov /
     ChiCTR / JPRN / CTRI records carry only `url` (jump to source platform) and default `documents=[]`;
     `download_docs.py` has "no downloadable links" even if patched. `enrich_docs.py` routes by `url` host:
     **EU-CTR** (euclinicaltrials.eu) reuses `fetch_eu_ctr_docs.fetch_docs`; CT.gov / ChiCTR / JPRN / CTRI /
     ISRCTN / DRKS (no public PDF API) keep `documents` empty, only `url` for manual download. `--run` actually
     hits CTIS; default PREVIEW only counts source distribution.

```bash
# Auto-fill structured detail + render homepage links, then LIST (do NOT download) PDFs:
python scripts/ct_registry.py --cond "NSCLC" --status RECRUITING \
    --with-cde --with-euctr --with-detail --out-dir ./out --run
# Actually download the listed EU-CTR PDFs (explicit confirmation gate):
python scripts/ct_registry.py --cond "NSCLC" --status RECRUITING \
    --with-cde --with-euctr --with-detail --download-docs --out-dir ./out --run
# Or download standalone against an existing normalized file:
python scripts/download_docs.py --in ./out/normalized.json --out-dir ./out/docs --yes
```

> **CDE caveat (verified against `cde_detail.json`):** CDE detail mode returns 65 structured fields but **0
> attachment/PDF URLs**. No automated way to fetch CDE protocol PDFs — the report prints "附件: CDE 公示平台详情页
> 可手动下载（自动化受 WAF 限制，无直链）" per CDE record. Only EU-CTR documents are auto-downloadable today.

### Resource-usage policy (v0.3.1 intro, v0.3.5 changed to per-demand demand_id counting)

WHO / CDE search is **currently free**, but via a **shared third-party endpoint** (Coze /run workflow);
follow the **minimal shared-resource occupancy** principle. The three limits are auto-enforced per search
**demand** (deduped by `demand_id`, no manual judgement):

1. **Minimal occupancy + bulk coordination:** WHO/CDE and similar external-workflow sources (ChiCTR / ISRCTN /
   DRKS) share one endpoint. For **bulk search needs**, guide the user to **contact the skill author Wintone**
   for coordination, rather than high-frequency self-scraping.
2. **Daily demand cap 10 (counted per demand_id):** searches against the shared endpoint count per **demand**
   (one `ct_registry.py --run`, or one agent task's grouped stepwise searches) — whether it contains WHO+CDE,
   how many keyword tweaks, or repeats, all consume **1 quota** (same `demand_id` already counted → later calls
   say "already counted, not re-counted"). Preview, `--store-token`, direct sources CT.gov/EU-CTR/PubChem are
   **NOT counted**. `usage_guard` still enforces a **hard daily cap of 1000 demands** (local time, midnight roll).
   **Currently free** — the cap exists purely for fair shared-resource use; see README "配额与资源使用". At 100
   demands the run stops with "please use again tomorrow". Counter in `config/usage.json` (new `demands` list);
   read/write exceptions **fail open** (warn only, never block the skill).
3. **PDF not auto-downloaded by default:** `download_docs.py` only **lists** links by default (`--yes` to
   actually download); orchestrator downloads only with explicit `--download-docs` (user explicitly requested).
   No path auto-writes PDF without explicit user request.

> Implementation: `scripts/usage_guard.py` (`check()` daily count + cap block); call sites cover
> `search_ictrp.py` (unified WHO/CDE), `CDE/search_cde_workflow.py` (standalone CDE + detail, archived),
> `extsvc_client.dispatch()` (ChiCTR/ISRCTN/DRKS); `ct_registry.py` preview also prints this policy;
> `download_docs.py` defaults to preview.
