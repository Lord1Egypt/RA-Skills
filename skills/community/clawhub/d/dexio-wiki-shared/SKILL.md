---
name: dexio-wiki-shared
description: "Rules for an LLM wiki that several agents, machines or people write to: read before writing, detect concurrent edits, prefer small edits to rewrites, attribute every change with a note, derive the index and log instead of hand-editing shared files, and keep scoped content where only the right readers see it. Use when more than one agent or person maintains the same wiki, or when setting up a wiki for a team or an agent fleet."
license: MIT
metadata:
  author: dexio
  version: "1.1.0"
---

# Share a wiki between writers

The reference LLM-wiki setup has one writer: one person, one agent, one folder. Add a second
writer and new failures appear:

- Two agents rewrite the same page and the second silently discards the first's work.
- Every ingest rewrites `index.md` and `log.md`, so every parallel change conflicts there.
- Nobody can tell which agent wrote a claim or whether anyone checked it, so one agent's
  mistake becomes everyone's.
- Pages merge across boundaries that should stay apart: one client's details on another's
  page, private notes on a page everyone reads.
- A folder on one machine has to be synced before agents elsewhere see it.

These rules close those gaps. They add a little work per write and save a great deal of
cleanup.

## Rules

1. **Read before you write, in the same task.** Never edit a page from memory of how it
   looked earlier. Reread it immediately before the edit.
2. **Detect concurrent edits.** Hosted wiki: pass the version you read (on Dexio,
   `base_version`) so the write fails if someone changed the page in between; then reread,
   merge, and retry. Git: pull before you start and again before you push; resolve conflicts
   by reading both sides, never by taking yours wholesale.
3. **Edit small.** Replace the sentence or section that changed. Whole-page rewrites are for
   pages you own in this task or a deliberate refactor. Small edits merge; rewrites collide.
4. **Attribute every change.** Name the writer (agent name in the hosted tool's agent field,
   or the git commit author) and leave a note saying what changed and why. The history then
   answers who wrote a claim and when, which is the first question when a claim turns out
   wrong.
5. **Do not hand-edit shared catalog and log files.** Give every page a one-line
   `description:` and derive the catalog from them (`wiki-lint`'s `--catalog`, or the host's
   page list). Use git history or the host's change history as the log. If the wiki must
   keep an `index.md`, regenerate it in one place (a scheduled job) instead of having every
   writer edit it.
6. **Own pages lightly.** A page can name its maintainer in frontmatter (`owner: research-agent`).
   Others may still fix errors and add facts, but restructuring waits for the owner or a
   person.
7. **Draft freely, promote deliberately.** Where accuracy matters more than speed, agents
   write to `drafts/` or mark pages `status: draft`, and a person or a reviewing agent
   promotes them (`wiki-review`). Use this for decisions and anything customer-facing, not for
   every note.
8. **Keep scope explicit.** If some readers must not see some content (a client, a
   household, a private project), give it its own wiki or folder with its own access, and
   never merge pages across that boundary. A `scope:` or `tenant:` field on pages helps
   agents notice before they merge.
9. **Settle conflicts, do not race.** If two writers disagree on a claim, follow
   `wiki-conflicts`. Reverting each other's edits is not a resolution.

## Setting up a shared wiki

- One schema page that every writer reads first (`wiki-setup`), and a line in each agent's
  instructions file pointing to it.
- A single canonical copy. A synced folder with several writers needs pull-before-write
  discipline from every one of them; a hosted wiki with conditional writes and per-change
  history does it for them.
- A scheduled lint (`wiki-lint`) that one agent runs and reports on, so link and frontmatter
  drift is caught weekly rather than when someone needs the page.
- A scheduled review of agent edits (`wiki-review`) by an agent that did not make them, and a
  capture step at the end of each agent's sessions (`wiki-capture`).

## Pitfalls

- "I'll just regenerate the page from scratch." Other writers' additions vanish, and the
  history shows one huge diff nobody reviews.
- Committing many unrelated wiki edits in one commit. Nobody can revert one bad change.
- Letting agents write secrets or private details "because the wiki is internal". Internal
  wikis get shared, exported and read by new agents with different scopes.
