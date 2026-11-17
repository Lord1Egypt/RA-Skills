# Plan: Ad Audience Performance (ad-audience-performance)

## 1. Metadata

- **version**: 0.1.0
- **suite**: Performance Marketing Copilot
- **functions.md scenario (mapping key)**: 广告受众表现诊断
- **requires functions.md version**: `1.1.0` — verified in §4; on mismatch, halt.
- **dev status**: in-development
- **related files**:
  - data: `functions.md` §1 interfaces (primary `#4 ad_analysis_list`; optional `#8 meta_query` / `#9 google_query`), `access.yaml`
  - report assembly: `functions.md` §3
  - chained plans: `retargeting-incrementality`, `creative-performance`, `channel-budget-allocation`
  - on-the-fly artifacts: `utilities/`
- **analysis approach**: evaluate audience / ad-set performance on **true ROAS** and new-customer share. Detect overlap / cannibalization between prospecting and retargeting (retargeting can inflate `ad_net_roas` while adding little incremental value), judge lookalike seed quality (favor high-LTV seeds), and read saturation / frequency signals that depress CTR and CVR.
- **solution space**: a per-audience verdict (scale / refresh seed / de-dup overlap / cap frequency) + the matching specialist plan to chain. Recommendations only; human-executed.

## 2. Trigger & Boundary

- **Invocation**: always invoked by SKILL.md routing (no auto-trigger).
- **Intent examples that route here**: "which audiences perform best", "is retargeting cannibalizing prospecting", "are my lookalikes any good", "audience fatigue / frequency too high".
- **Boundary**: this plan diagnoses audience efficiency and overlap; it does NOT prove retargeting incrementality (that is `retargeting-incrementality`) nor rebalance the channel budget (that is `channel-budget-allocation`).
- **Pre-flight clarification (converge BEFORE fetching; skip what's known from memory/context):**
  1. **Period & comparison?** (default = last full week vs prior equal week)
  2. **Scope — which channel, and which audience types?** (prospecting / retargeting / lookalike; if named, scope to it)
  3. **Attribution model?** (default `First click`; both periods must match)

## 3. Pre-flight Checks

- **tier**: Basic. Empty `records` → distinguish "no data" vs "tier not open"; never fabricate.
- **business prerequisites**: period, `model`, `goal` (confirm via `#1 setting_goals`, default `purchase`).
- **caliber**: audience efficiency judged on **true `roas`** and new-customer share (`new_lead_conversions / conversions`); `ad_net_roas` is reference only — especially important for retargeting over-report. Both periods equal length, same `model`/`goal`.

## 4. Data Context Preparation

- **functions.md version gate**: built against `functions.md` **`1.1.0`**. On load, read the version in functions.md Metadata; **if it differs, STOP**: tell the user "Data cannot be prepared — functions.md version mismatch (plan expects 1.1.0, found <X>); the data contract may have changed." and terminate.
- **fetch plan**:

| Step | Interface | Params template | Purpose |
|------|-----------|-----------------|---------|
| a | `#4 ad_analysis_list` (current + prior, ad_set) | `{start_date,end_date,dimensions:"ad_set",model,goal,sort_by:"spend",sort:"desc"}` ×2 | per-audience true roas / cpa / new-customer share / cpm / ctr / cvr |
| b | `#4 ad_analysis_list` (drill an audience) | `{...,dimensions:"ad"}` | frequency / fatigue read; confirm saturation vs creative |
| c | `#8/#9` passthrough (optional) | platform-native frequency / audience fields | confirm saturation signals only |

- **caliber reminders**: see §1 of functions.md; key here — retargeting `ad_net_roas` systematically over-reports; judge on true `roas` and incremental new customers.

## 5. Analysis Steps (Data → Analyze → Compare → Conclude → Next)

1. **Data**: fetch a (ad_set, both periods); drill b on key audiences.
2. **Analyze — read audience quality**:
   - rank audiences by true ROAS AND new-customer share (a high-ROAS retargeting set with near-zero new customers is suspect overlap, not real performance).
   - compare prospecting vs retargeting: if retargeting `ad_net_roas` is high but its conversions overlap users prospecting already reached, flag cannibalization for `retargeting-incrementality`.
   - lookalike seed quality: prefer audiences seeded on high-LTV customers; flag weak seeds.
   - saturation: rising CPM / frequency with falling CTR/CVR ⇒ audience fatigue.
3. **Compare**: per audience, Δ% of true roas / new-customer share / cpm / ctr / cvr vs prior; tag 🟡/🔴.
4. **Conclude**: per audience, scale / refresh seed / de-dup overlap / cap frequency.
5. **Next**: chain per §7.

**Audience symptom table:**

| Symptom | Diagnosis | Next plan |
|---------|-----------|-----------|
| Retargeting high `ad_net_roas`, low new-customer share | overlap / cannibalization | `retargeting-incrementality` |
| CPM ↑, CTR/CVR ↓, frequency ↑ | audience saturation / fatigue | `creative-performance` (refresh) |
| Lookalike weak vs prospecting | poor seed quality | refresh seed (high-LTV) |
| Strong audiences with headroom | rebalance toward them | `channel-budget-allocation` |

## 6. Output

- **(A) Direct single-scenario call** — may render the self-contained template below.
- **(B) Inside a daily/weekly/monthly or suite report** — no own template; defer to `functions.md` §3 assembly; supply only the blocks below.

**Self-contained template (mode A only):**

```markdown
# Ad Audience Performance — <period>
**Shop:** <shop>　**Range:** <current> vs <prior>　**Model:** <model>　**Scope:** <channel / audiences>

## Audience ranking
| Audience (type) | True ROAS | New-customer share | CPM / Freq | Verdict |
|-----------------|-----------|--------------------|------------|---------|

## Overlap / saturation flags
<cannibalization, fatigue, weak seeds>

## Next Step
<chained plans; "recommendation, pending human execution">
```

**Blocks to feed assembly (mode B):**
- metric block: per-audience true roas / new-customer share / cpm / ctr / cvr / frequency — current/prior/Δ%.
- diagnosis block: overlap / saturation / seed-quality findings with evidence.
- recommendation block: per-audience action + chained plan; mark "recommendation, pending human execution".

## 7. Chaining & Notes

**Chaining**: cannibalization → `retargeting-incrementality`; fatigue → `creative-performance`; strong audiences with headroom → `channel-budget-allocation`.

**Data notes:**
- Equal-length windows, same model — otherwise audience deltas mislead.
- Judge on true `roas` + new-customer share; retargeting `ad_net_roas` over-reports the most.
- Split channel by the user's prompt — internalize `meta_query` / `google_query`; do NOT create per-platform variants.
- Frequency/saturation reads need ≥ 7 days to be stable.
- Empty `records` ≠ 0 — handle per §3; never fabricate audience performance.
