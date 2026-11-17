# Plan: Site Funnel Diagnosis (site-funnel-diagnosis)

## 1. Metadata

- **version**: 0.1.0
- **suite**: Site Conversion Diagnostic Suite
- **functions.md scenario (mapping key)**: 站内转化漏斗诊断
- **requires functions.md version**: `1.1.0` — verified in §4; on mismatch, halt.
- **dev status**: in-development
- **related files**:
  - data: `functions.md` §1 interface (primary `#7 web_analysis_list`), `access.yaml`
  - report assembly: `functions.md` §3
  - chained plans: `landing-page-reception`, `add-to-cart-anomaly`, `roas-decline-diagnosis`, `ad-landing-page-match`, `platform-vs-onsite-discrepancy`
  - on-the-fly artifacts: `utilities/`
- **analysis approach**: a flat overall CVR hides stage-level leakage. Walk the on-site funnel **Homepage → Product View → Add-to-Cart → Purchase**, find the weakest rung, then isolate which channel / campaign / landing page creates the leak, and rank fixes by lost revenue.
- **solution space**: the bottleneck stage + the worst segments driving it + a prioritized remediation list (which page/stage, est. revenue impact) + chained next plan. Does NOT change pages/checkout (human execution).

## 2. Trigger & Boundary

- **Invocation**: always invoked by SKILL.md routing (no auto-trigger).
- **Intent examples that route here**: "why did CVR drop", "where are users dropping off", "run funnel analysis", "high add-to-cart but no purchase".
- **Boundary**: this plan locates the leaking stage + segments and dispatches; deep landing-page friction goes to `landing-page-reception`, checkout/ATC specifics go to `add-to-cart-anomaly`. If the leak is really traffic quality (not the site), hand back to `roas-decline-diagnosis` / audience.
- **Pre-flight clarification (converge BEFORE fetching; skip what's known):**
  1. **Period & comparison?** (default = last full week vs prior equal week; or single-period snapshot if user just wants "where's the leak now")
  2. **Scope — overall, or a specific channel / landing page / campaign?**
  3. **Stage focus?** (whole funnel by default; or a named stage like checkout)

## 3. Pre-flight Checks

- **tier**: Basic. Empty `records` → "no data" vs "tier not open"; never fabricate. Guard division-by-zero on stage ratios → report stage CVR as 0 and flag a data-quality note.
- **business prerequisites**: period; `dimensions` non-empty. `goal`/`model` per functions.md defaults.
- **note**: `web_analysis_list` `spend` is 0 for organic channels — don't treat organic as "free conversions with no cost context".

## 4. Data Context Preparation

- **functions.md version gate**: built against `functions.md` **`1.1.0`**. On load, read the version in functions.md Metadata; **if it differs, STOP** with "Data cannot be prepared — functions.md version mismatch (plan expects 1.1.0, found <X>)." and terminate.
- **fetch plan**:

| Step | Interface | Params template | Purpose |
|------|-----------|-----------------|---------|
| a | `#7 web_analysis_list` (current) | `{start_date,end_date,dimensions:"channel"}` (call once each for utm_campaign / landing_page) | funnel by segment: homepage_view_users → product_view_users → atc_users → purchases, + engagement_rate, spend |
| b | `#7 web_analysis_list` (prior, optional) | same, prior equal window | stage-level trend (is the leak new or chronic?) |
| c | `#7 web_analysis_list` (drill) | `dimensions:"landing_page"` filtered to the worst segment | page-level isolation |

- **stage ratios** (compute in reasoning):
  - Homepage→Product = `product_view_users / homepage_view_users`
  - Product→ATC = `atc_users / product_view_users`
  - ATC→Purchase = `purchases / atc_users`
  - Overall = `purchases_rate`

## 5. Analysis Steps (Data → Analyze → Compare → Conclude → Next)

1. **Data**: fetch a (segmented funnel); b for trend; c to isolate worst page.
2. **Analyze — leakage detection**: compute the three stage ratios + overall; find the stage with the largest abnormal drop vs baseline (store median or prior period).
3. **Compare**: rank worst segments (channel / campaign / landing_page) by drop-off × volume; quantify lost revenue using `spend`, the purchase gap, and value sourced from all-attribution `conversion_value`.
4. **Conclude**: name the bottleneck stage + top leaking segments (e.g., "Product→ATC is the leak; concentrated on /products/hero from paid_social").
5. **Next**: route per stage (§7).

**Stage root-cause (stage → likely cause → next):**

| Weakest stage | Likely cause | Next |
|---------------|--------------|------|
| Homepage→Product (drop > 20%) | message mismatch / low-quality traffic / weak relevance | `ad-landing-page-match`; if traffic quality → `roas-decline-diagnosis` |
| Product→ATC (drop > 15%) | pricing / weak PDP / stock | `landing-page-reception` (PDP); pricing review |
| ATC→Purchase (drop > 15%) | checkout friction / shipping surprise / payment | `add-to-cart-anomaly` (checkout/payment) |
| Low `engagement_rate` | poor audience fit | `ad-audience-performance` |

**Default stage thresholds (vs baseline):** 🟡 > 15% drop / 🔴 > 30% drop; overall `purchases_rate` 🟡 < 2% / 🔴 < 1%; `engagement_rate` 🟡 < 40% / 🔴 < 20%.

## 6. Output

- **(A) Direct single-scenario call** — may render the self-contained template below.
- **(B) Inside a daily/weekly/monthly or suite report** — no own template; defer to `functions.md` §3; supply only the blocks below.

**Self-contained template (mode A only):**

```markdown
# Site Funnel Diagnosis — <period>
**Shop:** <shop>　**Range:** <current>　**Scope:** <overall / segment>

## Health Summary
Overall CVR <X%>. Primary bottleneck: <stage>. Severity: <Normal/Watch/Alert>.

## Stage Breakdown
| Stage | Users | Drop-off | CVR to next | Status |
|-------|------:|---------:|------------:|--------|
(Homepage / Product View / Add to Cart / Purchase)

## Worst Segments (by drop-off × volume)
| Channel | Campaign | Landing page | Stage | Est. lost revenue |

## Next Step
<which specialist plan; "recommendation, pending human execution">
```

**Blocks to feed assembly (mode B):**
- metric block: stage ratios + overall CVR + engagement, current/prior/Δ/status.
- diagnosis block: bottleneck stage + top leaking segments + est. lost revenue.
- recommendation block: next plan per stage; mark "recommendation, pending human execution".

## 7. Chaining & Notes

**Chaining**: see the stage root-cause table (§5).

**Data notes:**
- Page-type baselines differ (blog vs /products/ vs /collections/): judge each landing page against its own type, not a single store-wide bar.
- Organic `spend` = 0; frame organic leaks by volume/revenue, not ROAS.
- Short windows skew stage ratios; prefer ≥ 7 days for trend, but a single-period snapshot is fine for "where's the leak now".
- If purchases diverge from backend orders, the leak may be a tracking gap, not a real funnel drop → `platform-vs-onsite-discrepancy`.
- Empty `records` ≠ 0 — handle per §3; never fabricate.
