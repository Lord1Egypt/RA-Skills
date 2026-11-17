# Plan: Attribution Conflict (attribution-conflict)

## 1. Metadata

- **version**: 0.1.0
- **suite**: Attribution & Budget Allocation Suite
- **functions.md scenario (mapping key)**: 归因冲突诊断
- **requires functions.md version**: `1.1.0` — verified in §4; on mismatch, halt.
- **dev status**: in-development
- **related files**:
  - data: `functions.md` §1 interfaces (primary `#5 all_attribution_list`, `#6 all_attribution_sum`), `access.yaml`
  - report assembly: `functions.md` §3
  - chained plans: `platform-vs-onsite-discrepancy`, `channel-budget-allocation`
  - on-the-fly artifacts: `utilities/`
- **analysis approach**: detect cross-channel attribution overlap and model sensitivity. Run all-channel attribution under at least two contrasting models (e.g. `First click` vs `Last click`) over the same window and compare each channel's credited `conversion_value` / `roas`; channels whose credit swings sharply between models are where conflict concentrates. Identify likely double-counting or credit-stealing — for example, a last-touch channel (often retargeting/brand) inflating under `Last click` at the expense of an upper-funnel channel that earns credit under `First click`.
- **solution space**: a verdict naming the conflicting channel pair(s) and which model flatters whom, plus a recommendation on which caliber to trust for budgeting. Recommendations only — no spend reallocation (human execution).

## 2. Trigger & Boundary

- **Invocation**: always invoked by SKILL.md routing (no auto-trigger).
- **Intent examples that route here**: "are channels stealing each other's credit", "retargeting looks too good", "First click vs Last click disagree", "is my brand search just claiming sales that came from prospecting".
- **Boundary**: this plan diagnoses cross-channel credit conflict and model sensitivity; it does NOT measure platform-vs-attributed over-reporting (that is `platform-vs-onsite-discrepancy`) nor decide final budget splits (that is `channel-budget-allocation`).
- **Pre-flight clarification (converge BEFORE fetching; skip what's known from memory/context):**
  1. **Period?** (default = last full week; the same window is reused across models)
  2. **Which two models to contrast?** (default `First click` vs `Last click`; both runs must share the identical window and `goal`)
  3. **Scope — all channels or a suspected pair?** (if the user named channels, focus the conflict read on them)

## 3. Pre-flight Checks

- **tier**: Basic. Empty `records` → distinguish "no data" vs "tier not open"; never fabricate.
- **business prerequisites**: period, `goal` (confirm via `#1 setting_goals`, default `purchase`). Two attribution models to compare.
- **caliber**: diagnosis uses true `roas` / `conversion_value` only; `ad_net_roas` is not the subject here. The ONLY variable that changes between the two fetches is `model` — window, `goal`, and dimensions are held identical, otherwise the credit swing is not attributable to the model.

## 4. Data Context Preparation

- **functions.md version gate**: built against `functions.md` **`1.1.0`**. On load, read the version in functions.md Metadata; **if it differs, STOP**: tell the user "Data cannot be prepared — functions.md version mismatch (plan expects 1.1.0, found <X>); the data contract may have changed." and terminate.
- **fetch plan**:

| Step | Interface | Params template | Purpose |
|------|-----------|-----------------|---------|
| a | `#6 all_attribution_sum` (model 1 + model 2) | `{start_date,end_date,dimensions:"channel",goal,model:"First click"}` and `{...,model:"Last click"}` | overall credit totals under each model — sanity anchor that totals are comparable |
| b | `#5 all_attribution_list` (model 1 + model 2) | `{...,dimensions:"channel",sort_by:"main_conversions",sort:"desc"}` ×2 | per-channel `conversion_value`/`roas`/`conversions` under each model → measure per-channel credit swing. 🔴 sort_by must be a whitelisted field (spend/main_conversions); sort_by:"conversion_value" silently returns empty — rank by `conversion_value` in-kernel after fetch |

- **caliber reminders**: see §1 of functions.md; key here — `#5`/`#6` paired on identical params except `model`; same `goal` and `new_lead_conversions` available if the user asks whether the conflict is over new vs returning customers.

## 5. Analysis Steps (Data → Analyze → Compare → Conclude → Next)

1. **Data**: fetch a (overall under each model) and b (per channel under each model).
2. **Analyze — measure model sensitivity** per channel:
   - credit swing = `conversion_value(model A) − conversion_value(model B)` and the same as a %.
   - a channel gaining heavily under `Last click` while another loses the matching amount under `First click` is the signature of credit moving between them (double-counting risk / credit-stealing).
3. **Compare**: rank channels by absolute and % credit swing; pair the biggest gainer with the biggest matching loser; tag 🟡 (sensitive) / 🔴 (highly sensitive / likely conflict).
4. **Conclude**: name the conflicting channel pair(s), which model flatters which channel, and the likely conflict type (e.g. retargeting over-credited last-touch vs prospecting under-credited).
5. **Next**: to test whether the inflated channel is also over-reported by its platform → `platform-vs-onsite-discrepancy`; to act on the split → `channel-budget-allocation`. Recommendations only.

**Conflict ladder (symptom → diagnosis → next):**

| Symptom | Diagnosis | Next plan |
|---------|-----------|-----------|
| Channel A surges under `Last click`, B drops under `First click` (matched) | credit-stealing between A and B | `channel-budget-allocation` |
| Retargeting/brand high last-touch, low first-touch | likely claiming demand created upstream | `platform-vs-onsite-discrepancy` |
| Most channels swing little | low model sensitivity — attribution is stable | (no action; note stability) |
| Swing concentrated in new-customer credit | conflict is over true incrementality | `channel-budget-allocation` |

## 6. Output

- **(A) Direct single-scenario call** — may render the self-contained template below.
- **(B) Inside a daily/weekly/monthly or suite report** — no own template; defer to `functions.md` §3 assembly; supply only the blocks below.

**Self-contained template (mode A only):**

```markdown
# Attribution Conflict — <period>
**Shop:** <shop>　**Range:** <window>　**Models:** <model A> vs <model B>　**Scope:** <all / pair>

## Verdict
Largest conflict: <channel A> gains <X%> under <model A> while <channel B> loses <Y%> under <model B> — likely credit-stealing.

## Credit Swing by Channel
| Channel | conversion_value (A) | conversion_value (B) | Swing | Swing % | roas (A) | roas (B) | Status |
|---------|----------------------|----------------------|-------|---------|----------|----------|--------|

## Next Step
<which plan to chain; "recommendation, pending human execution">
```

**Blocks to feed assembly (mode B):**
- metric block: per-channel `conversion_value`/`roas` under both models, credit swing and swing %.
- diagnosis block: conflicting channel pair(s), which model flatters whom, conflict type + evidence.
- recommendation block: which caliber to trust + chain target(s); mark "recommendation, pending human execution".

## 7. Chaining & Notes

**Chaining**: `platform-vs-onsite-discrepancy` (test whether the over-credited channel is also platform over-reported), `channel-budget-allocation` (act on the corrected split). See the conflict ladder (§5).

**Data notes:**
- Only `model` changes between the two fetches; window, `goal`, dimensions identical — otherwise the swing is not a model effect.
- Use true `roas` / `conversion_value`; `ad_net_roas` is out of scope here.
- Channel split follows the user prompt — no per-platform variants; `#8`/`#9` are not needed for this model-comparison diagnosis.
- Empty `records` ≠ 0 — handle per §3; never fabricate.
- Some model sensitivity is normal; the signal is a *matched* gain-and-loss across a channel pair, not isolated movement.
