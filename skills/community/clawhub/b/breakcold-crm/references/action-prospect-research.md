# Action 4 — Prospect research

Enrich CRM records by researching the person and their company on the web, then writing the findings back into Breakcold as notes (and, where relevant, onto the related deal). The user opens the record and gets a ready-made briefing.

## When this triggers

User says things like: "research these prospects", "enrich my contacts", "what does this company do", "tell me about the people I'm meeting with this week", "do a prospect dossier on John from Acme".

## What to ask first

Almost nothing. The user already gave you the records — research them.

Ask once **only if** the scope is wide-open ("research my prospects"):

> Just to scope it: should I research **all** active contacts, the ones added in the last **{N}** days, or a specific set you'll point me at?

Defaults:
- "Research these" with named records → just those.
- "Research my new contacts" → records created in the last 7 days.
- "Research everyone" → push back, suggest a smaller cohort first (cost and time).

## Confidence is the most important rule

Only write a finding to Breakcold if you're confident it's **about the right person or company**. The cost of a wrong note is high (the user trusts CRM data and acts on it). The cost of skipping a person is low (you can always re-run later).

### Inputs that establish high confidence

Stack the signals — one alone usually isn't enough.

| Input on the record                                                  | Why it helps                                                  |
|----------------------------------------------------------------------|---------------------------------------------------------------|
| Company website URL                                                  | Strong company identifier. **Best signal.**                   |
| Work email with a domain (e.g. `john@acmecorp.com`)                  | Implies company. Pair with the person's name to confirm.      |
| LinkedIn URL                                                         | Strong person identifier.                                     |
| Full name + company name                                             | OK if both unusual; weak if either is common.                 |
| Phone number                                                         | Weak alone.                                                   |
| Location (city + role)                                               | Useful to disambiguate common names.                          |

**Decision rule:** Proceed if you have **at least one strong identifier** (website, LinkedIn, work email domain) AND can corroborate against a second source. Otherwise, skip and breadcrumb why.

## Playbook — exact tool sequence

### Execution mode — small-batch first, main thread only, page size 20

Before iterating, three universal rules apply (see `SKILL.md` universal rules + `fundamentals.md § 7.5`):

- **Page size:** every `records_list` call uses **`limit: 20`**. Non-negotiable. Especially relevant when the cohort is "all new records added in the last N days" — that can easily be 50+ records, which would exceed the inline payload threshold without page-size discipline.
- **Main thread only:** every tool call (`records_list`, `notes_list`, `notes_create`, web searches, `custom_activities_create`) runs in the main thread. Do **not** invoke any sub-agent / task-delegation tool. Research benefits especially from main-thread continuity because the web-search results need to flow into the same context as the CRM data.
- **Small-batch first for one-shot runs:** process only the first 20 records of the cohort, write the notes, then surface results and ask the user "say *continue* to sweep the rest." Scheduled runs proceed end-to-end. For narrow cohorts (≤20 records — e.g., "research these 3 contacts I just added"), there's nothing to small-batch; just process them.

For each record in scope:

1. **Read the record.** `records_get` to pull full field values — including any custom fields the user has. Also `notes_list` to see if research already exists.

2. **Skip-if-exists check.** If a recent note (last 30 days) on this record is already a research brief (starts with the prefix below, see step 6), skip — or update if the user explicitly asks for a refresh.

3. **Pick the research targets.**
   - **Person research**: name, role, recent moves, content they've published (LinkedIn posts, blog, podcast, talks).
   - **Company research**: what they do, size, recent news, funding, key product, ICP fit signals for the user's business.

4. **Run the web research.** Use the agent runtime's web-search and fetch capabilities.
   - **Try the domain first.** From the website URL, or derived from the email domain. Visit the homepage, About, and Pricing/Product pages.
   - **Then LinkedIn (person + company).** If accessible to the agent.
   - **Then a focused web search** for recent news (last 6 months) using the company name + verticals like "funding", "launch", "hire", "acquisition", or the person's name + their company.
   - **Cross-check.** Mention of the company on a third-party site (TechCrunch, industry trade press) raises confidence.

5. **Decide if you have enough.** If after a reasonable search you can't establish high confidence:
   - Don't fabricate.
   - Don't write a half-empty note.
   - Write a `custom_activities_create` with prefix `[breakcold-crm:research-skipped]` and a one-line "couldn't confidently identify".
   - Move to the next record.

6. **Write the note.** `notes_create` on the record. **The note body must be properly formatted HTML** — Breakcold renders the `content` field as rich text. Plain text with `\n` line breaks comes out as a single unbroken paragraph and the user has to ask you to reformat. Don't make them ask.

   **Required structure** — use real HTML elements, not line breaks:

   ```html
   <p><strong>[breakcold-crm:research {YYYY-MM-DD}]</strong></p>

   <h3>Company — {company name}</h3>
   <p><strong>What they do:</strong> {one or two sentences}</p>
   <p><strong>Size / stage:</strong> {e.g., Series B, ~120 employees, founded 2018}</p>
   <p><strong>Recent:</strong></p>
   <ul>
     <li>{news item with rough date}</li>
     <li>{another news item}</li>
   </ul>
   <p><strong>Why we might fit:</strong> {one line, in the user's business context}</p>

   <hr>

   <h3>Person — {full name}</h3>
   <p><strong>Role:</strong> {title} at {company}, since {year if known}</p>
   <p><strong>Background:</strong> {one line — previous role or notable past}</p>
   <p><strong>Interests / signals:</strong> {recent posts, talks, themes — if anything}</p>

   <hr>

   <p><strong>Sources:</strong></p>
   <ul>
     <li><a href="{url}">{descriptive title}</a></li>
     <li><a href="{url}">{descriptive title}</a></li>
   </ul>
   ```

   **`notes_create` payload shape** (the API takes both fields — see `fundamentals.md § 11 - notes_create`):

   ```json
   {
     "title": "Prospect research — {company name}",
     "content": "<p><strong>[breakcold-crm:research 2026-05-23]</strong></p><h3>Company — Acme Corp</h3>...",
     "contentPlain": "[breakcold-crm:research 2026-05-23]\n\nCompany — Acme Corp\nWhat they do: ...\n\nPerson — Jane Doe\nRole: VP Product at Acme...\n\nSources:\n- https://..."
   }
   ```

   - `content` = the HTML version above. **Always provide this.** Single-line JSON-encoded.
   - `contentPlain` = the same content as plain text with real newlines. Used by Breakcold's search and exports. **Always provide this too** — the API expects both.
   - `title` = `Prospect research — {company name}` so the user spots research notes at a glance in the notes list.

   **Quality bar for the note body:**
   - Keep total HTML body under ~250 words of actual content.
   - Use `<h3>` for the two main sections (Company, Person), `<p>` for prose, `<ul>/<li>` for any list (recent news, sources, interests if more than two items), `<strong>` for the field labels, `<hr>` to separate the three blocks.
   - **No `<div>` walls, no inline styles, no `<br>` chains.** Use semantic tags. Breakcold's note renderer styles them correctly.
   - **No `<h1>` or `<h2>`** — they're too big inside a note. Start at `<h3>`.
   - Avoid empty sections. If you have no "Interests / signals," drop the line; don't write "N/A" or "None found."

   **For non-research notes elsewhere in the skill** (breadcrumbs, deal summaries, etc.), use the same HTML + plain dual format. The skill never writes a note as raw text only.

7. **If the record is linked to a deal**, also add the research to the deal. Use the **same HTML structure as step 6** — never plain text. Two options:
   - Write the same note on the deal record (full HTML body, identical to step 6).
   - **Or** (preferred when the person and deal are both in scope) write a shorter HTML summary on the deal that points at the person:

     ```html
     <p><strong>[breakcold-crm:research {YYYY-MM-DD}]</strong></p>
     <p>Full research on linked contact: <a href="{person record URL or just name}">{person name}</a>.</p>
     <h3>Quick context</h3>
     <p><strong>Company:</strong> {one-sentence what-they-do}</p>
     <p><strong>Buying signal:</strong> {one line — why they might be evaluating now, if known}</p>
     ```

     Same dual `content` + `contentPlain` requirement as step 6.

   The user explicitly asked: *"If the user has individuals/companies attached to a deal, add the information of the prospect research as notes in the deal itself."*

   To find linked deals: look at the record's relation fields (linked records) and find the related Deal records. If unsure of the relation field name, inspect via `crm_fields_list` for fields of type `relation`.

8. **Update structured fields when high-confidence facts are available.** If you found a clean **company size, industry, headquarters location, LinkedIn URL** and the record has empty fields for any of these, update them with `records_update`. This makes future segmentation and reporting (Action 3) sharper. Don't overwrite non-empty fields without asking.

9. **Breadcrumb.** `custom_activities_create` with prefix:
   ```
   [breakcold-crm:research {YYYY-MM-DD}] Note added; confidence: HIGH; sources: {N}.
   ```

10. **Move to the next record.** Respect rate limits.

## What to write and what to leave out

**Write:**
- Verifiable, dated facts (founding year, funding round, recent product launches).
- Public statements (a recent talk, blog post, podcast).
- Crisp framing of what they do — readable in 5 seconds.

**Leave out:**
- Salaries / personal financial estimates.
- Personal life details (family, health, religion).
- Anything from low-quality sources (random forums, anonymous blogs).
- Anything that reads like profiling — stick to professional, public information.

If you can't verify, don't write it.

## Edge cases

- **No website URL, no work email, only a Gmail/Outlook address.** Try LinkedIn from the person's name and any company tag in the CRM. If neither pans out, skip with a breadcrumb.
- **Common name** ("John Smith"). Disambiguate using company, location, or LinkedIn URL. If you can't confidently land on one person, skip.
- **Multiple people at the same company in the CRM.** Research the company once (note on the company record if it exists, or shared across the people), then research each person individually. Don't re-research the company per person.
- **Stealth company / minimal web footprint.** Note that openly: "Limited public footprint — stealth or pre-launch. Worth asking on the next call."
- **The "company" is actually a holding entity or shell.** Note it — the user needs to know.
- **The person changed roles recently.** If LinkedIn or recent press shows a new role, the CRM may be stale. Update the title field (with `records_update`) and add a note: "Title updated based on {source} — was {old}, now {new}."
- **The record is a Person but no Company is linked.** Try to identify the company from the email domain. If found and confident, create or link the Company record (see `action-contact-detection.md` for duplicate handling) — but only when explicitly enabled, or when the user opted in at setup.

## Schedule it as a routine

Hand off to `routines.md`. Default cadence: **daily, but only on new records added since the last run.**

Confirmation message:

> I'll research **new records** added each day and write a research note on each one I can confidently identify. If a record is linked to a deal, the note goes on the deal too. Want a daily email recap of what got researched?

This is the right cadence — researching old records repeatedly is wasteful, and new records are exactly when the user wants context fastest.

## Quality bar before shipping

Before writing the note, ask yourself: "If the user opens this record cold tomorrow, will they walk into their call already feeling prepared?" If yes, ship. If no, either tighten the note or skip.
