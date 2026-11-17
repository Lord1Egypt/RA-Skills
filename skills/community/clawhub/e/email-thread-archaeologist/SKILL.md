---
name: email-thread-archaeologist
description: Use when reconstructing what actually happened in a long, mangled email thread (deep quote nesting, forwards-inside-forwards, mixed Gmail/Outlook quoting) — splits quoting strata, attributes lines to authors, dedupes repeated quote layers, and outputs a chronological decision ledger plus questions that were never answered.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [email, threads, decision-history, quote-parsing, information-retrieval, meetings]
---

# Email Thread Archaeologist

Long email threads arrive as archaeology: fourteen replies deep, quoted
by four different clients, with an Outlook forward somewhere in the
middle that embedded the whole prior history with `From:/Sent:/To:`
headers. The same sentences appear five times at five quoting depths.
When someone asks "wait, what did we actually decide, and did anyone
ever answer the insurance question?" — the answer is in there, but
reading it means mentally un-nesting quotes for twenty minutes.

This skill excavates instead. It takes one `.eml` or text dump of the
thread and produces:

- **A chronological timeline** — oldest fact first, each fact once,
  attributed to its original author
- **A decision ledger** — lines containing agreement/decision markers
  ("agreed", "let's go with", "approved", "locked in", "action item")
  with who committed
- **Open questions** — questions that no later message answered

## When to Use

- "What did we decide in that thread?" — reconstruct the history
- Pre-meeting prep — the decision ledger IS the agenda's "previously
  decided" section
- Catching dropped questions — the open-questions pass finds the thing
  everyone forgot to answer three replies ago
- Onboarding into a project — one dig beats reading a 40-message chain
- Answering "who said that?" — attribution survives quote mangling

**Don't use for:** legal discovery (this is heuristic attribution, not
certified evidence), or threads where the mail client collapsed quotes
entirely (nothing to excavate — fetch the originals).

## How It Works

1. **Strata splitting** — lines are grouped by quote depth (`> ` count)
   and client attribution headers (`On ... wrote:`, `From:/Sent:/To:`,
   `--- Forwarded message ---`). Each attribution starts a new stratum
   (a buried message).
2. **Attribution** — the author is parsed from the attribution line
   (`On Tue, X wrote:` → X; `From: Chen, Robert` → Chen, Robert).
3. **Dedup, oldest-first** — every line is normalized (quotes and
   whitespace stripped) and compared against the history with fuzzy
   matching (difflib ≥0.90): the fifth copy of the same sentence dies;
   the FIRST (oldest) occurrence survives.
4. **Reorder** — strata are re-sorted deepest-first, since deeper
   quoting = older message. Output reads as a timeline.
5. **Classify** — decision markers flag commitments; questions that
   lack a later answer line (yes/no/agreed/done starters within the
   next facts) are reported as open.

## Commands

```bash
python3 scripts/thread_archaeologist.py dig thread.txt        # everything
python3 scripts/thread_archaeologist.py decisions thread.eml  # ledger only
python3 scripts/thread_archaeologist.py questions thread.txt  # unanswered only
python3 scripts/thread_archaeologist.py strata thread.txt     # debug: layer view
```

`.eml` files are parsed with the stdlib email module (prefers
text/plain part; falls back to html). `.txt` = raw paste, works fine.

## Example Output

```
Strata (quoting layers): 7  |  Unique facts after dedupe: 15

--- RECONSTRUCTED TIMELINE (oldest first) ---
[Oct 13, 2026 at 9:02 AM Dana Whitfield] Marcus — can you get the vendor quotes ...?
[Oct 13, 2026 at 5:20 PM Marcus Lee] Got quotes. Voltix $13,900, Signature $14,200. ...
[Oct 14, 2026 at 1:02 PM Marcus Lee] ... Decision: approve the extra $1,200 ...
...
--- DECISION LEDGER ---
✔ [Oct 14, 2026 at 3:12 PM Dana Whitfield] Agreed — ... Let's go with Signature.
✔ [layer-0] ... meeting booked for Thursday 10am ...
--- OPEN QUESTIONS (never answered in-thread) ---
? [Oct 14, 2026 at 3:12 PM Dana Whitfield] One open item: who owns the punch-list documentation?
```

`layer-0` = the newest (unquoted) message, whose author is whoever
sent you the mail.

## Common Pitfalls

1. **Bottom-quoting threads.** Some threads quote BELOW the new text.
   The strata split still works (depth still marks age), but the
   newest-message attribution may land on the wrong stratum — verify
   `layer-0` lines against the actual latest mail.
2. **HTML-only mails.** Clients that reply in HTML convert to quote
   bars, not `>` characters, when pasted. Export/paste with "show
   quoted text" expanded, or use the .eml.
3. **Fuzzy dedup thresholds.** 0.90 keeps paraphrase-level differences
   alive; if your thread has many near-identical boilerplate lines
   ("Thanks!", "Sounds good"), they may survive as duplicates — they're
   junk for the ledger but harmless.
4. **Decisions phrased as questions.** "Shall we go with Signature?"
   is a proposal, not a decision — the ledger wants a later agreement
   line; if the thread only has the question, check open questions
   instead.
5. **Forwarded attachments.** An attached .eml inside a forward is not
   excavated — extract and dig it separately.

## Verification Checklist

- [ ] Timeline starts with the genuinely oldest message (spot-check
      the deepest-quoted line in the source)
- [ ] Decision ledger lines read as commitments, not questions
- [ ] Open questions verified against the thread tail (the last
      message may have answered without marker words)
- [ ] `layer-0` attribution = who sent you the mail

## References

- `references/quoting-formats.md` — how each client quotes, what the
  strata look like, and the marker vocabulary for decisions/answers.
