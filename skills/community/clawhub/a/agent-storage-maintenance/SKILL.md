---
name: "agent-storage-maintenance"
description: "Find and reclaim what an agent accumulates on disk: oversized sessions, duplicated transcripts, stale embedding caches, abandoned trees."
---

# Agent storage maintenance

Use when an agent database grows without matching work, when a storage alert
fires, when a session becomes too large for its own tooling, or before a
maintenance window.

The unit here is **bytes on disk**. That is a different problem from what an
agent pays per turn to read its instructions; if the question is token cost per
turn, this is the wrong procedure.

## 1. Measure before deleting anything

1. Compare the database file size against the sum of what its tables actually
   hold. A large gap is free-list pages from earlier deletions, not live data,
   and it is reclaimed differently.
2. Break the content down by session and by table. One session is usually
   responsible for most of it.
3. Check whether the growth matches the work done. Growth without matching work
   is a defect, not capacity, and raising a threshold to silence the alert hides
   it.

## 2. Transcripts: look for copies, not volume

Count assistant events against **distinct response identifiers** per session. A
ratio far above one means the transcript stores the same model response many
times. Repeat counts landing on a doubling sequence — 2, 4, 8, 16, 30, 60, 120,
240 — indicate the transcript is re-persisted wholesale rather than appended to,
so every rewrite copies everything already there. Sessions that compact or reset
frequently accumulate this fastest.

Two consequences. The disk figure is not the work done. And **any cost estimate
summed from transcript events is inflated by that same ratio** — count each
response once.

## 3. Sessions have hard ceilings you cannot configure

Session tooling carries limits that are compiled in, not settings: an archive
size beyond which deletion refuses, and an event count beyond which export
refuses. Past them the supported commands stop working and the failure reads as
"nothing happened" rather than an error.

Do not plan to raise them. Plan to stay under them:

- alert well below the ceiling, while the ordinary commands still work;
- prefer truncating a transcript to its last N lines over deleting the session,
  which keeps recent context and skips summarisation entirely, so it costs
  nothing;
- remember that retention settings prune whole sessions **by age**, so an
  actively used session never becomes eligible at any size.

## 4. Caches: classify, never delete by age

An embedding or derived-content cache typically has no expiry, no size cap and
no eviction. Classify each entry against the live index:

| class | test | disposition |
|---|---|---|
| useful | content hash **and** model both match a live entry | keep |
| dead-model | no live entry uses that model at all | safe to delete |
| unreferenced | model is live, no entry carries that hash | delete outside a grace window |

The dead-model class holds the surprising volume. A cache keyed by the model
*identifier string* rather than the model's identity stores the same vectors
twice whenever that reference is renamed — a local path becoming a registry ref,
a provider prefix changing. Both copies are valid; one is unreachable forever.
Report the identifiers side by side so a human confirms they denote the same
model before the duplicate goes.

Protect recent unreferenced entries. Where the provider is local, a miss costs
CPU and nothing else, so prune freely; where it is remote, a miss costs a call,
so keep a longer window.

## 5. Check what your connection can see

Before deleting rows from any agent database, confirm the client can open every
object the schema defines. Databases of this kind carry virtual tables backed by
loadable extensions, vector indexes in particular. A client without the extension
reads ordinary tables fine while being blind to the virtual ones, and a delete
from it can leave a derived index inconsistent.

Restrict deletes to plain tables with no triggers, which need no extensions.
Prefer the agent's own supported commands, which go through the code that owns
every table. And test any full rebuild on a copy before running it for real.

## 6. Reclaim in two passes

1. Deleting rows returns pages to the free list; the file does not shrink. Only a
   full rebuild returns space, and that needs exclusive access — take the
   maintenance window rather than working around it.
2. Incremental auto-vacuum does not help with pages freed before it was enabled.
   If the free-list count barely moves after a checkpoint, a full rebuild is the
   only option.
3. **Expect a cascade.** Compacting transcripts invalidates derived index entries
   that pointed at them, and the index prunes itself shortly after, leaving a
   fresh free list. A single rebuild immediately after the delete looks like a
   failure. Plan a second pass.
4. Verify integrity after any rebuild, and confirm the index reports the same
   file and entry counts as before.

## 7. Look outside the database

Abandoned trees are usually larger than anything inside it. Failed migrations,
rehearsal copies and pre-upgrade snapshots each hold a full workspace and can
outweigh every database on the host combined. Before removing one:

- confirm nothing references it — configuration, service units, scheduled jobs;
- keep the most recent of a series and treat earlier attempts as redundant;
- expect parts of it to be owned by another user and to need a second pass.

## 8. Make the growth visible

Every failure here is silent: the disk simply fills. Add checks that report the
**ratio** as well as the absolute size — duplicate-to-unique for transcripts,
useful-to-total for caches — because a ratio distinguishes a large working set
from an accumulating one, and a threshold alone does not.

## 9. Report

State what was measured, counts by class before and after, bytes returned, the
free-list behaviour across both passes, and the index counts before and after as
evidence that nothing live was lost.
