# Action 2 — Auto-movement of contacts in the pipeline

Automatically advance contacts (or companies, or deals) through the user's Kanban-style pipeline based on what's actually happening in their conversations and the rest of the record.

## When this triggers

User says things like: "advance my pipeline", "move contacts forward based on activity", "update my Kanban", "auto-progress deals", "keep my pipeline in sync with my inbox".

## What to ask first — and what not to

### Always ask once (if ambiguous)

**Which object's pipeline?** Some users run pipelines on Person, others on Company, others on Deal — or several at once. If the user has stage-like fields on multiple objects:

> Should I auto-progress people, companies, or deals? You can pick more than one.

If only one object has a clear pipeline field, pick it silently.

### Don't ask about obvious stages

If the pipeline reads cleanly (e.g., `New → Contacted → Qualified → Proposal → Negotiation → Won` or `Lost`), don't ask the user what each stage means. Operate from common sense.

### Ask only on **unclear or non-standard terminology**

If a stage uses internal-jargon names you can't infer ("Wave 1", "Tier B Q3", "Bucket Charlie"):

> Quick check on the pipeline: what does "**{stage name}**" mean for you? Is it earlier or later than "**{adjacent stage}**"?

Ask in one batched message if multiple stages are unclear. Don't ask one at a time.

### Cache the stage order

After clarification (or your own inference), cache the **ordered list** of stage option IDs. Also flag any stages that are terminal or off-flow:
- **Won / Closed Won** — terminal positive.
- **Lost / Closed Lost / Rejected** — terminal negative.
- **On Hold / Paused / Stalled** — off-flow side-bucket.

These are not part of the forward direction.

## The directionality rule — never move backwards by default

**Pipelines flow forward.** A contact in "Interested" cannot be auto-moved back to "Cold Lead", even if their recent behavior looks lukewarm. The reasoning: auto-movement should only ever **reflect new positive signal**. Disengagement is handled by tasks (Action 1), not by reversing pipelines.

Exceptions:

- **Re-opening after Lost.** If a contact is in a terminal "Lost" stage and sends a new positive message, that's a signal worth surfacing — but don't auto-move them. Instead, create a `custom_activities_create` flagging it for the user, and surface it in the run summary:
  > **{Name}** is marked Lost but replied today — worth a look.
- **Explicit user instruction.** "Move all my Negotiation deals back to Proposal" is fine because the user said so.

## What signals advance a contact

A move forward needs **positive signal in the source data**. Examples:

| Source signal                                                                 | Suggests moving toward…             |
|-------------------------------------------------------------------------------|-------------------------------------|
| First reply received on cold outreach                                         | Cold → Contacted / Engaged          |
| Reply expresses interest, asks for more info, agrees to a call                | Contacted → Qualified / Interested  |
| Meeting happened (calendar event in linked conversation)                      | Qualified → Discovery / Demo done   |
| Proposal sent / link to proposal in outbound message                          | → Proposal                          |
| Pricing discussion, redlining, contract language                              | → Negotiation                       |
| "We're in" / "send the contract" / signed PDF                                 | → Won                               |
| "Not the right fit" / "going with someone else" / "we'll pass"                | → Lost                              |
| Reply asks to reschedule, deprioritize, "check back in Q4"                    | → On Hold                           |

These are **heuristics, not rules**. Use the actual message content from `inbox_messages_list` plus any record notes / custom activities to decide. When the signal is ambiguous or weak, **do not move** — keep the contact where they are and write a breadcrumb explaining the uncertainty.

## Playbook — exact tool sequence

### Execution mode — small-batch first

Before iterating, decide which mode this run is in:

- **One-shot user-initiated run:** process **only the first 20 candidate records** of the cohort, decide and apply moves, then surface results and ask:
  > I processed the first 20 — moved **{N}**, flagged **{M}**, left **{K}** unchanged. Say *continue* to sweep the rest.
- **Scheduled routine run:** process end-to-end with page-by-page pagination.

This is a universal skill rule (SKILL.md → "Small-batch first for one-shot runs"). It bounds context, gives the user a reversible checkpoint, and prevents the file-dump degradation cascade.

### Page sizes and no sub-agents

- Every `records_list` and `inbox_conversations_*` call uses **`limit: 20`**. Hard rule. See `fundamentals.md § 7.5` for the rationale.
- Every tool call runs in the **main thread**. Do not invoke any sub-agent / task-delegation tool. The skill's caching architecture only works in one continuous main-thread context.

### The steps

1. **Discover — or use pre-cached IDs.**
   - **If this is a scheduled run, the prompt should embed all the IDs** the agent needs: `workspaceId`, target `objectTypeId`(s), `pipelineStageFieldId`, the ordered list of stage option IDs (so the agent can apply the directionality rule without re-fetching), and the option IDs for terminal stages. Embed them in the scheduled prompt (`routines.md`). Don't re-discover at scheduled-run time.
   - **If this is a one-shot run and the IDs aren't cached:** discover once — `workspaces_list`, `crm_objects_list`, `crm_fields_list`, `crm_field_options_list` on the stage field. Cache the ordered options.
   - **List the user's saved views once:** `crm_record_views_list` — useful for cohort scoping in step 2.

2. **Define the cohort.**

   **Option A — Use a saved view (preferred when one fits).** If the user has a saved record view that signals an actionable cohort (e.g., "Active deals", "My open opportunities", "This quarter"), use it:
   > I'll review the **{view name}** view — say so if you'd rather sweep all open records.

   Pass `viewId` on every `records_list` call.

   **Option B — All non-terminal records.** All records on the target object **except** those in terminal stages (Won, Lost) — filter terminal stages client-side per page from the cached option list.

3. **Iterate the cohort page-by-page.** The canonical loop:

   ```
   cursor = None
   while True:
       page = records_list(
           workspaceId, objectTypeId,
           limit = 20,
           cursor = cursor,
           viewId = optional from step 2
       )

       # Filter terminal stages client-side
       candidates = [r for r in page.data if r.stage not in terminal_stages]

       # For each candidate, run steps 4 (signal) + 4b (cross-object) + 5 (self-check) + 6 (decide) + 7-8 (apply)
       # Batch parallel sub-fetches in groups of ≤10
       for candidate in candidates:
           [step 4: gather direct signal]
           [step 4b: cross-object signal — only for Deals / Companies]
           [step 5: self-check]
           decision = [step 6: decide STAY/MOVE/FLAG]
           [step 7 or 8: apply]

       if one_shot:
           break
       if not page.pagination.hasMore:
           break
       cursor = page.pagination.cursor
   ```

   **Hard rules:** one page of raw data at a time; main-thread only; if a tool result is dumped to a file by the runtime, read it once whole, not line-by-line.

4. **Per-record: gather signal from the record itself.**
   - `inbox_conversations_list` (record-scoped, `limit: 20`) → use the response's `lastMessageAtMs` and `lastMessageSnippet` directly. Don't refetch messages just for staleness.
   - Only fetch `inbox_messages_list` (last 5-10 messages) when you need message *content* to interpret the signal (the snippet isn't enough).
   - `notes_list` on the record → recent notes (last 5).
   - The record's own field values from the `records_list` response — already in hand.

4b. **Per-record: cross-object signal — for Deals and Companies only.** This step is **non-negotiable** when operating on Deals or Companies — conversations happen with **people**, not with deals.

   For each Deal or Company candidate:
   - Read the record's relation fields → linked Person IDs.
   - For each linked Person (cap at the **5 most recently updated**):
     - `inbox_conversations_list` on that Person (`limit: 20`).
     - Read `lastMessageAtMs` and `lastMessageSnippet` from the response. Fetch messages only if needed for interpretation.
   - **Aggregate the signal across all linked People** for this Deal/Company: most recent timestamp, who sent it, substance.
   - For Companies: also check linked Deals' direct conversations if any.

5. **Per-record: self-check before deciding — exhaust signal sources.**
   - ✓ Checked the record's own conversations (step 4).
   - ✓ For Deals or Companies, checked conversations on linked People (step 4b).
   - ✓ Checked recent notes for context.
   - ✓ Checked `custom_activities` for prior breadcrumbs (so the agent doesn't re-litigate a previous decision).
   - ✓ No sub-agent was invoked. If yes, restart in the main thread.

   If you find yourself concluding "no signal" on a Deal that the user has touched in the last week, or a Company with active linked People, **that's a hint you didn't exhaust signal sources**. Re-check before writing the decision.

6. **Per-record: decide.** Apply the heuristics in "What signals advance a contact" to the **aggregated** signal. Output:
   - **MOVE** → target stage ID.
   - **STAY** → current stage.
   - **FLAG** → keep the record where it is, but write a custom activity surfacing the signal for human review.

   Apply the directionality rule: a MOVE is only valid if the target stage index ≥ current stage index in the cached ordering. If not, convert it to a FLAG.

7. **Per-record: apply MOVE.**
   - `records_update` on the stage field with the new option ID.
   - `custom_activities_create` with prefix:
     ```
     [breakcold-crm:auto-pipeline {YYYY-MM-DD}] Moved {From} → {To}. Signal: {one-line reason quoting the trigger, naming the person and channel where the signal came from}.
     ```

8. **Per-record: apply FLAG.** Write the `custom_activities_create` only (no field change). Roll into the run summary.

9. **Summarize:**
   > Moved **{N}** contacts forward, flagged **{M}** for review, left **{K}** unchanged. Biggest movers: **{name}** ({From} → {To}), **{name}** ({From} → {To})…

   For one-shot runs, end with: "Say *continue* to sweep the rest of the cohort."



## Optional but valuable: the breadcrumb-as-memory pattern

Always write a `custom_activities_create` for every decision (MOVE, STAY-with-strong-signal, FLAG). The user said: *"if you believe that creating a custom activity with explanations for both the user and yourself as mini extended context memory can help you for future updates and let the user know why you did what you did, then do it without asking."*

Do it. It's the difference between an automation that gets smarter every run and one that re-litigates the same decisions.

## Edge cases

- **Record has no pipeline stage set at all.** Treat as "new / unassigned". If signal is positive, move to the first non-empty forward stage (usually "Contacted" or "Engaged"). If no signal, leave it but breadcrumb that the stage is empty.
- **Two pipelines on the same object.** Rare but possible (e.g., a Person object with both a sales stage and a partnership stage). Ask the user once which to operate on, then cache the answer.
- **Stage option deleted between runs.** A record may sit on an option ID that no longer exists. Treat as "unknown stage" and surface in the run summary; don't fail silently.
- **Custom object pipelines.** Run the same logic on custom objects with a clear single-select stage field — no special casing required. If the custom object is a "parent of People" (like a project or campaign), apply step 3b — check conversations on linked People.
- **A contact replies after being moved to Won.** Don't move — they're already at the top. Surface in the summary if the reply contains a complaint or churn signal (e.g., "cancel", "refund", "unhappy") so the user can intervene.
- **A contact replies after being moved to Lost.** See the re-opening rule above — flag, don't move.

## Schedule it as a routine

Hand off to `routines.md`. The confirmation message becomes:

> I'll review the **{object(s)}** pipeline **{frequency}** and move contacts forward based on activity. I'll never move anyone backwards — disengagement gets handled by follow-up tasks instead. Want a **{matching cadence}** email recap?

Default frequency: **daily**. Acceptable: daily to every 3 days. More frequent than daily triggers the cost warning from `routines.md`.

## How this plays with Action 1 (follow-up tasks)

These two actions are **complementary**:

- Action 1 (tasks) handles contacts who are **falling out of momentum** — generates work for the user.
- Action 2 (pipeline) handles contacts who are **gaining momentum** — keeps the visual state of the CRM honest.

Run them in this order if both are scheduled the same day: **pipeline first, tasks second**. That way the task pass sees the freshest stage data (e.g., a contact just moved to Won won't get a "follow up" task created for them).
