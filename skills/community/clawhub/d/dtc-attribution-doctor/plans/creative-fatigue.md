# Plan: Creative Fatigue (creative-fatigue)

## 1. Metadata

- **version**: 0.1.0
- **suite**: Creative Intelligence Suite
- **functions.md scenario (mapping key)**: 素材疲劳诊断
- **requires functions.md version**: `1.1.0`
- **dev status**: in-development
- **related files**:
  - data: `functions.md` §1 interfaces (primary `#4 ad_analysis_list`; passthrough `#8 meta_query` / `#9 google_query`), `access.yaml`
  - report assembly: `functions.md` §3
  - chained plans: `creative-performance`, `ad-audience-performance`, `landing-page-reception`
  - on-the-fly artifacts: `utilities/`
- **analysis approach**: detect creative fatigue by trending each asset across equal-length periods — **rising frequency**, **declining CTR**, and **impression saturation** are the fatigue signature. Confirm the decay is sustained (not a single-window dip) and that falling CTR is dragging `roas`, then flag assets needing refresh or rotation. Frequency and saturation metrics that Convbox does not aggregate are read via passthrough and internalized.
- **solution space**: a per-asset fatigue verdict (fresh / watch / fatigued) with a refresh/rotation recommendation; creative production and budget moves are recommendations only, pending human execution.

## 2. Trigger & Boundary

- **Invocation**: always invoked by SKILL.md routing (no auto-trigger).
- **Intent examples that route here**: "are my creatives burning out", "CTR is dropping on our ads", "ad fatigue check", "do we need new creative".
- **Boundary**: this plan detects *fatigue over time* and flags refresh candidates; it does NOT rank current absolute performance or assign scale/pause buckets (→ `creative-performance`) and does NOT produce the new creative brief.
- **Pre-flight clarification (converge BEFORE fetching; skip what's known from memory/context):**
  1. **Channel scope?** (which platform — Meta / Google / both; if unspecified, take the highest-spend channel and state so)
  2. **Trend window & granularity?** (default = last full week vs prior equal week; ≥ 7-day windows for a reliable CTR trend)
  3. **Asset set?** (all active assets, or a named campaign/ad set)

## 3. Pre-flight Checks

- **tier**: Basic. Empty `records` → distinguish "no data" vs "tier not open"; never fabricate.
- **business prerequisites**: period, `model`, `goal` (confirm via `#1 setting_goals`, default `purchase`). Fatigue itself does not require profit; COGS optional for a profit-impact note.
- **caliber**: trend uses **true `roas`**; `ad_net_roas` is reference only. Every compared window equal length, same `model`/`goal`.

## 4. Data Context Preparation

- **functions.md version gate**: built against `functions.md` **`1.1.0`**. On load, read the version in functions.md Metadata; **if it differs, STOP**: tell the user "Data cannot be prepared — functions.md version mismatch (plan expects 1.1.0, found <X>); the data contract may have changed." and terminate.
- **fetch plan**:

| Step | Interface | Params template | Purpose |
|------|-----------|-----------------|---------|
| a | `#4 ad_analysis_list` (current) | `{start_date,end_date,dimensions:"ad",channel,model,goal,sort_by:"spend",sort:"desc"}` | current asset ctr/cvr/impressions/roas/spend |
| b | `#4 ad_analysis_list` (prior, equal) | same params, prior equal window | period-over-period CTR / CVR / impression trend per asset |
| c | `#8/#9` passthrough (optional) | minimal native fields per channel | frequency / reach / impression-saturation fields Convbox does not aggregate; internalized, not per-platform output |

- **caliber reminders**: see §1 of functions.md; key here — `roas` vs `ad_net_roas` never mixed; equal-length windows for any trend; frequency from passthrough is platform-native and not summed into Convbox figures.

## 5. Analysis Steps (Data → Analyze → Compare → Conclude → Next)

1. **Data**: fetch a (current) and b (prior equal); pull c when frequency/saturation is needed.
2. **Analyze — read the fatigue signature** per asset:
   - **CTR trend**: sustained decline period-over-period is the lead signal.
   - **Frequency** (passthrough): rising frequency against flat/declining reach indicates audience exhaustion.
   - **Impression saturation**: impressions plateau or climb while CTR falls → diminishing returns.
   - tie the CTR decline to `roas`: falling CTR dragging `roas` confirms real fatigue impact, not a cosmetic dip.
3. **Compare**: per asset, Δ% of ctr / frequency / impressions / roas vs prior; tag 🟡/🔴; require the decline to be directional, not a one-window blip.
4. **Conclude — assign a fatigue state**:

| State | Signature | Action |
|-------|-----------|--------|
| Fresh | CTR stable/up, frequency in range | keep running |
| Watch | early CTR softening or frequency creeping up | monitor; queue a variant |
| Fatigued | sustained CTR ↓ + frequency ↑ + impression saturation, roas dragging | recommend refresh / rotate out |

5. **Next**: route per the chaining table (§7).

## 6. Output

- **(A) Direct single-scenario call** — may render the self-contained template below.
- **(B) Inside a daily/weekly/monthly or suite report** — no own template; defer to `functions.md` §3 assembly; supply only the blocks below.

**Self-contained template (mode A only):**

```markdown
# Creative Fatigue — <period>
**Shop:** <shop>　**Range:** <current> vs <prior>　**Model:** <model>　**Channel:** <scope>

## Verdict
<N> assets trended. Fatigued: <list>. Watch: <list>. Lead signal: <CTR −Z% on <asset> with frequency <up to X.X>>.

## Fatigue Trend
| Asset | CTR (cur/prior/Δ%) | Frequency* | Impressions Δ | Roas Δ% | State |
|-------|--------------------|------------|---------------|---------|-------|
(* frequency only where passthrough available)

## Next Step
<which assets to refresh/rotate; which plan to chain — "recommendation, pending human execution">
```

**Blocks to feed assembly (mode B):**
- metric block: per-asset ctr / frequency / impressions / roas — current/prior/Δ%/status.
- diagnosis block: fatigue state per asset + evidence (which signal fired).
- recommendation block: refresh / rotate / monitor; mark "recommendation, pending human execution".

## 7. Chaining & Notes

**Chaining:**
- fatigued assets needing replacement ranking → `creative-performance`.
- rising frequency / audience exhaustion → `ad-audience-performance`.
- CTR holds but CVR falls (not fatigue) → `landing-page-reception`.

**Data notes:**
- Equal-length windows, same model/goal — fatigue is a trend, not a snapshot.
- Require a directional, multi-window decline; one soft window is not fatigue.
- Very short windows are noisy; use ≥ 7 days for a CTR trend.
- Frequency / reach / saturation come via `#8`/`#9` passthrough — platform-native, internalized by user-named channel, never summed into Convbox roas and never split into per-platform plans.
- `roas` vs `ad_net_roas` never mixed; report true `roas` drag, `ad_net_roas` only as reference.
- Empty `records` ≠ 0 — handle per §3; never fabricate.
