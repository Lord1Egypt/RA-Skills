# Plan: CPA Rise Diagnosis (cpa-rise-diagnosis)

## 1. Metadata

- **version**: 0.1.0
- **suite**: Performance Marketing Copilot
- **functions.md scenario (mapping key)**: CPA上升诊断
- **requires functions.md version**: `1.1.0` — verified in §4; on mismatch, halt.
- **dev status**: in-development
- **related files**:
  - data: `functions.md` §1 interfaces (primary `#4 ad_analysis_list`, `#5 all_attribution_list`; optional `#8 meta_query` / `#9 google_query`), `access.yaml`
  - report assembly: `functions.md` §3
  - chained plans: `creative-fatigue`, `site-funnel-diagnosis`, `landing-page-reception`, `ad-audience-performance`, `roas-decline-diagnosis`
  - on-the-fly artifacts: `utilities/`
- **analysis approach**: when **CPA** (`spend / conversions`) rises period-over-period, split the cause into the **cost side** (CPM/CPC up → auction pressure / audience saturation) vs the **conversion side** (CTR/CVR down → weaker click-through or on-site conversion). Compare **new-customer CPA** (`spend / new_lead_conversions`) against blended CPA to see whether acquisition specifically got more expensive. Drill channel → campaign and separate a genuine efficiency loss from a mere delivery/mix change.
- **solution space**: a ranked root-cause verdict (which channel, cost-side vs conversion-side lever) + the matching specialist plan to chain. Recommendations only; spend/bid changes are human-executed downstream.

## 2. Trigger & Boundary

- **Invocation**: always invoked by SKILL.md routing (no auto-trigger).
- **Intent examples that route here**: "CPA went up", "our cost per acquisition is rising", "customers are getting more expensive", "Meta CPA spiked this week".
- **Boundary**: this plan diagnoses the CPA rise and names the broken lever; it does NOT execute creative/audience/landing fixes — it hands off to the matching specialist plan.
- **Pre-flight clarification (converge BEFORE fetching; skip what's known from memory/context):**
  1. **Period & comparison?** (default = last full week vs prior equal week)
  2. **Scope — overall or specific channel(s)?** (if the user named a platform, scope to it; else diagnose at channel level then drill the worst)
  3. **CPA caliber — blended or new-customer?** (default report both; decisions weigh new-customer CPA)

## 3. Pre-flight Checks

- **tier**: Basic. Empty `records` → distinguish "no data" vs "tier not open"; never fabricate.
- **business prerequisites**: period, `model`, `goal` (confirm via `#1 setting_goals`, default `purchase`). Profit fields optional (need COGS); CPA diagnosis itself does not require profit.
- **caliber**: CPA derived from **true** `conversions` / `new_lead_conversions`; decisions use true `roas`, not `ad_net_roas`. Both periods equal length, same `model`/`goal`.

## 4. Data Context Preparation

- **functions.md version gate**: built against `functions.md` **`1.1.0`**. On load, read the version in functions.md Metadata; **if it differs, STOP**: tell the user "Data cannot be prepared — functions.md version mismatch (plan expects 1.1.0, found <X>); the data contract may have changed." and terminate.
- **fetch plan**:

| Step | Interface | Params template | Purpose |
|------|-----------|-----------------|---------|
| a | `#5 all_attribution_list` (current + prior) | `{start_date,end_date,dimensions:"channel",model,goal}` ×2 | per-channel spend / conversions / new_lead_conversions → blended & new-customer CPA Δ; locate the channel driving it |
| b | `#4 ad_analysis_list` (drill the worst channel) | `{...,dimensions:"campaign"}` (then `ad_set`/`ad` if needed) | cost-side (cpm/cpc) vs conversion-side (ctr/cvr) levers; campaign-level CPA |
| c | `#8/#9` passthrough (optional) | platform-native fields | confirm a platform-side auction/cost change only |

- **caliber reminders**: see §1 of functions.md; key here — blended CPA uses `conversions`, new-customer CPA uses `new_lead_conversions`; `roas` vs `ad_net_roas` not mixed.

## 5. Analysis Steps (Data → Analyze → Compare → Conclude → Next)

1. **Data**: fetch a (per channel, both periods); drill b on the worst channel.
2. **Analyze — decompose the CPA rise**:
   - `CPA = spend / conversions`. Did `spend` rise, `conversions` fall, or both?
   - **Cost side**: walk `cpm → cpc`. Rising CPM/CPC with stable CTR ⇒ auction pressure / audience saturation.
   - **Conversion side**: walk `ctr → cvr`. Falling CTR ⇒ creative; falling CVR ⇒ landing/funnel.
   - **New vs blended**: compute new-customer CPA (`spend / new_lead_conversions`); if it rose faster than blended CPA, acquisition specifically got more expensive (not just a returning-customer mix shift).
3. **Compare**: per channel, Δ% of CPA / new-CPA / spend / cpm / cpc / ctr / cvr vs prior; tag 🟡/🔴.
4. **Conclude**: name the **primary driver channel + cost-side vs conversion-side lever** (e.g., "Meta CPA +34%: CPM auction pressure, conversion levers intact").
5. **Next**: route per the root-cause table (§7).

**Root-cause ladder (symptom → diagnosis → next):**

| Symptom | Diagnosis | Next plan |
|---------|-----------|-----------|
| CPM/CPC ↑, CTR ~ | auction pressure / audience saturation | `ad-audience-performance` |
| CTR ↓ | creative fatigue / weak hook | `creative-fatigue` |
| CVR ↓ (clicks ok) | landing/offer/funnel issue | `site-funnel-diagnosis` → `landing-page-reception` |
| New-CPA ↑ ≫ blended-CPA | acquisition efficiency loss | `ad-audience-performance` |
| CPA ↑ with roas ↓ | broad efficiency erosion | `roas-decline-diagnosis` |

## 6. Output

- **(A) Direct single-scenario call** — may render the self-contained template below.
- **(B) Inside a daily/weekly/monthly or suite report** — no own template; defer to `functions.md` §3 assembly; supply only the blocks below.

**Self-contained template (mode A only):**

```markdown
# CPA Rise Diagnosis — <period>
**Shop:** <shop>　**Range:** <current> vs <prior>　**Model:** <model>　**Scope:** <overall / channel>

## Verdict
Blended CPA <X → Y, ΔZ%> (new-customer CPA <A → B, ΔC%>). Primary driver: <channel> — <cost-side / conversion-side lever>.

## Decomposition (driver channel)
| Lever | Current | Prior | Δ% | Status |
|-------|---------|-------|----|--------|
(CPA, new-CPA, spend, cpm, cpc, ctr, cvr)

## Next Step
<which specialist plan to run; "recommendation, pending human execution">
```

**Blocks to feed assembly (mode B):**
- metric block: overall + per-channel blended CPA & new-customer CPA, spend, cpm/cpc/ctr/cvr — current/prior/Δ%/status.
- diagnosis block: primary driver channel + cost-side vs conversion-side lever + evidence.
- recommendation block: next specialist plan(s); mark "recommendation, pending human execution".

## 7. Chaining & Notes

**Chaining**: see the root-cause ladder (§5) — CTR → `creative-fatigue`; CVR → `site-funnel-diagnosis` / `landing-page-reception`; CPM/audience → `ad-audience-performance`; broad erosion → `roas-decline-diagnosis`.

**Data notes:**
- Equal-length windows, same model — otherwise the decomposition is meaningless.
- Blended CPA (`conversions`) and new-customer CPA (`new_lead_conversions`) are distinct calibers; report which one moved.
- A rising CPA can be pure delivery/mix change, not efficiency loss — separate the two explicitly.
- Profit/margin commentary requires COGS configured; if absent, stay on spend/conversion CPA and say so.
- Empty `records` ≠ 0 — handle per §3; never fabricate.
