# data-element-dx-skillkit

<p align="center">
  <b>Data-Element Transformation · End-to-End Delivery Skill Suite for China's SOEs and Traditional Conglomerates</b><br />
  <sub>Not a tutorial — deliverables you can put straight into a board presentation.</sub>
</p>

<p align="center">
  <img alt="version" src="https://img.shields.io/badge/version-2.0-1F4E35" />
  <img alt="license" src="https://img.shields.io/badge/license-Apache--2.0-062032" />
  <img alt="skills" src="https://img.shields.io/badge/skills-7-1F4E35" />
  <img alt="language" src="https://img.shields.io/badge/lang-EN%20%7C%20中文-062032" />
</p>

---

## What It Actually Produces

Not "advice", not "methodology" — **physical deliverables** ready for the reporting folder:

| Deliverable | Audience | Shape |
|---|---|---|
| Application scenario map (value × feasibility quadrants) | CIO | 12 ranked candidates, incl. explicit "why not" |
| Data product list (internal 7 + external 4) | Business owners | Two classes designed separately |
| Data-asset capitalization path (MOF interim rules) | CFO | Step-by-step confirmation → conclusion |
| Value quantification table | Board chair | Order-of-magnitude only, no hard promises |
| **20-page board deck** | Board chair | Value first, tech in the appendix |

> Full end-to-end demo (fictional "Group A", zero real client data) lives in [`_demo-run/`](_demo-run/README.md) — including the actual 20-slide deck.

---

## Why It Exists (the gap)

The existing high-star open-source Agent Skills ecosystem is **all single-point tooling**:
data governance, data quality rules, DuckDB querying, PPT generation. None of them deliver an
**end-to-end consulting pipeline** — from industry research through baseline survey, architecture,
data quality, application planning, to a board-level deck with enforced stage gates and
cross-material numeric consistency.

This suite fills that gap for one specific, underserved audience: **Chinese state-owned and
traditional conglomerates going through data-element transformation** (数据要素).

### Four differentiators

1. **Delivery pipeline, not tooling** — each skill = one repeatable delivery action + a standard artifact + a quality gate.
2. **A uniquely Chinese SOE skeleton** — the "Seven Processes" (汇存治管服用模: ingest/store/govern/manage/serve/use/model), DCMM (GB/T 36073) alignment, and policy anchors: the "20 Measures for Data Elements", MOF interim rules on data-asset capitalization, and public-data authorized operation.
3. **An orchestration layer that no open-source skill has** — `dx-engagement-orchestrator` enforces causal ordering (no skipping the baseline survey) and stage gates with a machine-checkable gate script.
4. **Gotchas fed by real projects** — every anti-intuitive lesson (each skill carries 8–13 of them) is a moat nobody can fork.

---

## The Seven Skills

| Skill | Seven-Process | Does | Version |
|---|---|---|---|
| `dx-engagement-orchestrator` | orchestration | 8 onboarding questions · enforced order · stage gates · numeric consistency | v2.0 |
| `dx-industry-research` | external insight | policy → market → players, three layers | v2.0 |
| `dx-competitor-scout` | external insight | 4-dimension classification + moat judgment | v2.0 |
| `dx-data-baseline` | ingest + store | system survey → asset inventory → data-flow map → DCMM score | v2.0 |
| `dx-architecture-opt` | store + govern + manage | 7-layer blueprint · roadmap · HALT governance gates | v2.0 |
| `dx-data-quality` | govern | metric dictionary · named owners · machine-checkable rule set | v2.0 |
| `dx-application-plan` | serve + use + model | scenario map · product list · capitalization path · board deck | v2.0 |

**Enforced order** (reasons for each are in the orchestrator):

```
industry research → competitor scout → baseline survey ★ → architecture → quality → application planning
```

---

## Quick Start

### Install (copy, no dependencies)

```bash
# user-level (available across projects)
cp -r data-element-dx-skillkit/dx-* ~/.workbuddy/skills/
cp -r data-element-dx-skillkit/_shared ~/.workbuddy/skills/
```

> ⚠️ **`_shared/` must stay a sibling of the `dx-*` skill directories** — skills reference it
> via relative paths (`../_shared/...`). Do NOT copy `_shared/` alone into a skills dir.

### Try it (3 minutes to a real artifact)

```
Use the dx-application-plan skill on this group:
A local SOE running 6 wholesale agricultural markets, ~1B RMB revenue in 2024,
14 systems connected, ~1,000 tables, DCMM preliminary level L2.
```

### Scripts (all zero-dependency)

```bash
# DCMM 8-domain maturity score
python _shared/scripts/maturity_score.py --input scores.json

# Data asset scan (Excel / CSV / directories)
python _shared/scripts/scan_assets.py <target-dir>

# Gate check: existence / substance / process-mapping / numeric consistency
python _shared/scripts/gate_check.py <delivery-dir> \
  --expect "scenario-map.md,product-list.md,value-table.md,deck-outline.md" \
  --numbers "6 markets,14 systems,L2,10 metrics"
```

> `gate_check.py` is a **machine pre-check** — it can under-/over-report; conclusions require human review.

---

## Why the English Market Should Care

Two of our policy anchors are **rarely covered in English-language skill ecosystems**:

1. **Data-asset capitalization (数据资产入表)** — China's MOF interim rules let enterprises
   recognize qualified data resources as intangible assets or inventory on the balance sheet.
   The path (confirmation conditions → cost attribution → recognition) is a complete,
   non-obvious methodology — and it is built into `dx-application-plan`.
2. **Public-data authorized operation (公共数据授权运营)** — the emerging model where
   governments license public data to qualified operators. It shapes both the research layer
   (`dx-industry-research`) and the product layer.

The seven-process skeleton and the orchestration-with-gates pattern, meanwhile, are
language-agnostic consulting craft.

---

## Case Layer (pluggable, zero sensitive data)

The case layer is **physically isolated** from the skill layer: the public repo ships only
interface specs, templates, and a fictional sample (`Group A`). Real cases live in
`cases/<your-case>/` and are excluded by `.gitignore`. See `cases/README.md`.

---

## Fused Upstream Capabilities

See [`NOTICE.md`](NOTICE.md) for attribution (Apache-2.0 preserved via `metadata.fused_from`):

- **data-governance** → metric dictionary, named owners, "measured not claimed" quality → `dx-data-quality`
- **des-governance-and-security** → RBAC/RLS, PII classification, retention, HALT gates → `dx-architecture-opt`
- **csv-data-wrangler / duckdb-skills** → tool-selection decision tree + DuckDB profiling → `dx-data-baseline`
- **data-analyst** → What / So What / Now What narrative → `dx-application-plan`

---

## Status

**v2.0 — all 7 skills production-grade**, shared base + case-layer interface complete.
The bottleneck is no longer the skeleton but **case gotchas** — feed it with de-identified
lessons from real projects and the suite gets sharper with every delivery.

---

## License

[Apache-2.0](LICENSE) © 2026 Big Data Hunter (Li Keshun)

---

<sub>Disclaimer: methodology and tooling only — **not** accounting, legal, or investment advice.
Capitalization conclusions must be confirmed by a licensed accounting firm.</sub>
