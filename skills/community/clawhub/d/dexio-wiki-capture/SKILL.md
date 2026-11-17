---
name: dexio-wiki-capture
description: "Capture what an agent session settled into an LLM wiki before it is lost: at the end of a task or session (or over saved transcripts), pick out decisions, verified facts, corrections and working procedures, drop the chatter, and file each item on the page that owns it. Use when a session or task ends, before context is compacted, when a person says to remember something, or on a schedule over past agent sessions (Claude Code, Codex, Hermes, OpenClaw)."
license: MIT
metadata:
  author: dexio
  version: "1.1.0"
---

# Capture a session into the wiki

Most of what a wiki should hold is decided in conversations: a person picks an option, an
agent verifies a number, a procedure finally works on the third try. If nobody files it when
the session ends, it is gone, and the next agent rediscovers it or, worse, guesses. Capture is
the habit that keeps the wiki fed.

It is also where most wiki noise comes from. The goal is the few things that will matter
again, not a summary of the session.

## When

- At the end of any task that changed what is known or decided.
- Before the agent's context is compacted or the session is closed.
- When a person says "remember this", "note that", or "put that in the wiki".
- On a schedule, over saved transcripts, to catch sessions that ended without a capture.

## Steps

1. **List candidates from the session.** Only these kinds count:
   - Decisions a person made, with their words, the date, and the reason if given.
   - Facts verified during the session, with where they were verified.
   - Corrections: anything the session showed the wiki gets wrong. These come first.
   - Procedures that worked, including the step that failed before it worked.
   - Preferences or constraints a person stated that will apply again.
2. **Drop the rest.** Leave out plans that were not decided, the agent's own guesses, task
   progress, anything already in the wiki, secret values, and anything private a person has
   not cleared for everyone who reads the wiki. An agent proposing something and nobody
   objecting is not a decision. Where a credential is kept is worth filing; the value never
   is.
3. **Check each survivor against the wiki** (`wiki-orient`, search step). Already recorded:
   skip it. If the session showed the page is wrong or out of date, do not just overwrite
   it: follow `wiki-conflicts` (superseded when something changed, corrected when the page
   was wrong), which keeps a dated line of the old claim.
4. **File each item with `wiki-record`**: on the page that owns it, smallest edit, dated,
   sourced. The source is the session: who said or verified it, and when ("Dana in chat,
   2026-09-28"; "checked on the vendor pricing page, 2026-09-28").
5. **Ask rather than guess.** If something might be a decision but nobody said so, or a fact
   rests on the agent's reading alone, ask the person in one line before filing it. If they
   are not there, leave it out, or file it labelled `(unverified: <why>)` and lower
   `confidence` if the page carries one. A possible decision is never filed as a decision.
6. **Report what you filed**, one line per item with the page path, and what you skipped on
   purpose if a person might expect it to be there.

Keep it small. A typical session yields zero to five items. If you find fifteen, you are
summarizing, not capturing.

## Capturing from saved transcripts

For sessions that ended without a capture:

1. Find the transcripts. Claude Code keeps them as JSONL under
   `~/.claude/projects/<project>/`; Hermes exports them with `hermes sessions export`; other
   agents document their own location.
2. Keep a state file so each transcript is read once. Default: `.wiki-state.json` at the
   wiki root, listed in `.gitignore` (the checker reads only `.md` files), holding
   `{"capture": {"done": ["<transcript path or session id>", ...]}}`. On a hosted wiki keep
   it in the agent's own workspace. Never keep run state in a page.
3. Read only the person's messages and the agent's final answers first. Tool output is long
   and mostly noise; open it only to confirm a fact you intend to file.
4. Apply the steps above. Items from old sessions need extra care: check them against the
   current wiki and, for anything mutable, against the source, since they may have changed.
5. When several agents capture into one wiki, follow `wiki-shared`: search immediately before
   each write, because another agent may have filed the same item minutes ago. Treat the
   wiki as shared if the schema says so, the history shows more than one writer, or you
   cannot tell.

## Pitfalls

- Filing a transcript or a session summary as a page. Nobody reads them, and they bury the
  real pages in search results.
- Recording the agent's suggestion as the person's decision.
- Capturing the same fact on three pages. One page owns it; the others link to it.
- Waiting for the end of a very long session. Capture after each settled decision if the
  session is long enough that early context may be compacted.
