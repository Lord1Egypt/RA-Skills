# Action 3 — Auto-report

Produce a visually stunning, on-brand report **adapted to what the user actually does in their workspace**. The agent reads the schema and the data first, then assembles a report from modules that *have data backing them*. Never force a B2B-sales template on a workspace that doesn't have deals.

## When this triggers

User says things like: "give me a report", "how is my CRM doing", "what's working", "deal review", "sales recap", "show me the numbers", "weekly sales report", "agency review", "candidate update", "community engagement report".

## The core principle

> The report adapts to the user, not the other way around.

A B2B SaaS user gets pipeline / win rate / lost reasons. An agency gets project mix / referrals / repeat-client rate. A recruiter gets candidates / placements / time-to-place. A community manager gets active members / engagement / channels. **None of them gets sections backed by data they don't have.**

This is handled by reading the workspace first (introspection), then assembling the report from modules (see `references/report-design-guide.md` for the module catalog).

## Setup questions — bare minimum

Almost everything is decided from workspace introspection. The only thing you sometimes need to ask:

**One-time or recurring?**
> One-time snapshot, or do you want this on a weekly/monthly cadence by email?

If recurring, hand off to `routines.md` for the rest. Default cadence: weekly.

**The user's business — only if the schema is ambiguous.** If you've inferred the business type cleanly from stage names, view names, and object renames, **don't ask**. Only ask when introspection comes back genuinely ambiguous:

> Quick check — should I treat this report as a sales/deal view, a project/agency view, a placement/recruiting view, or a community/engagement view?

Cache the answer for the session.

**Don't ask** about:
- Date range — default to last 30 days. State it in the report; let the user say "make it 90" if they want.
- Which sales rep — show all reps, with a per-rep breakdown only if the workspace is multi-member.
- Format — render in the agent's native rich content surface (artifact, canvas, inline HTML).

## Playbook — exact tool sequence

### Phase 1 — Read the workspace (no writes, fast, cached)

Run discovery once at the top of the report. Cache all results.

1. `workspaces_list` → workspace ID (skip if cached from prior actions).
2. `crm_objects_list` → which objects exist (Person, Company, Deal, custom). Note any renames (`Deal` → `Project`, `Placement`, etc.).
3. `crm_fields_list` (per relevant object) → field IDs, types, names.
4. `crm_field_options_list` on the **pipeline-stage field** (if any) → stage labels and order. **The stage names reveal the business type.**
5. `crm_record_views_list` (per object) → view names. **The view names confirm the business type and reveal what the user actively curates.**
6. `inbox_views_list` → inbox view names.
7. `records_list` per object with a small page size → count records per object, see field-population rates.

### Phase 2 — Detect business type

Use the heuristic table in `report-design-guide.md § Business-type detection`. Examples:

- Stage names `Lead → Engaged → Proposal → Won/Lost`, currency on Deal, multi-member workspace → **B2B sales.**
- Deal object renamed to `Project`, no currency field but a `Status` field with `Briefed / Scoped / Delivered`, Company records central → **Agency.**
- Deal renamed to `Placement`, stages `Sourced → Submitted → Offer → Placed` → **Recruiting.**
- Person object 1,200 records, Deal object 0 records, views like `VIPs / Lapsed / New` → **Community.**

When the inference is clean, **don't ask**. When two business types are plausible (e.g., agency vs B2B sales), ask once with the wording above.

### Phase 3 — Pull data for the reporting window

Default window: **last 30 days**. Default to "rolling" not "calendar" — the date the report runs minus 30 days.

For each in-scope object:

- `records_list` with date filter on `created_at` and `updated_at` → period activity, plus a sample for population stats.
- For deal-cycle math, pull `created_at` + close-date timestamps.
- For channel/reply analytics: `inbox_conversations_search` workspace-wide, filtered to the period. Sample `inbox_messages_list` per conversation to compute reply times and direction. **Sampling is fine** — a stratified sample of 1,000 conversations covers most patterns even in a workspace with 50,000.
- `notes_list` only where qualitative context is needed (loss-reason clustering, spotlight quotes).

**Respect rate limits.** Parallelize within the per-route 120 rpm budget; back off on 429.

### Phase 4 — Decide which modules to render

Walk the module catalog (`report-design-guide.md § The module catalog`) in order. For each module, check its data requirements against what Phase 3 returned. Include or omit.

For each business type, the typical assembly is:

**B2B sales:**
```
M0 (chassis) + M1 (KPI grid: pipeline/won/win-rate/new)
+ M2 (pipeline by stage + donut outcomes) + M3 (loss reasons + spotlight if quotes available)
+ M4 (sources) + M5 (active channels)  — paired two-column
+ M6 (reply rate by channel)
+ M7 (hygiene tiles)
+ M8 (one pattern, if found)
```

**Agency / consultancy:**
```
M0 + M1 (KPI: active projects / repeat clients / avg value / new briefs)
+ M2-lite (project status — 2-4 stages only)
+ M4 (sources — referral lean) + M5 (active channels)
+ M7 (hygiene tiles tuned to agency metrics)
+ M8 (one pattern: e.g., referral renewals vs cold-outreach renewals)
```

**Recruiting:**
```
M0 + M1 (KPI: active candidates / placements / time-to-place / new)
+ M2 (candidate flow by stage — Sourced/Submitted/Offer/Placed)
+ M3 ("Why candidates fall out" if rejection reasons populated)
+ M4 (sources — job board vs referral vs LinkedIn)
+ M7 (hygiene tiles — missing role, missing rate, etc.)
```

**Community / network:**
```
M0 + M1 (KPI: active members / engagement rate / top channel / new members)
+ (skip M2, M3 — no pipeline)
+ M5 (active channels — primary value)
+ M6 (reply rate by channel) — if you've been doing outreach
+ M7 (hygiene tiles: active vs lapsed, missing tags, top segment, total)
+ M8 (one pattern — e.g., reactivation success by re-engagement message style)
```

**Investor / VC:**
```
M0 + M1 (KPI: active deals / closed / avg check / new opportunities)
+ M2 (deal flow by stage)
+ M3 (passed-deal reasons)
+ M4 (sources — inbound vs proprietary)
+ M7 (hygiene: missing stage, missing check size)
```

The assembly above is a **starting point per type, not a rigid template**. If a B2B-sales workspace doesn't have a `lost_reason` field and notes are too sparse to cluster, M3 still gets omitted — never invent a chart.

### Phase 5 — Assemble the HTML

**The chassis is copied verbatim from `assets/report-template.html`. The agent does not rewrite, restructure, or regenerate it.** This is non-negotiable — the brand identity lives in the chassis, and any drift (different header height, repositioned mascot, missing top-bar tag, modified gradients) breaks visual consistency across reports and makes the skill look amateur.

**What "chassis" means precisely:**

| Region              | Status      | What the agent may change                                                                 |
|---------------------|-------------|-------------------------------------------------------------------------------------------|
| `<style>` block     | **VERBATIM**| Nothing. Copy the entire `<style>` block as-is — every CSS variable, every rule, every keyframe. Do not delete unused rules, do not "optimize," do not reorder. |
| Top bar (`.topbar`) | **VERBATIM**| The right-side `.tb-tag` text only (e.g., "7-day sales audit" → "Monthly community pulse"). Nothing else — not the logo SVG, not the heights, not the live-dot. |
| Hero structure (`.hero`, `.hero-bg`, `.hero-row`, `.hero-l`, `.hero-r`, `.bubble`, `.mascot`) | **VERBATIM**| Only the **text content** of `.kicker`, `.h1` headline, `.lede` paragraph, `.bubble` insight, and the three `.hstat` cards' label/value text. The HTML structure, classes, mascot `<img>` element, ambient circles, and all positioning **stay exactly as in the template**. |
| Section headers (`.sec-head`, `.sec-no`, `.kicker`, `.sec-h`) | **STRUCTURE VERBATIM** | Only the kicker label, section number, and title text. Don't change the outlined-number styling or layout. |
| Footer (`.foot`)    | **VERBATIM**| Only the source line text on the right (e.g., "Data: Breakcold inbox & CRM · {date}"). Logo SVG and "Breakcold / CRM audit report" left side stay verbatim. |
| Module bodies (`.card`, `.bars`, `.donut`, `.spotlight`, `.cmp`, `.tiles`) | **CONTENT FILLED** | The bar widths, KPI numbers, labels, captions, donut percentages, spotlight quotes — all replaced with real values. Markup structure stays. |

**The mechanical procedure** (do it in this order):

1. **Read** `assets/report-template.html` start-to-end. Don't paraphrase it from memory — read the actual file each session.
2. **Copy** the file verbatim into your scratchpad as the starting point.
3. **Modify text content only** for the chassis regions per the table above. No CSS edits, no structural HTML edits, no element reordering.
4. **For included modules** (M2 pipeline, M3 spotlight, etc.): take the corresponding HTML block from the template and replace data values inside it. Keep the surrounding markup.
5. **For omitted modules** (e.g., no pipeline data → omit M2): delete the entire `<section>` block cleanly. Don't leave empty divs, dangling section numbers, or commented-out blocks.
6. **Renumber sections** if any were omitted (`.sec-no` runs 01, 02, 03 sequentially with no gaps). This is the *only* structural edit the agent makes.

**Hero specifics — the part the user is most likely to notice:**

- Headline (`.h1`): write per `report-design-guide.md § Hero headline rules`. One sentence, one underlined emphasis (`<span class="ul">...</span>`).
- Lede paragraph (`.lede`): one short paragraph (2-3 sentences) summarizing the week's posture.
- Three `.hstat` cards: pick the right three KPI labels for the business type from `report-design-guide.md § M1 KPI grid`. Use the `<span class="cu">` counter wrapper with static text = final value (see counter contract in the design guide).
- Mascot speech bubble (`.bubble`): one sentence ≤22 words, the single most actionable insight in the entire report. The mascot `<img>` element itself never moves.

**Footer source line:** `Data: Breakcold inbox & CRM · {start} – {end}`.

**Each chart card ends** with a 1-sentence caption (`<p class="cap">`) explaining what's noteworthy — never restating the chart, always saying *the implication*. Max 2 sentences.

### Phase 6 — Deliver

- **Inline render:** drop the HTML into the agent's rich-content surface. Inline the SVG logos and preserve the mascot image already embedded in `assets/report-template.html`.
- **File delivery:** save as `breakcold-report_{YYYY-MM-DD}.html` and present it. Reference the `assets/` folder relatively for SVG assets; the mascot is already embedded in the template.
- **Email delivery** (for recurring routines): the HTML goes in the email body, not as an attachment — the user scrolls, doesn't double-click. Inline the assets.
- **Plain-text fallback** (rare): use a markdown version following the same module structure and order. ASCII bar charts (`|████░░░░ 28`). Skip mascot and visual flourishes. Same omission rules — never fake metrics to look complete.

## Edge cases

- **Workspace has very little data** (< 20 records, < 50 conversations). Tell the user honestly: "Not enough data yet for pattern detection — here's the basic snapshot." Render only the chassis + a single hygiene tile section. Don't fabricate.
- **Mid-month migration or recent setup.** Workspaces that were reorganized recently may have inconsistent stage data. Note it in the footer: "Note: this workspace was reorganized {N} days ago; older records may be missing some fields." Render what you can.
- **Multi-currency.** Convert to a single currency for the headline KPIs. State the conversion source in the footer (e.g., "USD equivalents using current spot rates"). Show original currencies only in detail breakdowns if helpful.
- **Multi-pipeline workspaces** (rare — only when the user opted in during Action 6 setup). Ask the user which pipeline to focus the report on. Don't try to merge them.
- **No clear pipeline-stage field** (e.g., community workspaces). Skip M2 and M3 entirely; lead with channel + engagement (M5, M6).
- **No `lost_reason` field but rich notes.** Use the AI-clustering path described in M3 ("Why deals are lost — from your notes"). Always label that section so the user knows it's inferred, not field-driven.
- **No notes anywhere.** Skip the spotlight (and the legacy callout) sub-module in M3. Bars only.
- **Sample bias warning.** If you sampled conversations (vs. exhaustive read), note it in the relevant section caption ("from a sample of 1,000 of your 47,000 conversations"). Don't pretend the numbers are exhaustive.
- **Mobile rendering.** The template's CSS already includes responsive breakpoints at 720px. Don't add extra mobile logic.

## Quality bar — before shipping

Before delivering, ask yourself:

1. **Does every section have real data behind it, or did I fill in numbers?** If any number is invented or rough-estimated, either remove the section or label it as inferred.
2. **Is the headline insight actually the most actionable thing in the data?** Not the biggest number — the most actionable. "Trial credit-card friction killed 28% of lost deals" beats "you have 1,190 people in your CRM" every time.
3. **Could I delete any section without making the report worse?** If yes, delete it. Shorter = more useful.
4. **Is there a single recommendation paragraph at the bottom?** There shouldn't be. The breakdown does the recommending — if the data is clear, the user knows what to do.
5. **Does it look like Breakcold shipped this?** If a stranger saw the report, would they recognize the brand? If the answer is no, the design tokens weren't applied properly — re-check `branding.md` and the chassis CSS.

## Schedule it as a routine

Hand off to `routines.md`. Default cadence: **weekly**. Anything more frequent triggers the cost warning:

> Weekly is the sweet spot for sales reports — daily reports usually have too little new data to be insightful. Stick with weekly?

The confirmation message becomes:

> I'll send you a **{weekly / monthly}** Breakcold report by email. Each one covers the prior **{7 / 30}** days, adapted to your workspace — pipeline if you have one, projects if you run an agency, candidates if you're recruiting, engagement if you manage a community. Want a custom date range or default to the last **{N}** days?

The recap email body **is** the report HTML — same chassis, same modules, inlined. Subject: `[Breakcold] {Workspace name} report — {date range}`.

## How this composes with the other actions

- After **Action 6 (CRM setup)**, the first report a user runs is a great validation that the workspace is correctly configured. If the report comes out half-empty, that's signal to fill missing fields or run **Action 5 (contact detection)** to populate.
- After **Action 1 (auto-tasks)** runs for a few weeks, the report's "active channels" and "reply rate" modules become much richer — there's data to show.
- After **Action 4 (prospect research)** runs, the report can surface ICP patterns (industry mix, company size mix) because those structured fields are now populated.
