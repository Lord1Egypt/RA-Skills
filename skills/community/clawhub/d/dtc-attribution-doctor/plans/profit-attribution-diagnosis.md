# Plan: Profit Attribution Diagnosis (profit-attribution-diagnosis)

## 1. Metadata

- **version**: 0.1.0
- **suite**: Profit Protection Dashboard
- **functions.md scenario (mapping key)**: 利润归因诊断
- **requires functions.md version**: `1.1.0` — verified in §4; on mismatch, halt.
- **dev status**: in-development
- **related files**:
  - data: `functions.md` §1 interfaces (primary `#6 all_attribution_sum`, `#5 all_attribution_list`; drill `#4 ad_analysis_list`), `access.yaml`
  - report assembly: `functions.md` §3
  - chained plans: `channel-profit-quality`, `budget-expansion-decision`, `roas-decline-diagnosis`
  - on-the-fly artifacts: `utilities/`
- **analysis approach**: revenue and ROAS can look healthy while **profit bleeds** — COGS, shipping, fees and discounts eat the margin. This plan re-bases the picture on **net profit / margin** by channel/campaign, exposing "positive ROAS, negative profit" pockets, and ranks by profit contribution rather than vanity revenue.
- **solution space**: a profit-ranked channel/campaign view + flagged unprofitable or thin-margin pockets + recommendations (pause/scale-back unprofitable, protect margin) + chained next plan. Issues **recommendations only**; no spend changes.

## 2. Trigger & Boundary

- **Invocation**: always invoked by SKILL.md routing (no auto-trigger).
- **Intent examples that route here**: "are we actually profitable", "profit by channel", "ROAS is good but are we making money", "which channels lose money".
- **Boundary**: this plan does channel/campaign profit attribution. Deeper per-channel margin drivers go to `channel-profit-quality`; reallocation toward profitable channels goes to `budget-expansion-decision`.
- **Pre-flight clarification (converge BEFORE fetching; skip what's known):**
  1. **Is COGS configured in Convbox?** (HARD prerequisite — see §3; if unknown, confirm before promising profit output)
  2. **Period & scope?** (default last full month for profit stability; channel or campaign level)
  3. **Profit definition expectation?** (net profit = sales − COGS − shipping − fees − spend, per platform config; state what's included)

## 3. Pre-flight Checks

- **HARD prerequisite — COGS configured**: profit fields (`profit` / `margin`) depend on the shop having configured COGS / shipping / fees in Convbox. **On load, probe one summary call; if profit fields are null/empty, do NOT fabricate profit.** Either:
  - **halt** with: "Profit analysis needs cost (COGS) configured in Convbox; currently unavailable. Configure costs, or I can run a ROAS-only view instead." — and offer the degraded path; or
  - proceed in an explicitly-labeled **revenue/ROAS-only** mode if the user accepts.
- **tier**: Basic. Empty `records` → "no data" vs "tier not open"; never fabricate.
- **caliber**: profit is computed on **attributed** revenue (`roas` caliber), not platform-reported; state this.

## 4. Data Context Preparation

- **functions.md version gate**: built against `functions.md` **`1.1.0`**. On load, read the version in functions.md Metadata; **if it differs, STOP** with "Data cannot be prepared — functions.md version mismatch (plan expects 1.1.0, found <X>)." and terminate.
- **fetch plan**:

| Step | Interface | Params template | Purpose |
|------|-----------|-----------------|---------|
| a | `#6 all_attribution_sum` | `{...,dimensions:"channel",model,goal}` | overall profit / margin / spend / conversion_value (and COGS-presence probe) |
| b | `#5 all_attribution_list` | `{...,dimensions:"channel",sort_by:"main_conversions",sort:"desc"}` | per-channel profit / margin / roas. 🔴 sort_by:"profit" silently returns empty — sort server-side by main_conversions, rank by `profit`/`margin` in-kernel |
| c | `#4 ad_analysis_list` (drill) | `{...,dimensions:"campaign"}` | campaign-level profit / margin within a channel |

> `dimensions` takes a **single string value** (e.g. `"channel"`), not an array — an array collapses to one bogus aggregate row. To split by multiple dimensions, call the interface once per dimension.

- **caliber reminders**: `profit` / `margin` need COGS (see §3). ROAS (`roas`) and profit can diverge — a high-ROAS channel can be unprofitable if margin is thin or discount-heavy. Rank by **profit contribution**, not revenue. *(`margin` from the API is a decimal, not a percent — ×100 before display/threshold compare.)*

## 5. Analysis Steps (Data → Analyze → Compare → Conclude → Next)

1. **Data**: probe a (overall + COGS presence). If profit available, fetch b (per channel); drill c on the worst/largest.
2. **Analyze**: for each channel/campaign compare **ROAS vs margin** — flag the "positive ROAS / negative-or-thin profit" pockets; compute profit contribution share.
3. **Compare**: rank by `profit`; tag margin against thresholds; identify which channels carry vs drain total profit.
4. **Conclude**: state overall profitability (profitable / break-even / loss) + the specific unprofitable/thin pockets driving it.
5. **Next**: chain to `channel-profit-quality` (why a channel's margin is thin), `budget-expansion-decision` (shift toward profitable), or `roas-decline-diagnosis` (if the profit drop traces to an efficiency drop).

**Profit root-cause (symptom → likely cause → next):**

| Symptom | Likely cause | Next |
|---------|--------------|------|
| Positive ROAS, negative profit | COGS/discount eating margin | `channel-profit-quality`; review promo |
| Thin margin on a big channel | low-margin product mix promoted | `channel-profit-quality` |
| Profit ↓ but ROAS flat | rising COGS/fees/shipping | cost-side review (later-tier plans) |

**Default margin thresholds (override by shop baseline):** margin 🟡 < 15% / 🔴 < 10%; profit 🟡 < break-even / 🔴 < −(material loss); profit Δ% 🟡 −15~−25% / 🔴 < −25%. *(`margin` is a decimal — ×100 before comparing to these % thresholds.)*

## 6. Output

- **(A) Direct single-scenario call** — may render the self-contained template below.
- **(B) Inside a daily/weekly/monthly or suite report** — no own template; defer to `functions.md` §3; supply only the blocks below.

**Self-contained template (mode A only):**

```markdown
# Profit Attribution Diagnosis — <period>
**Shop:** <shop>　**Range:** <period>　**Basis:** attributed revenue, net of COGS/shipping/fees/spend

## Verdict
Overall: <Profitable / Break-even / Loss>, net profit <$X> (margin <Y%>). Drain: <channel(s)>.

## Profit by Channel (ranked by net profit)
| Channel | Net profit | Net margin | True ROAS | Spend | Flag |
|---------|-----------:|-----------:|----------:|------:|------|

## Recommendations
<pause/scale-back unprofitable; protect margin; "recommendation, pending human execution">
```

**Blocks to feed assembly (mode B):**
- metric block: per channel — profit, margin, true ROAS, spend; overall profitability.
- diagnosis block: profitability verdict + unprofitable/thin pockets + profit-contribution shares.
- recommendation block: pause/scale-back/margin-protect actions; mark "recommendation, pending human execution".

## 7. Chaining & Notes

**Chaining:** `channel-profit-quality` (per-channel margin drivers); `budget-expansion-decision` (reallocate toward profit); `roas-decline-diagnosis` (if profit drop is an efficiency drop).

**Data notes:**
- **No COGS → no profit.** Never infer or fabricate profit; either halt or run an explicitly-labeled ROAS-only view (§3).
- Profit is on attributed revenue, not platform-reported — state the basis so it isn't confused with platform dashboards.
- Use a longer window (month) for profit stability; refunds/returns lag and distort short windows.
- Empty `records` ≠ 0 — handle per §3; never fabricate.
