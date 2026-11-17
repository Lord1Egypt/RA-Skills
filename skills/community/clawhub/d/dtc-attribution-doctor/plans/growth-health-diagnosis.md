# Plan: Growth Health Diagnosis (growth-health-diagnosis)

## 1. Metadata

- **version**: 0.1.0
- **suite**: Growth Command Center
- **functions.md scenario (mapping key)**: 增长健康度诊断
- **requires functions.md version**: `1.1.0` — verified in §4; on mismatch, halt.
- **dev status**: in-development
- **related files**:
  - data: `functions.md` §1 interfaces (primary `#6 all_attribution_sum`, `#5 all_attribution_list`, `#4 ad_analysis_list`), `access.yaml`
  - report assembly: `functions.md` §3 (cadence / role tailoring / tone / shared template)
  - chained plans: `channel-roas`, `roas-decline-diagnosis`, `funnel-analysis`, `budget-expansion` (to be built)
  - on-the-fly artifacts: `utilities/` (charts / web pages, as needed)
- **analysis approach**: a growth "radar". Take a small set of core dashboard metrics (GMV, true ROAS, new-customer share, profit, blended ROAS), compare against a prior period, flag yellow/red anomalies, then ROUTE each anomaly to a specialist plan. This plan does not do deep root-cause; it finds problems, ranks them, and dispatches.
- **solution space**: a Growth Health rating (Healthy / Watch / Alert) + a ranked anomaly list (by impact × deviation) + a next-step per anomaly (which plan to chain into). It does NOT issue spend/budget/bid changes (those belong to downstream plans and require human execution).

## 2. Trigger & Boundary

- **Invocation**: this plan is ALWAYS invoked by SKILL.md routing. It has **no auto-trigger** of its own.
- **Intent examples that make SKILL route here**: "check overall growth health", "how did last week look", "is our growth okay", "growth health check".
- **Boundary**: this plan only does the dashboard check + dispatch. Once a concrete channel / conversion / budget issue is located, HAND OFF to the matching specialist plan (see §7); do not expand deep root-cause here.
- **Pre-flight clarification (converge BEFORE fetching; skip any item already known from memory/context):**
  1. **Period & cadence?** (daily / weekly / monthly / custom; default = last full calendar week)
  2. **Target role?** (drives report tailoring & tone; default = Founder / MD view)
  3. **Attribution model?** (default `First click`; only differs if the user is doing model comparison)
  4. **Health thresholds — confirm or override.** Present the default threshold table (§5) and ask the user to either confirm the defaults or input their own (e.g. their break-even ROAS, acceptable GMV swing). **If the platform supports persistent memory, write the confirmed/overridden thresholds to `memory.md`** (shop-level baseline) so future runs reuse them without re-asking.

## 3. Pre-flight Checks

- **tier**: Basic (current matrix is all Basic). If an interface returns empty `records`, first decide whether it is "no data in range" or "capability not open at this tier" — never fabricate conclusions from empty data.
- **business prerequisites**:
  - required: analysis period, `model`, `goal` (confirm available goal via `#1 setting_goals`; default `purchase`).
  - optional: profit fields (`profit` / `margin`) require COGS configured in Convbox; if absent, mark profit items "unavailable" and continue with GMV / ROAS / new-customer parts. *(`margin` is a decimal, not a percent — ×100 before display/threshold compare.)*
- **required inputs**: period, role, model (resolved via clarification / memory).

## 4. Data Context Preparation

- **functions.md version gate**: this plan was built against `functions.md` version **`1.1.0`**. On load, read the version in functions.md Metadata. **If it differs, STOP**: tell the user "Data cannot be prepared — functions.md version mismatch (plan expects 1.1.0, found <X>); the data contract may have changed." and **terminate the analysis** (do not proceed on a stale/ahead contract).
- **fetch plan** (pick the relevant interfaces from functions.md §1):

| Step | Interface | Params template | Purpose |
|------|-----------|-----------------|---------|
| a | `#1 setting_goals` | `{}` | confirm goal (first time / when unsure) |
| b | `#6 all_attribution_sum` | `{start_date,end_date,dimensions:"channel",model,goal}` | **overall anchor**: current-period dashboard (spend / conversion_value / roas / ad_net_roas / profit / margin / conversions / new_lead_conversions) |
| c | `#6 all_attribution_sum` (prior period) | same as b, prior equal-length window | period-over-period delta (same model) |
| d | `#5 all_attribution_list` | `{...,dimensions:"channel",sort_by:"main_conversions",sort:"desc"}` | channel breakdown to find driver / drag channels. 🔴 sort_by:"conversion_value" silently returns empty — sort server-side by main_conversions, rank by `conversion_value` in-kernel |
| e | `#4 ad_analysis_list` (on demand) | `{...,dimensions:"channel"}` | paid-side dual-caliber drill (only if b/d show paid anomaly) |

> `dimensions` takes a **single string value** (e.g. `"channel"`), not an array — an array collapses to one bogus aggregate row. To split by multiple dimensions, call the interface once per dimension. (ad_analysis's `dimensions` is already a string.)

- **caliber reminders (specific to this scenario)**:
  - **True ROAS = `roas`**; `ad_net_roas` is reference only, gap = platform over-reporting. Health judgement uses `roas` only.
  - **New-customer share = `new_lead_conversions / conversions`** (this API has no `new_order_roas`; approximate new-customer strength by share — do not invent fields).
  - **Blended ROAS (≈ MER proxy) = Σ`conversion_value` / Σ`spend`**; this is the ATTRIBUTION caliber, not store-level revenue/MER (current API has no backend total-revenue field) — state this in the note.
  - Both periods must be **equal length, same `model`, same `goal`**.

## 5. Analysis Steps (Data → Analyze → Compare → Conclude → Next)

1. **Data**: fetch b/c (two-period sums); fetch d (channel breakdown) when needed.
2. **Analyze**: compute current-period core metrics — GMV (`conversion_value`), true ROAS, new-customer share, profit / margin (if available), blended ROAS.
3. **Compare**: for each metric compute `Δ% = (current − prior) / prior` and tag ✅/🟡/🔴 by the confirmed thresholds.
4. **Conclude**: roll up into a **Growth Health rating** — any core metric 🔴 → Alert; only 🟡 → Watch; all ✅ / mild 🟡 → Healthy. List anomalies ranked by impact × deviation.
5. **Next (dispatch)**: route each anomaly to a specialist plan (§7); state "issue → which plan to run next".

**Default health thresholds** (shown to the user in §2 for confirm/override; may be overridden by shop baseline):

| Metric | 🟡 Watch | 🔴 Alert |
|--------|----------|----------|
| GMV Δ% | −10%~−20% | < −20% |
| True ROAS Δ% | −10%~−20% | < −20% |
| True ROAS absolute (vs break-even ROAS) | 1.0×~1.2× break-even | < break-even |
| New-customer share Δ | −5pt~−10pt | < −10pt |
| Profit / margin Δ% (if available) | −15%~−25% | < −25% |
| Platform over-report gap (ad_net_roas−roas)/ad_net_roas | 30%~50% | > 50% |

## 6. Output

This plan has **two output modes**:

- **(A) Direct single-scenario call** — when the user invokes THIS scenario on its own, the plan MAY render the self-contained template below.
- **(B) Inside a daily / weekly / monthly or any suite report** — do NOT use this template. Defer to `functions.md` §3 assembly (cadence / role / tone / shared template) and only supply the blocks listed below.

**Self-contained template (mode A only):**

```markdown
# Growth Health Diagnosis — <period>
**Shop:** <shop>　**Range:** <current>　**vs:** <prior>　**Model:** <model>

## Health Rating: <Healthy / Watch / Alert>
<one-line verdict + the 1–2 highest-priority actions>

## Core Metrics
| Metric | Current | Prior | Δ% | Status |
|--------|---------|-------|----|--------|
(GMV, True ROAS [+ad_net_roas ref & gap], New-customer share, Profit/Margin*, Blended ROAS≈MER)

## Anomalies (ranked by impact × deviation)
| Metric | Deviation | Driver channel | Next plan |

## Next Steps
<chained plans to run; mark "recommendation, pending human execution">
* Profit shown only if COGS configured.
```

**Blocks to feed assembly (mode B):**
- **metric block**: GMV, true ROAS (with ad_net_roas reference + gap), new-customer share, profit/margin (if available), blended ROAS — each with current / prior / Δ% / status.
- **diagnosis block**: Growth Health rating + ranked anomaly list (metric, deviation, driver channel).
- **recommendation block**: per anomaly, the next specialist plan to chain into; mark "recommendation, pending human execution".

## 7. Chaining & Notes

**Chaining (detect → trigger):**

| Detected | Trigger plan |
|----------|--------------|
| A channel drags true ROAS / large platform over-report | `channel-roas` → if needed `roas-decline-diagnosis` |
| Conversion / CVR anomaly | `funnel-analysis` |
| Budget / scaling signal | `budget-expansion` / budget pacing |
| New-customer share deteriorating | new-customer growth contribution (plan TBD) |

**Data notes:**
- Very short windows (single day) are skewed by fulfillment/refund lag; a health check should use ≥ 7 days.
- Promo week vs normal week direct comparison misleads — flag campaign factors in the note (use YoY when needed).
- If COGS is missing, degrade only the profit items and say so; keep the rest.
- Empty `records` ≠ 0 — handle per §3; never fabricate.
