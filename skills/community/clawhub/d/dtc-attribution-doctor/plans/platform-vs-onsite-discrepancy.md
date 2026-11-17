# Plan: Platform vs On-site Discrepancy (platform-vs-onsite-discrepancy)

## 1. Metadata

- **version**: 0.1.0
- **suite**: Data Quality & Tracking Governance
- **functions.md scenario (mapping key)**: 广告平台数据与站内数据差异诊断
- **requires functions.md version**: `1.1.0` — verified in §4; on mismatch, halt.
- **dev status**: in-development
- **related files**:
  - data: `functions.md` §1 interfaces (primary `#5 all_attribution_list`, `#6 all_attribution_sum`; optional passthrough `#8 meta_query` / `#9 google_query`), `access.yaml`
  - report assembly: `functions.md` §3
  - chained plans: `attribution-conflict`, `tracking-health-monitor`, `channel-budget-allocation`
  - on-the-fly artifacts: `utilities/`
- **analysis approach**: quantify the systematic gap between platform-reported performance (`ad_net_roas` / `ad_net_conversion_value`) and Convbox first-party attribution (`roas` / `conversion_value`) at the channel level. For each channel, compute over-report % `(ad_net_roas − roas) / roas` and the absolute conversion-value delta, then rank channels by the size of the gap to surface the worst over-reporters. Optionally cross-check a single channel against platform-native passthrough (`#8` Meta / `#9` Google) to confirm the platform-side figure.
- **solution space**: a ranked over-reporting verdict per channel + a recommendation to treat true `roas` as the budgeting caliber and to investigate or de-weight the worst over-reporters. Recommendations only — no spend changes (human execution).

## 2. Trigger & Boundary

- **Invocation**: always invoked by SKILL.md routing (no auto-trigger).
- **Intent examples that route here**: "platform numbers don't match our store", "Meta says ROAS is way higher than we see", "why is Facebook reporting more sales than we got", "ad platform vs actual revenue gap".
- **Boundary**: this plan measures and ranks the platform-vs-attributed discrepancy and names the worst over-reporting channels; it does NOT resolve cross-channel credit conflicts (that is `attribution-conflict`) nor fix tracking config (that is `tracking-health-monitor`).
- **Pre-flight clarification (converge BEFORE fetching; skip what's known from memory/context):**
  1. **Period & comparison?** (default = last full week; single window is enough since both calibers come from the same fetch)
  2. **Scope — all channels or named platform(s)?** (if the user named Meta/Google, scope there and consider passthrough; else rank all channels)
  3. **Attribution model?** (default `First click`; the `roas` side must use one consistent model)

## 3. Pre-flight Checks

- **tier**: Basic. Empty `records` → distinguish "no data" vs "tier not open"; never fabricate.
- **business prerequisites**: period, `model`, `goal` (confirm via `#1 setting_goals`, default `purchase`). For optional passthrough, `account_id` via `#2 connection_source`.
- **caliber**: `ad_net_roas` (platform self-reported) and `roas` (Convbox-attributed) are the two sides of the gap and must NOT be mixed or summed; both come from the same `#5`/`#6` call so they are inherently the same window and model. Passthrough (`#8`/`#9`) is platform-native and is for cross-checking only, never added to attributed figures.

## 4. Data Context Preparation

- **functions.md version gate**: built against `functions.md` **`1.1.0`**. On load, read the version in functions.md Metadata; **if it differs, STOP**: tell the user "Data cannot be prepared — functions.md version mismatch (plan expects 1.1.0, found <X>); the data contract may have changed." and terminate.
- **fetch plan**:

| Step | Interface | Params template | Purpose |
|------|-----------|-----------------|---------|
| a | `#6 all_attribution_sum` | `{start_date,end_date,dimensions:"channel",model,goal}` | overall `roas` vs `ad_net_roas` and total conversion_value vs ad_net_conversion_value |
| b | `#5 all_attribution_list` | `{...,dimensions:"channel",sort_by:"spend",sort:"desc"}` | per-channel `roas`/`ad_net_roas`/`conversion_value`/`ad_net_conversion_value` → compute and rank the gap |
| c | `#8 meta_query` / `#9 google_query` (optional) | platform-native fields (e.g. spend, conversion value) | cross-check one named channel's platform figure against `ad_*` |

- **caliber reminders**: see §1 of functions.md; key here — `roas` vs `ad_net_roas` never mixed; `#5`/`#6` paired on identical params; passthrough used only as a reference, not added in.

- **API limitation (state explicitly)**: there is NO backend-total-orders / store-truth / store-revenue field in the current 9-interface API. "Platform vs on-site" is therefore operationalized as **platform-reported (`ad_net_roas` / `ad_net_conversion_value`) vs Convbox-attributed (`roas` / `conversion_value`)**, NOT platform vs a raw store-of-record total. Any conceptual desire for a backend store-truth comparison must be flagged as a current-API limitation; do not invent a backend field.

## 5. Analysis Steps (Data → Analyze → Compare → Conclude → Next)

1. **Data**: fetch a (overall summary) and b (per channel); optionally c for a named channel.
2. **Analyze — quantify the gap** per channel:
   - over-report % = `(ad_net_roas − roas) / roas`; absolute value gap = `ad_net_conversion_value − conversion_value`.
   - a large positive gap means the platform is claiming more efficiency/value than first-party attribution confirms (typical drivers: view-through, brand-term cannibalization, returning customers counted by the platform).
3. **Compare**: rank channels by over-report % and by absolute value gap; tag 🟡 (moderate) / 🔴 (large) per gap size; if passthrough was fetched, confirm the platform `ad_*` figure aligns with the platform's own native number.
4. **Conclude**: name the worst over-reporting channel(s) and the magnitude of over-statement; state that `roas` is the caliber budgeting should trust.
5. **Next**: if the gap looks like cross-channel credit theft → `attribution-conflict`; if it looks like tracking loss inflating the gap → `tracking-health-monitor`; to act on budget → `channel-budget-allocation` (reduce over-reporting channels). Recommendations only.

**Gap ladder (symptom → diagnosis → next):**

| Symptom | Diagnosis | Next plan |
|---------|-----------|-----------|
| One channel's `ad_net_roas` ≫ `roas` | platform over-reporting concentrated there | `channel-budget-allocation` (de-weight) |
| Gap widening period-over-period | tracking loss may be dropping attributed conversions | `tracking-health-monitor` |
| Gap looks like credit shifted between channels | cross-channel attribution conflict | `attribution-conflict` |
| Passthrough `≈ ad_*` but `≫ roas` | genuine platform self-attribution inflation | `channel-budget-allocation` |

## 6. Output

- **(A) Direct single-scenario call** — may render the self-contained template below.
- **(B) Inside a daily/weekly/monthly or suite report** — no own template; defer to `functions.md` §3 assembly; supply only the blocks below.

**Self-contained template (mode A only):**

```markdown
# Platform vs On-site Discrepancy — <period>
**Shop:** <shop>　**Range:** <window>　**Model:** <model>　**Scope:** <all channels / named>

## Verdict
Platform over-reports overall by <X%>. Worst channel: <channel> (`ad_net_roas` <a> vs `roas` <r>, over-report <%>).

## Gap by Channel
| Channel | ad_net_roas | roas | Over-report % | ad_net_conversion_value | conversion_value | Value gap | Status |
|---------|---------|------|---------------|---------------------|------------------|-----------|--------|

## Note
On-site = Convbox-attributed (`roas`); no backend store-truth field exists in the current API.

## Next Step
<which plan to chain; "recommendation, pending human execution">
```

**Blocks to feed assembly (mode B):**
- metric block: per-channel `ad_net_roas`/`roas`, over-report %, `ad_net_conversion_value`/`conversion_value`, value gap — with status tags.
- diagnosis block: worst over-reporting channel(s) + magnitude + likely driver; explicit note that "on-site" = attributed, not store-truth.
- recommendation block: trust `roas` for budgeting; chain target(s); mark "recommendation, pending human execution".

## 7. Chaining & Notes

**Chaining**: `attribution-conflict` (if the gap is cross-channel credit movement), `tracking-health-monitor` (if tracking loss is widening the gap), `channel-budget-allocation` (to reduce over-reporting channels). See the gap ladder (§5).

**Data notes:**
- `roas` vs `ad_net_roas` never mixed; passthrough (`#8`/`#9`) never added to attributed totals — reference only.
- Equal-length window, single consistent `model` — both calibers come from one fetch so they are aligned by construction.
- Empty `records` ≠ 0 — handle per §3; never fabricate a store-truth number that the API does not expose.
- If the user named one platform, scope there and consider passthrough; otherwise rank all channels by gap.
- A persistent gap is normal (platforms over-attribute structurally); the signal is the *relative size and trend* of the gap by channel, not its mere existence.
