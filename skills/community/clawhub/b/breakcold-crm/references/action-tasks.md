# Action 1 — Multichannel auto-task creation

Create follow-up tasks for contacts where the user is losing momentum, across email, LinkedIn, WhatsApp, Telegram, and meetings. Every task links back to the actual conversation so the user opens the task and lands inside the thread.

## When this triggers

User says things like: "follow up with the cold ones", "create tasks for people who went quiet", "ping anyone I haven't heard from in two weeks", "set up daily follow-ups", "task me on the deals that lost momentum".

## What "losing momentum" means

There is no universal definition. Ask the user once, in plain language:

> What counts as losing momentum for you? Should I create a follow-up task when there's been no reply for **3 days**, **7 days**, **14 days**, or something else?

Cache the answer for the session. Default if the user can't decide: **7 days**.

The reference is the **last inbound or outbound message** across any linked conversation channel — email, LinkedIn, WhatsApp, Telegram, meeting note. **Use the most recent across all channels**, not just one.

## Assignee — ask, default to the requesting user

Ask the user once who should own these tasks:

> Who should own these follow-up tasks? **You** (default), **{Member A}**, **{Member B}**, or **the existing record owner** on each?

Defaults if the user doesn't answer or says "you decide":

- **The requesting user** (the one who triggered the workflow). This is the default and the safest fallback — they're the one running the workflow and the one who will see the tasks in their list. Use `CURRENT_USER_ID` from the boot sequence (see `SKILL.md` § Session-start orientation).
- Single-member workspace: that one member (same person as the requesting user).
- Only fall back to "the existing record owner" if the user explicitly chooses it.

**Never** create tasks with a null/empty assignee. Unassigned tasks vanish from everyone's queue. If `CURRENT_USER_ID` is somehow still unknown when the first task fires (rare), create one task with the cleanest fallback you have, read the user's ID from the create response, and use it for all subsequent tasks in the batch — see `fundamentals.md` § "Resolving the current user ID".

## Playbook — exact tool sequence

### Execution mode — small-batch first

Before iterating the cohort, decide which mode this run is in:

- **One-shot user-initiated run** (the user said "create follow-up tasks for X" in chat): process **only the first 20 records** of the cohort, write everything, then surface results and ask:
  > I processed the first 20 — created **{N}** tasks, skipped **{M}** for duplicates. Say *continue* to sweep the rest.
  Wait for the user's confirmation before fetching more pages.
- **Scheduled routine run** (a saved cadence is triggering this): process end-to-end with page-by-page pagination — the user already approved the cadence and isn't watching the run live.

This is a universal skill rule (SKILL.md → "Small-batch first for one-shot runs"), not a workflow-specific tip. It bounds context, prevents the file-dump-then-degrade cascade, and gives the user a reversible checkpoint.

### Page sizes — never higher than 20

Every `records_list` and `inbox_conversations_search` call in this playbook **uses `limit: 20`**. This is non-negotiable. Larger pages produce responses that exceed the inline payload threshold on common agent runtimes, get saved to a file, and trigger the model's confidence-loss cascade (file truncation → sub-agent delegation → context restart → loop). See `references/fundamentals.md § 7.5` for the full rationale.

### No sub-agent delegation

Every tool call below runs in the main thread. Do **not** invoke any sub-agent / task-delegation tool (`Agent`, `Task`, `dispatch_agent`, `subagent`, `delegate` — by whatever name the runtime calls it). Sub-agents lose the cached IDs, can't share parallel fetches with the main thread, and stall on tool-approval prompts the user can't see.

### The steps

1. **Discover — or use pre-cached IDs.**
   - **If this is a scheduled run, the prompt should embed all the IDs the agent needs:** `workspaceId`, `objectTypeId` for Person (and Deal/Company if the cohort comes from there), `pipelineStageFieldId`, and the option IDs for skip-stages (`Lost`, `Won`, `Not a fit`, etc.). Embed them in the scheduled prompt itself (via `routines.md`). The agent should never re-discover them at scheduled-run time — that's 4-6 wasted tool calls and a common source of early-run failures.
   - **If this is a one-shot run and the IDs aren't cached:** discover once — `workspaces_list`, `crm_objects_list`, `crm_fields_list` for relevant objects, `crm_field_options_list` on the stage field. Cache everything for the session.
   - **Also list the user's saved views once:** call `crm_record_views_list` (on Person, and Deal/Company if relevant). The view names are signal for the cohort-selection step below.
   - **Pull the member list** — from `capabilities_list` or workspace context.

2. **Define the cohort. Tasks always land on Person records — never on Deals or Companies.** Conversations live on people; tasks are about conversations; therefore tasks live on people.

   **Option A — Use a saved view (preferred when one fits).** If the user has a saved record view on Person whose name signals an actionable cohort (e.g., "Active prospects", "Hot leads", "Engaged this week", "My pipeline"), use it directly:
   > I'll run on your **{view name}** view — say so if you'd rather use a different one or sweep all active people.

   Pass `viewId` on every `records_list` call. The user's view is the filter language; trying to invent a separate filter is wasted effort.

   **Option B — All active Person records.** If no relevant view exists or the user explicitly wants the full cohort, list all active People, excluding records in pipeline stages that mean "lost", "closed lost", "rejected", "do not contact" (filter client-side per page from the cached stage option list).

   **If the user asks for tasks "on deals" or "on companies":** don't iterate over Deals or Companies themselves. Instead, **walk each Deal (or Company) → its linked Person records → and the resulting cohort is those People.** One task per stalled Person, attached to the Person record. (Walking the relations still uses `limit: 20` per page on the Deal/Company side.)

   **Why "tasks always on People" exists:** a task on a Deal can't link to a conversation (deals don't have conversations directly). A task on a Person can. Putting tasks on Deals or Companies produces orphan reminders the user can't act on — they open the task and have no thread to reply into.

3. **Iterate the cohort page-by-page.** This is the canonical loop pattern for every cohort-iterating workflow in this skill:

   ```
   cursor = None
   while True:
       page = records_list(
           workspaceId,
           objectTypeId = Person,
           limit = 20,
           cursor = cursor,
           viewId = optional from step 2
       )

       # Filter the page client-side immediately — discard rejected records
       candidates = [r for r in page.data if r.stage not in terminal_stages]

       # For each candidate, do steps 4-7 (per-record sub-steps below)
       # Batch the parallel fetches in groups of up to 10 to respect rate limits
       for candidate in candidates:
           [step 4: gather signal]
           [step 5: idempotency check]
           [step 6: create task, with the conversationId]
           [step 7: breadcrumbs]

       # Stop here for one-shot runs — see Execution mode
       if one_shot:
           break

       # Continue for scheduled runs
       if not page.pagination.hasMore:
           break
       cursor = page.pagination.cursor
   ```

   **Hard rules inside this loop:**
   - One page of raw record data at a time. Discard the page object before fetching the next.
   - No `view`-on-a-file or line-by-line reading of any dumped tool result. If a response is dumped to a file by the runtime (rare with `limit: 20`, but possible), read it once whole or use code execution to extract specific fields. Never iterate the file in chunks.
   - All parallel calls go in the **main thread**. No sub-agent delegation.

4. **Per-record: gather signal.** For the active Person:
   - `inbox_conversations_list` (record-scoped) → all linked conversations. Use the response's `lastMessageAtMs` directly — don't call `inbox_messages_list` just to check the timestamp.
   - Only if you need the message *content* (to derive the topic for the task title), call `inbox_messages_list` on the most recent conversation with a small page (last 5-10 messages).
   - Compute days since last message. If ≥ the user's threshold, the record qualifies.

5. **Per-record: idempotency check.** Call `tasks_list` on the record. **Skip** if any open task on this record has:
   - A title that contains "follow up", "ping", "check in", or similar (case-insensitive), **and**
   - A due date within the next 7 days.

6. **Per-record: self-check before creating.** Before calling `tasks_create`:
   - ✓ The record is a Person (not a Deal or Company).
   - ✓ A conversation ID is in hand (or you've decided to use the fallback "no clear topic" title).
   - ✓ `CURRENT_USER_ID` is known (or you'll resolve it from the response of this very call — see `fundamentals.md § 3.5`).
   - ✓ No sub-agent was invoked. If yes, restart this record's processing in the main thread.

   Then call `tasks_create` with:
   - **record_id:** the **Person** record being followed up on. Never a Deal ID, never a Company ID — see step 2.
   - **title:** follow the pattern `Follow up: {2-6 word topic}` — see "Task title pattern" later in this file for full rules. Examples: `Follow up: Pricing concerns around tokens`, `Follow up: Q4 contract terms`.
   - **due_date:** today (or next business day if today is weekend; do not auto-schedule weeks out).
   - **assigneeUserIds:** array containing the cached `CURRENT_USER_ID` (or whoever was selected during setup). **Never null, never empty.**
   - **conversationId:** include the conversation ID from step 4 so the task deep-links into the thread when opened.

7. **Per-record: breadcrumbs.**
   - **On the Person:** `custom_activities_create` with prefix:
     ```
     [breakcold-crm:auto-tasks {YYYY-MM-DD}] Follow-up task created; last activity {N} days ago ({channel}).
     ```
   - **On the linked Deal (only when the cohort was sourced from deals):** also write a `custom_activities_create` on each Deal that produced follow-up tasks for its linked People:
     ```
     [breakcold-crm:auto-tasks {YYYY-MM-DD}] {N} follow-up task(s) created for linked Person(s): {name1}, {name2}.
     ```
     This gives the user audit visibility on the Deal record — they see "tasks were created for this deal" without losing the fact that the actual tasks live on the People. **Don't** create a task on the Deal; only the breadcrumb.

8. **Summarize** to the user in one short message:
   > Created **{N}** follow-up tasks across **{N}** contacts. Quietest thread: **{name}** at **{N} days**. Skipped **{M}** records that already had open follow-up tasks.

   For one-shot runs, end with: "Say *continue* to sweep the rest of the cohort."



## Edge cases

- **No conversations on a record.** Skip — can't follow up on a thread that doesn't exist. (Don't create a "cold outreach" task unless the user explicitly asks for that — different action.)
- **Multiple conversations, multiple channels.** Use the **most recent message timestamp across all channels** to compute "days quiet". Derive the topic from the messages in that most-recent thread — that's where the live context is.
- **The most recent message is from the user (outbound).** That's *also* "losing momentum" — the user reached out and got nothing back. Still create the task; the topic comes from what the user asked or proposed in that unanswered message (e.g., `Follow up: Demo scheduling`, `Follow up: Proposal review`).
- **The most recent message is from the contact (inbound) and the user hasn't replied.** That's a "you owe them a reply" situation, which is more urgent. Use the `Reply needed: {topic}` prefix — see "Special case — pending replies" in the Task title pattern section. Set due date to **today** with high priority if the API supports it.
- **Deal in cohort has no linked Person records.** Rare but it happens — deals created without linking a contact yet. Skip the Deal entirely (no Person to attach a task to) and write `custom_activities_create` on the Deal with prefix `[breakcold-crm:auto-tasks {YYYY-MM-DD}] Skipped — no linked Person records. Add a contact to this deal to enable follow-up tasks.` That tells the user why nothing happened on that deal.
- **Record is in a "won" or "closed" stage.** Skip unless the user explicitly asks to follow up with closed customers (different intent — that's usually an upsell or check-in routine).
- **Record has no owner and the workspace is multi-member.** Use the assignee chosen in setup (default: the requesting user). Don't silently leave it unassigned.
- **Conversation is a group thread (multiple participants).** The task still links to the record; if multiple records share the same conversation, create one task per record only if the user wants distinct follow-ups — otherwise create one task on the most relevant record (usually the deal, falling back to the primary contact).
- **The contact opted out / unsubscribed.** If a custom field or status marks this (look for "unsubscribed", "DNC", "do not contact"), skip and breadcrumb it.

## Schedule it as a routine

If the user wants this on a schedule, hand off to `routines.md` for the universal setup. The one-confirmation message becomes:

> I'll create follow-up tasks **{frequency}** for contacts where the last conversation activity is older than **{threshold}** days, assigned to **{assignee}**. Want a **{matching cadence}** email recap of what got created?

Default frequency: **daily**. Acceptable range: daily–weekly. Anything more frequent triggers the cost warning from `routines.md`.

## Task title pattern

Every follow-up task title follows this pattern:

```
Follow up: {2-6 word topic}
```

Notes on the format:
- **No person's name in the title.** The task lives on the Person record — the name is already in context everywhere the task appears. Adding it to the title is redundant and clutters the user's task list.
- **Colon, not dash.** `Follow up` then `:` then a space then the topic.
- **Topic is 2-6 concrete-noun words.** Same derivation procedure as before.

Examples that work:
- `Follow up: Pricing concerns around tokens`
- `Follow up: Q4 contract terms`
- `Follow up: Demo follow through`
- `Follow up: SOC 2 questions`
- `Follow up: Custom domain setup`

Examples that don't (avoid these):
- ❌ `Follow up` — no topic.
- ❌ `Follow up:` — colon with no topic.
- ❌ `Follow up Katy: Pricing concerns` — drop the name; it's redundant with the record.
- ❌ `Follow up Katy - Pricing concerns` — drop the name *and* use a colon, not a dash.
- ❌ `Follow up: email thread went quiet (9 days)` — channel + duration is implementation detail, not topic.
- ❌ `Follow up: Discussion about various topics` — generic filler; says nothing.
- ❌ `Follow up: Pricing` — too thin, expand to a real 2-6 words.

### How to derive the topic

1. Pull the **last 3-5 messages** in the most recent conversation thread on this Person (across whichever channel is most active).
2. Identify the **dominant subject** — what they were actually discussing in concrete nouns. "Pricing for the enterprise tier" → "Pricing concerns" or "Enterprise tier pricing" depending on the angle the user was wrestling with.
3. Compress to **2-6 words**.
4. **Avoid empty connector words:** "discussion", "questions about", "topic of", "various things". The 2-6 words should be **concrete nouns** doing the work.
5. **Pick the angle that matters to the user**, not the literal subject line. If the customer's email subject was "Re: Re: Re: Fwd: Quick question" but the actual content is about contract length, the topic is "contract length" — read the body, not the subject.
6. **The topic comes from the Person's conversation, not from the parent Deal.** If the cohort was sourced from deals (step 2), don't name the task after the deal (e.g., `Follow up: Acme deal`). Name it after what the *Person* was actually discussing.

### When you can't derive a clear topic

Very short conversations (one-line "hey are you free?" with no reply) won't yield a topic. Fall back:

```
Follow up: {channel} thread ({N} days)
```

E.g., `Follow up: email thread (9 days)`. This is the **only** acceptable fallback. It's still without the person's name (which would be redundant anyway since the task lives on the Person).

### Language

**Match the user's working language.** If the conversation and the user's other workspace content are in French, write the title in French:

- `Relancer : Préoccupations sur les tokens`
- `Relancer : Termes du contrat Q4`

Same for Spanish (`Seguimiento: ...`), German (`Nachfassen: ...`), Portuguese (`Acompanhar: ...`), etc. Mirror the user's language for the prefix and the topic; keep the colon separator. See `SKILL.md` § Universal rules → "Mirror the user's language" for the broader rule.

### User override

If the user explicitly requested a different naming pattern at workflow start ("Use 'Reach out' instead of 'Follow up'", "Include the person's name", "Use the format X"), follow their pattern instead. They're the boss; the pattern above is the default, not a constraint.

### Special case — pending replies (user owes the contact)

When the most recent message is from the contact (inbound) and the user hasn't replied, the task is more urgent and the framing changes — the user owes a reply, not a follow-up. Use:

```
Reply needed: {2-6 word topic}
```

Examples:
- `Reply needed: Pricing concerns around tokens`
- `Reply needed: Question about onboarding`

Set the due date to today and bump priority if the API supports it.

### Length sanity

Keep the whole title under ~70 characters so it reads cleanly in the Breakcold task list. If your topic compression pushes the title past that, tighten further — usually the topic was still too verbose.
