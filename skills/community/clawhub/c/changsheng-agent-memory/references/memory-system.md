# The memory system behind ChangSheng

This is the design this skill implements, written so you can copy the shape into
your own setup — with any file layout, any naming, any tool. The scripts are
conveniences; this document is the method.

Everything below is expressed twice: the **skeleton** (true for any agent
system of comparable size) and **this package** (what the shipped scripts do).

---

## 1. The problem

An agent that forgets is usually not an agent with a storage problem. It is an
agent with three unseparated problems:

1. **Reading too much** — recovery re-reads everything, costs tens of thousands
   of tokens, and still misses the one thing that mattered.
2. **Writing too little** — the conclusions of a session live only in the chat
   that is about to be discarded.
3. **Never reviewing** — what was written once stays forever, even after it
   became wrong, and nobody notices because nobody was asked to look.

Store more, read more, and check more rarely — the memory gets heavier and
less true at the same time. The three problems need three separate answers.

---

## 2. Four layers by depth

Memory is stored in four layers, ordered by how close they sit to the raw
material. A fact has exactly one home.

| Layer | Holds | Written by | Read when | Cost |
|---|---|---|---|---|
| **Raw** | transcripts, logs, imported documents | machines | only when you need the exact original wording | ~0 (search only) |
| **Working** | dated logs, open items, handovers | every session, automatically | every session (a small budgeted set) | small, fixed |
| **Reference** | distilled notes, decision records, extracted lessons | a curation pass | when the task touches that subject | ~0 until flagged |
| **Always-on** | identity, rules, user profile | you, deliberately | every session, by the host itself | tiny |

Two rules do the real work:

- **Upper layers store how to read; lower layers keep the original words.** A
  summary never replaces the source it summarises.
- **Nothing lives in two layers.** When a new note belongs in "reference", it
  does not also stay in "working" — one home, or it will be read twice and
  fixed once.

*This package:* the raw layer is your own files; the working layer is what
`scripts/memory_index.py` discovers (rules / todos / journal); the reference
layer is what you point `tracked_files_extra` at; the always-on layer is what
your host injects (and the skill detects and skips).

---

## 3. Two orthogonal questions: whose, and which direction in time

Depth answers *how far down* a memory lives. Two further questions answer
*what kind* it is. They are independent of depth — one memory, one tag, and
the tag decides where it goes.

**Whose** — my own state, or the user's.

**Which direction in time** — what already happened, what is happening now,
what is coming, or what does not move (a standing rule or a relationship).

| Whose | Direction | Typical content | Lives in |
|---|---|---|---|
| Mine | now / this session | what I am doing, what I just learned | working layer, handover |
| Mine | past | projects I finished, lessons I hit | reference layer |
| Mine | future | what I will do next | open items |
| Mine | standing | my operating rules | always-on layer |
| The user's | now / this session | what they just told me | working layer |
| The user's | past | their history, prior decisions | reference layer |
| The user's | future | their plans, deadlines | open items |
| The user's | standing | who they are, how they want to work | always-on layer |
| Mutual | standing | how we work together, what is off-limits | always-on layer, as triggers |

The last row is the one most systems skip, and it is the one users notice
most: rules that only exist as prose in a document are not applied. A rule
becomes real when it is written as *situation → what to do*.

**How to use the table:** when something new arrives, ask the two questions,
place it, and stop. If two answers look plausible, prefer the shallower layer
that is read more often — over-inclusion is what makes recovery expensive.

---

## 4. Entry points — nothing enters without a door

A memory that arrives without a named door is a memory nobody will find
later. Each kind of event gets exactly one landing place, and the place is
named so it can be checked.

| Event | Lands in | Check that it happened |
|---|---|---|
| Work finished | lesson / decision record | the curation pass reports "collected N" |
| A decision or a changed rule | decision record (append one line, never edit) | the record is the first source when the rule is questioned |
| A correction or a mistake | mistake log, then the always-on layer if it generalises | the rule was actually added to the always-on layer |
| A file or link the user gave | reference layer, named by subject | the file exists where the record says |
| A task | open items, with who it waits on | the open-items file grows |
| Who the user is | profile, reviewed weekly | the weekly review says "0 candidates" out loud |

Note the last column. **An entry point without a check is a wish.** If nothing
counts it, it will silently stop happening — and the first sign is a question
the user asks that the agent should have answered.

*This package:* the checks are yours to run; the skill gives you the two
scripts that make two of the doors cheap to keep (see §6).

---

## 5. The must-read layer is a budget, not a wish list

The always-read set is the expensive part: every session pays it. Treat it as
a budget with a hard cap.

- **Hard cap** on the total size of the always-read set. Above it, recovery
  fails loudly rather than quietly getting expensive.
- **Target waterline** below the cap: aim to sit under it, do not fill it.
  Unused budget is headroom, not debt.
- **Adding one entry requires naming one that leaves.** The budget is finite
  and attention is finite; a net-zero edit is the only kind that keeps the
  layer honest.
- **Every entry carries an expiry**: a review date, a maximum age, and the
  action to take when it expires (demote it, archive it, or ask again). An
  entry with no expiry is an entry that will never be questioned.
- **Stale entries are flagged, never presented as fresh.** A rule read from a
  file that has not been touched in months is a historical fact, not a current
  instruction.

*This package:* `scripts/memory_ledger.py` is exactly this budget, as a table
you can read and a check you can run.

---

## 6. Two doors, made cheap

**The ledger** (`scripts/memory_ledger.py`) — the budget of §5 as a table:
every always-read entry with its reason, its review date, its maximum age and
its expiry action. It reports missing files, incomplete entries, overdue
reviews, stale entries and budget overruns, and it exits non-zero so it can be
wired into a hook.

**The recall** (`scripts/recall.py`) — the question *"why did we decide this?"*
is the one memory systems answer worst. A grep tells you a string appears
somewhere; it does not tell you what you concluded, when, or on what grounds.
The recall searches the four surfaces where conclusions actually get written —
open items, dated logs, notes/decisions, and the archive — and prints them
with file and line. Two properties matter:

- **Each surface is reported even when it had no hits.** Silence would be
  indistinguishable from "never looked".
- **If nothing could be searched at all, that is an error, not an answer.**
  "Not found" and "not looked" must never share an exit code.

**The handover** (`assets/handover-template.md`) — the working layer's pointer
across a session boundary: done, leftover, pointers, next step. One writer
only, overwritten each time, read once and deleted. A handover that lingers
becomes a stale pointer that lies to the next session.

---

## 7. The write side: dreams

Recovery is the read side. The write side is the periodic pass where the
agent tidies what it has stored — merge duplicates, split look-alikes, retire
stale entries, re-home new ones, escalate the ones it cannot call. Each move
has a checkable criterion, and nothing is decided alone: doubts go into the
report, not into a silent edit.

The rhythm is a cycle, not a schedule: at least a few days since the last
pass. The output is one page, written for the reader.

Boundary worth keeping: the tidier ships discipline and criteria, never
autonomy over your files. It proposes; a human (or an explicitly authorised
agent) disposes.

---

## 8. Honest reporting

The whole method fails if recovery claims more than it did. Two rules:

- **Name every source.** "Read the rules file, the open items and the log"
  beats "recovered". A source that came up empty is listed as empty.
- **Never invent a number.** Context usage, file sizes, token counts: if the
  platform does not expose it, say the platform does not expose it.

---

## 9. What this does not solve

- **Nothing survives the host.** These scripts live in your repo and read your
  files; if the host injects identity, that injection is the host's business.
- **No semantic search.** Everything here is deterministic and literal —
  a keyword across files. Fuzzy retrieval is a different tool.
- **No automatic capture.** The write side is a discipline, not a background
  daemon. Someone (or some scheduled agent) has to run the pass.
- **The ledger does not judge truth.** It judges freshness, completeness and
  budget. Whether a memory is *correct* is a human call.
