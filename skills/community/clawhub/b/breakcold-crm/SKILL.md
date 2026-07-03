---
name: breakcold-crm-openclaw
description: Operate Breakcold CRM through the hosted Breakcold MCP server from OpenClaw or ClawHub. Use for Breakcold CRM work, deals, pipeline or Kanban updates, follow-up tasks, reports, prospect research, inbox contact detection, CRM setup, notes, custom fields, and multichannel inbox workflows.
version: 1.0.0
metadata:
  openclaw:
    skillKey: breakcold-crm
    homepage: https://github.com/breakcold/mcp/tree/main/skills/breakcold-crm-openclaw
    primaryEnv: BREAKCOLD_MCP_TOKEN
    envVars:
      - name: BREAKCOLD_MCP_TOKEN
        required: false
        description: Optional Breakcold MCP bearer token for clients that cannot use OAuth.
---

# Breakcold CRM

The expert playbook for any AI agent operating a user's Breakcold CRM through the Breakcold MCP server. Optimized for **speed**, **error-proofing**, and **minimum back-and-forth** with the user.

This OpenClaw/ClawHub edition is a strict text-only skill package. It keeps the same Breakcold CRM operating playbooks as the universal `breakcold-crm` skill, but removes platform-specific bundles and binary assets so ClawHub can publish and scan it cleanly.

## What this skill covers

Six headline workflows the user explicitly cares about, plus the universal plumbing that makes them fast and safe. Open the reference file for the workflow you're running — don't operate from memory.

| # | Workflow                                                            | Reference                                |
|---|---------------------------------------------------------------------|------------------------------------------|
| 1 | Multichannel auto-task creation (follow-ups linked to conversations)| `references/action-tasks.md`             |
| 2 | Auto-movement of contacts in the pipeline (Kanban)                  | `references/action-pipeline.md`          |
| 3 | Auto-report (visual, Breakcold-branded, actionable insights)        | `references/action-reports.md`           |
| 4 | Prospect research (web research → notes on records)                 | `references/action-prospect-research.md` |
| 5 | Contact detection & creation from the inbox                         | `references/action-contact-detection.md` |
| 6 | CRM setup & reorganization from a website URL                       | `references/action-crm-setup.md`         |

Anything not listed above is still in scope — the Breakcold MCP exposes the full CRM, inbox, tasks, notes, and metadata surface. The six workflows are simply the ones to deliver perfectly.

## Cross-cutting references

- `references/fundamentals.md` — auth, regions, workspaces, rate limits, attribute types, conversation/record linking, error handling, **canonical tool-call examples**. Read this once at the start of any complex run.
- `references/routines.md` — how to schedule any of the six actions, set frequency, and offer daily/weekly recap emails. Linked from every action's "schedule it" step.
- `references/branding.md` — Breakcold color tokens (primary `#0059F7`), tag-color palette, asset paths, and visual style for every report or visual deliverable.
- `references/report-design-guide.md` — the **module catalog** for Action 3 reports: which sections to include based on what's actually in the user's workspace, plus hero / headline / mascot rules.
- `assets/` — text-based brand assets: Breakcold mark SVG, full logo SVG, and a fully populated `report-template.html` chassis with the mascot embedded inline.

## Session-start orientation (mandatory boot sequence)

Run this in one shot at session start. Cache results in your scratchpad — never re-fetch within the same session.

```
SESSION_START:
  1. capabilities_list()                       → cache scopes
                                                 IF auth error: see fundamentals.md § 9
                                                 IF the response includes the authenticated actor's user ID,
                                                 cache it as CURRENT_USER_ID immediately.
  2. workspaces_list()                         → cache workspace IDs
                                                 IF count == 1: select silently
                                                 IF count  > 1: ask user ONCE, cache choice
                                                 Same as step 1: cache CURRENT_USER_ID if it appears here.
  3. Resolve CURRENT_USER_ID if still unknown   → see fundamentals.md § "Resolving the current user ID".
                                                 Default fallback: read it from the response of the next
                                                 write call (records_create, tasks_create, notes_create,
                                                 custom_activities_create) and cache from then on. The
                                                 user's ID appears as the createdBy / actorId field on
                                                 any write response.
                                                 CURRENT_USER_ID is the default assignee for any task
                                                 the agent creates on the user's behalf (see action-tasks.md).
  4. (lazy, when first action runs)
     crm_objects_list(workspace_id)            → cache object IDs
     crm_fields_list(object_id)                → cache per object as needed
     crm_field_options_list(field_id)          → cache only for select/multiselect you'll touch
```

Anything outside this boot sequence (action-specific reads) is owned by the relevant `action-*.md`.

## Universal rules — apply to every workflow

These rules exist because the user explicitly asked for **speed, error-proofing, and minimal actions**. Violating any of them creates work for the user.

- **Authenticate once.** Never ask the user to re-authenticate mid-session. If a tool call returns an auth error, surface it once with a one-tap reconnect path. Don't loop.
- **Cache discovery aggressively.** A second call to `workspaces_list`, `crm_objects_list`, or `crm_fields_list` for the same object in the same session is a bug. Reuse the IDs you already hold.
- **Verify before mutating.** Before `records_update`, `records_archive`, `tasks_create`, `tasks_complete`, `notes_update`, or any `crm_*_delete`, confirm the target ID exists from a prior read. Never trust speculative IDs.
- **Never create duplicates.** Before creating a record, task, or note, check for an equivalent. For tasks: call `tasks_list` on the record and bail if an open task with the same intent and a due date in the next 7 days already exists. For records: see the duplicate-detection rules in `references/action-contact-detection.md`.
- **Leave a breadcrumb when it helps.** For any non-trivial automated decision (moving a contact, auto-creating a record, choosing a pipeline stage on weak signal), call `custom_activities_create` on the record with a one-line explanation. This is your shared memory across runs and the user's audit trail. Don't ask permission for this — just do it when it adds clarity for the next run.
- **Confirm once, then act.** When the user kicks off an automated workflow, confirm parameters in a single message (criteria, frequency, assignee, recap channel). Don't re-prompt for what they already answered.
- **Never move pipelines backwards.** Treat pipeline stages as a directed flow. See `references/action-pipeline.md` for the exact rule.
- **Ask only when it actually changes the output.** Defaults are your friend; surface them as "I'll do X — say so if you'd rather Y." Don't ask about obvious stages or obvious decisions.
- **Respect rate limits gracefully.** On HTTP 429 / JSON-RPC `-32029`, wait the `Retry-After` interval and resume from the same point. Don't restart the workflow. See `references/fundamentals.md § 7`.
- **Mirror the user's language for anything written into Breakcold or shown to the user.** Task titles, note bodies, report headlines, confirmation messages, stage names, and view names all match the user's language (and the language already present in their workspace). If a user writes to you in French, write `Relancer — fil email en silence (9 jours)` not `Follow up — email thread went quiet (9 days)`. The single exception: **internal breadcrumb prefixes** like `[breakcold-crm:auto-tasks 2026-05-23]` stay in English so future runs can parse them reliably across users. Everything else translates.
- **Conversations live on people — traverse relations before concluding "no signal", and create tasks on the Person where the conversation lives.** Deals, Companies, and most non-Person objects don't usually have conversations attached directly. Their **linked People do**. Whenever a workflow checks for "activity" on a parent object, **always also fetch conversations on the linked People records**. And whenever a workflow creates a task in response to conversation activity, **the task goes on the Person record, not on the parent Deal or Company** — so the task can link to the actual conversation. Concluding "inactive" on a Deal whose linked Contacts are actively replying, or creating a task on a Deal that can't link to the conversation, are the two most common false-negatives in this skill. See `references/action-pipeline.md` step 3b for the signal-traversal procedure and `references/action-tasks.md` step 2 for the task-placement rule.
- **Notes are HTML.** When calling `notes_create` or `notes_update`, the `content` field renders as rich HTML in Breakcold. Plain text with `\n` line breaks comes out as one unbroken paragraph — the user will have to ask you to reformat. Use semantic HTML (`<h3>`, `<p>`, `<ul>/<li>`, `<strong>`, `<hr>`) for any note longer than two sentences. Always also provide `contentPlain` as the plain-text fallback. See `references/fundamentals.md § 11 - notes_create` for the payload shape and `references/action-prospect-research.md` step 6 for a structured template.
- **Small pages, processed inline.** Cap every list call at `limit: 20` — `records_list`, `inbox_conversations_search`, anywhere the API takes a `limit` parameter. Process each page completely (filter → decide → mutate → write breadcrumbs) **before** fetching the next page. Never accumulate more than one page of raw data in working context at once. **Why this is a hard rule, not a tip:** when a tool response exceeds the runtime's payload threshold (~50KB on several agent platforms), the runtime saves the response to a file and returns a truncated preview. The model, now working from a partial view of its own data, loses confidence and may delegate to a sub-agent, restart the workflow, or stall. A 20-record page stays well under the threshold across every runtime, and the model keeps full context. 20 × ~5KB ≈ 100KB worst-case raw, but the filtering happens inline immediately so the *processed* set stays tiny. See per-action playbooks for the exact loop structure.
- **No sub-agent delegation for any workflow in this skill.** Make every tool call directly in the main thread. Do **not** use any sub-agent / task-delegation tool — by whatever name the runtime exposes it (`Agent`, `Task`, `dispatch_agent`, `subagent`, `delegate`, etc.). Sub-agents start with zero cached context, re-discover the schema from scratch, hit the same payload limits the main agent does, and stall on tool-approval prompts that the user can't see. The skill's caching architecture only works in one continuous main-thread context. If you find yourself reaching for a sub-agent because "this loop is long" — that's a signal to apply the small-pages rule, not to delegate.
- **Small-batch first for one-shot runs.** Default to a first-page-only test run for any one-shot action invocation (auto-tasks, pipeline movement, contact detection, prospect research). Process only the first 20 records, write the breadcrumbs, then surface the result with: "I processed the first 20 — say *continue* to sweep the rest." This bounds context, proves the pipeline works on real data, and is reversible if anything looks off. The exception is **scheduled runs** triggered by a saved routine — those proceed end-to-end because the user already approved the cadence at setup time and isn't watching the run live. Apply small-batch-first even when the user's request was specific and explicit (e.g., "Create tasks for any contact I haven't talked to in 5 days") — the upside is huge, the cost is one word ("continue") from the user.

## Routing — match the user's phrasing to a reference

The user rarely says "run workflow 3." Match on intent:

| User says something like…                                                                  | Open this reference                       |
|--------------------------------------------------------------------------------------------|-------------------------------------------|
| "follow up", "ping the cold ones", "tasks for people who went quiet"                       | `references/action-tasks.md`              |
| "move contacts forward", "advance my pipeline", "update my Kanban", "auto-progress deals"  | `references/action-pipeline.md`           |
| "give me a report", "how is my CRM doing", "what's working", "deal review", "sales recap"  | `references/action-reports.md`            |
| "research these prospects", "what does this company do", "enrich my contacts"              | `references/action-prospect-research.md`  |
| "find missing contacts in my inbox", "add new people from emails", "who isn't in the CRM"  | `references/action-contact-detection.md`  |
| "set up my CRM", "reorganize Breakcold", "I'm new", "redo my pipeline from scratch"        | `references/action-crm-setup.md`          |
| "set up a routine", "do this every morning", "schedule a weekly recap"                     | `references/routines.md`                  |
| "what can you do?", "I'm a bit lost", "help me with Breakcold"                             | See "If the user is lost" below           |

Same matching applies across languages. "Relancer mes contacts" → `action-tasks.md`. "Reorganiza mi CRM" → `action-crm-setup.md`.

## If the user is lost or asks what you can do

Don't list every MCP tool. Lead with the six headline workflows — one line each, **in the user's language** — and let them pick:

> Here's where I really shine inside Breakcold:
>
> 1. **Auto follow-up tasks** for contacts where you're losing momentum — every task links straight to the conversation.
> 2. **Pipeline auto-movement** based on what's actually happening in your emails, LinkedIn, WhatsApp, Telegram, and meetings.
> 3. **Visual CRM reports** that point to what's working and what's not — no fluff, just actionable insights.
> 4. **Prospect research** that writes itself back into your notes and deals.
> 5. **Inbox → CRM** — find people you're talking to who aren't in the CRM yet and add them.
> 6. **Full CRM setup or reorganization** from your website URL, no consultant needed.
>
> Beyond these I can also create or update records, tasks, notes, and custom activities; manage pipeline stages, fields, options, and views; search your inbox; and almost anything else the Breakcold API supports. Where would you like to start?

## Recap emails for routines

Any of the six actions can run as a routine. When you set one up, always offer the user a daily or weekly recap by email — a short summary of what got done since the last run. This requires the user's email connector (Gmail, Outlook, etc.) be linked. Follow `references/routines.md` for the exact wording and setup.

## Deliverables outside Breakcold (reports, exports)

When an action produces a visual artifact (most relevant for action 3 — reports), always render it on-brand. Pull `references/branding.md` first so colors, type, and layout are consistent without thinking.

**Reminder.** Open the reference file for the action you're running. The references contain the exact tool sequences, defaults, and edge cases. Operating from memory is how mistakes happen — and the user explicitly asked for error-proofing.
