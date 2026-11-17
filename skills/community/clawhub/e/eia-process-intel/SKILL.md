---
name: eia-process-intel
slug: eia-process-intel
displayName: EIA Process Intelligence
summary: Turn Chinese EIA filings into production-line intelligence — extract facts, audit numbers for regulatory gaming, back-calculate capacity and yield, infer equipment selection, and accumulate a provenance-tracked triple ledger.
license: MIT
description: 'Investigation workflow that turns Chinese EIA filings (环评报告/环评公示) into investment due-diligence intelligence: structured extraction (product scheme, per-step process flow, equipment list, material balance), adversarial field-credibility grading, physics-based cross-validation (low-risk fields as trust anchors to back-calculate capacity/yield/emissions), process-to-equipment mapping inference, and an append-only triple ledger with provenance. Use when: (1) analyzing a company EIA filing or 受理公示, (2) verifying capacity claims / 产能真实性核验, (3) inferring equipment selection from a 设备清单, (4) back-calculating yield from 物料平衡 / material balance, (5) auditing EIA numbers for gaming patterns (批小建大), (6) building a process/equipment fact ledger across deals. Triggers: 环评, EIA report, material balance, equipment list, capacity verification, yield back-calculation, regulatory gaming audit.'
version: 0.3.0
metadata: {"clawdbot":{"emoji":"🏭"}}
agent_created: true
---

# EIA Process Intelligence (环评工艺情报)

Turn Chinese EIA filings (环境影响评价报告 / 报告表 / 受理公示) into investment due-diligence intelligence. The EIA is a rare document the company itself wrote under legal liability and disclosed before construction: equipment lists, material balances and product schemes are mandatory disclosures. This skill reads it adversarially — extract, grade every number for regulatory gaming, cross-validate with low-risk trust anchors, infer process routes and equipment tiers, and book everything into a provenance-tracked triple ledger.

Core move: EIAs almost never disclose per-step yields. Back-calculate end-to-end yield from the material balance (key inputs such as substrates vs chip outputs), then localize the bottleneck step. Worked demo: `examples/format-demo-ir-detector.md` (fictional case, all numbers marked illustrative).

## When to Use

| Situation | Action |
|-----------|--------|
| Analyzing a company EIA filing (环评报告/报告表/公示) | Run the full Phase 0–6 workflow below |
| Verify capacity claims (产能真实性核验) | Capacity back-calc recipes + external permit records |
| Infer process route or equipment tier | Three-face route evidence + `references/mappings/<track>.md` |
| Back-calculate yield from material balance (物料平衡) | Yield recipe + bottleneck localization |
| Audit EIA numbers for distortion | Field grading table + threshold-hugging signatures |
| Reconcile EIA caliber vs BP / interviews / prospectus | Caliber conflict table (report section 2) |
| Build a reusable process/equipment fact base | Ledger schema, append-only JSONL |

## Design principles (override any specific step)

1. **Query first.** Extraction and inference exist only to answer the Seven Questions. Adding an entity/relation/field to the ontology requires at least one real failed query as justification (see `references/ledger-schema.md`).
2. **EIA numbers are not facts.** They are declared calibers negotiated under regulatory gaming. Before any number enters the ledger it must pass two gates: an interest review (which regulatory consequence does it affect, and which direction does distortion help?) and physical cross-validation (low-risk fields back-calculate high-risk fields).
3. **Caliber discipline.** Every fact carries a source (file + page + verbatim quote) and disclosure date. 【Disclosed】and【Inferred】are strictly separated. Back-calculated outputs are always ranges with explicit caliber footnotes — never point values.
4. **One vocabulary.** The process→equipment mapping library IS the ontology vocabulary layer (equipment-class aliases normalized). Mapping files and the ledger share a single equipment-class word list — one asset, not two.

## The Seven Questions (every EIA must answer)

| # | Question | Primary evidence |
|---|----------|------------------|
| 1 | Actual capacity vs financing-story capacity, and build-out pace | Product scheme, construction phases, approval info |
| 2 | Which process route is actually in use | Process sequence + materials + pollutants (three faces) |
| 3 | Equipment selection tier (origin / generation / density) | Equipment list, models, counts vs capacity ratio |
| 4 | Yield and unit consumption; which step is the bottleneck | Material balance |
| 5 | Do pollution fingerprints reveal undisclosed processes | Hazardous chemicals / hazardous waste / special gases |
| 6 | Where EIA caliber contradicts company claims | All fields vs BP / interviews / announcements |
| 7 | Credibility grading and back-calculation of each number | Field grading table below |

## Field credibility grading (v1 prior)

Principle: the more a number affects approval outcome, environmental spend, or regulatory burden, the more it is shaped by gaming between the company and the regulator. Update grades as cross-validation evidence accumulates; a falsified grade changes the table, with the case noted in `references/field-credibility.md`.

| Field | game_risk | Typical distortion direction | Cross-validation path |
|-------|-----------|------------------------------|------------------------|
| Design capacity 设计产能 | High | Both ways: inflate (grab emission quotas, reserve expansion headroom) or deflate (stay under high-level approval thresholds) | Equipment counts × industry cycle time; material inputs; annual hours; permit execution reports |
| Product mix 产品结构 | High | Split SKUs, disguise mass production as pilot/R&D, hide restricted products | Hazardous-waste types, waste-liquid composition, byproducts reveal real products |
| Pollutant generation/emission 污染物 | High | Understate → lower monitoring frequency and treatment specs | Treatment facility design capacity back-calc; industry per-unit factors; execution-report actuals |
| Raw material usage 原辅材料 | Med-high | Understate toxic/hazardous chemicals → smaller buffer zone, lower regulatory class | Material-balance self-consistency; hazwaste ratio; warehouse size |
| Operating hours 设备利用率 | Med-high | Understate annual run hours → lower emission estimates | Implied cycle time from equipment density; power/water consumption |
| Process route 工艺路线 | Medium | Vague or blended wording to dodge specialized review | Pollutant fingerprints; equipment models |
| Equipment count 设备数量 | Med-low | Understate advanced units, omit cross-period equipment | Ratio vs capacity; permit application cross-check |
| Physical info 厂房/排放口/环保设施 | Low | Essentially trustworthy (site-verifiable, later documents cross-check) | **Use as trust anchors** to back-calculate everything above |

### Threshold-hugging signatures (gaming traces)

- Design capacity sits right at an approval-tier boundary (报告书 ↔ 报告表 cutoff)
- One project split into many small EIAs; multiple approvals on one site
- EIA capacity clearly mismatched with permitted (排污许可) capacity — either direction
- Mass-production SKUs declared as "R&D / pilot" (以研发中试名义量产)
- Hazardous-chemical list missing common reagents the declared process requires
- Annual operating hours inconsistent with industry-normal shift patterns

Discovery output: gaming traces (批小建大、化整为零、hidden process steps、pilot-name mass production) go into a dedicated list AND are booked under the ledger relation 博弈痕迹 — they are also governance-DD evidence.

### Interest review: three questions per high-risk number

1. Which regulatory consequence does this number hit — approval tier, total-emission quota, monitoring frequency, or buffer distance?
2. Which distortion direction favors the company, and how large must the distortion be before it is worth the risk?
3. Which physical data (equipment / materials / energy / hazwaste) can bracket this number from both sides?

### Credibility evolution (prior → evidence → posterior)

The grading table is a prior, not a verdict. Every high-risk field evolves within a case:

- **Prior** — game_risk from the table above, assigned at extraction.
- **In-case evidence** — the `status` tag as cross-validation proceeds (申报值 / 已交叉验证 / 与外部冲突).
- **Posterior** — mandatory end state in the report for every high-risk field, one of three: **maintained / upgraded / downgraded** vs prior, each with the deciding evidence in one line. Never leave a high-risk field at its prior without a stated check.

Worked instance: power consumption, prior 中高 → mean-load check found it inconsistent with the line's heating/RF/UPW configuration → posterior **downgraded to "conflicting evidence"**, two competing explanations recorded (caliber distortion vs under-declared utilization), pending utility bills.

**Prior-table feedback rule**: a single-case posterior never edits the grading table. The prior moves only when the same distortion direction is confirmed across ≥2 independent cases, or a hard counter-example appears — with the case list cited in `references/field-credibility.md`.

## Anomaly loops (backtracking protocol)

The phases above are the discipline skeleton, not the route — real investigations loop. Define an **anomaly** as anything that contradicts the current working hypothesis:

1. cross-validation conflict (a trust anchor contradicts a declared number)
2. mapping miss (a step or equipment class with no mapping row)
3. caliber self-inconsistency (numbers within the filing do not cohere)
4. unexpected process/equipment combination for the claimed product

Protocol on hitting an anomaly:
- state it in one sentence and list competing hypotheses (≥2 where possible);
- name the backtrack target — which phase, which table to re-read;
- **every loop ends in a written artifact**: the report conflict section, a gaming-trace entry, or `failed-queries.md`. Never resolve a loop in memory alone;
- cap: if 3 loops do not converge, stop and record it as an open DD question in the report.

Worked instance (nanoimprint acceptance report, 2026-09-10): bottle-scale special-gas usage (anomaly 4) triggered a material-balance re-check → solvent-vs-emission self-consistent, but the same loop surfaced the mean-load power inconsistency (anomaly 3) — one loop, two written artifacts.

## Workflow

### Phase 0 — Acquire the filing (if not provided)

Search in order (field-tested; append as you learn):
1. National EIA disclosure platform (全国建设项目环境影响评价信息公示平台); then provincial / municipal / county ecology-bureau sites, columns 环评受理 / 拟批准 / 审批决定
2. National pollutant-permit platform (全国排污许可证管理信息平台) — permit original + annual execution reports
3. Archives: 尚云环评云助手, 环评爱好者论坛 (for historical versions)

Query patterns: company full name; `项目名 环评报告表`; `项目名 环境影响报告书 受理` + city name. The same project usually has three versions (受理公示 / 拟批准公示 / 审批决定) — the acceptance version is the fullest. 报告表 (short) and 报告书 (full) differ substantially; grab both.

### Phase 1 — Structured extraction

Extract section by section into fact rows, each with source (file + page + verbatim quote) and disclosure date. OCR scanned PDFs first; transcribe tables from table text, never paraphrase.

- Project overview & approval: approval number, date, approval level, EIA preparer, construction nature (新建/扩建/技改)
- Product scheme & capacity: per product, per spec, per construction phase
- Process flow: step by step with pollution-generation marks; transcribe flowchart nodes to text, noted "transcribed from flowchart"
- Equipment list: name / model / count / source (purchased / leased / reused)
- Raw materials & hazardous chemicals: name / annual usage / hazard class
- Material & water balance: per-step inputs and outputs
- Pollution sources & treatment: generation point → pollutant → treatment → discharge destination
- Construction schedule & investment: phase pacing, total and environmental investment

### Phase 2 — Gaming review

Tag every numeric field with `game_risk` (高/中高/中/中低/低, defaults from the grading table) and a distortion direction (虚增/虚减/拆分). Run the three interest-review questions on every high-risk field. Sweep for the threshold-hugging signatures.

### Phase 3 — Cross-validation

Use low-risk trust anchors (equipment counts, floor area, outfall locations, treatment facility sizes — site-verifiable, later documents cross-check) to back-calculate high-risk fields. Then narrow with external sources, in order of availability:

1. Pollutant-permit platform: permit original (capacity / limits / treatment) + annual execution reports (actual emissions / output)
2. Hazardous-waste transfer manifests / hazwaste operating licenses (disposal volume back-calculates waste generation)
3. Credit China / local environmental penalty records
4. Prospectuses / annual reports: construction-in-progress, machinery original value, transfers-to-fixed-assets (vs equipment list)
5. Procurement/bidding sites, customs data (imported equipment model clues)

Tag every field `status`: `申报值` (declared only) / `已交叉验证` (≥1 independent path, recorded) / `与外部冲突` (conflicting evidence exists — never overwrite the number, the conflict itself goes into the report).

### Phase 4 — Inference

- **Process route**: cross the three faces — process sequence, material inputs, pollutant fingerprints (e.g. T2SL vs VOx; monolithic vs two-piece packaging; dry vs wet process). Cite which face supports what.
- **Equipment tier**: load `references/mappings/<track>.md`, walk 工序→设备类别→档次信号→国别/代表厂商. A step missing from the mapping gets tagged 【映射缺失】and enters the backlog — never improvise a mapping on the spot.
- **Yield / unit consumption**: material balance → end-to-end yield range + bottleneck step. Footnote mandatory: "estimated under EIA-caliber self-consistency; understated inputs shift the range — use external sources to tighten."
- **CAPEX intensity**: equipment counts × market price bands (externally quoted) → investment per unit capacity, vs financing amount and capacity promises.

Everything inferred is tagged 【推断】with the chain written out: which facts → which rule → which conclusion.

### Phase 5 — Report (fixed five sections, Markdown)

1. Structured fact table (with source / game_risk / status)
2. EIA caliber vs company caliber comparison table
3. Gaming-trace list
4. Inference summary (process route / equipment tier / yield range / CAPEX intensity)
5. Interview question list — every missing, vague, or conflicting EIA point becomes a DD question

### Phase 6 — Book into the ledger

Append triples per `references/ledger-schema.md`. Rules: append-only JSONL, one file per track, stored in the DD project workspace `{project dir}/eia-ledger/<track>.jsonl` — never in this skill directory. Every record carries source / game_risk / status / disclosure date / booking date. Queries the ontology cannot answer go to `failed-queries.md` in the same directory; the schema only moves when real failed queries justify it.

```json
{"s":"X-Detek (fictional)","p":"拥有","o":"T2SL detector line project (fictional)","q":{"建设性质":"新建"},"source":{"file":"x-detek-eia-20XX-acceptance.pdf (fictional)","page":12,"quote":"本项目新建…"},"game_risk":"低","status":"申报值","disc_date":"20XX-06","added":"2026-09-09"}
```

Ledger skeleton: 8 entities (公司/项目/产品/工序/设备/设备类别/物料/污染物) × 8 relations (拥有/包含工序/使用设备/归类/投入/产出/排放/博弈痕迹), each fact tagged game_risk + status. Full definitions, attribute scopes, and the schema-growth mechanism: `references/ledger-schema.md`.

## Cross-case aggregation (cases must query each other)

The ledger becomes an intelligence system only when cases call each other. At the end of every engagement, after Phase 6, run three standard aggregations over the track's ledger file(s) — plain grep/join over JSONL, no new infrastructure:

1. **Capacity-vs-equipment ratio** — all projects in the track: capacity ÷ key-equipment counts. What ratio range does a given configuration imply?
2. **Per-process emission intensity** — same process across companies: emissions ÷ capacity, to flag outliers in either direction.
3. **Same-equipment fingerprint** — a model/class appearing across projects, consolidating vendor and tier signals.

**Two-layer write rule — never fuse them:**

- **Fact layer**: aggregation output lands in `{project dir}/eia-ledger/cross-case-results.md` (dated; query type; cases involved; raw result). This is data, not knowledge.
- **Judgment layer**: the mapping library updates **only** on a stable pattern (≥2 independent cases pointing the same way) or a clear counter-example — never directly from one aggregation run. The rationale column cites the case results that justify it.

## Mapping library maintenance (`references/mappings/`)

One file per track; row shape: EIA signal (process / pollutant / hazchem keywords) → equipment class (vocabulary) → tier signal → country / representative vendors → rationale. Append rows after every engagement; no evidence, no row; uncertain rows marked 【待验证】with the verification path. Renaming an equipment class is a vocabulary change — sync `references/ledger-schema.md` in the same commit.

## File map

| File | Contents |
|------|----------|
| `references/field-credibility.md` | Grading table rationale, v1 prior, update log |
| `references/cross-validation.md` | Full recipes: capacity (cycle-time / material / energy), yield, emissions, product-mix fingerprints; status rules |
| `references/ledger-schema.md` | Ontology minimal set (8×8), JSONL format, failed-query growth mechanism |
| `references/mappings/semiconductor-equipment.md` | Seed mapping ~22 rows (semiconductor / IR detector / nanoimprint) |
| `examples/format-demo-ir-detector.md` | Fictional worked example: yield 18–26% back-calculated from material balance |
