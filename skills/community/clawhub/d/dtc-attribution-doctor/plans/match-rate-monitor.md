# Plan: Match Rate Monitor (match-rate-monitor)

## 1. Metadata

- **version**: 0.1.0
- **suite**: Data Quality & Tracking Governance
- **functions.md scenario (mapping key)**: 订单 / 用户 / Session 匹配率监控
- **requires functions.md version**: `1.1.0` — verified in §4; on mismatch, halt.
- **dev status**: in-development
- **related files**:
  - data: `functions.md` §1 interfaces (primary `#3 connection_destination`, `#5 all_attribution_list`), `access.yaml`
  - report assembly: `functions.md` §3
  - chained plans: `tracking-health-monitor`, `platform-vs-onsite-discrepancy`
  - on-the-fly artifacts: `utilities/`
- **analysis approach**: monitor capture/match quality by reading attributed conversions against the available attributed volume and the share that lands unattributed, then tie any low capture back to tracking configuration via `connection_destination`. Read attributed `conversions` / `conversion_value` per channel from `#5`, surface the unattributed/direct share, and cross-reference `#3` event flags so a low-capture symptom is explained by a concrete tracking gap rather than left as an unexplained number.
- **solution space**: a capture verdict framing attributed vs available volume and unattributed share, linked to the tracking-config root cause, with a recommendation on which tracking gap to close. Recommendations only — no config or spend changes (human execution).

## 2. Trigger & Boundary

- **Invocation**: always invoked by SKILL.md routing (no auto-trigger).
- **Intent examples that route here**: "what's our match rate", "how many orders are we capturing", "lots of sales show as direct/unattributed", "are we losing attribution coverage".
- **Boundary**: this plan frames capture/match quality and ties it to tracking config; it does NOT itself audit each event flag in depth (that is `tracking-health-monitor`) nor compare platform-reported vs attributed figures (that is `platform-vs-onsite-discrepancy`).
- **Pre-flight clarification (converge BEFORE fetching; skip what's known from memory/context):**
  1. **Period?** (default = last full week)
  2. **Scope — overall capture or per channel/destination?** (default = overall, then drill the weakest)
  3. **Attribution model & goal?** (default `First click`, `purchase`; held consistent across the read)

## 3. Pre-flight Checks

- **tier**: Basic. Empty `records` → distinguish "no data" vs "tier not open"; never fabricate.
- **business prerequisites**: period, `model`, `goal` (confirm via `#1 setting_goals`, default `purchase`) for the `#5` read; at least one configured destination for the `#3` cross-reference.
- **caliber**: capture is framed on **attributed `conversions` / `conversion_value` and the unattributed share**, using true attribution; `ad_net_roas` is not the subject. The `#3` read supplies tracking-config context, not metrics.

## 4. Data Context Preparation

- **functions.md version gate**: built against `functions.md` **`1.1.0`**. On load, read the version in functions.md Metadata; **if it differs, STOP**: tell the user "Data cannot be prepared — functions.md version mismatch (plan expects 1.1.0, found <X>); the data contract may have changed." and terminate.
- **fetch plan**:

| Step | Interface | Params template | Purpose |
|------|-----------|-----------------|---------|
| a | `#5 all_attribution_list` | `{start_date,end_date,dimensions:"channel",model,goal,sort_by:"main_conversions",sort:"desc"}` | attributed conversions / value per channel + the direct/unattributed share as a capture proxy |
| b | `#3 connection_destination` | `{}` (all destinations) | tracking config (`server_config.*` / `browser_config.*` / `configuration.code`) to explain low capture |

- **caliber reminders**: see §1 of functions.md; key here — true attribution only; `#3` is config not metrics; empty `records` may be no data or tier not open.

- **API limitation (state explicitly)**: there is NO backend-total-orders / store-truth field and NO full-match-rate / capture-rate field in the current 9-interface API. A literal "orders captured ÷ all store orders" cannot be computed. Capture is therefore framed against **attributed volume vs available attributed data plus the unattributed/direct share, cross-referenced with tracking health (`connection_destination`)** — NOT against a fabricated store-of-record total. Flag this as a current-API limitation wherever a true denominator would be wanted; do not invent a backend number.

## 5. Analysis Steps (Data → Analyze → Compare → Conclude → Next)

1. **Data**: fetch a (attributed per channel, incl. direct/unattributed) and b (tracking config).
2. **Analyze — frame capture** without inventing a store-truth denominator:
   - quantify the unattributed/direct share of `conversions` / `conversion_value` as a capture proxy.
   - for channels/destinations with high unattributed share, read the matching `#3` event flags — is `checkout_completed` off, or server-side disabled?
3. **Compare**: rank channels/destinations by unattributed share; overlay each weak one against its tracking-config gap; tag 🟡 (moderate unattributed) / 🔴 (high unattributed + a confirmed config gap).
4. **Conclude**: state the capture picture (attributed vs available, unattributed share) and name the tracking gap most likely driving low capture — explicitly noting the no-store-truth limitation.
5. **Next**: for a deep per-event config audit → `tracking-health-monitor`; if low capture coincides with a platform-vs-attributed gap → `platform-vs-onsite-discrepancy`. Recommendations only.

**Capture ladder (symptom → diagnosis → next):**

| Symptom | Diagnosis | Next plan |
|---------|-----------|-----------|
| High unattributed/direct share | capture loss — likely tracking gap | `tracking-health-monitor` |
| Low capture + `checkout_completed` off | purchase events not firing | `tracking-health-monitor` |
| Low capture + server-side disabled | browser-only loss to blockers/ITP | `tracking-health-monitor` |
| Low capture coincides with platform over-report | tracking loss inflating the platform gap | `platform-vs-onsite-discrepancy` |

## 6. Output

- **(A) Direct single-scenario call** — may render the self-contained template below.
- **(B) Inside a daily/weekly/monthly or suite report** — no own template; defer to `functions.md` §3 assembly; supply only the blocks below.

**Self-contained template (mode A only):**

```markdown
# Match Rate Monitor — <period>
**Shop:** <shop>　**Range:** <window>　**Model:** <model>　**Scope:** <overall / channel>

## Verdict
Unattributed/direct share <X%> of attributed conversions. Most likely driver: <destination> — <tracking gap>.

## Capture by Channel
| Channel | conversions (attributed) | conversion_value | Unattributed share | Linked config gap | Status |
|---------|-------------------------------|------------------|--------------------|-------------------|--------|

## Note
No backend store-truth/total-orders field exists in the current API; capture is framed on attributed + unattributed share + tracking health, not a true order denominator.

## Next Step
<which plan to chain; "recommendation, pending human execution">
```

**Blocks to feed assembly (mode B):**
- metric block: attributed `conversions`/`conversion_value` per channel + unattributed share; linked `#3` config gap.
- diagnosis block: capture picture + most-likely tracking driver; explicit no-store-truth limitation note.
- recommendation block: which tracking gap to close; chain target(s); mark "recommendation, pending human execution".

## 7. Chaining & Notes

**Chaining**: `tracking-health-monitor` (deep per-event config audit behind the capture gap), `platform-vs-onsite-discrepancy` (if low capture coincides with platform over-reporting). See the capture ladder (§5).

**Data notes:**
- No backend-total-orders / store-truth and no full-match-rate field exist in the current API — never fabricate a denominator; frame capture on attributed + unattributed share + tracking health.
- True attribution only; `ad_net_roas` is out of scope here.
- `#3` is config not metrics — it explains *why* capture may be low, it does not measure it.
- Equal-length window, consistent `model` for the `#5` read.
- Empty `records` ≠ 0 — handle per §3; state "no data" vs "tier not open".
