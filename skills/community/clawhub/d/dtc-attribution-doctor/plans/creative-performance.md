# Plan: Creative Performance (creative-performance)

## 1. Metadata

- **version**: 0.1.0
- **suite**: Creative Intelligence Suite
- **functions.md scenario (mapping key)**: 素材表现诊断
- **requires functions.md version**: `1.1.0`
- **dev status**: in-development
- **related files**:
  - data: `functions.md` §1 interfaces (primary `#4 ad_analysis_list`; passthrough `#8 meta_query` / `#9 google_query`), `access.yaml`
  - report assembly: `functions.md` §3
  - chained plans: `creative-fatigue`, `roas-decline-diagnosis`, `ad-audience-performance`, `landing-page-reception`
  - on-the-fly artifacts: `utilities/`
- **analysis approach**: rank paid creatives at ad/asset level on **true `roas`** and profit (where COGS is configured), then bucket each into **scale / keep / optimize / pause**. Separate winners (high spend-share, efficient) from losers (high spend, weak return) and surface under-funded efficient assets worth more budget. Asset-level platform metrics that Convbox does not aggregate are pulled via passthrough and internalized — not exposed as per-platform variants.
- **solution space**: a ranked creative scorecard with a bucket verdict per asset and a next-action recommendation; budget/creative changes are recommendations only, pending human execution.

## 2. Trigger & Boundary

- **Invocation**: always invoked by SKILL.md routing (no auto-trigger).
- **Intent examples that route here**: "which creatives are working", "best and worst performing ads", "which ads should I scale or pause", "creative-level ROAS breakdown".
- **Boundary**: this plan rates current creative performance and assigns scale/keep/optimize/pause buckets; it does NOT diagnose *why* a creative is decaying over time (→ `creative-fatigue`) and does NOT execute budget or creative edits.
- **Pre-flight clarification (converge BEFORE fetching; skip what's known from memory/context):**
  1. **Channel scope?** (which platform — Meta / Google / both; if unspecified, take the highest-spend channel and state so)
  2. **Period & comparison?** (default = last full week vs prior equal week)
  3. **Profit view wanted?** (only if COGS is configured; else rate on true `roas` and say so)

## 3. Pre-flight Checks

- **tier**: Basic. Empty `records` → distinguish "no data" vs "tier not open"; never fabricate.
- **business prerequisites**: period, `model`, `goal` (confirm via `#1 setting_goals`, default `purchase`). Profit/margin fields require COGS configured — if absent, degrade to a `roas`-only scorecard and state the limitation.
- **caliber**: bucketing uses **true `roas`** only; `ad_net_roas` is reference for the over-report check. Both periods equal length, same `model`/`goal`.

## 4. Data Context Preparation

- **functions.md version gate**: built against `functions.md` **`1.1.0`**. On load, read the version in functions.md Metadata; **if it differs, STOP**: tell the user "Data cannot be prepared — functions.md version mismatch (plan expects 1.1.0, found <X>); the data contract may have changed." and terminate.
- **fetch plan**:

| Step | Interface | Params template | Purpose |
|------|-----------|-----------------|---------|
| a | `#4 ad_analysis_list` (current) | `{start_date,end_date,dimensions:"ad",channel,model,goal,sort_by:"spend",sort:"desc"}` | asset-level roas/ad_net_roas/spend/conversions/profit/margin/ctr/cvr |
| b | `#4 ad_analysis_list` (prior) | same params, prior equal window | per-asset Δ to confirm trend vs one-off |
| c | `#8/#9` passthrough (optional) | minimal native fields per channel | asset-level metrics Convbox does not aggregate (e.g. thumbstop, video views); internalized, not per-platform output |

- **caliber reminders**: see §1 of functions.md; key here — `roas` vs `ad_net_roas` never mixed; profit needs COGS; new vs returning via `new_lead_conversions / conversions` when asked "are winners bringing new customers?".

## 5. Analysis Steps (Data → Analyze → Compare → Conclude → Next)

1. **Data**: fetch a (current asset list) and b (prior); pull c only when an asset-native metric is needed.
2. **Analyze — score each asset**:
   - efficiency = true `roas` vs the account/channel target; profit = `profit`/`margin` where COGS is available.
   - volume = spend-share and `conversions`; flag high-spend assets carrying the channel.
   - over-report gap `(ad_net_roas − roas)` per asset — a high gap on a "winner" tempers the scale call.
3. **Compare**: rank assets by spend-share; for each tag Δ% of roas / ctr / cvr / profit vs prior; mark 🟡/🔴.
4. **Conclude — assign a bucket per asset**:

| Bucket | Condition | Action |
|--------|-----------|--------|
| Scale | high `roas` (≥ target), profit-positive, room to spend | recommend more budget |
| Keep | at-target `roas`, stable | hold |
| Optimize | mid `roas`, weak CTR or CVR but salvageable | refresh hook / LP match |
| Pause | low `roas`, profit-negative, high spend | recommend pause / cut |

5. **Next**: route per the chaining table (§7) — decaying winners → `creative-fatigue`; CTR-driven weakness → originates from `roas-decline-diagnosis`.

## 6. Output

- **(A) Direct single-scenario call** — may render the self-contained template below.
- **(B) Inside a daily/weekly/monthly or suite report** — no own template; defer to `functions.md` §3 assembly; supply only the blocks below.

**Self-contained template (mode A only):**

```markdown
# Creative Performance — <period>
**Shop:** <shop>　**Range:** <current> vs <prior>　**Model:** <model>　**Channel:** <scope>

## Verdict
<N> assets reviewed. Scale: <list>. Pause: <list>. Top winner <asset> (roas <X.XX>); worst drain <asset> (roas <Y.YY>, spend <$>).

## Creative Scorecard
| Asset | Spend | Roas | ad_net_roas (ref) | CTR | CVR | Profit* | Bucket |
|-------|-------|------|---------------|-----|-----|---------|--------|
(* profit only when COGS configured)

## Next Step
<which assets to scale/pause; which plan to chain — "recommendation, pending human execution">
```

**Blocks to feed assembly (mode B):**
- metric block: per-asset roas (with ad_net_roas ref & gap), spend, ctr, cvr, profit/margin — current/prior/Δ%/status.
- diagnosis block: bucket assignment per asset + winners/losers + evidence.
- recommendation block: scale/keep/optimize/pause actions; mark "recommendation, pending human execution".

## 7. Chaining & Notes

**Chaining:**
- decaying or saturating winners → `creative-fatigue`.
- CTR-driven ROAS weakness arrives from → `roas-decline-diagnosis`.
- "optimize" assets failing on the landing side → `landing-page-reception`.
- audience-saturation signals on scaled assets → `ad-audience-performance`.

**Data notes:**
- Equal-length windows, same model/goal — otherwise the ranking is meaningless.
- Profit buckets need COGS configured; without it, rate on true `roas` only and say so.
- A "winner" with a large `ad_net_roas − roas` gap may be over-credited; temper the scale call.
- Asset-level native metrics (e.g. thumbstop, video play rate) come via `#8`/`#9` passthrough — internalized by user-named channel, never split into per-platform plans. Search-term and quality-score data are not assumed present for Meta.
- Empty `records` ≠ 0 — handle per §3; never fabricate.
