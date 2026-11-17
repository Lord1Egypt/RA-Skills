# Plan: Tracking Health Monitor (tracking-health-monitor)

## 1. Metadata

- **version**: 0.1.0
- **suite**: Data Quality & Tracking Governance
- **functions.md scenario (mapping key)**: Pixel / Server-side Tracking 异常监控
- **requires functions.md version**: `1.1.0` — verified in §4; on mismatch, halt.
- **dev status**: in-development
- **related files**:
  - data: `functions.md` §1 interfaces (primary `#3 connection_destination`), `access.yaml`
  - report assembly: `functions.md` §3
  - chained plans: `platform-vs-onsite-discrepancy`, `match-rate-monitor`
  - on-the-fly artifacts: `utilities/`
- **analysis approach**: audit per-destination tracking configuration via `connection_destination`. For each destination, inspect `server_config` and `browser_config` event flags to determine whether server-side / CAPI is enabled and which key events (`checkout_completed`, `product_added_to_cart`, `checkout_started`, `product_viewed`) are on or off, and read `configuration.code` warnings. Missing or disabled key events — especially `checkout_completed` or a server-side path that is off — are flagged as tracking-loss risk that can silently undercount conversions.
- **solution space**: a per-destination health verdict listing disabled/missing key events and config warnings, with a recommendation on which tracking gaps to close first. Recommendations only — no config changes (human execution).

## 2. Trigger & Boundary

- **Invocation**: always invoked by SKILL.md routing (no auto-trigger).
- **Intent examples that route here**: "is our pixel set up right", "check server-side tracking / CAPI", "are we missing purchase events", "tracking health check", "why might we be losing conversion data".
- **Boundary**: this plan audits tracking configuration and flags loss risk; it does NOT quantify the resulting attributed-vs-available gap (that is `match-rate-monitor`) nor measure platform-vs-attributed reporting (that is `platform-vs-onsite-discrepancy`).
- **Pre-flight clarification (converge BEFORE fetching; skip what's known from memory/context):**
  1. **Scope — all destinations or a named one?** (default = audit all configured destinations)
  2. **Which events matter most?** (default = the four key events; confirm if the user cares about a specific one like `checkout_completed`)
  3. **Server-side focus?** (confirm whether the concern is CAPI/server-side specifically or the full browser+server picture)

## 3. Pre-flight Checks

- **tier**: Basic. Empty `records` → distinguish "no destinations configured / no data" vs "tier not open"; never fabricate a config state.
- **business prerequisites**: at least one configured destination. This is a configuration audit — no period/`model`/`goal` is required since `#3` returns config, not time-series metrics.
- **caliber**: this plan reads tracking config only (`server_config.*`, `browser_config.*`, `configuration.code`); it does NOT read `roas`/`ad_net_roas` and makes no attribution claims — it identifies *risk*, which downstream plans quantify.

## 4. Data Context Preparation

- **functions.md version gate**: built against `functions.md` **`1.1.0`**. On load, read the version in functions.md Metadata; **if it differs, STOP**: tell the user "Data cannot be prepared — functions.md version mismatch (plan expects 1.1.0, found <X>); the data contract may have changed." and terminate.
- **fetch plan**:

| Step | Interface | Params template | Purpose |
|------|-----------|-----------------|---------|
| a | `#3 connection_destination` | `{}` (all destinations) | per-destination `server_config.*` / `browser_config.*` event flags + `configuration.code` |

- **caliber reminders**: see §1 of functions.md; key here — `#3` returns configuration, not metrics; treat absent flags as "unknown / verify", not as a fabricated "off"; empty `records` may mean no destination configured *or* tier not open.

## 5. Analysis Steps (Data → Analyze → Compare → Conclude → Next)

1. **Data**: fetch a — all destinations with their `server_config` / `browser_config` flags and `configuration.code`.
2. **Analyze — read the event matrix** per destination:
   - is server-side / CAPI enabled? (read `server_config`)
   - for each key event (`checkout_completed`, `product_added_to_cart`, `checkout_started`, `product_viewed`): on or off in browser and/or server?
   - parse `configuration.code` for warnings indicating misconfiguration.
3. **Compare**: build a destination × event on/off matrix; flag any destination where a key event (especially `checkout_completed`) is disabled or where the server-side path is off; tag 🟡 (partial gap) / 🔴 (key event or server-side missing).
4. **Conclude**: name the destinations with tracking-loss risk and the specific missing/disabled events or config warnings.
5. **Next**: if loss risk is found, it may explain a platform-vs-attributed gap → `platform-vs-onsite-discrepancy`; to quantify how much capture is lost → `match-rate-monitor`. Recommendations only.

**Tracking-risk ladder (symptom → diagnosis → next):**

| Symptom | Diagnosis | Next plan |
|---------|-----------|-----------|
| `checkout_completed` off / missing | purchase undercount — highest-severity loss | `match-rate-monitor` |
| Server-side / CAPI disabled | browser-only — vulnerable to blockers/ITP loss | `platform-vs-onsite-discrepancy` |
| Upper-funnel events off (`product_viewed`, `product_added_to_cart`) | weak signal for optimization & funnel diagnosis | `match-rate-monitor` |
| `configuration.code` warning present | explicit misconfiguration to resolve | (flag for human fix) |

## 6. Output

- **(A) Direct single-scenario call** — may render the self-contained template below.
- **(B) Inside a daily/weekly/monthly or suite report** — no own template; defer to `functions.md` §3 assembly; supply only the blocks below.

**Self-contained template (mode A only):**

```markdown
# Tracking Health Monitor
**Shop:** <shop>　**Scope:** <all destinations / named>

## Verdict
<N> destination(s) audited; <M> with tracking-loss risk. Highest severity: <destination> — <missing/disabled event>.

## Event Matrix by Destination
| Destination | Server-side / CAPI | checkout_completed | product_added_to_cart | checkout_started | product_viewed | configuration.code | Status |
|-------------|--------------------|--------------------|------------------------|------------------|----------------|--------------------|--------|

## Next Step
<which plan to chain; "recommendation, pending human execution">
```

**Blocks to feed assembly (mode B):**
- metric block: destination × event on/off matrix + server-side flag + config warnings.
- diagnosis block: destinations with loss risk + specific missing/disabled events/warnings.
- recommendation block: which gaps to close first; chain target(s); mark "recommendation, pending human execution".

## 7. Chaining & Notes

**Chaining**: `platform-vs-onsite-discrepancy` (tracking loss can explain a widening platform-vs-attributed gap), `match-rate-monitor` (quantify the capture impact of the loss). See the tracking-risk ladder (§5).

**Data notes:**
- `#3` is configuration, not metrics — this plan flags *risk*, it does not measure conversion volume.
- Treat an absent flag as "verify", not as a confirmed "off"; never fabricate a config state.
- Empty `records` ≠ 0 — may mean no destination configured or tier not open; state which per §3.
- A disabled `checkout_completed` event is the single highest-severity finding — surface it first.
