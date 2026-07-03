# Action 5 — Contact detection & creation from the inbox

Scan the user's inbox across email, LinkedIn, WhatsApp, and Telegram. Find people they're talking to who aren't in the CRM yet. **Auto-add** them if confidence is ≥ 95%; otherwise **suggest** them for review.

## When this triggers

User says things like: "find missing contacts in my inbox", "add new people from emails", "who am I talking to who isn't in the CRM yet", "populate the CRM from my conversations".

## Frame the rules tightly

Two things must be true for every candidate before any write:

1. **The record matches the kind of records the user wants in the CRM.** A B2B salesperson doesn't want their personal trainer in the CRM. Use the inferred ICP (from existing records' patterns: most are external, have work emails, have a company associated) to filter.
2. **No duplicate exists.** Duplicate detection is the most important part of this action — see below.

## Duplicate detection — the careful part

A duplicate isn't just "same email." A real contact might already exist under a different channel. The user explicitly called this out: *"the user might have a record with a conversation via email, but for whatever reason, the linkedin conversation is not linked to the record because maybe they didn't add the LinkedIn URL to the person."*

### Multi-signal matching

For each candidate person you find in the inbox, check `records_list` on the Person object with the following matches in order:

1. **Exact email match** on any email field.
2. **Exact LinkedIn URL match** on any LinkedIn field.
3. **Exact phone match** (WhatsApp / Telegram numbers, E.164 normalized).
4. **Name + company match** — full name plus a related Company record matching the candidate's company.
5. **Name + domain match** — full name plus the candidate's email domain matches a known existing record (e.g., the contact emails from `john@acmecorp.com` and the CRM has another contact from `@acmecorp.com` named John).

If **any** of these matches a confident hit:
- **Do not create a new record.**
- Instead, **enrich the existing record** with the missing channel info you just discovered: add the LinkedIn URL to the existing email contact, link the new conversation to the existing record, etc.
- Write a `custom_activities_create`:
  ```
  [breakcold-crm:contact-detection {YYYY-MM-DD}] Linked existing record to {channel} conversation; was previously missing {field}.
  ```

If no match → candidate is a real new contact, proceed to the 95% rule.

### Linking conversations to existing records

When you discover that an existing CRM record matches an inbox conversation but the conversation isn't yet linked to that record, **link it**. This is what makes the user's "open record → see all channels" experience work. The exact mechanism depends on what the API exposes — check the relation between conversations and records via `inbox_conversations_list` (record-scoped) vs. `inbox_conversations_search` (workspace-scoped). If a direct link API isn't exposed via MCP, surface this as a manual suggestion in the run summary.

## The 95% confidence rule

For a brand-new record (no duplicate found), confidence is **not** a vague vibe — it's a specific question:

> **"Based on the user's existing CRM taxonomy — their pipeline stage names, their view names, and the kinds of records already in the workspace — am I 95%+ sure this candidate fits into one of those existing categories?"**

The user's CRM is the source of truth for what belongs. If they have stages like `Lead → Engaged → Customer` and views like `Prospects`, `Partnerships`, `Customers`, that tells you exactly what types of contacts they keep. A new candidate either slots into one of those categories cleanly or they don't.

### How to read the user's taxonomy

Pull these from your cached discovery, in order:

1. **Pipeline stage names** (from `crm_field_options_list` on the stage field). Names like `Cold Lead`, `Prospect`, `Customer`, `Investor`, `Partner` literally enumerate the categories that belong in this CRM.
2. **Record view names** (from `crm_record_views_list`). Names like `Partnerships`, `VIP Customers`, `EU Prospects`, `Influencers` indicate categories the user actively curates.
3. **Inbox view names** (from `inbox_views_list`) can also signal what the user cares about (e.g., a `Partnerships` inbox view means partnership-type contacts belong in the CRM).
4. **Existing records' patterns** as a tiebreaker — if most existing Person records have a work email and a linked Company, that's the implicit ICP.

A candidate qualifies for **auto-create (≥95% confidence)** when you can confidently say "this person is a *{stage or view category}*" — e.g., "this is clearly a Prospect" or "this is clearly a Partner." If you can't comfortably name which category they'd belong to, confidence isn't 95% — surface for review instead.

### The hard-negative rule — pitchers never qualify

**Anyone pitching the user where the user has not replied does not qualify, ever.** Categorical, no exceptions, no judgement call.

This covers:
- Cold outreach the user received and ignored (sales pitches, agency outreach, "saw your post" DMs, partnership cold-asks).
- Marketing emails the user is subscribed to but doesn't engage with.
- LinkedIn connection-request messages where the user accepted but never wrote back.
- Anyone whose only messages are inbound-only, with zero outbound reply from the user.

These contacts pollute the CRM with people the user has actively chosen not to engage. **Do not auto-create them. Do not even suggest them.** Skip silently and breadcrumb the skip:

```
[breakcold-crm:contact-detection {YYYY-MM-DD}] Skipped — inbound-only pitch, no user reply.
```

The litmus test: **has the user sent at least one outbound message to this person in this conversation?** If yes, they're engaged — proceed to category-fit evaluation. If no, skip.

### Confidence decision flow

For each new candidate (after duplicate detection clears them):

```
1. Has the user sent at least one outbound message to this person?
   ├─ NO   → SKIP (hard rule, no exceptions). Breadcrumb the skip. Move on.
   └─ YES  → continue

2. Can you confidently name which of the user's CRM categories this person fits?
   (Read the stage names and view names from cached discovery.)
   ├─ NO  → SUGGEST for user review (don't auto-create). Note in summary.
   └─ YES → continue

3. Is the candidate's identity verifiable?
   (Name present, work email or LinkedIn URL, not a shared/no-reply inbox.)
   ├─ NO  → SUGGEST for user review.
   └─ YES → AUTO-CREATE.
```

All three checks must pass for auto-create. The first is the most important — it's the floor that keeps cold pitchers out of the CRM regardless of other signals.

### Signals that disqualify on top of the hard rule

Even when the user has replied, skip auto-create (suggest for review at most) when:

- The sender is a shared inbox (`support@`, `sales@`, `team@`, `info@`) — there's no individual person to add.
- The sender is a no-reply / automated address (`noreply@`, `notifications@`, `marketing@`).
- The conversation is transactional (receipts, shipping notifications, calendar bots, invoice systems).
- The conversation hasn't had activity in 6+ months (the user has effectively moved on).

These are duplicates of "this person doesn't fit a CRM category" but worth calling out explicitly so they aren't missed.

## Playbook — exact tool sequence

### Execution mode — small-batch first, main thread only, page size 20

Before iterating the inbox, three universal rules apply (see `SKILL.md` universal rules + `fundamentals.md § 7.5`):

- **Page size:** every `inbox_conversations_search` / `inbox_conversations_list` / `records_list` call uses **`limit: 20`**. This is non-negotiable — larger pages exceed the inline payload threshold on common agent runtimes, get saved to a file, and trigger the model's confidence-loss cascade.
- **Main thread only:** every tool call runs directly in the agent's main thread. Do **not** invoke any sub-agent / task-delegation tool. Contact detection in particular is sensitive to this: sub-agents lose the cached duplicate-check state and may create the same record twice.
- **Small-batch first for one-shot runs:** process only the first 20 conversations of the cohort, decide and create, then surface results and ask the user "say *continue* to sweep the rest." Scheduled runs proceed end-to-end without confirmation.

1. **Discover** (cached): workspace, Person object, Person fields (especially email, LinkedIn, phone, company, source, status), existing Person records (you'll need them indexed for duplicate detection). Crucially, also pull the **user's CRM taxonomy** so you can evaluate category-fit (per the 95% confidence rule above):
   - Pipeline stage option labels via `crm_field_options_list` on the stage field.
   - Record view names via `crm_record_views_list` for Person and Company.
   - Inbox view names via `inbox_views_list`.

   These category names are what you'll match candidates against in step 5.

2. **Index existing contacts.** Build a lookup table in your scratchpad — emails, LinkedIn URLs, phones, normalized names — from `records_list`. Use this for fast duplicate checks throughout the run.

3. **Sweep the inbox.** `inbox_conversations_search` workspace-wide for the recent period (default last 30 days). For each conversation:
   - `inbox_messages_list` (a small page is fine — first message + last few are enough).
   - Identify the **non-user participant(s)**. Email and LinkedIn give you a sender name and address; WhatsApp/Telegram give you a phone or handle.
   - **Determine direction.** Has the user sent at least one outbound message in this conversation? Record this — it's the input to the hard-negative rule.

4. **For each non-user participant**, check duplicates (steps above). If duplicate found, enrich and move on.

5. **For each genuinely new candidate**, apply the decision flow from the 95% rule above:
   - **Step 5a — Hard-negative check.** If the user has not sent any outbound message in this conversation → **SKIP**. Breadcrumb the skip (`[breakcold-crm:contact-detection {YYYY-MM-DD}] Skipped — inbound-only pitch, no user reply.`) and move on. No exceptions, no review queue, just gone.
   - **Step 5b — Category-fit check.** Can you confidently name which of the user's CRM categories (stage name, view name) this candidate fits? If no → **SUGGEST** for user review with the candidate's identity info and your best-guess category, but don't create.
   - **Step 5c — Identity check.** Is the candidate's identity verifiable (name + verifiable channel, not a shared/no-reply inbox)? If no → **SUGGEST** for user review.
   - **All three pass → AUTO-CREATE.** Call `records_create` with the fields you can populate (name, email, LinkedIn, phone, company-domain-inferred). Set the `source` field if it exists — e.g., `"Inbox detection"`. Set the stage field to whichever stage best matches the category you identified in step 5b. After creation, attempt to **link the source conversation to the new record** so the user sees the conversation history immediately.

6. **Company records.** If you're creating a Person and their company doesn't exist as a Company record:
   - Check for Company duplicates by domain.
   - If genuinely new and the candidate passed all three checks above, create the Company record too and link it.
   - If the candidate only made it to SUGGEST, link only the company name as a text field on the Person and skip Company creation.

7. **Breadcrumb.** For every auto-creation, write:
   ```
   [breakcold-crm:contact-detection {YYYY-MM-DD}] Auto-created from {channel} conversation; category: {category name from user's CRM}.
   ```
   For enrichment of existing records:
   ```
   [breakcold-crm:contact-detection {YYYY-MM-DD}] Enriched existing record with {field added}; conversation linked.
   ```
   For skips:
   ```
   [breakcold-crm:contact-detection {YYYY-MM-DD}] Skipped — inbound-only pitch, no user reply.
   ```

8. **Summarize:**
   > Found **{N}** new contacts (auto-added) and **{M}** suggested for your review. Also linked **{K}** existing records to conversations they were missing. Want me to research the new ones now? (→ Action 4)

## Edge cases

- **The user emails themselves** (forwarded to / cc). Skip — the participant matching the user is filtered out.
- **Internal team conversations.** The user's coworkers (other workspace members) showing up as participants should be skipped. Use the cached member list to filter them out.
- **Aliases of the same person.** Two emails (`john@acmecorp.com` and `j.smith@acmecorp.com`) belonging to the same person. If the conversations also share a thread or are within the same domain and same name, treat as the same person. Add the alternate email to the existing record.
- **No name in the message metadata** (raw address only, e.g., `j.smith@acmecorp.com`). Try to derive a name from the address or the signature. If neither works, suggest don't auto-create — names are visible to the user and ugly auto-derived names are annoying.
- **Spam / cold-inbound emails the user never replied to.** Skip by default. The user can run a wider sweep manually.
- **GDPR / consent-sensitive contexts.** If the user's region looks EU and the contact is also EU, auto-create is still defensible because the user has lawful interest (they're actively conversing). Document it via the custom activity. If the user later wants to scrub something, archive.
- **The "person" is really an event registration bot.** No-reply addresses, calendar invites from a no-reply, transactional senders — skip.
- **Same contact appears via different channels in the sweep** (email + LinkedIn from the same person). Detect after the email entry is created; when the LinkedIn one is being evaluated, the duplicate detection will catch it and enrich rather than create twice.

## Memory pattern — use custom activities aggressively

The user explicitly asked: *"when running this action, if you believe that creating a custom activity with explanations for both the user and yourself as mini extended context memory can help you for future updates and let the user why you did what you did, then do it without asking the user."*

So:
- One custom activity per record touched per run.
- Use the consistent prefix `[breakcold-crm:contact-detection {YYYY-MM-DD}]` so future runs can filter for prior decisions.
- This is also the user's audit trail — they can see why their CRM grew.

## Schedule it as a routine

Hand off to `routines.md`. Default cadence: **daily**, scanning the last 24–48 hours of inbox activity (with a small overlap to catch latecomers).

Confirmation:

> I'll scan your inbox daily for people you're talking to who aren't in your CRM yet. I'll auto-add the high-confidence ones, link existing records to conversations they were missing, and surface anything ambiguous for your review. Want a daily email recap?

## How this plays with Actions 4 and 6

- After contact detection adds new records, **Action 4 (prospect research)** is the natural next step on those records.
- **Action 6 (CRM setup)** typically ends by offering to run contact detection, so a freshly set-up CRM gets populated from the inbox automatically.
- When all three are scheduled, run in order: **setup (one-time) → detection → research**.
