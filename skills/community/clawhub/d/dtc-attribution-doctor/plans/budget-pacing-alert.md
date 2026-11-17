# Plan: Budget Pacing Alert (budget-pacing-alert)

## 1. Metadata

- **version**: 0.1.0
- **suite**: Growth Command Center
- **functions.md scenario (mapping key)**: 预算 Pacing / 超支预警
- **requires functions.md version**: `1.1.0`
- **dev status**: in-development
- **related files**:
  - data: `functions.md` §1 interfaces (primary `#6 all_attribution_sum`, `#4 ad_analysis_list`), `access.yaml`
  - report assembly: `functions.md` §3
  - chained plans: `budget-expansion-decision`, `campaign-anomaly-alert`
  - on-the-fly artifacts: `utilities/`
- **analysis approach**: track spend pace against a **planned budget** — compute daily burn, project end-of-period spend at the current run-rate, and raise an over- / underspend alert. The budget cap / plan is a **required input** from the user or memory; without it there is no pacing baseline. Localize over-pace to the channel / campaign driving it.
- **solution space**: an over- / on- / underspend verdict with a projected end-of-period figure and the driver, plus a pace-correction recommendation (recommendations only, human execution).

## 2. Trigger & Boundary

- **Invocation**: always invoked by SKILL.md routing (no auto-trigger).
- **Intent examples that route here**: "are we on budget", "will we overspend this month", "is spend pacing right", "alert me if we're burning too fast".
- **Boundary**: this plan reports pace vs plan and flags over/underspend; it does NOT decide whether the budget level itself should change (that is `budget-expansion-decision`) and does NOT diagnose performance anomalies — it hands those to `campaign-anomaly-alert`.
- **Pre-flight clarification (converge BEFORE fetching; skip what's known from memory/context):**
  1. **Planned budget / cap and its period?** (required — from user or memory; without it, no pacing baseline)
  2. **Pacing scope — account total or per channel / campaign?**
  3. **Period boundary?** (calendar month / flight dates — defines elapsed vs remaining)

## 3. Pre-flight Checks

- **tier**: Basic. Empty `records` → distinguish "no data" vs "tier not open"; never fabricate.
- **business prerequisites**: a **planned budget / cap** (required input) and the period boundary. `model`/`goal` confirm via `#1 setting_goals` if performance context is wanted; pacing itself is spend-based. No profit fields needed.
- **caliber**: pace is computed on Convbox-attributed `spend`; do not mix platform-reported spend with attributed spend. Use elapsed days vs total period days consistently.

## 4. Data Context Preparation

- **functions.md version gate**: built against `functions.md` **`1.1.0`**. On load, read the version in functions.md Metadata; **if it differs, STOP**: tell the user "Data cannot be prepared — functions.md version mismatch (plan expects 1.1.0, found <X>); the data contract may have changed." and terminate.
- **fetch plan**:

| Step | Interface | Params template | Purpose |
|------|-----------|-----------------|---------|
| a | `#6 all_attribution_sum` (period-to-date) | `{start_date:<period_start>,end_date:<today>,dimensions:"channel"}` | spend-to-date for burn + projection |
| b | `#4 ad_analysis_list` (drill over-pace channel) | `{...,dimensions:"campaign"}` | locate which campaign drives over/under pace |

- **caliber reminders**: see §1 of functions.md; key here — daily burn = spend-to-date / elapsed days; projected end-of-period = daily burn × total period days; compare projection to the planned budget; empty `records` ≠ 0.

## 5. Analysis Steps (Data → Analyze → Compare → Conclude → Next)

1. **Data**: fetch a (spend-to-date) for the period; drill b if a channel over-paces.
2. **Analyze — pacing math**:
   - daily burn = spend-to-date / elapsed days.
   - projected end-of-period spend = daily burn × total period days.
   - pace variance = projected − planned budget (and % of plan consumed vs % of period elapsed).
3. **Compare**: projection vs planned budget; per channel, identify who runs ahead / behind plan; tag 🟡/🔴.
4. **Conclude**: verdict — overspend / on-pace / underspend, with the projected figure and the driver channel/campaign.
5. **Next**: route per the pacing map (§7).

**Pacing map (symptom → diagnosis → next):**

| Symptom | Diagnosis | Next plan |
|---------|-----------|-----------|
| Projection > plan (overspend) | burn too fast | `budget-expansion-decision` (level call) |
| Projection < plan (underspend) | unspent budget / delivery limited | `campaign-anomaly-alert` (delivery check) |
| One channel drives over-pace | concentrated burn | `budget-expansion-decision` |
| Pace ok but performance shifting | not a pacing issue | `campaign-anomaly-alert` |

## 6. Output

- **(A) Direct single-scenario call** — may render the self-contained template below.
- **(B) Inside a daily/weekly/monthly or suite report** — no own template; defer to `functions.md` §3 assembly; supply only the blocks below.

**Self-contained template (mode A only):**

```markdown
# Budget Pacing Alert — <period>
**Shop:** <shop>　**Period:** <start>–<end>　**Planned budget:** <cap>　**Elapsed:** <d / D days>

## Verdict
<Overspend / on-pace / underspend>. Projected end-of-period: <X> vs plan <Y> (<Δ%>). Driver: <channel/campaign>.

## Pacing Table
| Scope | Spend-to-date | Daily burn | Projected EoP | Planned | Variance | Status |
|-------|---------------|-----------|---------------|---------|----------|--------|

## Next Step
<which specialist plan to run; "recommendation, pending human execution">
```

**Blocks to feed assembly (mode B):**
- metric block: spend-to-date, daily burn, projected end-of-period vs planned budget, % consumed vs % elapsed — overall and per channel/status.
- diagnosis block: over/under pace verdict + driver + evidence.
- recommendation block: pace-correction action; mark "recommendation, pending human execution".

## 7. Chaining & Notes

**Chaining**: out to `budget-expansion-decision` (when the budget level itself is in question) and `campaign-anomaly-alert` (when underspend signals a delivery problem or pace is fine but performance shifts) — see the pacing map (§5).

**Data notes:**
- A planned budget / cap is a **required input**; without it there is no pacing baseline — ask for it, do not assume.
- Elapsed-vs-total day counts must be consistent with the stated period boundary.
- Pace uses Convbox-attributed `spend`; do not mix in platform-reported spend.
- Early-period projections are noisy; flag low confidence when few days have elapsed.
- Empty `records` ≠ 0 — handle per §3; never fabricate.
