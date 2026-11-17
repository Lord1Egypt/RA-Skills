---
name: inner-life
description: Keeps a dated record of how an agent's work has been going — an evening journal, free thinking at night, and a way to read it back. Use when asked to run the inner-life evening or night routine, to note something in state, or to recall how a stretch went. Writes under inner-life/ and replaces a short summary in native memory, which is injected into later sessions.
version: 1.2.2
author: DKistenev
license: MIT-0
metadata:
  hermes:
    tags: [journal, dreams, self-reflection, continuity, memory]
  openclaw:
    emoji: 🌙
    homepage: https://github.com/DKistenev/agent-inner-life
---

# Inner Life

## Overview

An agent accumulates a great deal in a day and keeps almost none of it. Facts survive, procedures survive — but how things have been going does not. Every morning starts the same way regardless of whether yesterday was a good day or a rough one.

This skill adds three things: **state**, a running record of dated facts about how things are going; an **evening journal** that turns the day into a written entry; and **dreams**, free thinking during the quiet hours. Tomorrow is reached through a short summary written into native memory, which is injected into the system prompt of every session. There are no scores anywhere in this — how long ago something happened carries the meaning that a number would only obscure.

## When to Use

This skill only runs when it is asked to run. It is not a background habit, and nothing here should be triggered by a conversation simply having been interesting.

- A scheduled run fires — the evening job, the night job, or the weekly rollup
- The user asks to note something in state, or names a thing to remember about how work is going
- The user asks how things have been going, what happened during some stretch, or what is still open — read the record back rather than reconstruct it

If `inner-life/state.md` does not exist, the skill has not been set up. Do not create it mid-conversation to record something — ask first. Setup is a decision to start keeping a record, and it is the user's to make.

**Don't use for:** storing facts or procedures. Whatever runtime this is on already has somewhere durable facts live and somewhere reusable workflows live, and something already maintains both. This skill does not duplicate either.

## Four modes

| Mode | When | Read |
|---|---|---|
| Logging | something happened | `references/state.md` |
| Evening | once a day, and the weekly rollup on Sunday | `references/journal.md` |
| Night | quiet hours | `references/dreams.md` |
| Recall | someone asks how things have been going | `references/recall.md` |

Read only the reference for the mode at hand. All four are never needed at once.

Three of them write and one only reads. Recall answers from what is already on disk; it does not update state, refresh the memory summary, or prune anything.

## First run

If `inner-life/state.md` does not exist:

1. Copy `templates/state.md` to `inner-life/state.md` in the working directory.
2. Create `inner-life/journal/` and `inner-life/dreams/`.

Nothing else is needed — there is no configuration and no setup script.

Say plainly, once, what starting this means: the agent will keep a dated record of how work is going, and a few lines of it will be visible in every later session.

## What this writes down

This skill keeps a record. Anyone enabling it should know what that means before the first run, not after.

| Where | What lands there | Who sees it later |
|---|---|---|
| `inner-life/state.md` | dated one-line facts about how work is going | read at the start of each run |
| `inner-life/journal/` | one entry per day, a few hundred words | nobody, unless asked — it never enters a session by itself |
| `inner-life/dreams/` | free thinking, unrelated to the user's data | nobody, unless asked |
| native memory | two or three lines, replaced each evening | **every later session, in the system prompt** |

The last row is the one that matters. Everything else stays on disk and is read only when a run opens it. What goes into native memory is different in kind: it is injected into the system prompt of every session that follows, including sessions about something else entirely, and — on a shared or multi-user host — including sessions that are not the same person's.

So the rule for the summary is narrower than the rule for the rest:

- Write about how the work has been going, not about who the user is.
- Never carry over secrets, credentials, tokens, or anything that arrived in confidence.
- Never carry over personal details about the user or about third parties — health, employment, relationships, location, legal or financial matters — even when they came up naturally and even when they feel relevant.
- If a fact would be awkward to see quoted back in an unrelated session next month, it does not belong in the summary.

The same restraint applies to state and the journal, with more room: they stay local. But the file the agent writes today is the file it reads back in a month, and there is no undo — so prefer the shorter version of anything sensitive, and leave out what does not need to be there at all.

**Turning it off.** Removing the skill stops the writing; it does not delete what was written. `inner-life/` and the memory summary persist until they are removed by hand. Anyone who wants the record gone should delete the directory and clear the summary through the `memory` tool.

## What this is not

Not a memory system: the agent already has one, and this skill deliberately stays out of it.

Not mood tracking. There are no levels, percentages, or bars here on purpose. A date already says everything a rating would claim to say, it cannot drift out of sync with reality, and it requires nobody to be trusted with keeping it accurate.

## Common Pitfalls

1. **Writing the journal and skipping the memory summary.** The journal never enters a future session's context. Only the summary does. Skip it and tomorrow notices nothing.
2. **Recording judgments instead of facts.** `getting frustrated with deploys` is useless in a month; `third failed deploy, same missing env var` is not.
3. **Dreaming without checking the last two weeks.** The same preoccupation comes back in new words, and the record loses its value.
4. **Filling native memory with prose.** The budget there is a couple of thousand characters; long text displaces something that mattered more.
5. **Writing to satisfy the schedule.** An empty day deserves one honest line, and an empty night deserves no file at all.
6. **Reconstructing instead of reading back.** A stretch with no entries is a stretch where nothing was written, and saying so is the correct answer. Filling the gap with what probably happened puts events into the record that never occurred.
7. **Letting something private reach the summary.** A detail that was fine to hear once is not automatically fine to repeat in every session for a month. The summary is the widest-reaching thing this skill writes and deserves the narrowest content.

## Verification Checklist

- [ ] `inner-life/state.md` exists and its entries are dated
- [ ] Today's journal entry exists, or the day was deliberately left blank
- [ ] The native memory summary reflects recent dates, not last month's situation
- [ ] Stale state entries have been pruned, and anything still open remains in `Waiting`
- [ ] The summary holds nothing private, nothing confidential, and nothing about a third party
- [ ] A read-back answered from entries that exist, and named the gaps instead of filling them
