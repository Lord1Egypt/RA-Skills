# Plan: Landing Page Reception (landing-page-reception)

## 1. Metadata

- **version**: 0.1.0
- **suite**: Site Conversion Diagnostic Suite
- **functions.md scenario (mapping key)**: 落地页承接诊断
- **requires functions.md version**: `1.1.0`
- **dev status**: in-development
- **related files**:
  - data: `functions.md` §1 interfaces (primary `#7 web_analysis_list`), `access.yaml`
  - report assembly: `functions.md` §3
  - chained plans: `site-funnel-diagnosis`, `add-to-cart-anomaly`, `platform-vs-onsite-discrepancy`
  - on-the-fly artifacts: `utilities/`
- **analysis approach**: assess how well landing pages **receive** incoming traffic — for each `landing_page`, read `engagement_rate`, `event_per_session`, and the early-funnel users (`homepage_view_users` / `product_view_users` / `atc_users`). Set page-type baselines (blog vs `/products/` vs `/collections/` vs `/pages/`) because a blog post and a PDP convert very differently, then rank high-friction pages by traffic × drop-off so the largest recoverable loss surfaces first.
- **solution space**: a ranked list of pages that leak the most reception value plus the friction hypothesis for each (recommendations only, human execution). Hands off the deeper fix to funnel / ATC plans.

## 2. Trigger & Boundary

- **Invocation**: always invoked by SKILL.md routing (no auto-trigger).
- **Intent examples that route here**: "are our landing pages converting", "this campaign's landing page feels weak", "which pages bounce traffic", "why do paid clicks not engage on site".
- **Boundary**: this plan diagnoses page-level reception (engagement + early-funnel entry); it does NOT diagnose the add-to-cart sub-step or rebuild pages — it hands off to `add-to-cart-anomaly` for the ATC stage and to `site-funnel-diagnosis` for whole-funnel context.
- **Pre-flight clarification (converge BEFORE fetching; skip what's known from memory/context):**
  1. **Period & comparison?** (default = last full week vs prior equal week)
  2. **Scope — all pages or specific landing page(s) / campaign landers?**
  3. **Page-type focus?** (blog / `/products/` / `/collections/` / `/pages/` — else baseline all types)

## 3. Pre-flight Checks

- **tier**: Basic. Empty `records` → distinguish "no data" vs "tier not open"; never fabricate.
- **business prerequisites**: period and a page or page-type scope. No profit fields needed.
- **caliber**: `web_analysis_list` is onsite-only; do NOT mix with platform-reported metrics. Both periods equal length. Compare like-for-like page types — never benchmark a blog against a PDP.

## 4. Data Context Preparation

- **functions.md version gate**: built against `functions.md` **`1.1.0`**. On load, read the version in functions.md Metadata; **if it differs, STOP**: tell the user "Data cannot be prepared — functions.md version mismatch (plan expects 1.1.0, found <X>); the data contract may have changed." and terminate.
- **fetch plan**:

| Step | Interface | Params template | Purpose |
|------|-----------|-----------------|---------|
| a | `#7 web_analysis_list` (current + prior) | `{start_date,end_date,dimensions:"landing_page"}` ×2 | per-page reception metrics + period Δ |
| b | `#7 web_analysis_list` (current) | `{...,dimensions:"landing_page"}` | rank pages by traffic, weighting drop-off by volume (sort client-side by unique_users; web-analysis sort_by returns empty) |

- **caliber reminders**: see §1 of functions.md; key here — onsite metrics only; `engagement_rate` and `event_per_session` read together (high traffic + low engagement = reception leak); empty `records` ≠ 0.

## 5. Analysis Steps (Data → Analyze → Compare → Conclude → Next)

1. **Data**: fetch a (per-page metrics, both periods) and b (traffic ranking).
2. **Analyze — reception health per page**:
   - read `engagement_rate` and `event_per_session` as the reception signal (did arriving visitors do anything?).
   - trace early funnel: `homepage_view_users` / `product_view_users` / `atc_users` relative to `unique_users` — where does each page drop visitors first?
   - set page-type baselines so blog vs `/products/` vs `/collections/` vs `/pages/` are judged on their own curve.
3. **Compare**: per page, Δ% of engagement_rate / event_per_session / product_view share vs prior and vs page-type baseline; tag 🟡/🔴.
4. **Conclude**: rank pages by **traffic × drop-off** (recoverable loss); name the top friction pages + hypothesis (slow load, mismatch, weak hero, irrelevant lander).
5. **Next**: if drop concentrates at ATC → `add-to-cart-anomaly`; if it spans the whole funnel → `site-funnel-diagnosis`; if onsite purchases diverge from backend → `platform-vs-onsite-discrepancy`.

**Friction map (symptom → diagnosis → next):**

| Symptom | Diagnosis | Next plan |
|---------|-----------|-----------|
| Low `engagement_rate`, low `event_per_session` | weak reception / mismatch / slow page | (recommend page review) |
| Engaged but `product_view_users` low | lander does not route to product | `site-funnel-diagnosis` |
| `product_view_users` ok, `atc_users` low | PDP / ATC friction | `add-to-cart-anomaly` |
| Onsite purchases vs backend diverge | tracking / attribution gap | `platform-vs-onsite-discrepancy` |

## 6. Output

- **(A) Direct single-scenario call** — may render the self-contained template below.
- **(B) Inside a daily/weekly/monthly or suite report** — no own template; defer to `functions.md` §3 assembly; supply only the blocks below.

**Self-contained template (mode A only):**

```markdown
# Landing Page Reception — <period>
**Shop:** <shop>　**Range:** <current> vs <prior>　**Scope:** <pages / page-type>

## Verdict
Top reception leak: <page> — <friction hypothesis>. Recoverable traffic at risk: <est>.

## Page Ranking (traffic × drop-off)
| Page | Type | Traffic | Engagement | Event/Session | Product-view share | ATC share | Status |
|------|------|---------|-----------|---------------|--------------------|-----------|--------|

## Next Step
<which specialist plan to run; "recommendation, pending human execution">
```

**Blocks to feed assembly (mode B):**
- metric block: per-page `engagement_rate`, `event_per_session`, early-funnel user shares — current/prior/Δ%/status, weighted by traffic.
- diagnosis block: top friction pages + hypothesis + page-type baseline evidence.
- recommendation block: page-level reception fixes to review; mark "recommendation, pending human execution".

## 7. Chaining & Notes

**Chaining**: from `site-funnel-diagnosis` (when the funnel points at landers); out to `add-to-cart-anomaly` (ATC sub-step) and `platform-vs-onsite-discrepancy` (when onsite purchases vs backend diverge).

**Data notes:**
- Equal-length windows — otherwise reception trend is meaningless.
- Never benchmark across page types; a blog's engagement profile is not a PDP's.
- Weight by traffic: a 5% drop on a high-traffic lander beats a 30% drop on a fringe page.
- `web_analysis_list` is onsite-only; do not add platform-reported numbers to it.
- Empty `records` ≠ 0 — handle per §3; never fabricate.
