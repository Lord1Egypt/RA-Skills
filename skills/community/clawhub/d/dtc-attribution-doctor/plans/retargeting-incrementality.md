# Plan: Retargeting Incrementality (retargeting-incrementality)

## 1. Metadata

- **version**: 0.1.0
- **suite**: Attribution & Budget Allocation Suite
- **functions.md scenario (mapping key)**: 再营销真实增量判断
- **requires functions.md version**: `1.1.0`
- **dev status**: in-development
- **related files**:
  - data: `functions.md` §1 interfaces (primary `#5 all_attribution_list`, `#4 ad_analysis_list`), `access.yaml`
  - report assembly: `functions.md` §3
  - chained plans: `ad-audience-performance`, `budget-expansion-decision`, `attribution-conflict`
  - on-the-fly artifacts: `utilities/`
- **analysis approach**: separate **true incremental** conversions from retargeting / brand cannibalization — compare platform `ad_net_roas` against true `roas` on retargeting campaigns, and read new vs returning via the `new_lead_conversions` share (low new-customer share signals re-serving people who would have converted anyway). Detect the **Hollow Victory** pattern: high platform-reported ROAS with low true ROAS.
- **solution space**: a verdict on whether retargeting spend is genuinely incremental or cannibalizing, plus a cap / continue / reduce recommendation (recommendations only, human execution).

## 2. Trigger & Boundary

- **Invocation**: always invoked by SKILL.md routing (no auto-trigger).
- **Intent examples that route here**: "is retargeting actually working", "is my retargeting incremental", "Facebook says retargeting ROAS is great but sales aren't", "are we just cannibalizing organic with retargeting".
- **Boundary**: this plan judges retargeting incrementality and recommends a cap; it does NOT redesign audiences or set total budget level — it hands audience tuning to `ad-audience-performance` and the spend-cap decision to `budget-expansion-decision`.
- **Pre-flight clarification (converge BEFORE fetching; skip what's known from memory/context):**
  1. **Period & comparison?** (default = last full week vs prior equal week)
  2. **Which retargeting campaigns / channel?** (name them, or split by user prompt — no per-platform variants)
  3. **Attribution model?** (default `First click`; both periods must match)

## 3. Pre-flight Checks

- **tier**: Basic. Empty `records` → distinguish "no data" vs "tier not open"; never fabricate.
- **business prerequisites**: period, `model`, `goal` (confirm via `#1 setting_goals`, default `purchase`). Profit fields optional; incrementality judgment does not require profit.
- **caliber**: judgment uses **true `roas`**; `ad_net_roas` is the over-report reference, never the basis. Both periods equal length, same `model`/`goal`.

## 4. Data Context Preparation

- **functions.md version gate**: built against `functions.md` **`1.1.0`**. On load, read the version in functions.md Metadata; **if it differs, STOP**: tell the user "Data cannot be prepared — functions.md version mismatch (plan expects 1.1.0, found <X>); the data contract may have changed." and terminate.
- **fetch plan**:

| Step | Interface | Params template | Purpose |
|------|-----------|-----------------|---------|
| a | `#5 all_attribution_list` (current + prior) | `{start_date,end_date,dimensions:"channel",model,goal}` ×2 | channel-level `roas` vs `ad_net_roas` + `new_lead_conversions` share |
| b | `#4 ad_analysis_list` (retargeting campaigns) | `{...,dimensions:"campaign"}` (then `ad_set` if needed) | isolate retargeting: `roas`/`ad_net_roas`/`new_lead_conversions`/`conversions` |

- **caliber reminders**: see §1 of functions.md; key here — `roas` vs `ad_net_roas` not mixed; new vs returning via `new_lead_conversions / conversions`; channel split internalized from the user prompt (no per-platform variants); empty `records` ≠ 0.

## 5. Analysis Steps (Data → Analyze → Compare → Conclude → Next)

1. **Data**: fetch a (channel anchor) and b (retargeting campaigns).
2. **Analyze — incrementality signals**:
   - over-report gap `(ad_net_roas − roas)` on retargeting: a wide gap flags platform inflation.
   - new-customer share = `new_lead_conversions / conversions`: low share on retargeting = serving existing intenders (likely non-incremental).
   - **Hollow Victory**: high `ad_net_roas`, low `roas`, low new-customer share → reported wins are not real increments.
3. **Compare**: retargeting vs prospecting on `roas`, gap, and new-customer share; tag 🟡/🔴.
4. **Conclude**: verdict — genuinely incremental vs cannibalizing; recommend cap / continue / reduce.
5. **Next**: route per the incrementality map (§7).

**Incrementality map (symptom → diagnosis → next):**

| Symptom | Diagnosis | Next plan |
|---------|-----------|-----------|
| High `ad_net_roas`, low `roas`, low new-cust share | Hollow Victory / cannibalization | `budget-expansion-decision` (cap) |
| `roas` healthy, new-cust share reasonable | genuinely incremental | `ad-audience-performance` (scale audience) |
| `ad_net_roas` ≈ `roas`, mixed signals | audience overlap to investigate | `ad-audience-performance` |
| Reported vs true diverge broadly | attribution model conflict | `attribution-conflict` |

## 6. Output

- **(A) Direct single-scenario call** — may render the self-contained template below.
- **(B) Inside a daily/weekly/monthly or suite report** — no own template; defer to `functions.md` §3 assembly; supply only the blocks below.

**Self-contained template (mode A only):**

```markdown
# Retargeting Incrementality — <period>
**Shop:** <shop>　**Range:** <current> vs <prior>　**Model:** <model>　**Scope:** <retargeting campaigns>

## Verdict
<Incremental / cannibalizing>. Over-report gap <X>, new-customer share <Y%>. Recommendation: <cap / continue / reduce>.

## Incrementality Table
| Campaign | roas | ad_net_roas | Over-report gap | New-cust share | Read |
|----------|------|---------|-----------------|----------------|------|

## Next Step
<which specialist plan to run; "recommendation, pending human execution">
```

**Blocks to feed assembly (mode B):**
- metric block: retargeting `roas` (with `ad_net_roas` ref & gap) and new-customer share vs prospecting — current/prior/Δ%/status.
- diagnosis block: incremental vs cannibalizing verdict + Hollow Victory evidence.
- recommendation block: cap / continue / reduce; mark "recommendation, pending human execution".

## 7. Chaining & Notes

**Chaining**: out to `ad-audience-performance` (audience tuning), `budget-expansion-decision` (cap), `attribution-conflict` (when reported vs true diverge broadly) — see the incrementality map (§5).

**Data notes:**
- Equal-length windows, same model — otherwise the gap trend is meaningless.
- True `roas` is the basis; `ad_net_roas` only reveals the over-report magnitude.
- Low new-customer share is the core cannibalization signal; read it with the gap, not alone.
- Channel split comes from the user prompt; do not build per-platform variants.
- Recommendations only — no spend is changed without human execution.
- Empty `records` ≠ 0 — handle per §3; never fabricate.
