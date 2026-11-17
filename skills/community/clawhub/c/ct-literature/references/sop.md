# ct-literature Operating SOP

> Scope: systematic retrieval of **published-evidence literature** (papers / reviews / abstracts / citations), normalized and de-duplicated into an evidence-base report.
> Tier: A (non-confidential input + public retrieval, zero confidential data).
> Red line: default is PREVIEW only; real network retrieval requires explicit `--run`.
> Complements `ct-registry`: this skill fetches **only literature metadata** (title / authors / journal / citations / year / type) and never fetches registry structured fields (phase / status / enrollment).

---

## 1. When to use

- Answer *"what evidence has been published about this topic?"* — systematic review, RCT, meta-analysis, scoping review, case report.
- Build an **evidence base**: highly-cited works, study-type distribution, yearly trend, safety subset.
- `--safety` extracts **qualitative published safety literature** — complements (never replaces) `ct-safety`'s FAERS quantitative signals.

## 2. Prerequisites

- Python 3 (the OpenAlex primary path uses stdlib `urllib` — zero hard `requests` dependency; `requests` is optional with a `try/except` fallback).
- Network access:
  - OpenAlex (`api.openalex.org`, no key, primary, citation-rich)
  - Europe PMC (`ebi.ac.uk`, MEDLINE/MeSH, no key, optional biomedical enrichment)
  - Semantic Scholar (no key, optional citation ranking; prone to HTTP 429 → **gracefully degrades to empty, no interruption**)

## 3. Command examples (from invocation to output)

### 3.1 PREVIEW first (no network)

```bash
python scripts/ct_literature.py --topic "osimertinib" --review-type systematic-review --safety
# prints: [PREVIEW] would run literature pipeline: topic=... sources=[OpenAlex] (use --run)
```

### 3.2 Primary retrieval (OpenAlex)

```bash
python scripts/ct_literature.py --topic "osimertinib" --review-type systematic-review \
    --year-from 2018 --safety --max 30 --run --out-dir ./out
```

### 3.3 Two-source enrichment (Europe PMC + Semantic Scholar)

```bash
python scripts/ct_literature.py --topic "osimertinib" --review-type all \
    --with-europepmc --with-semantic-scholar --run --out-dir ./out
```

> If Semantic Scholar hits 429 it is skipped automatically; only OpenAlex (+ Europe PMC) results are merged, no error.

## 4. Parameter table

| Parameter | Default | Notes |
|---|---|---|
| `--topic` | **required** | Free-text topic / drug / disease |
| `--review-type` | `all` | `all` / `systematic-review` / `scoping-review` / `meta-analysis` / `rct` / `case-report` |
| `--year-from` | — | Lower bound of publication year |
| `--year-to` | — | Upper bound (giving `--year-from` alone does NOT narrow to a single year) |
| `--safety` | off | Safety / CSM bias (AE, toxicity, case report, pharmacovigilance) |
| `--max` | `50` | Max works per source |
| `--with-europepmc` | off | Add Europe PMC (MEDLINE/MeSH precision) |
| `--with-semantic-scholar` | off | Add Semantic Scholar (citation ranking; 429-degrades) |
| `--run` | off | **Required** to actually hit the network; otherwise PREVIEW only |
| `--out-dir` | `./out` | Output directory |
| `--depth` | —（旧 `--max`） | 检索深度预算 `quick`/`standard`/`deep`：决定每源上限与弱化结果救援（非证据质量评级） |
| `--concept` | — | 结构化 PICO 概念（可重复）`TYPE=VALUE`，TYPE∈{condition,population,intervention,comparator,outcome,endpoint,study_design,biomarker,drug,indication}；概念 AND 拼入检索式、做 MeSH 归一化审计 |

## 5. Output files (under `--out-dir`)

| File | Notes |
|---|---|
| `openalex.json` | Raw OpenAlex fetch (primary, always produced) |
| `europepmc.json` | Europe PMC fetch (only with `--with-europepmc`) |
| `semantic_scholar.json` | Semantic Scholar fetch (only with `--with-semantic-scholar`; empty on 429) |
| `merged.json` | **Cross-source merged + de-duplicated** (`{count, works[]}`, sorted by citations desc, with `sources` provenance) |
| `lit_report.md` | **Main deliverable**: Markdown evidence report (summary / top-works table / type distribution / yearly trend / safety subset) |

## 6. Typical workflow

1. PREVIEW to confirm `--topic` spelling → `--run` to produce `lit_report.md`.
2. Need broader coverage → add `--with-europepmc` (biomedical precision) + `--with-semantic-scholar` (citation ranking).
3. Safety review → add `--safety`; results sit alongside `ct-safety`'s FAERS signals (qualitative vs quantitative, methodologically complementary).
4. Use `lit_report.md` as the *evidence-base* dimension of the intel brief, alongside `ct-registry` (landscape) and `ct-safety` (signals).

## 7. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| PREVIEW only, no network | `--run` missing | Add `--run` |
| Too few results | Topic too narrow | Broaden `--topic` or use `--review-type all` |
| Semantic Scholar segment empty | HTTP 429 rate limit | Expected degradation; results still include OpenAlex (+ Europe PMC), no action needed |
| Year filter odd | Only `--year-from` given | Fixed: lower bound opens to 1900, upper to 3000 — never narrows to a single year |
| Titles contain `<i>` tags | Source returned HTML | Fixed: `_strip_html()` cleans it |

## 8. Known design constraints

- The OpenAlex primary path has **zero `requests` dependency** — runs in any standard Python; only `ct-safety` (FAERS) genuinely needs `requests`.
- Merge/dedupe keys on DOI (regex `10.\d{4,9}/...`), else normalized title; the `sources` field records each work's origin for traceability.
