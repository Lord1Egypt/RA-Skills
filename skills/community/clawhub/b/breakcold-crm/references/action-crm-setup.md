# Action 6 — CRM setup & reorganization

Set up a Breakcold workspace from scratch — or take a messy existing one and reorganize it — based on the user's website URL. The goal: replace what a CRM-integrator consultant would charge thousands of dollars for, in a few minutes. **Simple, actionable, no fluff.**

## When this triggers

User says things like: "set up my CRM", "I'm new to Breakcold", "reorganize my CRM", "make my CRM make sense", "redo the pipeline from scratch", "I want a clean Breakcold workspace".

## What you need from the user — minimal input

### Best case: a website URL

> Send me your website URL — I'll do the rest.

You'll scrape the homepage and key pages (About, Pricing, Product, Services) to infer:
- What they sell.
- Who they sell to (their ICP language).
- The sales motion (transactional, consultative, enterprise).
- Vocabulary they use ("clients" vs "customers" vs "members", "engagement" vs "deal" vs "project").

### Fallback: ask once

If there's no website (or nothing scrapeable), or the site is bare:

> Tell me about your business in a few sentences — what do you sell, who do you sell to, and what's the typical sales cycle like? Even a rough sketch is enough.

Don't run a long interview. One paragraph is plenty.

## The opinionated defaults — apply unless the user pushes back

These are constraints, not suggestions. They exist because the user explicitly asked for "simple but actionable."

### Objects

- **Do not create custom objects** unless the user explicitly asks. Person, Company, Deal cover 99% of cases.
- **You may rename the Deal object** if "deal" doesn't fit the user's vocabulary. Examples:
  - Agency → **Project** or **Engagement**
  - Recruiter → **Placement**
  - Real estate → **Listing** or **Transaction**
  - Investor → **Opportunity**
  - Membership business → **Member**
  - SaaS → keep **Deal**, it works
- Use `crm_objects_update` to rename. Don't rename Person or Company unless the user insists.

### Custom fields

- **Maximum 3 custom fields per object type.** Be ruthless — every field must change a decision the user makes.
- **Multi-select is often the best fit** — flexible, filterable, low cognitive cost. Use single-select when there's a clear order or strict cardinality.
- Default candidates to consider (pick the **3 that matter most** for the user's business):

  **Person:**
  - **Role** (multi-select: Decision Maker / Champion / Influencer / End User / Gatekeeper)
  - **Source** (single-select: Inbound / Outbound / Referral / Event / Existing Network)
  - **Seniority** (single-select: C-level / VP / Director / Manager / IC)
  - **ICP fit** (single-select: 1 / 2 / 3 / Out)

  **Company:**
  - **Industry** (multi-select, tailored to the user's market)
  - **Size** (single-select: 1-10 / 11-50 / 51-200 / 201-1k / 1k+)
  - **Stage** (single-select: Cold / Active / Customer / Churned) — only if there's no equivalent on Deal

  **Deal:**
  - **Source** (single-select)
  - **Lost reason** (single-select: Budget / Timing / Competitor / No Fit / No Decision / Ghosted)
  - **Channel** (multi-select: Email / LinkedIn / WhatsApp / Telegram / Phone / Meeting)

  Pick the most relevant **3** per object. **No more.**

### Pipeline stages

- **One pipeline** by default. **Two only when there's a strong reason** (e.g., the user does both inbound and outbound and wants to manage them separately, or sells two distinct products). Never three.
- **8 to 10 stages maximum.** Five to seven is the sweet spot for most.
- **Use the user's language**, not generic sales jargon. If they say "engaged" and "scoping", use those.
- A clean default template (rename to match the user's vocabulary):

  | # | Default name      | Meaning                                              |
  |---|-------------------|------------------------------------------------------|
  | 1 | Lead              | Identified, not yet contacted                        |
  | 2 | Contacted         | Outreach sent, no reply yet                          |
  | 3 | Engaged           | Two-way conversation started                         |
  | 4 | Qualified         | Confirmed fit, mutual interest                       |
  | 5 | Proposal          | Proposal / quote sent                                |
  | 6 | Negotiation       | Price, terms, contract back-and-forth                |
  | 7 | Won               | Closed positive (terminal)                           |
  | 8 | Lost              | Closed negative (terminal)                           |

  Plus, optionally, **On Hold** as a side-bucket if the user mentioned long-tail re-engagement.

  Translate freely. An agency might use: *Lead → Briefed → Scoped → Proposal → Signed → Delivered → Lost.* A recruiter: *Sourced → Reached out → Interviewing → Submitted → Offer → Placed → Lost.*

- Use `crm_field_options_create` and `crm_field_options_reorder` to build / order the stages.

### Record views

- **People: 5 max.** Tailored to the user's actual workflow.
- **Companies: 3 max.**
- **Deals: 3 max.**

Each view must be **actionable** — answer one specific question the user opens the CRM to answer.

**Default Person views (pick the 5 most useful):**

| View name             | What it shows                                                  |
|-----------------------|----------------------------------------------------------------|
| `All`                 | Everyone. Always include.                                      |
| `Hot`                 | Engaged / Qualified stages, sorted by last activity desc       |
| `Quiet`               | Last activity > 7 days, in any non-terminal stage              |
| `New`                 | Created in the last 7 days                                     |
| `My open`             | Owner = current user, non-terminal stage                       |

**Default Company views:**

| View name      | What it shows                                                  |
|----------------|----------------------------------------------------------------|
| `All`          | Everyone                                                       |
| `Active`       | Companies with at least one Deal in a non-terminal stage       |
| `Customers`    | Companies with a Won Deal                                      |

**Default Deal views:**

| View name      | What it shows                                                  |
|----------------|----------------------------------------------------------------|
| `Pipeline`     | Kanban / board view of non-terminal stages                     |
| `This month`   | Close date this month                                          |
| `At risk`      | Non-terminal, no activity in 14+ days                          |

Use `crm_record_views_create` per view, then `crm_record_views_reorder` to put the most useful first.

### Inbox views

- **4 max.** Each one actionable. Usually based on **last interaction** (for follow-ups) or **stage filtering** (group of people in the same pipeline stage).

**Default inbox views (pick 4):**

| View name        | What it shows                                                  |
|------------------|----------------------------------------------------------------|
| `Unanswered`     | Last message inbound, no reply from user                       |
| `Quiet`          | Last message > 7 days ago, non-terminal stage                  |
| `Hot`            | Recent activity on records in Engaged / Qualified stages       |
| `Untriaged`      | Conversations not yet linked to a record                       |

Use `inbox_views_create` for each, then `inbox_views_sidebar_reorder` so they appear in the chosen order.

### Naming convention — strict

The user said: **2 words max, or 3 words max with one being very short** (e.g., a number, or a 1–3 char proper word).

Good: `Hot`, `Quiet`, `My open`, `At risk`, `Lost 2026`, `Top 50`, `New leads`.
Bad: `High priority opportunities`, `Recently active customer prospects`, `Q4 enterprise pipeline focus`.

Apply the same rule to field names, option names, and view names.

### Column order in views

For each view created, **reorder the columns** so the most useful columns appear first, given the view's purpose:

- `Hot` Person view: Name | Stage | Last activity | Owner | Source.
- `Pipeline` Deal view: Name | Stage | Value | Close date | Owner.
- `At risk` Deal view: Name | Stage | Last activity | Days quiet | Owner.

Use `crm_record_views_update` with the full saved config to set column order — the API replaces the full config, so include the complete configuration in the call.

## Playbook — exact tool sequence

### Phase 1 — Scrape and decide (no writes yet)

1. **Get the website URL.** Fetch the homepage + 2–3 key pages. Extract the user's vocabulary, ICP, sales motion. If no URL, ask the single fallback question above.

2. **Plan, don't write yet.** Build a full picture **internally**:
   - Object renames (just Deal, maybe).
   - 3 custom fields per object — chosen with the user's business in mind.
   - The pipeline (stage names + count).
   - The views (Person, Company, Deal, Inbox) with names and column order.

3. **Show the user the plan in one message** before touching the workspace:

   > Based on **{site or description}**, here's the plan:
   >
   > **Objects** — keep Person and Company as-is; rename Deal to **{X}** (matches your vocabulary).
   > **Custom fields** — Person: {3}. Company: {3}. {X}: {3}.
   > **Pipeline** — one pipeline, **{N}** stages: {comma-separated names}.
   > **Views** — Person: {names}. Company: {names}. {X}: {names}. Inbox: {names}.
   >
   > Want me to ship this, or change anything first?

   This is the **only** confirmation message in the entire setup. Make it count. Don't go field-by-field.

### Phase 2 — Discover existing state (if reorganizing)

Skip if it's a fresh workspace.

4. **Inventory what exists now:**
   - `crm_objects_list` — what objects exist? Custom ones?
   - `crm_fields_list` per object — which fields exist? Which are user-created vs system?
   - `crm_field_options_list` for each select/multiselect field.
   - `crm_record_views_list` per object — which views exist?
   - `inbox_views_list` — which inbox views exist?
   - `records_list` per object — how many records exist? (Just a count or a small sample.)

5. **Decide what to keep, rename, remap, or delete.** Be conservative:
   - **Keep** any field that has data, unless it's clearly broken or redundant.
   - **Rename** fields that have data but bad names — never delete data the user might still want.
   - **Remap** option IDs where you're consolidating stages (e.g., user had 14 stages, you're going to 8 — map old → new before deleting old options, so existing records survive).
   - **Delete** only after remapping is in place.

### Phase 3 — Apply the plan (writes)

6. **Apply in this order to avoid orphan states:**

   a. **Rename objects** (`crm_objects_update`) — if Deal is being renamed.

   b. **Create new fields** (`crm_fields_create`) — for each of the 3 chosen per object.

   c. **Create options** for each select / multiselect (`crm_field_options_create`), then order them (`crm_field_options_reorder`). Pipeline stages especially — the order is what defines progression.

   d. **Rename existing fields** if any are being renamed (`crm_fields_update`).

   e. **Remap existing records** to new option IDs where stages are being consolidated (see step 8 — but only the in-between remap pass; the full data sweep is step 8).

   f. **Delete dropped fields/options** only after remapping is done.

   g. **Create record views** (`crm_record_views_create`) with full saved config including columns, filters, sort.

   h. **Order the views** (`crm_record_views_reorder`).

   i. **Create inbox views** (`inbox_views_create`).

   j. **Order the inbox sidebar** (`inbox_views_sidebar_reorder`).

7. **Tell the user the structure is ready.**
   > Workspace is set up. {N} stages, {N} fields per object, {N} record views, {N} inbox views.
   >
   > **One more pass coming**: I'm going to update your existing records so they slot into the new structure. This is the long part — it runs in the background. I'll let you know when it's done.

### Phase 4 — Sweep existing records (the long step)

This is the part the user explicitly said to do **last and silently**: *"After a reorganization/CRM setup, if the user already had contacts in the CRM, update the fields of the contacts so that they're correctly organized in the CRM but this is a final and long step, so therefore focus about everything else before, say to the user it's done and then automatically do this."*

8. **For each existing record:**
   - Map old field values to new field IDs / option IDs based on the remap table from step 5.
   - Where confident, fill any new fields you created in step 6 (e.g., infer Industry from Company name + cached web research; infer Size from public LinkedIn data if available).
   - Where unclear, leave the new field empty rather than guessing.
   - `records_update` to apply changes.
   - Respect rate limits — pace yourself, this is a marathon.

9. **Final summary**:
   > Done. Updated **{N}** records with the new structure. **{M}** records had fields I couldn't auto-fill — they're in the **Untriaged** view if you want to clean them up.

### Phase 5 — Offer the natural next step

10. **Ask once if the user wants contact detection now.**
    > Want me to scan your inbox and pull in any people you're talking to who aren't in the CRM yet? Takes about a minute. (→ Action 5)

## Edge cases

- **The user already has hundreds of custom fields.** Don't try to preserve all of them. Show the user a list of fields you're proposing to consolidate / drop, with which fields have data. Get explicit approval to drop fields with data. Default to **keep**.
- **The existing pipeline has 15+ stages.** Propose your consolidation in the plan message (step 3) with a mapping table: "I'll merge {Old A} + {Old B} into {New X}." Don't apply silently.
- **The user runs sales in multiple languages.** Use the user's primary language for stage names. If multiple workspaces, ask per workspace.
- **No homepage content** (site is a single-page app, behind login, broken). Use the fallback question; don't fabricate ICP from a thin signal.
- **The user has integrations writing to specific fields** (Zapier, webhooks). Renaming or deleting those fields will break the integration. Before deleting any field, write a breadcrumb noting integrations are possibly affected. When unsure, ask.
- **Existing record views in use are heavily customized.** If a view has clearly been tuned by the user (unusual column order, filters), preserve it instead of replacing — add the new ones alongside, up to the cap.

## Don't do this

- Don't create custom objects.
- Don't go above 3 custom fields per object.
- Don't go above 10 pipeline stages.
- Don't create more than 1 pipeline by default (2 only with reason).
- Don't exceed 5 / 3 / 3 / 4 view caps.
- Don't use 4+ word names anywhere.
- Don't ask the user 20 questions — make the plan, present it once, then ship.
- Don't expose `_id`-style internal names in user-facing labels.

## Routine cadence

Setup is **one-time**. Don't schedule it. (The data-sweep phase 4 can run in the background but completes once.) Reorganizations happen on demand when the user's business shifts — wait for them to ask.
