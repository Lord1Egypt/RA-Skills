# Plan: ROAS Decline Diagnosis (roas-decline-diagnosis)

## 1. Metadata

- **version**: 0.1.0
- **suite**: Performance Marketing Copilot
- **functions.md scenario (mapping key)**: ROAS下降诊断
- **requires functions.md version**: `1.1.0` — verified in §4; on mismatch, halt.
- **dev status**: in-development
- **related files**:
  - data: `functions.md` §1 interfaces (primary `#6 all_attribution_sum`, `#5 all_attribution_list`, `#4 ad_analysis_list`; optional `#8 meta_query` / `#9 google_query`), `access.yaml`
  - report assembly: `functions.md` §3
  - chained plans: `creative-performance`, `creative-fatigue`, `site-funnel-diagnosis`, `landing-page-reception`, `ad-audience-performance`, `attribution-conflict`
  - on-the-fly artifacts: `utilities/`
- **analysis approach**: when **true ROAS** (`roas`) drops period-over-period, decompose WHY via the efficiency ladder — is it the **revenue side** (fewer conversions / lower value per order) or the **cost side** (higher CPM/CPC)? then trace conversions = clicks × CVR, clicks = impressions × CTR, and check whether the drop is real or just **platform over-report shrinking** (`ad_net_roas`−`roas`). Localize to the channel/campaign driving it.
- **solution space**: a ranked root-cause verdict (which channel, which lever) + targeted next-step (which specialist plan to chain). Does NOT issue spend/bid changes (downstream + human execution).

## 2. Trigger & Boundary

- **Invocation**: always invoked by SKILL.md routing (no auto-trigger).
- **Intent examples that route here**: "why did ROAS drop", "ROAS is down this week", "our return on ad spend fell", "Facebook ROAS tanked".
- **Boundary**: this plan diagnoses the ROAS drop and points to the root lever; it does NOT execute creative/audience/landing fixes — it hands off to the matching specialist plan.
- **Pre-flight clarification (converge BEFORE fetching; skip what's known from memory/context):**
  1. **Period & comparison?** (default = last full week vs prior equal week)
  2. **Scope — overall or specific channel(s)?** (if the user named a platform, scope to it; else diagnose at channel level then drill the worst)
  3. **Attribution model?** (default `First click`; both periods must match)

## 3. Pre-flight Checks

- **tier**: Basic. Empty `records` → distinguish "no data" vs "tier not open"; never fabricate.
- **business prerequisites**: period, `model`, `goal` (confirm via `#1 setting_goals`, default `purchase`). Profit fields optional (need COGS); ROAS diagnosis itself does not require profit.
- **caliber**: diagnosis uses **true `roas`** only; `ad_net_roas` is reference for the over-report check. Both periods equal length, same `model`/`goal`.

## 4. Data Context Preparation

- **functions.md version gate**: built against `functions.md` **`1.1.0`**. On load, read the version in functions.md Metadata; **if it differs, STOP**: tell the user "Data cannot be prepared — functions.md version mismatch (plan expects 1.1.0, found <X>); the data contract may have changed." and terminate.
- **fetch plan**:

| Step | Interface | Params template | Purpose |
|------|-----------|-----------------|---------|
| a | `#6 all_attribution_sum` (current + prior) | `{start_date,end_date,dimensions:"channel",model,goal}` ×2 | overall true ROAS Δ + spend/conversion_value/conversions deltas |
| b | `#5 all_attribution_list` (current + prior) | `{...,dimensions:"channel",sort_by:"spend",sort:"desc"}` ×2 | per-channel `roas`/`ad_net_roas`/spend/conversions → find the channel(s) driving the drop |
| c | `#4 ad_analysis_list` (drill the worst channel) | `{...,dimensions:"campaign"}` (then `ad_set`/`ad` if needed) | efficiency levers: cpm/cpc/ctr/cvr/impressions/clicks |
| d | `#8/#9` passthrough (optional) | platform-native fields | only to confirm a platform-side change (auction cost, delivery) |

- **caliber reminders**: see §1 of functions.md; key here — `roas` vs `ad_net_roas` not mixed; new vs returning via `new_lead_conversions` when "is the drop from losing new customers?".

## 5. Analysis Steps (Data → Analyze → Compare → Conclude → Next)

1. **Data**: fetch a (overall) and b (per channel); drill c on the worst channel.
2. **Analyze — decompose the ROAS drop** along the ladder:
   - `roas = conversion_value / spend`. Did `conversion_value` fall or `spend` rise (or both)?
   - `conversions = clicks × CVR`; `clicks = impressions × CTR`. Walk cpm → cpc → ctr → cvr to find the broken rung.
   - Compute over-report gap trend `(ad_net_roas − roas)`: if `roas` fell while `ad_net_roas` held, real efficiency dropped; if both fell together, platform delivery worsened.
3. **Compare**: per channel, Δ% of roas / spend / cpm / cpc / ctr / cvr vs prior; tag 🟡/🔴.
4. **Conclude**: name the **primary driver channel + broken lever** (e.g., "Meta ROAS −28%: CVR collapsed on the hero LP, not a media-cost issue").
5. **Next**: route per the root-cause table (§7).

**Root-cause ladder (symptom → diagnosis → next):**

| Symptom | Diagnosis | Next plan |
|---------|-----------|-----------|
| CPM/CPC ↑, CTR ~ | auction pressure / audience saturation | `ad-audience-performance` |
| CTR ↓ | creative fatigue / weak hook | `creative-fatigue` → `creative-performance` |
| CVR ↓ (clicks ok) | landing/offer/funnel issue | `site-funnel-diagnosis` → `landing-page-reception` |
| Value per order ↓ | discount/product mix | profit/promo plans (later tier) |
| Spend ↑, roas ↓ | over-scaled past efficient frontier | `budget-expansion-decision` (pull back) |
| `ad_net_roas` high, `roas` ↓ | platform over-reporting rising | `attribution-conflict` / `platform-vs-onsite-discrepancy` |

## 6. Output

- **(A) Direct single-scenario call** — may render the self-contained template below.
- **(B) Inside a daily/weekly/monthly or suite report** — no own template; defer to `functions.md` §3 assembly; supply only the blocks below.

**Self-contained template (mode A only):**

```markdown
# ROAS Decline Diagnosis — <period>
**Shop:** <shop>　**Range:** <current> vs <prior>　**Model:** <model>　**Scope:** <overall / channel>

## Verdict
Overall true ROAS <X.XX → Y.YY, ΔZ%>. Primary driver: <channel> — <broken lever>.

## Decomposition (driver channel)
| Lever | Current | Prior | Δ% | Status |
|-------|---------|-------|----|--------|
(roas, ad_net_roas, spend, cpm, cpc, ctr, cvr, value/order)

## Next Step
<which specialist plan to run; "recommendation, pending human execution">
```

**Blocks to feed assembly (mode B):**
- metric block: overall + per-channel roas (with ad_net_roas ref & gap), spend, cpm/cpc/ctr/cvr — current/prior/Δ%/status.
- diagnosis block: primary driver channel + broken lever + evidence.
- recommendation block: next specialist plan(s); mark "recommendation, pending human execution".

## 7. Chaining & Notes

**Chaining**: see the root-cause ladder (§5) — each symptom maps to a next plan.

**Data notes:**
- Equal-length windows, same model — otherwise the decomposition is meaningless.
- A real ROAS drop and a shrinking `ad_net_roas`−`roas` gap are different stories; state which.
- Very short windows are skewed by fulfillment/refund lag; use ≥ 7 days for trend.
- If the user named one platform, scope there but still note cross-channel spillover (a Meta drop can be a shared-LP issue).
- Empty `records` ≠ 0 — handle per §3; never fabricate.
