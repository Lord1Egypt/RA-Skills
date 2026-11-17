# Plan: Budget Expansion Decision (budget-expansion-decision)

## 1. Metadata

- **version**: 0.1.0
- **suite**: Growth Command Center
- **functions.md scenario (mapping key)**: 预算扩张判断
- **requires functions.md version**: `1.1.0` — verified in §4; on mismatch, halt.
- **dev status**: in-development
- **related files**:
  - data: `functions.md` §1 interfaces (primary `#5 all_attribution_list`, `#6 all_attribution_sum`, `#4 ad_analysis_list`), `access.yaml`
  - report assembly: `functions.md` §3
  - chained plans: `bid-strategy-optimization`, `ad-scaling-decision`, `channel-budget-allocation`, `roas-decline-diagnosis`, `profit-attribution-diagnosis`
  - on-the-fly artifacts: `utilities/`
- **analysis approach**: decide **where it is safe to add budget** (and where to hold/cut) using true ROAS — not platform ROAS. A channel/campaign is a scale candidate only if it is a **True Winner** (high platform AND true ROAS) with **healthy new-customer share** and **no efficiency decay** (true ROAS held as spend rose). "Hollow Victory" (high platform / low true) is capped, not scaled.
- **solution space**: a ranked scale-up / hold / cut list with **magnitude ranges** (not fake-precise numbers) and the rationale per item. Issues **recommendations only** — every budget change requires human approval and is executed by the user in the ad platform.

## 2. Trigger & Boundary

- **Invocation**: always invoked by SKILL.md routing (no auto-trigger). Often chained from `growth-health-diagnosis` (budget signal).
- **Intent examples that route here**: "where should I add budget", "can we scale", "which campaigns to push", "should we increase spend".
- **Boundary**: decides direction + magnitude of budget moves at channel/campaign level. Translating a true target into platform back-end params (tCPA/tROAS) is `bid-strategy-optimization`; campaign-level execution detail is `ad-scaling-decision`.
- **Pre-flight clarification (converge BEFORE fetching; skip what's known):**
  1. **Primary goal?** (maximize ROAS / profit / new-customer acquisition — changes how candidates are ranked; default from shop memory)
  2. **Budget cap / headroom?** (never recommend beyond an approved cap — confirm or read from memory)
  3. **Period & scope?** (default last 2–4 weeks for stability; channel or campaign level)

## 3. Pre-flight Checks

- **tier**: Basic. Empty `records` → "no data" vs "tier not open"; never fabricate.
- **business prerequisites**: period, `model`, `goal`. **Break-even ROAS / margin** (from gross margin) needed to judge "profitable to scale"; if profit fields unavailable (no COGS), fall back to true-ROAS + new-customer share and state the profit blind spot. *(`margin` is a decimal, not a percent — ×100 before display/threshold compare.)*
- **safety**: never recommend exceeding the approved budget cap; mark all moves "requires human approval".

## 4. Data Context Preparation

- **functions.md version gate**: built against `functions.md` **`1.1.0`**. On load, read the version in functions.md Metadata; **if it differs, STOP** with "Data cannot be prepared — functions.md version mismatch (plan expects 1.1.0, found <X>)." and terminate.
- **fetch plan**:

| Step | Interface | Params template | Purpose |
|------|-----------|-----------------|---------|
| a | `#6 all_attribution_sum` | `{...,dimensions:"channel",model,goal}` | overall true ROAS / blended baseline + total spend headroom |
| b | `#5 all_attribution_list` | `{...,dimensions:"channel",sort_by:"main_conversions",sort:"desc"}` | per-channel `roas`/`ad_net_roas`/spend/new_lead_conversions/profit/margin. 🔴 sort_by:"conversion_value" silently returns empty — sort server-side by main_conversions, rank by value/profit in-kernel |
| c | `#4 ad_analysis_list` (drill) | `{...,dimensions:"campaign"}` | campaign-level candidates within a winning channel |
| d | trend (optional) | a–c over an earlier equal window | efficiency-decay check: did `roas` hold as `spend` rose? |

> `dimensions` takes a **single string value** (e.g. `"channel"`), not an array — an array collapses to one bogus aggregate row. To split by multiple dimensions, call the interface once per dimension.

- **caliber**: scale decisions use **true `roas`**; `ad_net_roas` only flags Hollow Victory. New-customer share = `new_lead_conversions / conversions`. Profit/margin require COGS.

## 5. Analysis Steps (Data → Analyze → Compare → Conclude → Next)

1. **Data**: fetch a (baseline) + b (channels); drill c on winners; d for decay check.
2. **Analyze — classify each channel/campaign** on the Platform × True ROAS quadrant (functions/SKILL decision framework):
   - **True Winner** (platform high + true high): scale candidate.
   - **Hidden Gem** (platform low + true high): do not pause; consider modest scale, watch.
   - **Hollow Victory** (platform high + true low): cap, do not scale; flag for incrementality (`retargeting-incrementality`).
   - **True Loser** (both low): cut/hold.
3. **Compare**: among scale candidates, prefer those with (a) true ROAS ≥ target/break-even with margin headroom, (b) healthy/ rising new-customer share, (c) no efficiency decay (true ROAS stable as spend rose), (d) room under the budget cap.
4. **Conclude**: produce the scale-up / hold / cut list with magnitude ranges (e.g., scale True Winners +20% every 3–5 days; cap Hollow Victory −15~20%).
5. **Next**: chain to `bid-strategy-optimization` (set platform targets), `ad-scaling-decision` (execution), or `profit-attribution-diagnosis` (if profit blind).

**Scaling heuristics (defaults, override by shop baseline):**

| Class | Condition | Move |
|-------|-----------|------|
| Scale | True Winner, true ROAS ≥ target, new-customer share healthy, no decay | +20% per 3–5 days, re-check |
| Hold | True ROAS near break-even, or decay starting | keep, monitor |
| Cap | Hollow Victory (gap > 30%) | cap / −15~20%, investigate incrementality |
| Cut | True Loser (true ROAS < break-even) | reduce/pause, refresh first |

## 6. Output

- **(A) Direct single-scenario call** — may render the self-contained template below.
- **(B) Inside a daily/weekly/monthly or suite report** — no own template; defer to `functions.md` §3; supply only the blocks below.

**Self-contained template (mode A only):**

```markdown
# Budget Expansion Decision — <period>
**Shop:** <shop>　**Range:** <period>　**Goal:** <roas/profit/new-customer>　**Cap:** <budget cap>

## Verdict
Scale headroom: <summary>. Top moves: <scale X +20%, cap Y>.

## Channel / Campaign Decision
| Item | Spend | True ROAS | Platform ROAS | New-cust share | Class | Move (range) |
|------|------:|----------:|--------------:|---------------:|-------|--------------|

## Reallocation
<from Cut/Cap items toward Scale items; direction + magnitude range>
All moves: recommendation, pending human approval & execution.
```

**Blocks to feed assembly (mode B):**
- metric block: per item — spend, true ROAS (+ad_net_roas ref), new-customer share, profit/margin (if available).
- diagnosis block: quadrant class per item + decay/new-customer notes.
- recommendation block: scale/hold/cap/cut with magnitude ranges; mark "recommendation, pending human approval & execution".

## 7. Chaining & Notes

**Chaining:** `bid-strategy-optimization` (translate true targets to platform tCPA/tROAS); `ad-scaling-decision` (campaign execution); `profit-attribution-diagnosis` (when profit unavailable or margins thin); `retargeting-incrementality` (for Hollow Victory channels).

**Data notes:**
- Use a stable window (2–4 weeks) — single-week noise causes over-/under-scaling.
- Scaling is gradual; never recommend a step change beyond +20–30% or beyond the cap.
- A high `ad_net_roas` alone is NOT a scale signal — only true `roas` is.
- Profit blind without COGS — say so; do not imply profitable scaling you can't verify.
- Empty `records` ≠ 0 — handle per §3; never fabricate.
