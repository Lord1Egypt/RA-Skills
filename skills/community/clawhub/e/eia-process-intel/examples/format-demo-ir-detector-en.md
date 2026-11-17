# Worked Example: Fictional IR-Detector Company EIA · Format Demo (Phase 1→6)

> This file demonstrates the skill's standard output format. **The case is entirely fictional**: the company (X-Detek), site, year, and numbers are invented for teaching purposes and correspond to no real company or filing; the industry setting (T2SL cooled IR detectors) is generic industry knowledge. Numbers marked 【示例值】(illustrative) are placeholders. Not investment advice.

## Input

- Target: X-Detek (fictional; T2SL cooled IR detector chips, an industrial-park site)
- Filing: 20XX project EIA, acceptance-disclosure version (fictional)
- Company claim (background): marketing covers 640×512@15μm, 320×256 cooled detector products【示例值】

---

## 1. Structured fact table (excerpt)

| Field | Content | game_risk | status | source |
|-------|---------|-----------|--------|--------|
| Product scheme | 640×512@15μm, 320×256 T2SL detector chips【示例值】 | High (product mix) | declared | EIA · product scheme p.【示例值】 |
| Process flow | MBE epitaxy → litho → etch → deposition → flip-chip interconnect → dewar/cooler packaging | Medium (route) | declared | EIA · process chapter (transcribed from flow diagram) |
| Equipment list | MBE systems ×N【示例值】, litho/etch/deposition tools | Med-low (trust anchor) | declared | EIA · equipment table |
| Raw materials | GaSb substrates N pcs/yr【示例值】, III/V source materials | Med-high | declared | EIA · materials table |
| Specialty gases | Arsine, phosphine, etc.【示例值】 | Med-high | declared | EIA · hazchem list |
| Hazardous waste | Arsenic-bearing waste liquid, scrap substrates | Med-high | declared | EIA · hazwaste chapter |

## 2. Gaming review

- **Capacity (high)**: distortion possible both ways — inflate for quota/headroom; understate to avoid higher-tier approval. Check distance to the report-form/report tiering threshold【示例值, to compute】
- **Materials (med-high)**: if GaSb substrate usage is understated, apparent yield rises in tandem — discount the upper bound of the yield range
- **Equipment count (med-low)**: use as trust anchor for capacity back-calculation
- **Three interest-review questions** (substrate usage as the example): ① affects hazardous-waste generation and protection-distance computation; ② understatement is the favorable direction (less arsenic waste, smaller distance); ③ physical bracketing — chip output ÷ yield implies a minimum substrate demand

## 3. Cross-validation

- **Cycle-time method**: MBE units × growth time per wafer【示例值】 × annual effective hours → epitaxy capacity ceiling, vs. declared capacity
- **Material balance (material-balance method)**: GaSb substrate input vs. chip output → end-to-end yield range **18–26%【示例值】**. Caliber footnote: estimated under EIA-caliber self-consistency, not the true yield; understated substrates shift the real value away from this range
- **External checks**: permit execution report (pending); arsenic-waste transfer manifests (pending)
- status updates: capacity → cross-validated (cycle-time method, medium confidence); yield → cross-validated (material balance, medium confidence)

## 4. Inference summary

- Process route 【inferred】: T2SL cooled — MBE equipment fingerprint + arsine specialty gas + GaSb substrate, three evidence faces consistent
- Equipment selection 【inferred】: MBE is the core bottleneck tool; country-of-origin lead 【to verify】 against the equipment-source column
- Yield bottleneck 【inferred】: epitaxy and flip-chip interconnect (largest loss distribution)
- CAPEX intensity 【inferred】: MBE count × market price range (tens of M RMB per unit【示例值】) → investment intensity per unit capacity; to be narrowed with external quotes

## 5. Interview question list

1. Differences between the EIA equipment list and actually installed equipment (cross-phase, leased, held by others)?
2. Yield distribution in MBE batch records — how far from the EIA material-balance caliber?
3. Capacity split and switching cost between the two product lines?
4. Disposal contracts and transfer manifests for arsenic-bearing waste (validates true waste generation)?

## 6. Ledger booking (`{project dir}/eia-ledger/ir-detector.jsonl`)

```json
{"s":"X-Detek (fictional)","p":"owns","o":"T2SL detector line project (fictional)","q":{"construction":"new build"},"source":{"file":"x-detek-eia-20XX.pdf (fictional)","page":0,"quote":"【示例值】"},"game_risk":"low","status":"declared","disc_date":"20XX-06","added":"2026-09-09"}
{"s":"Epitaxy step","p":"uses_equipment","o":"MBE system","q":{"count":"【示例值】"},"source":{"file":"x-detek-eia-20XX.pdf (fictional)","page":0,"quote":"【示例值】"},"game_risk":"med-low","status":"declared","disc_date":"20XX-06","added":"2026-09-09"}
{"s":"Epitaxy step","p":"consumes","o":"GaSb substrate","q":{"annual usage":"【示例值】"},"source":{"file":"x-detek-eia-20XX.pdf (fictional)","page":0,"quote":"【示例值】"},"game_risk":"med-high","status":"declared","disc_date":"20XX-06","added":"2026-09-09"}
{"s":"Epitaxy step","p":"produces","o":"T2SL detector chip","q":{"capacity":"【示例值】"},"source":{"file":"x-detek-eia-20XX.pdf (fictional)","page":0,"quote":"【示例值】"},"game_risk":"high","status":"declared","disc_date":"20XX-06","added":"2026-09-09"}
```

`failed-queries.md` example:

```
20XX-09-09 | "What is the industry percentile for end-to-end T2SL yield?" | gap type: missing industry baseline (no anchor entity for yield benchmarks) → record only, add nothing, revisit when similar queries accumulate
```
