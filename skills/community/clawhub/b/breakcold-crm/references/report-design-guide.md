# Report design guide

How to assemble a Breakcold-branded report that adapts to **what's actually in the user's workspace**, instead of forcing the same B2B-sales template on everyone.

## The mental model

```
report = chassis (always)  +  N modules (conditional, data-driven)
```

- **Chassis** = top bar with logo, hero with mascot + headline, footer with mark. Always present. Visual identity. Comes straight from `assets/report-template.html`.
- **Modules** = self-contained sections (KPI grid, pipeline bars, channel comparison, hygiene tiles, etc.). Each one has explicit **data requirements**. If the user's workspace doesn't meet them, the module is omitted — never rendered empty, never faked.

The agent never "fills in" a section it doesn't have real data for. Empty sections are worse than missing sections.

## Workspace introspection — run this before assembling

Before picking modules, gather:

```
read once (cache for the session):
  - crm_objects_list                       → which objects exist (Person, Company, Deal, custom)
  - crm_fields_list (per object)           → which fields exist; which are select/multiselect/currency/date/relation
  - crm_field_options_list (stage field)   → stage names and order — REVEALS BUSINESS TYPE
  - crm_record_views_list                  → view names — REVEALS WHAT THE USER TRACKS
  - inbox_views_list                       → inbox view names
  - records_list (counts per object)       → how much data each object has
  - records_list (small sample with field population stats)
                                           → which fields are actually populated
```

Three things matter most:

1. **Which objects have meaningful data.** A workspace with 1,200 people and 0 deals is not a B2B-sales workspace — don't render a pipeline section, no matter what fields exist.
2. **Which fields are populated.** A `lost_reason` field with 4 distinct values across 80 lost deals is rich. The same field empty on 80 lost deals = skip the section (or cluster from notes — see below).
3. **What the stage names and view names reveal.** Stage names like `Lead / Engaged / Proposal / Won` say "classic sales." `Sourced / Submitted / Offer / Placed` says "recruiting." `Briefed / Scoped / Delivered` says "agency." `Active / VIP / Lapsed` says "community." Use this to choose KPI metrics and section emphasis.

## Business-type detection from the schema

Rough rules (heuristic, override with explicit user statement):

| Schema signal                                                                | Likely business type    |
|------------------------------------------------------------------------------|-------------------------|
| Deal object has currency field + sales-stage names (`Lead → Won/Lost`)       | **B2B sales (SaaS / services)** |
| Deal object renamed to `Project` / `Engagement` + clients in Company         | **Agency / consultancy**        |
| Deal object renamed to `Placement` + stages like `Sourced → Submitted → Offer` | **Recruiting**                  |
| No Deal records; only Person + Company; engagement-style views               | **Community / network management** |
| Deal object renamed to `Opportunity` + stages like `Sourced → Closed`        | **Investor / VC**               |
| Deal object renamed to `Listing` / `Transaction`                             | **Real estate**                 |

When in doubt and the schema is ambiguous, **ask the user once**: "Quick check — should I treat this report as a sales/deal view, a project/agency view, a placement/recruiting view, or a community/engagement view?" Cache the answer for the session.

## The module catalog

Each module lists: **what it shows**, **data requirements** (must all be true to include), and **the snippet** (copy from `assets/report-template.html`).

### M0 — Chassis (always — copied verbatim)

**The chassis is the brand. It is copied verbatim from `assets/report-template.html`, never regenerated, never restructured, never "improved."** Header height, top-bar tag layout, hero gradient, mascot position, glass `hstat` cards, footer mark — these are visual constants. Drift here is what makes a skill look amateur instead of shipped-by-the-company.

The chassis comprises:

- **Top bar** with `<svg class="logo">` (the full Breakcold wordmark) on the left and a status tag (`.tb-tag`) on the right — e.g., `7-day sales audit`, `Monthly community pulse`, `Q1 partnership review`. The tag includes a small green live dot (`.tb-tag .live`) for a sense of freshness. **Only the tag text changes between reports.**
- **Scroll progress bar** at the very top of the page (`.scrollbar` / `#sp`) — driven by the JS layer, fills as the user scrolls. Pure visual polish. **Don't touch.**
- **Hero** with a deep blue gradient background, two soft radial-glow circles (`hero-bg::before` and `hero-bg::after`) for ambient depth, a subtle SVG-noise overlay for texture, mascot + speech bubble, headline, lede paragraph, and three glass `hstat` pill cards in the bottom row (open metric / rate metric / volume metric). **Only the text content changes: the kicker line, the headline, the lede paragraph, the bubble insight, and the three hstat labels/values. The mascot `<img>`, ambient circles, gradients, paddings, and positioning all stay identical to the template.**
- **Section headers** use the large outlined number style (`.sec-no` with `-webkit-text-stroke`) on the left, a small uppercase blue `kicker` label, and the section title (`sec-h`). **Only the section number and the title text change.** Number sections sequentially with no gaps (`01`, `02`, `03` — if a module is omitted, renumber what remains).
- **Footer** with `<svg>` Breakcold mark + "Breakcold" + a small subtitle ("CRM audit report" or whatever fits the report's type) on the left, source line + generation date on the right. **Only the source line and the subtitle text change.**

**What the agent never modifies:**
- The `<style>` block — verbatim, every rule.
- The logo SVG markup.
- The mascot `<img>` element (`src`, dimensions, positioning).
- The top-bar / hero / footer HTML structure.
- CSS variable values, spacing tokens, shadow tokens, animation keyframes.
- The `<script>` block at the bottom.

If the chassis somehow "looks different" between two reports for the same workspace, that's a bug — the chassis isn't supposed to vary.

### M1 — KPI grid (almost always)

Four-card row at the top of the body. Almost always included; **what's in the cards varies by business type**:

| Business type             | KPI 1            | KPI 2          | KPI 3                  | KPI 4               |
|---------------------------|------------------|----------------|------------------------|---------------------|
| B2B sales                 | Open pipeline $  | Deals won      | Win rate               | New deals           |
| Agency / consultancy      | Active projects  | Repeat clients | Avg project value      | New briefs / leads  |
| Recruiting                | Active candidates| Placements     | Time-to-place (days)   | New candidates      |
| Community / network       | Active members   | Engagement %   | Top channel            | New members         |
| Investor / VC             | Active deals     | Closed (qty)   | Avg check size         | New opportunities   |
| Real estate               | Active listings  | Closed (qty)   | Avg days on market     | New listings        |

**Data requirements (per KPI):**
- A money-denominated KPI (Open pipeline, Avg deal value, Avg check size) requires a currency field on the relevant object with values populated on at least 50% of active records. Otherwise drop that KPI and replace with a count-based one (Active deals, Active projects).
- A rate KPI (Win rate, Engagement %) requires terminal states (Won/Lost or replied/not) identifiable, with at least 10 records in terminal states.
- A time KPI (Time-to-place, Avg cycle) requires creation and close timestamps to span at least 5 closed records.

If only 2 KPIs qualify, render a 2-up grid instead of 4-up (just remove two `<div class="kpi">` blocks; the CSS handles it).

### M2 — Pipeline by stage

**What it shows:** horizontal bars of record count per pipeline stage in the "open pipeline" section, then a **donut chart** sub-component for terminal outcomes (Won / Lost / Not a fit) with a centered win-rate percentage and a legend listing counts and percentages per outcome.

**Layout:** the open-pipeline bars come first (under a `divider` with the total open-pipeline value). The donut comes second under an `Outcomes` divider, paired with the right-side legend (`oc-legend`). On mobile the donut and legend stack.

**Data requirements:**
- A clear pipeline-stage field exists on the primary object.
- At least 10 records distributed across at least 3 stages.
- The total open pipeline value (sum of currency field on open-stage records) is non-zero — *or* drop the dollar amount from the divider and show count only.
- For the donut: at least 5 records in terminal stages so the percentage is meaningful (with fewer, fall back to outcome bars instead of donut).

**Alternate variant — outcome bars** (use when the donut would mislead): swap the `.outcomes` block for the simple bar-row layout from v0.1 — Won/Lost/Not-a-fit as three horizontal bars. Use when terminal counts are very small or when the workspace has 4+ terminal states (donut gets crowded above 3 slices).

**When to omit:** community / network workspaces without a meaningful pipeline. Agencies with a 2-stage flow (`Active / Done`) — render a simpler "Project status" version instead (just 2 bars, skip the donut).

### M3 — Loss / drop-off reasons

**What it shows:** ranked horizontal bars of reasons records exit the pipeline negatively, plus an optional **spotlight panel** highlighting the single biggest leak with quoted user-language from notes on lost records.

**Data requirements:**
- At least 5 records in terminal-negative stages (Lost, Not a fit, Disqualified, Rejected).
- One of:
  - A `lost_reason` (or equivalent) select field populated on at least 60% of lost records. **Or**
  - At least 10 lost records with notes containing reason language the agent can cluster (e.g., "budget," "timing," "competitor"). When clustering, label the section "Loss reasons · clustered from deal notes" so the user knows it's inferred.

**When to omit:** if there's no field and notes are too sparse to cluster — say nothing. Don't invent a chart.

**Spotlight sub-module:** the dark gradient panel (`spotlight` with `spot-l` / `spot-r` two-column layout) is the dramatic version of the old callout. Use it for the single biggest leak in the data — the loss reason that towers over the rest. It surfaces:
- A huge gradient percentage on the left (`spot-big`) — e.g., "28%" of lost deals died at the same cause.
- A short context sentence under it (`spot-bigsub`) — e.g., "18 of 65 — bigger than competitors, price and timing combined."
- Three or fewer direct quotes from your prospects' notes/messages on the right (`spot-q`), each under 25 words.
- A 1-sentence punch line under the quotes (`spot-punch`) connecting the pattern to a concrete fix.

**Spotlight requirements:** include only when (a) you have actual direct quotes — never fabricate, and (b) the top reason is meaningfully larger than the second (at least 1.5× the count). Without those, omit the spotlight and let the bars speak.

**Alternate variant — `callout`** (legacy soft-red panel): if the spotlight feels too dramatic for the data (e.g., medium-sized pattern, not a single dominant cause), the older red-tinted `callout` style is still in the CSS as a milder alternative. Same content rules — under 3 quotes, never fabricated.

### M4 — Sources / acquisition channels

**What it shows:** horizontal bars of record counts grouped by source (Inbound, Outbound, Referral, Event, LLMs, SEO, etc.).

**Data requirements:**
- A `source` field exists on the primary object with at least 60% of records populated. **Or**
- Source can be inferred reliably from another signal (e.g., the channel of the first inbound message — email, LinkedIn, WhatsApp).

**When to omit:** workspace doesn't track source. Don't invent buckets.

### M5 — Active channels by week (paired with M4 in a two-column layout)

**What it shows:** count of records with last-interaction this period, grouped by channel (email, LinkedIn, WhatsApp, Telegram, meeting).

**Data requirements:**
- Inbox conversations span at least 2 channels.
- At least 20 conversations had activity in the reporting period.

**When to omit:** single-channel workspace.

### M6 — Reply rate by channel (comparison cards)

**What it shows:** side-by-side cards showing reply rate per channel from a sampled set of outbound threads.

**Data requirements:**
- At least 2 channels with at least 10 outbound threads each (so the rate isn't 1-of-1 noise).
- The agent can determine outbound vs. inbound on each thread.

**When to include single-channel:** if only one channel has volume, replace this section with a single-card "Reply rate this period" instead of the comparison layout.

### M7 — Hygiene tiles

**What it shows:** 4 small tiles with counts (e.g., monthly vs. annual subscriptions, records missing key fields, average won-deal value, total CRM size).

**Data requirements:** none — this section is always available. The metrics shown adapt:

| Workspace type     | Tile candidates                                                    |
|--------------------|--------------------------------------------------------------------|
| B2B sales          | Monthly vs. annual subs · Missing plan type · Avg won value · CRM size |
| Agency             | Active vs. completed projects · Missing project value · Repeat-client % · CRM size |
| Recruiting         | Open roles · Missing role detail · Avg time-to-place · Candidate pool size |
| Community          | Active vs. lapsed members · Missing tags · Top engagement segment · Member count |
| Generic            | Records added this period · Records missing X · Avg X · Total CRM size |

Always include "CRM size" as the last tile — it grounds the rest.

### M8 — Pattern detection (replaces or augments M3)

**What it shows:** one paragraph or one inferred chart highlighting **a single strong pattern** the agent found in the data — e.g., "reply rate jumps 60% on emails under 40 chars" or "deals from referrals close 2× faster than cold outreach."

**Data requirements:**
- Enough data to make the pattern statistically meaningful (not 2 cases vs. 1 case).
- The pattern is novel (not just restating a metric already in the KPIs).

**When to include:** if you find one strong, actionable pattern. **Maximum one pattern per report.** If you have three patterns, pick the highest-leverage one — the report's job is the breakdown, not the data dump.

## Progressive enhancement — the JS layer

The template ships with a small inline `<script>` at the bottom that adds **purely visual** enhancements on top of the static HTML. Everything still renders correctly without JavaScript — the JS only adds polish.

What the JS does:
- **Scroll progress bar** — the thin gradient bar at the top of the page fills as the reader scrolls.
- **Counter animations** — any `<span class="cu">` with `data-to`, `data-pre`, `data-suf`, and optional `data-dec` attributes animates from 0 up to the target value when scrolled into view. Examples in the template:
  - `<span class="cu" data-to="2596" data-pre="$">$2,596</span>` — animates to `$2,596`.
  - `<span class="cu" data-to="21.7" data-dec="1" data-suf="%">21.7%</span>` — animates to `21.7%` with one decimal.
- **Intersection-observer reveals** — elements with `data-reveal` attribute fade up as they enter the viewport. Stagger them with `data-d="1"` / `data-d="2"` / `data-d="3"` / `data-d="4"` for cascade timing.
- **Bar fills and donut sweep** animate in once the section is revealed (CSS transitions gated on the `.in` class added by the observer).
- **`prefers-reduced-motion: reduce`** is respected — users with motion-reduction enabled see the final state immediately, no animation.

What the agent needs to do when filling in the template:
- Wrap KPI numbers, donut percentages, hygiene tile values, and spotlight numbers in `<span class="cu" data-to="NUMBER" data-pre="PREFIX" data-suf="SUFFIX" data-dec="DECIMALS">DISPLAY VALUE</span>`.
- **Set the static text inside `<span class="cu">` to the FINAL value, not zero.** The template's starter file ships with `0` / `$0.00` placeholders, but those are just placeholders — when the agent fills in real data, the static text should match what `data-to` resolves to. Example: a hygiene tile showing 104 monthly plans must render as `<span class="cu" data-to="104">104</span>`, not `<span class="cu" data-to="104">0</span>`. **Why:** the JS calls `setZero` on load before animating up, so the user with JS sees the count-up animation regardless. The user **without JS** (PDF export, email preview, accessibility-tool reader, JS-stripped artifact renderer) sees the static text — and a wall of zeros is worse than no animation. Always populate the static text.
- Set bar fill widths with `style="--w:42.5%"` — the JS reads the CSS variable and animates from 0 to that width on reveal.
- Add `data-reveal` (and optional `data-d="1..4"` for stagger) to any section you want to fade in on scroll. The static fallback (no JS) shows everything immediately, so this is purely additive.
- Don't add new tracking, analytics, or external script dependencies — the JS is self-contained and ~30 lines. Keep it that way.

If the agent is rendering inside a chat-platform surface that strips `<script>` tags (some artifact renderers do), the report still looks great — the static HTML is the full visual. The animations just don't fire.

## Hero headline rules

The hero headline is a single sentence with **one strong noun phrase**, plus an underlined emphasis on the most actionable insight. Examples:

- B2B sales: `A strong week of grooming — and one leak worth plugging.`
- Agency: `Three new briefs — and one client renewing for the third year.`
- Recruiter: `Six placements in two weeks — your fastest cycle this quarter.`
- Community: `Engagement is up 18% — driven entirely by your Discord push.`

**The mascot speech bubble** holds the single most actionable insight the report contains. 1 sentence, ≤22 words, ends with a concrete number when possible. Examples:

- `Trial credit-card friction killed 28% of your lost deals — your #1 deal-killer.`
- `Referral-sourced clients renew at 3× the rate of cold-outreach ones.`
- `LinkedIn replies in under 4 hours; email takes 38. Lead with LinkedIn.`

The mascot insight must be the same as (or feed) the underlined emphasis in the headline. They reinforce, not duplicate.

## What never goes in the report

- "Generated by AI" footer / disclaimer.
- Vanity counts ("you sent 412 emails this month") without an outcome attached.
- A "Recommendations" wall of bullet points — the breakdown does the recommending.
- Pie charts with 5+ slices.
- Rainbow gradients on bar fills (use Breakcold blue or one tag-palette color per series).
- Lorem-ipsum-style filler when a section runs short on data — omit the section.

## How to fill the template

1. Open `assets/report-template.html`.
2. Keep the `<style>` block as-is. Keep the chassis (top bar, hero, footer).
3. **For each module, decide include or omit using the data-requirements rules above.**
4. For included modules, copy the corresponding section block and replace numbers/labels/captions with real values from the workspace.
5. The mascot image is already embedded inline in `assets/report-template.html`; the SVG mark in the footer comes from the assets folder. Keep SVG paths relative if the user will open the file locally, or inline the SVG XML if delivering inline in chat.
6. Update the date range, the workspace name (subtle, in the kicker), and the footer source line.

## When delivering inline (no file)

If the agent's runtime renders HTML inline, inline the SVG logos and preserve the template's embedded mascot image. The CSS is self-contained — paste the `<style>` block, then the module HTML in order.

If the runtime can't render HTML, fall back to a markdown version that follows the same module structure and ordering. Skip the mascot and visual flourishes; keep the section headings and the bar-chart-style counts as `|███████░░░ 28` ASCII bars. **Same modules, same omission rules** — never a "default sales template" pretending the user has deals.
