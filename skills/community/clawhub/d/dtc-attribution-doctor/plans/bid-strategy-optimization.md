# Plan: Bid Strategy Optimization (bid-strategy-optimization)

## 1. Metadata

- **version**: 0.1.0
- **suite**: Performance Marketing Copilot
- **functions.md scenario (mapping key)**: 出价策略优化
- **requires functions.md version**: `1.1.0` — verified in §4; on mismatch, halt.
- **dev status**: in-development
- **related files**:
  - data: `functions.md` §1 interfaces (primary `#4 ad_analysis_list`; optional `#8 meta_query` / `#9 google_query`), `access.yaml`
  - report assembly: `functions.md` §3
  - chained plans: `budget-expansion-decision`, `ad-scaling-decision`, `profit-attribution-diagnosis`
  - on-the-fly artifacts: `utilities/`
- **analysis approach**: derive bid targets by reasoning from margin to platform parameters — user gross margin → break-even CPA / ROAS → add a profit buffer → a **true** target CPA/ROAS → then translate that true target into the platform back-end tCPA / tROAS using the platform over-report factor (`ad_net_roas / roas`). The platform target is the true target adjusted by that factor, so the back-end is set against the caliber the platform itself optimizes on.
- **solution space**: per-campaign recommended back-end tCPA / tROAS values plus the true-target rationale. Recommendations only; bid changes are human-executed in the ad platform.

## 2. Trigger & Boundary

- **Invocation**: always invoked by SKILL.md routing (no auto-trigger).
- **Intent examples that route here**: "what tROAS should I set", "what target CPA", "derive my bid targets", "set the right tCPA in Meta/Google".
- **Boundary**: this plan derives bid targets; it does NOT decide portfolio budget (`budget-expansion-decision`) or per-campaign scaling steps (`ad-scaling-decision`), and it relies on margin from `profit-attribution-diagnosis` when COGS is configured.
- **Pre-flight clarification (converge BEFORE fetching; skip what's known from memory/context):**
  1. **Margin input — gross margin / COGS configured?** (break-even derivation needs it; if absent, halt or degrade — see §3)
  2. **Profit buffer — target net margin or buffer %?** (confirm the buffer to add over break-even)
  3. **Scope & period — which campaigns, and which window to read the over-report factor from?** (default = last full week)

## 3. Pre-flight Checks

- **tier**: Basic. Empty `records` → distinguish "no data" vs "tier not open"; never fabricate.
- **business prerequisites**: period, `model`, `goal` (confirm via `#1 setting_goals`, default `purchase`). **Gross margin / COGS must be configured** for break-even — if `profit / margin` fields are empty, either halt with a clear message or proceed only with a user-supplied margin and state the assumption.
- **caliber**: true target derived against true `roas`; the over-report factor is `ad_net_roas / roas` from the same window/campaign. Both periods equal length, same `model`/`goal`.

## 4. Data Context Preparation

- **functions.md version gate**: built against `functions.md` **`1.1.0`**. On load, read the version in functions.md Metadata; **if it differs, STOP**: tell the user "Data cannot be prepared — functions.md version mismatch (plan expects 1.1.0, found <X>); the data contract may have changed." and terminate.
- **fetch plan**:

| Step | Interface | Params template | Purpose |
|------|-----------|-----------------|---------|
| a | `#4 ad_analysis_list` (campaign) | `{start_date,end_date,dimensions:"campaign",model,goal}` | per-campaign `roas`, `ad_net_roas`, `margin`, cpa → over-report factor + margin read |
| b | `#4 ad_analysis_list` (drill ad_set, optional) | `{...,dimensions:"ad_set"}` | per-audience over-report factor when it varies inside a campaign |
| c | `#8/#9` passthrough (optional) | platform-native target / value fields | sanity-check current back-end target vs platform caliber |

- **caliber reminders**: see §1 of functions.md; key here — break-even uses true `roas` and configured margin; the over-report factor `ad_net_roas / roas` does the truth→platform translation.

## 5. Analysis Steps (Data → Analyze → Compare → Conclude → Next)

1. **Data**: fetch a (campaign), read true `roas`, `ad_net_roas`, margin, cpa.
2. **Analyze — derive the target chain**:
   - **Break-even**: from gross margin → break-even ROAS = `1 / margin` (and break-even CPA = margin-value per order). *(`margin` from the API is a decimal, not a percent — use it as-is in `1/margin`; ×100 only when displaying it as a %.)*
   - **Profit buffer**: add the user's buffer → **true target ROAS / CPA** (above break-even).
   - **Over-report factor**: per campaign, factor = `ad_net_roas / roas` (how much the platform over-reports).
   - **Translate to back-end**: platform tROAS = true target ROAS × factor; platform tCPA = true target CPA ÷ factor — so the back-end target reflects the platform's own inflated caliber.
3. **Compare**: current back-end target (if known via `#8/#9`) vs derived target; show the gap.
4. **Conclude**: per campaign, recommend back-end tCPA / tROAS with the true-target rationale.
5. **Next**: chain per §7.

**Derivation chain (truth → platform):**

| Step | From | To |
|------|------|----|
| Break-even | gross margin | break-even ROAS / CPA |
| Buffer | break-even + profit buffer | true target ROAS / CPA |
| Factor | `ad_net_roas / roas` | platform over-report factor |
| Translate | true target × / ÷ factor | back-end tROAS / tCPA |

## 6. Output

- **(A) Direct single-scenario call** — may render the self-contained template below.
- **(B) Inside a daily/weekly/monthly or suite report** — no own template; defer to `functions.md` §3 assembly; supply only the blocks below.

**Self-contained template (mode A only):**

```markdown
# Bid Strategy Optimization — <period>
**Shop:** <shop>　**Range:** <window>　**Model:** <model>　**Scope:** <campaigns>

## Derived targets
| Campaign | Margin | Break-even ROAS | True target ROAS/CPA | Over-report factor | Back-end tROAS / tCPA |
|----------|--------|-----------------|----------------------|--------------------|-----------------------|

## Rationale
<break-even → buffer → true target → translation>

## Next Step
<set in platform; "recommendation, pending human execution">
```

**Blocks to feed assembly (mode B):**
- metric block: per-campaign margin, true roas, ad_net_roas, over-report factor, derived back-end target.
- diagnosis block: break-even → buffer → true target → translation rationale.
- recommendation block: back-end tCPA / tROAS per campaign; mark "recommendation, pending human execution".

## 7. Chaining & Notes

**Chaining**: receives budget/scaling context from `budget-expansion-decision` / `ad-scaling-decision`; depends on `profit-attribution-diagnosis` for margin when COGS is configured.

**Data notes:**
- Break-even requires configured margin/COGS — without it, halt or use an explicit user-supplied margin and say so; never fabricate a margin.
- The whole derivation hinges on true `roas`; the back-end value is a translation of the true target, not a number read off `ad_net_roas`.
- The over-report factor `ad_net_roas / roas` varies by campaign/audience — derive it per unit, do not apply one global factor blindly.
- Equal-length windows, same model — otherwise the factor is unstable.
- Empty `records` ≠ 0 — handle per §3; never fabricate a target.
