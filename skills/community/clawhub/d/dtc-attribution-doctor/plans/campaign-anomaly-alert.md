# Plan: Campaign Anomaly Alert (campaign-anomaly-alert)

## 1. Metadata

- **version**: 0.1.0
- **suite**: Performance Marketing Copilot
- **functions.md scenario (mapping key)**: Campaign异常预警
- **requires functions.md version**: `1.1.0` — verified in §4; on mismatch, halt.
- **dev status**: in-development
- **related files**:
  - data: `functions.md` §1 interfaces (primary `#4 ad_analysis_list`), `access.yaml`
  - report assembly: `functions.md` §3
  - chained plans: `roas-decline-diagnosis`, `cpa-rise-diagnosis`, `creative-performance`, `ad-audience-performance`, `budget-pacing-alert`
  - on-the-fly artifacts: `utilities/`
- **analysis approach**: scan all campaigns for anomalies — spend spike/drop, **true ROAS** or CPA threshold breach, new campaigns still in learning, and paused campaigns. Threshold-flag each anomaly, rank by spend/impact, and dispatch the worst to the matching specialist plan. This is a campaign-level radar, not a deep root-cause analysis.
- **solution space**: a ranked anomaly list (campaign, anomaly type, impact) + the dispatch target for each. Recommendations only; pause/budget actions are human-executed.

## 2. Trigger & Boundary

- **Invocation**: always invoked by SKILL.md routing (no auto-trigger).
- **Intent examples that route here**: "anything wrong with my campaigns", "flag campaign anomalies", "what's off today", "which campaigns need attention".
- **Boundary**: this plan detects and ranks anomalies and points to the right specialist; it does NOT diagnose root cause in depth or execute fixes — it hands off per anomaly type.
- **Pre-flight clarification (converge BEFORE fetching; skip what's known from memory/context):**
  1. **Period & comparison?** (default = yesterday vs prior-day / trailing-7d same-position average)
  2. **Scope — all campaigns or a specific channel?** (if named, scope to it; else all)
  3. **Thresholds — use defaults or user limits?** (default: spend ±30%, ROAS −20%, CPA +25%; confirm if the user has internal targets)

## 3. Pre-flight Checks

- **tier**: Basic. Empty `records` → distinguish "no data" vs "tier not open"; never fabricate.
- **business prerequisites**: period, `model`, `goal` (confirm via `#1 setting_goals`, default `purchase`).
- **caliber**: threshold checks use **true `roas`** and true CPA (`spend / conversions`); `ad_net_roas` is reference only. Both periods equal length, same `model`/`goal`.

## 4. Data Context Preparation

- **functions.md version gate**: built against `functions.md` **`1.1.0`**. On load, read the version in functions.md Metadata; **if it differs, STOP**: tell the user "Data cannot be prepared — functions.md version mismatch (plan expects 1.1.0, found <X>); the data contract may have changed." and terminate.
- **fetch plan**:

| Step | Interface | Params template | Purpose |
|------|-----------|-----------------|---------|
| a | `#4 ad_analysis_list` (current + prior, campaign) | `{start_date,end_date,dimensions:"campaign",model,goal,sort_by:"spend",sort:"desc"}` ×2 | per-campaign spend / roas / cpa / status → flag threshold breaches |
| b | `#4 ad_analysis_list` (drill a flagged campaign) | `{...,dimensions:"ad_set"}` | confirm the anomaly is real before dispatch (optional) |

- **caliber reminders**: see §1 of functions.md; key here — flags computed on true `roas` / true CPA, not `ad_net_roas`; new campaigns in learning should not be flagged as "broken".

## 5. Analysis Steps (Data → Analyze → Compare → Conclude → Next)

1. **Data**: fetch a (campaign, both periods).
2. **Analyze — apply anomaly checks** per campaign:
   - spend spike / drop beyond threshold; true ROAS below floor; true CPA above ceiling.
   - new campaign in learning phase (mark "monitor, do not over-react").
   - paused / zero-delivery campaign (mark "delivery stopped").
3. **Compare**: campaign current vs prior; compute Δ%, flag 🟡 (near threshold) / 🔴 (breach).
4. **Conclude**: rank flagged campaigns by spend/impact; assign each an anomaly type + dispatch target.
5. **Next**: dispatch per the anomaly table (§7).

**Anomaly → dispatch table:**

| Anomaly | Dispatch to |
|---------|-------------|
| True ROAS breach | `roas-decline-diagnosis` |
| True CPA breach | `cpa-rise-diagnosis` |
| Creative/CTR-driven drop | `creative-performance` |
| Audience saturation / CPM spike | `ad-audience-performance` |
| Spend overshoot / pacing | `budget-pacing-alert` |
| New campaign in learning | monitor only (no dispatch yet) |
| Paused / zero delivery | flag for human review (delivery stopped) |

## 6. Output

- **(A) Direct single-scenario call** — may render the self-contained template below.
- **(B) Inside a daily/weekly/monthly or suite report** — no own template; defer to `functions.md` §3 assembly; supply only the blocks below.

**Self-contained template (mode A only):**

```markdown
# Campaign Anomaly Alert — <period>
**Shop:** <shop>　**Range:** <current> vs <prior>　**Model:** <model>　**Scope:** <all / channel>

## Flagged campaigns (ranked by impact)
| Campaign | Anomaly | Metric (cur → prior, Δ%) | Status | Dispatch |
|----------|---------|--------------------------|--------|----------|

## Watchlist
<new-in-learning / paused / zero-delivery — monitor only>

## Next Step
<dispatch targets; "recommendation, pending human execution">
```

**Blocks to feed assembly (mode B):**
- metric block: flagged campaigns with spend / true roas / true cpa / status — current/prior/Δ%.
- diagnosis block: anomaly type per campaign + evidence.
- recommendation block: dispatch target per anomaly; mark "recommendation, pending human execution".

## 7. Chaining & Notes

**Chaining**: see the anomaly → dispatch table (§5) — each anomaly type routes to its specialist plan; overspend → `budget-pacing-alert`.

**Data notes:**
- Equal-length windows, same model — otherwise thresholds misfire.
- Threshold flags use true `roas` / true CPA; `ad_net_roas` only contextualizes over-report.
- A new campaign in learning is NOT an anomaly — exclude it from breach flags, list it on the watchlist.
- A paused / zero-delivery campaign reads as empty/zero `records`; distinguish "no data" vs "delivery stopped" — never fabricate.
- Single-day windows are noisy; corroborate against the trailing-7d same-position average before escalating.
