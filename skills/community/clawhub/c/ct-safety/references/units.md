# Capability Units

> Schema: Input / Output / Dependencies / AI autonomy / Composition interface
> Designed per ct-base `BASE.md` §6. AI autonomy: ⬛ fully automatic / 🟨 semi-automatic (confirmation required) / ⬜ assistive.

---

## U1: fetch_faers / FAERS fetch

- Input: drug name `drug`, optional event `event` (MedDRA PT), fetch field `field`, top N `top`
- Output: `{"source":"FAERS","drug","event?","drug_total","grand_total","top_events":[...],"counts?":{a,b,c,d,...}}` JSON
- Depends on: none (entry)
- AI autonomy: 🟨 semi-automatic (confirm drug/event name)
- Composition interface: → U2
- Note: openFDA public API, no key needed (low frequency), zero WAF/anti-bot, direct `requests` connect; optional `--api-key` raises quota.

## U2: disproportionality / signal detection

- Input: U1 `counts` (a/b/c/d) or explicit 2×2 table
- Output: PRR / ROR / IC estimates + 95% CI + signal verdict `{signal_overall}`
- Depends on: U1
- AI autonomy: ⬛ fully automatic
- Composition interface: → U3
- Note: Pure local statistics, no network. Signal verdict: ROR lower-CI > 1; PRR ≥ 2 and χ² ≥ 4; IC lower-CI > 0. Any positive indicates a signal.

## U3: report / report output

- Input: U2 signal result (+ optional U4 CN-PV result)
- Output: Markdown report (primary) + JSON (optional) + PNG charts (optional); CN-PV rendered as a distinct qualitative block
- Depends on: U2 (and U4 when `--with-cn-pv`)
- AI autonomy: 🟨 semi-automatic (confirm output format)
- Composition interface: → `ct-protocol` / `ct-registry` (chained call)

## U4: fetch_cn_pv / China official PV bulletin search (qualitative enrichment)

- Input: drug name `drug` (Chinese preferred), optional `drug_en`, `event` (event keyword), `terms` (extra AND keywords), `max_per_column`
- Output: `{"source":"CN-PV (cdr-adr.org.cn)","hit_count","hits":[{title,column,date,url,snippet,matched_keywords}]}` JSON
- Depends on: none (independent enrichment); feeds U3 as a qualitative corroboration block
- AI autonomy: 🟨 semi-automatic (confirm drug / event Chinese terms)
- Composition interface: → U3 (report block)
- Note: scrapes public cdr-adr.org.cn columns (no WAF, no key, zero egress). NMPA main site is WAF-blocked (HTTP 412) and excluded. **NARRATIVE bulletins only — NOT case counts — must NOT enter disproportionality (PRR/ROR/IC).** Samples the latest N per column, not the full archive.

---

## Pipeline

```
input(drug [+ event]) → U1(fetch_faers) → U2(disproportionality) → U3(report) → output
                                                  ↑                         │
                              U4(fetch_cn_pv, optional) ──────────────────┘ (qualitative block)
                                                  └─→ ct-protocol / ct-registry
```

> FAERS remains the sole QUANTITATIVE source (U1→U2→U3). U4 (cdr-adr.org.cn) is an optional QUALITATIVE enrichment — it never feeds the 2x2 table. All computation local; ordinary input + public retrieval (B-tier).
