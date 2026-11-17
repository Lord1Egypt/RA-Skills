# Plan: Add-to-Cart Anomaly (add-to-cart-anomaly)

## 1. Metadata

- **version**: 0.1.0
- **suite**: Site Conversion Diagnostic Suite
- **functions.md scenario (mapping key)**: 加购率异常诊断
- **requires functions.md version**: `1.1.0`
- **dev status**: in-development
- **related files**:
  - data: `functions.md` §1 interfaces (primary `#7 web_analysis_list`), `access.yaml`
  - report assembly: `functions.md` §3
  - chained plans: `site-funnel-diagnosis`, `landing-page-reception`
  - on-the-fly artifacts: `utilities/`
- **analysis approach**: focus on the add-to-cart stage of the onsite funnel and split it into two sub-steps — **Product→ATC** (PDP, pricing, stock signals) and **ATC→Purchase** (checkout friction, shipping surprise, payment). Using `product_view_users`, `atc_users`, `purchases`, and `purchases_rate`, locate which sub-step breaks and on which segment, rather than reporting a single blended ATC rate.
- **solution space**: a verdict naming the broken sub-step and segment plus the leading friction hypothesis (recommendations only, human execution). Hands the broader funnel and page-reception context to neighbor plans.

## 2. Trigger & Boundary

- **Invocation**: always invoked by SKILL.md routing (no auto-trigger).
- **Intent examples that route here**: "add-to-cart rate dropped", "people view products but don't add to cart", "carts aren't converting to checkout", "ATC is down this week".
- **Boundary**: this plan isolates the ATC-stage break (which sub-step, which segment); it does NOT diagnose page reception upstream or rebuild checkout — it hands off to `landing-page-reception` for upstream entry quality and to `site-funnel-diagnosis` for end-to-end funnel context.
- **Pre-flight clarification (converge BEFORE fetching; skip what's known from memory/context):**
  1. **Period & comparison?** (default = last full week vs prior equal week)
  2. **Which sub-step suspected — Product→ATC or ATC→Purchase, or diagnose both?**
  3. **Segment to slice?** (device / landing page / collection — else slice by the strongest available dimension)

## 3. Pre-flight Checks

- **tier**: Basic. Empty `records` → distinguish "no data" vs "tier not open"; never fabricate.
- **business prerequisites**: period and a sub-step / segment focus. No profit fields needed.
- **caliber**: `web_analysis_list` is onsite-only; do NOT mix with platform-reported metrics. Both periods equal length. Read ATC as two sub-steps, not one blended rate.

## 4. Data Context Preparation

- **functions.md version gate**: built against `functions.md` **`1.1.0`**. On load, read the version in functions.md Metadata; **if it differs, STOP**: tell the user "Data cannot be prepared — functions.md version mismatch (plan expects 1.1.0, found <X>); the data contract may have changed." and terminate.
- **fetch plan**:

| Step | Interface | Params template | Purpose |
|------|-----------|-----------------|---------|
| a | `#7 web_analysis_list` (current + prior) | `{start_date,end_date}` ×2 | overall ATC sub-step rates + period Δ |
| b | `#7 web_analysis_list` (current + prior, segmented) | `{...,dimensions:"landing_page"}` (or device/collection) ×2 | locate which segment drives the break |

- **caliber reminders**: see §1 of functions.md; key here — onsite metrics only; Product→ATC = `atc_users / product_view_users`, ATC→Purchase = `purchases / atc_users`; empty `records` ≠ 0.

## 5. Analysis Steps (Data → Analyze → Compare → Conclude → Next)

1. **Data**: fetch a (overall sub-steps) and b (segmented).
2. **Analyze — split the ATC stage**:
   - **Product→ATC** = `atc_users / product_view_users` → PDP clarity, pricing, stock/availability signals.
   - **ATC→Purchase** = `purchases / atc_users` (cross-check `purchases_rate`) → checkout friction, shipping/tax surprise, payment.
   - decide which sub-step moved; do not blend the two into one number.
3. **Compare**: per segment, Δ% of each sub-step vs prior; tag 🟡/🔴; isolate the segment carrying the loss.
4. **Conclude**: name the **broken sub-step + segment + leading hypothesis** (e.g., "ATC→Purchase −18% on mobile: shipping surprise at checkout").
5. **Next**: route per the sub-step map (§7).

**Sub-step map (symptom → diagnosis → next):**

| Symptom | Diagnosis | Next plan |
|---------|-----------|-----------|
| Product→ATC ↓ | PDP / pricing / stock signal issue | `landing-page-reception` (if entry-driven) |
| ATC→Purchase ↓ | checkout friction / shipping surprise / payment | `site-funnel-diagnosis` |
| Both ↓ across segments | broad funnel issue | `site-funnel-diagnosis` |
| Drop isolated to one lander/segment | upstream traffic quality | `landing-page-reception` |

## 6. Output

- **(A) Direct single-scenario call** — may render the self-contained template below.
- **(B) Inside a daily/weekly/monthly or suite report** — no own template; defer to `functions.md` §3 assembly; supply only the blocks below.

**Self-contained template (mode A only):**

```markdown
# Add-to-Cart Anomaly — <period>
**Shop:** <shop>　**Range:** <current> vs <prior>　**Scope:** <segment>

## Verdict
Broken sub-step: <Product→ATC / ATC→Purchase> on <segment> — <friction hypothesis>.

## Sub-step Breakdown
| Sub-step | Segment | Current | Prior | Δ% | Status |
|----------|---------|---------|-------|----|--------|
(Product→ATC, ATC→Purchase, purchases_rate)

## Next Step
<which specialist plan to run; "recommendation, pending human execution">
```

**Blocks to feed assembly (mode B):**
- metric block: Product→ATC and ATC→Purchase rates + `purchases_rate`, overall and per segment — current/prior/Δ%/status.
- diagnosis block: broken sub-step + segment + hypothesis + evidence.
- recommendation block: targeted PDP / checkout fixes to review; mark "recommendation, pending human execution".

## 7. Chaining & Notes

**Chaining**: from `site-funnel-diagnosis` (when the funnel localizes to ATC); to `landing-page-reception` (when upstream entry quality drives it) — see the sub-step map (§5).

**Data notes:**
- Equal-length windows — otherwise the sub-step delta is meaningless.
- Never blend Product→ATC and ATC→Purchase into one ATC number; they fail for different reasons.
- `web_analysis_list` is onsite-only; do not add platform-reported numbers.
- A drop isolated to one segment is a different story than a broad one; state which.
- Empty `records` ≠ 0 — handle per §3; never fabricate.
