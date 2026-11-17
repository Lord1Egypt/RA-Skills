# Plan: Ad Scaling Decision (ad-scaling-decision)

## 1. Metadata

- **version**: 0.1.0
- **suite**: Performance Marketing Copilot
- **functions.md scenario (mapping key)**: 投放扩量判断
- **requires functions.md version**: `1.1.0` — verified in §4; on mismatch, halt.
- **dev status**: in-development
- **related files**:
  - data: `functions.md` §1 interfaces (primary `#4 ad_analysis_list`), `access.yaml`
  - report assembly: `functions.md` §3
  - chained plans: `budget-expansion-decision`, `bid-strategy-optimization`
  - on-the-fly artifacts: `utilities/`
- **analysis approach**: campaign-level scaling execution — distinct from portfolio-level `budget-expansion-decision`. Find campaigns sitting at the efficient frontier (strong true ROAS with delivery headroom) that can absorb more budget. Recommend a gradual ramp (about +20% every 3–5 days), flag learning-phase caution, and guard the decision with new-customer share so scaling does not just buy returning customers.
- **solution space**: a per-campaign scale / hold / pull-back call with a recommended step and cadence. Recommendations only; budget changes are human-executed.

## 2. Trigger & Boundary

- **Invocation**: always invoked by SKILL.md routing (no auto-trigger).
- **Intent examples that route here**: "which campaigns can I scale", "can I push more budget here", "is this campaign ready to scale", "how fast should I ramp this".
- **Boundary**: this plan decides which campaigns to scale and how; it does NOT set the portfolio budget split (that is `budget-expansion-decision`) nor tune bid targets (that is `bid-strategy-optimization`).
- **Pre-flight clarification (converge BEFORE fetching; skip what's known from memory/context):**
  1. **Period & comparison?** (default = last full week vs prior equal week)
  2. **Scope — which channel / campaigns?** (if named, scope to it; else main-spend channel)
  3. **Efficiency floor — what true ROAS / CPA must scaling protect?** (confirm the target; default = current portfolio average)

## 3. Pre-flight Checks

- **tier**: Basic. Empty `records` → distinguish "no data" vs "tier not open"; never fabricate.
- **business prerequisites**: period, `model`, `goal` (confirm via `#1 setting_goals`, default `purchase`).
- **caliber**: scaling judged on **true `roas`** and new-customer share (`new_lead_conversions / conversions`); `ad_net_roas` is reference only. Both periods equal length, same `model`/`goal`.

## 4. Data Context Preparation

- **functions.md version gate**: built against `functions.md` **`1.1.0`**. On load, read the version in functions.md Metadata; **if it differs, STOP**: tell the user "Data cannot be prepared — functions.md version mismatch (plan expects 1.1.0, found <X>); the data contract may have changed." and terminate.
- **fetch plan**:

| Step | Interface | Params template | Purpose |
|------|-----------|-----------------|---------|
| a | `#4 ad_analysis_list` (current + prior, campaign) | `{start_date,end_date,dimensions:"campaign",model,goal,sort_by:"spend",sort:"desc"}` ×2 | per-campaign true roas / cpa / spend / new_lead_conversions / conversions → find frontier campaigns with headroom |
| b | `#4 ad_analysis_list` (drill a candidate) | `{...,dimensions:"ad_set"}` | check whether headroom is real or already saturated (frequency/CPM trend) |

- **caliber reminders**: see §1 of functions.md; key here — scaling decisions use true `roas`; new-customer guard via `new_lead_conversions`.

## 5. Analysis Steps (Data → Analyze → Compare → Conclude → Next)

1. **Data**: fetch a (campaign, both periods); drill b on candidates.
2. **Analyze — locate the efficient frontier**:
   - true ROAS at/above the floor AND not already showing saturation (stable CPM, healthy frequency, no CVR decay as spend rose).
   - new-customer share holding or rising — scaling should add incremental customers, not just returning ones.
3. **Compare**: current vs prior per campaign — did marginal spend hold efficiency? Tag scale / hold / pull-back.
4. **Conclude**: per candidate, recommend a step (~+20%) and cadence (re-check every 3–5 days); flag any campaign in learning ("let it stabilize before scaling").
5. **Next**: chain per §7.

**Scaling decision table:**

| Signal | Call | Step |
|--------|------|------|
| True ROAS ≥ floor, headroom, new-customer share holding | scale | +~20% / 3–5 days |
| True ROAS ≥ floor but saturation signals | hold | re-test audience first → `ad-audience-performance` |
| In learning phase | wait | stabilize before scaling |
| True ROAS < floor | do not scale (pull back) | → `roas-decline-diagnosis` |

## 6. Output

- **(A) Direct single-scenario call** — may render the self-contained template below.
- **(B) Inside a daily/weekly/monthly or suite report** — no own template; defer to `functions.md` §3 assembly; supply only the blocks below.

**Self-contained template (mode A only):**

```markdown
# Ad Scaling Decision — <period>
**Shop:** <shop>　**Range:** <current> vs <prior>　**Model:** <model>　**Scope:** <channel / campaigns>

## Scaling candidates
| Campaign | True ROAS | New-customer share | Headroom | Call | Step / cadence |
|----------|-----------|--------------------|----------|------|----------------|

## Caution
<learning-phase / saturation flags>

## Next Step
<scale steps + chained plans; "recommendation, pending human execution">
```

**Blocks to feed assembly (mode B):**
- metric block: candidate campaigns true roas / cpa / spend / new-customer share — current/prior/Δ%.
- diagnosis block: frontier vs saturated vs learning, with evidence.
- recommendation block: per-campaign scale step + cadence; mark "recommendation, pending human execution".

## 7. Chaining & Notes

**Chaining**: receives portfolio budget direction from `budget-expansion-decision`; hands off bid-target tuning to `bid-strategy-optimization`; if a candidate fails the floor, route to `roas-decline-diagnosis`.

**Data notes:**
- Equal-length windows, same model — otherwise headroom reads are unreliable.
- Scale on true `roas`; `ad_net_roas` over-reports and will over-scale.
- Guard with new-customer share (`new_lead_conversions`) — high ROAS that is mostly returning customers is not real scaling headroom.
- Respect the learning phase — scaling a campaign mid-learning resets it; wait for stabilization.
- Empty `records` ≠ 0 — handle per §3; never fabricate headroom.
