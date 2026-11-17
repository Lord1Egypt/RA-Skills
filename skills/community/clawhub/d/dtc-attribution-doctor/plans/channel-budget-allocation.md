# Plan: Channel Budget Allocation (channel-budget-allocation)

## 1. Metadata

- **version**: 0.1.0
- **suite**: Attribution & Budget Allocation Suite
- **functions.md scenario (mapping key)**: 渠道预算分配
- **requires functions.md version**: `1.1.0`
- **dev status**: in-development
- **related files**:
  - data: `functions.md` §1 interfaces (primary `#5 all_attribution_list`, `#6 all_attribution_sum`, `#4 ad_analysis_list`), `access.yaml`
  - report assembly: `functions.md` §3
  - chained plans: `bid-strategy-optimization`, `retargeting-incrementality`, `profit-attribution-diagnosis`
  - on-the-fly artifacts: `utilities/`
- **analysis approach**: optimize the cross-channel **mix** rather than total spend level — rank channels on **true ROAS** (`roas`, not `ad_net_roas`), profit (`profit` / `margin`), and incrementality signals, then propose shifting budget away from over-reporting / low-true channels toward high-true ones. Complements `budget-expansion-decision` (scale / hold / cut at the portfolio level) by reallocating within a given envelope.
- **solution space**: a recommended reallocation (which channels up, which down, by how much) framed as recommendations only, pending human approval — no spend changes are executed.

## 2. Trigger & Boundary

- **Invocation**: always invoked by SKILL.md routing (no auto-trigger).
- **Intent examples that route here**: "how should I split my budget across channels", "where should ad dollars go", "is my channel mix right", "shift budget to the best channels".
- **Boundary**: this plan recommends the channel mix within an envelope; it does NOT decide whether to scale/hold/cut total spend (that is `budget-expansion-decision`) and does NOT set per-campaign bids — it hands those to the matching plans.
- **Pre-flight clarification (converge BEFORE fetching; skip what's known from memory/context):**
  1. **Period & comparison?** (default = last full week vs prior equal week)
  2. **Budget envelope — hold total constant, or is a new total given?**
  3. **Optimize on true ROAS, profit, or both?** (default both; profit requires COGS configured)

## 3. Pre-flight Checks

- **tier**: Basic. Empty `records` → distinguish "no data" vs "tier not open"; never fabricate.
- **business prerequisites**: period, `model`, `goal` (confirm via `#1 setting_goals`, default `purchase`). Profit-based allocation needs COGS configured; if absent, degrade to a true-ROAS-only allocation and say so.
- **caliber**: allocation uses **true `roas`** only; `ad_net_roas` is reference for the over-report check. `#5`/`#6` paired with identical params. Both periods equal length, same `model`/`goal`.

## 4. Data Context Preparation

- **functions.md version gate**: built against `functions.md` **`1.1.0`**. On load, read the version in functions.md Metadata; **if it differs, STOP**: tell the user "Data cannot be prepared — functions.md version mismatch (plan expects 1.1.0, found <X>); the data contract may have changed." and terminate.
- **fetch plan**:

| Step | Interface | Params template | Purpose |
|------|-----------|-----------------|---------|
| a | `#6 all_attribution_sum` (current + prior) | `{start_date,end_date,dimensions:"channel",model,goal}` ×2 | overall spend / value / true ROAS anchor |
| b | `#5 all_attribution_list` (current + prior) | `{...,dimensions:"channel",sort_by:"spend",sort:"desc"}` ×2 | per-channel `roas`/`ad_net_roas`/`profit`/`margin`/`new_lead_conversions` for the mix |
| c | `#4 ad_analysis_list` (drill paid channels) | `{...,dimensions:"campaign"}` | check headroom / saturation before recommending a shift |

- **caliber reminders**: see §1 of functions.md; key here — `roas` vs `ad_net_roas` not mixed; profit needs COGS; new-customer share via `new_lead_conversions / conversions`; empty `records` ≠ 0.

## 5. Analysis Steps (Data → Analyze → Compare → Conclude → Next)

1. **Data**: fetch a (anchor) and b (per-channel mix); drill c for headroom on candidate channels.
2. **Analyze — score each channel**:
   - true ROAS (`roas`) as the efficiency axis; `(ad_net_roas − roas)` as the over-report flag.
   - profit quality via `profit` / `margin` (skip / flag if COGS absent).
   - incrementality / new-customer lean via `new_lead_conversions` share.
3. **Compare**: rank channels; mark over-reporters (high `ad_net_roas`, low `roas`) and thin-profit channels; tag 🟡/🔴.
4. **Conclude**: propose a reallocation — pull from low-true / over-reporting / saturated channels toward high-true channels with headroom; quantify the shift.
5. **Next**: chain `bid-strategy-optimization` (execute target efficiency), `retargeting-incrementality` (validate retargeting before funding it), `profit-attribution-diagnosis` (if profit drives the call).

**Allocation map (signal → action → next):**

| Signal | Action | Next plan |
|--------|--------|-----------|
| High `ad_net_roas`, low `roas` | discount the channel; verify increments | `retargeting-incrementality` |
| High `roas`, headroom in `#4` | candidate to fund | `bid-strategy-optimization` |
| Decent `roas`, thin `margin` | reallocate cautiously; check profit | `profit-attribution-diagnosis` |
| Low `roas`, saturated | candidate to defund | `budget-expansion-decision` (level call) |

## 6. Output

- **(A) Direct single-scenario call** — may render the self-contained template below.
- **(B) Inside a daily/weekly/monthly or suite report** — no own template; defer to `functions.md` §3 assembly; supply only the blocks below.

**Self-contained template (mode A only):**

```markdown
# Channel Budget Allocation — <period>
**Shop:** <shop>　**Range:** <current> vs <prior>　**Model:** <model>　**Envelope:** <hold / new total>

## Verdict
Recommended mix shift: <from channels> → <to channels>. Basis: true ROAS + profit + increments.

## Channel Scorecard
| Channel | Spend | roas | ad_net_roas (ref) | Over-report gap | margin | New-cust share | Move |
|---------|-------|------|---------------|-----------------|------------|----------------|------|

## Next Step
<which specialist plan to run; "recommendation, pending human approval">
```

**Blocks to feed assembly (mode B):**
- metric block: per-channel spend, `roas` (with `ad_net_roas` ref & gap), `profit`/`margin`, new-customer share — current/prior/Δ%/status.
- diagnosis block: which channels over-report / are thin / have headroom + evidence.
- recommendation block: recommended reallocation with magnitude; mark "recommendation, pending human approval".

## 7. Chaining & Notes

**Chaining**: out to `bid-strategy-optimization`, `retargeting-incrementality`, `profit-attribution-diagnosis` — see the allocation map (§5). Pairs with `budget-expansion-decision` for the scale/hold/cut level call.

**Data notes:**
- Equal-length windows, same model — otherwise the mix comparison is meaningless.
- True `roas` only for the funding decision; `ad_net_roas` is a flag, never a basis.
- Profit-based allocation needs COGS; without it, degrade to true-ROAS-only and say so.
- Platform passthrough (`#8`/`#9`) is not additive with Convbox attribution; do not sum.
- Recommendations only — no spend is moved without human approval.
- Empty `records` ≠ 0 — handle per §3; never fabricate.
