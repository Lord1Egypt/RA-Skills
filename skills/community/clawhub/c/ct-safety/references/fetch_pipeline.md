# Fetch Pipeline & FAERS API Field Reference (agent-facing)

Technical companion to `## Data Sources` and `## Workflow` in SKILL.md.
Captures openFDA/FAERS field boundaries, count-endpoint pitfalls, the three-step
fetch workflow, caching, parallelism, XLSX layout, and MedDRA PT caveats.

## 1. Endpoints (openFDA public REST API)

| Endpoint | URL | Use |
|---|---|---|
| FAERS events | `https://api.fda.gov/drug/event.json` | Quantitative disproportionality + counts |
| FDA Label | `https://api.fda.gov/drug/label.json` | `--with-fda-label`: adverse_reactions / warnings |
| CN-PV | `https://cdr-adr.org.cn` public columns | `--with-cn-pv`: qualitative corroboration only |

- FAERS works **without a key** (anonymous quota: 240 req/min, 1,000 req/day per IP).
  Optional `--api-key` raises to 240 req/min, 120,000 req/day per key.
- `cdr-adr.org.cn` is the public portal of 国家不良反应监测中心; scrapeable with a
  normal `requests` call — **no WAF, no key, verified 2026-07-23**. These are
  **narrative bulletins, NOT individual case reports** — they carry no per-drug-event
  counts and **cannot** feed disproportionality. They only corroborate a FAERS signal.
- NMPA main site (incl. 《药品不良反应信息通报》) is WAF-blocked (HTTP 412) and is
  intentionally excluded.

## 2. Indexable vs Non-indexable FAERS fields (verified 2026-07-30)

**Indexable / searchable / countable:**
- `patient.drug.medicinalproduct` (drug name; default search field)
- `patient.reaction.reactionmeddrapt` (reaction PT; use `.exact` for Top-N)
- `receivedate` (range queries → time windows / yearly trend)
- `serious`, `seriousnessdeath`, `seriousnesshospitalization`,
  `seriousnesslifethreatening`, `seriousnessdisabling` (boolean, searchable)
- `patient.patientsex` (sex facet; 1=male / 2=female / 0=unknown)

**NOT indexable / NOT facetable (count/search/range → 404 or 500):**
- `patient.patientage` — **cannot `count` (404)**, but exists in case-report bodies
  → only after Step-3 case download + local stats.
- `primarysource.reportertype` (reporter type)
- `primarysourcecountry` — bare field `count` **persistently 500**; must use
  `primarysourcecountry.exact`.

> These non-facetable fields still exist in each case report. After the Step-3
> case download (≤10000) you can compute age / country / reporter-type
> distributions locally from CSV / XLSX / JSON.

## 3. `count` facet endpoint pitfalls (fast/cache mode)

- **`limit` upper bound:** `count` queries with `limit≥1000` return **403 Forbidden**
  (stricter than the case endpoint). Must be `≤100`. Categorical fields
  (seriousness/sex/type/role) have ≤4 values, so `limit=100` is ample.
  `receivedate` facet **ignores `limit`** and returns all daily buckets
  (2020+ ≈ 2000+), then the script aggregates by year.
- **`receivedate` result key is `time`, not `term`:** returns
  `[{"time":"20200101","count":5}, …]` — read `time` when aggregating years.
- **`primarysourcecountry` / `patient.drug.drugindication` bare `count` persistently
  500** — must append `.exact` (`primarysourcecountry.exact` /
  `patient.drug.drugindication.exact`).

## 4. MedDRA PT caveats

- Some three-word exact phrases (e.g. `RENAL FAILURE ACUTE`) **persistently 404** —
  the PT is not accepted by openFDA (not transient jitter). Use the standard PT
  `ACUTE KIDNEY INJURY` instead.
- Two-word PTs (e.g. `HEPATIC FAILURE`, `HYPERKALAEMIA`) usually work.
- `total()` has a built-in **"404 → `.exact` downgrade"**; if `.exact` still 404s,
  the PT is unindexed and must be swapped for a synonymous standard PT.
- Retry (3× exponential backoff) covers only **transient** 404/429/5xx; persistent
  404 is a real "PT not accepted" signal — do **not** rely on retries.

## 5. Three-step fetch workflow (default: present-in-context, Excel on-demand)

**Step 1 — Summary present (default, no confirmation):** `fetch_reports.py --drug X`
sends 8 `count` facet queries (seriousness / sex / report-type / source-country /
yearly / top-reactions / top-indications / drug-role), prints the summary to the
context in seconds, and writes `faers_summary_cache.json`. Analysis is over the
**full matched report set** (no "top-N" selection bias); first line shows the total.
Equivalent to the old `--fast` mode — now the default when no `--run`/`--out-xlsx`.
- Cost: `age` cannot be faceted via API (404) → age block omitted with a note; need
  the detail-download mode for age distribution.

**Step 2 — Summary Excel (on explicit request):** `fetch_reports.py --drug X
--out-xlsx summary.xlsx` builds a **3-sheet + 8-chart** workbook from the cache
(cache miss → re-facet):
1. **说明 (Cover)**: banner + 8 KPI cards (analysis base / matched total / serious /
   serious-rate / male / female / year span / report type) + retrieval overview +
   data-limitation statement.
2. **检索结果概要 (Results)**: 8 distribution blocks (table + native chart each):
   seriousness pie / sex pie / report-type bar / source-country Top12 / yearly
   trend line / top-reactions Top15 / top-indications Top12 / drug-role.
3. **个案明细 (Cases)**: unified per-case sheet (12 columns, frozen header +
   autofilter). Same template as `report_xlsx.build_signal_xlsx` (single source of
   truth in `xlsx_sheets.build_case_details`). Empty placeholder in fast mode.
UI labels via `ct-base/i18n.py` (bilingual); raw values (PT, country code, drug
name) kept verbatim. Visual spec (medical-red palette / 24px header / zebra rows /
cover logo) from shared `ct-base excel_style`.

**Step 3 — Case download (only when user explicitly wants cases):** `fetch_reports.py
--drug X --run --max 10000 --out-xlsx reports.xlsx` paginates via openFDA
`limit/skip` to download **individual case reports** (HARD_CAP=10000 to protect the
free quota). Then age / country distributions can be computed locally; XLSX becomes a
9-chart detail version (adds age block).
- **Timing:** openFDA single page (100 rows) for large result sets ≈ **50–60 s** →
  ~100 cases ≈ 1 minute. Slow, and analysis is over "API-return-order first N" (selection bias) — prefer Step 1/2 unless case-level data is needed.
- **Parallel `--parallel N`:** bottleneck is single-request server latency (not rate
  limit). `--parallel 2` splits `[0, n_target)` into N windows paged concurrently →
  wall-clock ≈ 1/N. Each worker writes per-page to disk (CSV/JSONL shards), merged at
  end. Anonymous 240/min is ample — **no API key needed**.
- **Per-page write:** each page flushed immediately (CSV incremental append + JSONL
  checkpoint append); interrupted pages are not lost; final JSON array + XLSX written
  at end.
- **Detail XLSX (9 charts):** ① Cover (KPI incl. downloaded / median age) ② Results
  (9 blocks, incl. age histogram) ③ Raw (case-level flat table, frozen header +
  auto-filter).

> **Which to use:** quick overview → `fetch_reports.py --drug X` (seconds, context).
> Excel archive/report → add `--out-xlsx` (cache hit, seconds). Case-level raw data
> → `--run`.

`scripts/overview.py` (separate pre-overview writer) is **deprecated since v0.1.18**:
its role is merged into the Step-1 present flow. Script retained but no longer called.
Signal detection etc. go through `ct_safety.py` / `disproportionality.py`, independent
of the fetch main delivery.

## 6. Script inventory (key CLI patterns)

```bash
# Overview (deprecated) — replaced by fetch_reports present flow
python scripts/overview.py --drug "candesartan" --top 10 \
    --date-from 20200101 --date-to 20261231 --run --out-dir ./out

# Step 2 summary Excel (auto count-facet, no confirmation needed)
python scripts/fetch_reports.py --drug "candesartan" \
    --date-from 20200101 --date-to 20261231 --out-xlsx faers_summary.xlsx

# Step 3 case download (--run), HARD_CAP 10000, ~100 rows/min
python scripts/fetch_reports.py --drug "candesartan" --max 10000 \
    --date-from 20200101 --date-to 20261231 --run \
    --out faers_reports_raw.json --out-csv faers_reports.csv --out-xlsx faers_reports.xlsx

# Parallel case download (no key needed)
python scripts/fetch_reports.py --drug "candesartan" --max 10000 \
    --date-from 20200101 --date-to 20261231 --run --parallel 2 \
    --out faers_reports_raw.json --out-csv faers_reports.csv --out-xlsx faers_reports.xlsx

# Single drug-event signal (2x2 → PRR/ROR/IC/EBGM)
python scripts/ct_safety.py --drug "candesartan" --event "ANGIOEDEMA" \
    --date-from 20200101 --date-to 20261231 --run --out-dir ./out

# With China PV qualitative corroboration
python scripts/ct_safety.py --drug "candesartan" --event "ANGIOEDEMA" \
    --with-cn-pv --drug-cn "坎地沙坦" --event-cn "血管性水肿" \
    --date-from 20200101 --date-to 20261231 --run --out-dir ./out

# Continuity correction (default ON; --no-continuity reproduces v0.1.8)
python scripts/ct_safety.py --drug "candesartan" --event "ANGIOEDEMA" \
    --date-from 20200101 --date-to 20261231 --run --out-dir ./out

# Pipeline self-check against known +/- controls (no --drug/--event needed)
python scripts/ct_safety.py --validate-controls --out-dir ./out

# Temporal trend anomaly (requires --event)
python scripts/ct_safety.py --drug "osimertinib" --event "PNEUMONITIS" \
    --trend --date-from 20200101 --date-to 20261231 --run --out-dir ./out

# Multi-drug aROR (first = focal, rest = reference pool; requires --event)
python scripts/ct_safety.py --drug "osimertinib" --event "PNEUMONITIS" \
    --compare-drugs osimertinib gefitinib erlotinib \
    --date-from 20200101 --date-to 20261231 --run --out-dir ./out

# Multi-source triangulation + score + tier (--with-fda-label enables 3rd source)
python scripts/ct_safety.py --drug "osimertinib" --event "PNEUMONITIS" \
    --with-cn-pv --drug-cn "奥希替尼" --event-cn "肺炎" \
    --with-fda-label \
    --date-from 20200101 --date-to 20261231 --run --out-dir ./out

# Low-level primitives (manual)
python scripts/fetch_faers.py --drug "osimertinib" --event "PNEUMONITIS" --run --out faers_pair.json
python scripts/disproportionality.py --in faers_pair.json --out disp.json
python scripts/report.py --in disp.json --out faers_report.md

# Standalone CN-PV search (no FAERS needed)
python scripts/fetch_cn_pv.py --drug "奥希替尼" --event-cn "肝损伤" --run --out cn_pv.json
```

### Non-ASCII drug-name auto-translation
`--drug 阿司匹林` auto-translates to `aspirin` via `drug_name_resolver.resolve_for_dialog()` (dialog-safe, no menu, aligns with ct-base §6.2 Triage); 471-entry Chinese→English INN map in `references/drug_name_map.json`. CLI-only `resolve(auto=False)` retains the multi-candidate number menu for terminal use. Disable with `--no-resolve-drug-name`.
