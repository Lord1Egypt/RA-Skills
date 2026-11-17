# Plan: Channel Profit Quality (channel-profit-quality)

## 1. Metadata

- **version**: 0.1.0
- **suite**: Profit Protection Dashboard
- **functions.md scenario (mapping key)**: 渠道利润质量分析
- **requires functions.md version**: `1.1.0`
- **dev status**: in-development
- **related files**:
  - data: `functions.md` §1 interfaces (primary `#5 all_attribution_list`, `#6 all_attribution_sum`, `#4 ad_analysis_list`), `access.yaml`
  - report assembly: `functions.md` §3
  - chained plans: `profit-attribution-diagnosis`, `channel-budget-allocation`
  - on-the-fly artifacts: `utilities/`
- **analysis approach**: explain a channel's **profit quality**, not just its ROAS — break down per-channel margin drivers via `margin`, AOV, and relative cost by channel, and surface why a channel earns thin profit despite a respectable ROAS (low AOV, discount-heavy mix, or high relative cost). COGS configuration is **required**; without it, halt or degrade to a no-profit version and say so. *(`margin` is a decimal — ×100 before displaying as a percent.)*
- **solution space**: a per-channel profit-quality verdict naming the thin-margin driver(s) (recommendations only, human execution). Hands the reallocation action to `channel-budget-allocation`.

## 2. Trigger & Boundary

- **Invocation**: always invoked by SKILL.md routing (no auto-trigger).
- **Intent examples that route here**: "which channels are actually profitable", "this channel's ROAS is fine but profit is thin", "why is channel X not making money", "rank channels by margin not ROAS".
- **Boundary**: this plan explains per-channel profit quality and its drivers; it does NOT decide the budget reallocation or do whole-account profit attribution — it hands the mix change to `channel-budget-allocation` and the account-level profit decomposition to `profit-attribution-diagnosis`.
- **Pre-flight clarification (converge BEFORE fetching; skip what's known from memory/context):**
  1. **Period & comparison?** (default = last full week vs prior equal week)
  2. **All channels or specific channel(s)?**
  3. **Is COGS configured?** (profit fields require it; confirm before profit analysis)

## 3. Pre-flight Checks

- **tier**: Basic. Empty `records` → distinguish "no data" vs "tier not open"; never fabricate.
- **business prerequisites**: period, `model`, `goal` (confirm via `#1 setting_goals`, default `purchase`). **COGS required** for `profit`/`margin`; if absent, halt or degrade to a no-profit version and state the limitation explicitly.
- **caliber**: efficiency read on true `roas`; `ad_net_roas` reference only. `#5`/`#6` paired with identical params. Both periods equal length, same `model`/`goal`.

## 4. Data Context Preparation

- **functions.md version gate**: built against `functions.md` **`1.1.0`**. On load, read the version in functions.md Metadata; **if it differs, STOP**: tell the user "Data cannot be prepared — functions.md version mismatch (plan expects 1.1.0, found <X>); the data contract may have changed." and terminate.
- **fetch plan**:

| Step | Interface | Params template | Purpose |
|------|-----------|-----------------|---------|
| a | `#6 all_attribution_sum` (current + prior) | `{start_date,end_date,dimensions:"channel",model,goal}` ×2 | overall profit / margin anchor |
| b | `#5 all_attribution_list` (current + prior) | `{...,dimensions:"channel",sort_by:"main_conversions",sort:"desc"}` ×2 | per-channel `margin`/AOV/`roas` for margin drivers. 🔴 sort_by:"profit" silently returns empty — sort server-side by main_conversions, rank by `profit`/`margin` in-kernel |
| c | `#4 ad_analysis_list` (drill thin-margin channel) | `{...,dimensions:"campaign"}` | locate cost / mix driver behind thin margin |

- **caliber reminders**: see §1 of functions.md; key here — profit needs COGS (else halt/degrade); `roas` vs `ad_net_roas` not mixed; AOV from value / `conversions`; empty `records` ≠ 0.

## 5. Analysis Steps (Data → Analyze → Compare → Conclude → Next)

1. **Data**: confirm COGS; fetch a (anchor) and b (per-channel margin drivers); drill c on the thin-margin channel.
2. **Analyze — margin drivers per channel**:
   - `margin` as the profit-quality axis, separate from `roas`.
   - AOV (value / `conversions`) to explain margin — low AOV thins profit even at decent ROAS.
   - cross-check cost via `#4`: high relative cost or discount-heavy mix as the driver.
3. **Compare**: per channel, `margin` / AOV / `roas` vs prior; tag 🟡/🔴; flag channels where ROAS is fine but margin is thin.
4. **Conclude**: name each thin-profit channel + its driver (low AOV, high relative cost, or discount mix).
5. **Next**: route per the profit-quality map (§7).

**Profit-quality map (symptom → diagnosis → next):**

| Symptom | Diagnosis | Next plan |
|---------|-----------|-----------|
| Decent `roas`, low `margin` | thin profit despite efficiency | `profit-attribution-diagnosis` |
| Low AOV driving thin margin | basket / mix issue | `channel-budget-allocation` (reweight) |
| Margin thin across channels | structural cost / pricing | `profit-attribution-diagnosis` |

## 6. Output

- **(A) Direct single-scenario call** — may render the self-contained template below.
- **(B) Inside a daily/weekly/monthly or suite report** — no own template; defer to `functions.md` §3 assembly; supply only the blocks below.

**Self-contained template (mode A only):**

```markdown
# Channel Profit Quality — <period>
**Shop:** <shop>　**Range:** <current> vs <prior>　**Model:** <model>　**COGS:** <configured / not configured>

## Verdict
Thinnest-margin channel: <channel> — driver: <low AOV / high relative cost / discount mix>.

## Channel Profit Scorecard
| Channel | roas | margin | AOV | Driver | Status |
|---------|------|--------|-----|--------|--------|
*(`margin` is a decimal — ×100 before displaying as a percent.)*

## Next Step
<which specialist plan to run; "recommendation, pending human execution">
```

**Blocks to feed assembly (mode B):**
- metric block: per-channel `margin`, AOV, `roas` — current/prior/Δ%/status.
- diagnosis block: thin-margin channels + driver + evidence.
- recommendation block: profit-quality fixes / reweight to consider; mark "recommendation, pending human execution".

## 7. Chaining & Notes

**Chaining**: from `profit-attribution-diagnosis` (when account-level profit points at channels); out to `channel-budget-allocation` (to reweight by profit quality) — see the profit-quality map (§5).

**Data notes:**
- **COGS required**: without it, `margin`/`profit` may be empty — halt or degrade to a no-profit version and say so explicitly.
- Equal-length windows, same model — otherwise margin trend is meaningless.
- Profit quality is not ROAS: a channel can be efficient yet unprofitable; report both.
- True `roas` only; `ad_net_roas` is reference.
- Empty `records` ≠ 0 — handle per §3; never fabricate.
