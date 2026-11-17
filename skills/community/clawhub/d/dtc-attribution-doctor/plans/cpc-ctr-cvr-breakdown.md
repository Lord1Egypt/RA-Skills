# Plan: CPC/CTR/CVR Breakdown (cpc-ctr-cvr-breakdown)

## 1. Metadata

- **version**: 0.1.0
- **suite**: Performance Marketing Copilot
- **functions.md scenario (mapping key)**: CPC / CTR / CVR拆解诊断
- **requires functions.md version**: `1.1.0` — verified in §4; on mismatch, halt.
- **dev status**: in-development
- **related files**:
  - data: `functions.md` §1 interfaces (primary `#4 ad_analysis_list`; optional `#8 meta_query` / `#9 google_query`), `access.yaml`
  - report assembly: `functions.md` §3
  - chained plans: `creative-performance`, `creative-fatigue`, `site-funnel-diagnosis`, `roas-decline-diagnosis`, `cpa-rise-diagnosis`
  - on-the-fly artifacts: `utilities/`
- **analysis approach**: a granular ad-funnel lever decomposition: `impressions → clicks (CTR, CPC) → conversions (CVR)`. Pinpoint which lever broke at the campaign/ad level, isolating cost-of-click (CPC) from click-rate (CTR) and post-click conversion (CVR). This plan is often chained from `roas-decline-diagnosis` or `cpa-rise-diagnosis` to localize the exact rung that failed.
- **solution space**: a pinpoint verdict on which funnel lever broke and at what level (campaign/ad) + the matching specialist plan to chain. Recommendations only; human-executed.

## 2. Trigger & Boundary

- **Invocation**: always invoked by SKILL.md routing (no auto-trigger).
- **Intent examples that route here**: "break down CTR and CVR", "is it CPC or CVR", "where in the funnel are we losing it", "CTR dropped but conversions held".
- **Boundary**: this plan decomposes and localizes the lever; it does NOT fix the creative or the landing experience — it hands off to the matching specialist plan.
- **Pre-flight clarification (converge BEFORE fetching; skip what's known from memory/context):**
  1. **Period & comparison?** (default = last full week vs prior equal week)
  2. **Scope & granularity — which channel, and campaign vs ad level?** (if named, scope to it; else main-spend channel, campaign first)
  3. **Attribution model?** (default `First click`; both periods must match)

## 3. Pre-flight Checks

- **tier**: Basic. Empty `records` → distinguish "no data" vs "tier not open"; never fabricate.
- **business prerequisites**: period, `model`, `goal` (confirm via `#1 setting_goals`, default `purchase`).
- **caliber**: CVR is measured on **true** conversions (`conversions`); decisions use true `roas`, not `ad_net_roas`. Both periods equal length, same `model`/`goal`.

## 4. Data Context Preparation

- **functions.md version gate**: built against `functions.md` **`1.1.0`**. On load, read the version in functions.md Metadata; **if it differs, STOP**: tell the user "Data cannot be prepared — functions.md version mismatch (plan expects 1.1.0, found <X>); the data contract may have changed." and terminate.
- **fetch plan**:

| Step | Interface | Params template | Purpose |
|------|-----------|-----------------|---------|
| a | `#4 ad_analysis_list` (current + prior, channel/campaign) | `{start_date,end_date,dimensions:"campaign",model,goal}` ×2 | impressions/clicks/ctr/cpc/cvr/conversions per campaign → find the broken lever |
| b | `#4 ad_analysis_list` (drill to ad) | `{...,dimensions:"ad"}` | confirm whether the break is campaign-wide or specific ads |
| c | `#8/#9` passthrough (optional) | platform-native fields | confirm a platform-side delivery/auction shift only |

- **caliber reminders**: see §1 of functions.md; key here — CVR on `conversions`; `roas` vs `ad_net_roas` not mixed.

## 5. Analysis Steps (Data → Analyze → Compare → Conclude → Next)

1. **Data**: fetch a (campaign, both periods); drill b to ad level where a campaign moved.
2. **Analyze — walk the funnel rungs**:
   - `clicks = impressions × CTR`; `CPC = spend / clicks`; `conversions = clicks × CVR`.
   - Identify which rung moved most: CTR (click-through), CPC (cost of click), or CVR (post-click conversion).
   - Distinguish a CTR drop (creative/relevance) from a CPC rise (auction cost) — both lower efficiency but route differently.
3. **Compare**: per campaign/ad, Δ% of impressions / ctr / cpc / cvr / conversions vs prior; tag 🟡/🔴.
4. **Conclude**: name the **broken lever + level** (e.g., "Campaign X: CTR −40% concentrated in 2 ads; CPC and CVR stable").
5. **Next**: route per the lever table (§7).

**Lever ladder (symptom → diagnosis → next):**

| Symptom | Diagnosis | Next plan |
|---------|-----------|-----------|
| CTR ↓ | creative fatigue / weak hook / relevance | `creative-performance` → `creative-fatigue` |
| CPC ↑, CTR ~ | auction cost / bid pressure | `roas-decline-diagnosis` / `cpa-rise-diagnosis` |
| CVR ↓ (clicks ok) | landing/offer/funnel issue | `site-funnel-diagnosis` |
| Multiple rungs move | feed up to parent diagnosis | `roas-decline-diagnosis` / `cpa-rise-diagnosis` |

## 6. Output

- **(A) Direct single-scenario call** — may render the self-contained template below.
- **(B) Inside a daily/weekly/monthly or suite report** — no own template; defer to `functions.md` §3 assembly; supply only the blocks below.

**Self-contained template (mode A only):**

```markdown
# CPC/CTR/CVR Breakdown — <period>
**Shop:** <shop>　**Range:** <current> vs <prior>　**Model:** <model>　**Scope:** <channel / campaign / ad>

## Verdict
Broken lever: <CTR / CPC / CVR> at <level>. <one-line evidence>.

## Funnel decomposition
| Lever | Current | Prior | Δ% | Status |
|-------|---------|-------|----|--------|
(impressions, ctr, cpc, clicks, cvr, conversions)

## Next Step
<which specialist plan to run; "recommendation, pending human execution">
```

**Blocks to feed assembly (mode B):**
- metric block: per-campaign/ad impressions, ctr, cpc, clicks, cvr, conversions — current/prior/Δ%/status.
- diagnosis block: broken lever + level + evidence.
- recommendation block: next specialist plan(s); mark "recommendation, pending human execution".

## 7. Chaining & Notes

**Chaining**: CTR → `creative-performance` / `creative-fatigue`; CVR → `site-funnel-diagnosis`; multi-rung or cost → feeds `roas-decline-diagnosis` / `cpa-rise-diagnosis`.

**Data notes:**
- Equal-length windows, same model — otherwise the funnel deltas are meaningless.
- CVR uses true `conversions`; do not read CVR off platform `ad_net_roas`-implied conversions.
- A CTR drop and a CPC rise are different stories even when both raise CPC-per-result; state which.
- Very short windows are noisy on CVR (fulfillment/refund lag); use ≥ 7 days for trend.
- Empty `records` ≠ 0 — handle per §3; never fabricate.
