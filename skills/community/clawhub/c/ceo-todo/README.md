# CEO To-Do

A CEO's single source of truth for everything they're on the hook for — one
canonical markdown file, kept current by the Getting Things Done loop, with a
reliability guarantee enforced in code. Distributed as a Claude Skill and a
companion Agent. MIT licensed.

- **Live directory:** https://skillsandagents.co
- **Catalog page:** https://skillsandagents.co/skills/ceo-todo/
- **License:** [MIT](../LICENSE)

## What this is

1. **CEO To-Do (skill)** — the portable, no-connector engine. Point it at one
   markdown file and it becomes the single source of truth for everything the
   CEO is on the hook for. It captures pasted emails / notes / asks, clarifies
   each into a next-action with an owner and a priority, runs the GTD loop over
   the one file, and applies the status transitions
   (`[OPEN]`/`[DONE]`/`[STALE]`/`[WAITING]`). Manual, no MCP required.
2. **CEO To-Do — Daily (agent)** — the automated version. On a daily run it
   sweeps the CEO's Gmail (Claude's native Google Workspace connector) and
   Slack (Claude's native Slack connector) **read-only** for new commitments,
   captures them into the same canonical doc, runs the same transitions, and
   surfaces the day's P0/P1 shortlist. It never sends email, never replies in
   Slack, never takes any write action — capture and draft-for-review only.

Both credit the single-doc format to the system
[Brian Halligan](https://x.com/bhalligan/status/2054689082857730097) (co-founder
of HubSpot) shared publicly.

## The reliability guarantee

The point of this tool is that the CEO can *trust the doc*, so the load-bearing
invariants live in deterministic code, not in model judgment. Every mutating run
is:

1. **fail-closed** — it first confirms the bundled validator can execute in
   Claude's sandbox; if not, it refuses to touch the doc,
2. **snapshot-backed** — the doc is copied to a timestamped backup before any
   write,
3. **append/archive-only** — items move to `## Archive`, never get deleted,
4. **validated before and after the write** — a non-zero validator exit stops
   the write, and
5. **reported** — every run ends with a postcondition report (items in/out,
   archived, IDs added/moved, validator PASS/FAIL).

`references/validate.mjs` is a zero-dependency Node script that asserts every
invariant: no lost items, no duplicate IDs, correct staleness math, no
auto-closed `[user-added]` item, an advancing stamp, and valid line grammar. It
runs in Claude's code-execution sandbox (the same mechanism the built-in
`docx`/`pptx`/`xlsx` skills use for their bundled Python) — the CEO installs the
skill, never a runtime.

## Layout

```
ceo-todo/
├── SKILL.md                       # The portable skill (manual, no MCP)
├── agents/
│   └── ceo-todo-daily.md          # The daily Gmail + Slack agent (read-only)
├── references/
│   ├── sample-todo.md             # A complete, validator-clean canonical doc
│   └── validate.mjs               # The reliability guarantee, in code
└── README.md

evals/ceo-todo/                    # Golden before/after cases + runner (repo-level,
├── run-evals.mjs                  # not shipped with the installed skill)
├── good-clean.md
├── good-dedup.md
├── good-prev-snapshot.md
├── bad-duplicate-id.md
├── bad-dropped-open.md
├── bad-stale-boundary.md
└── bad-user-added-closed.md
```

## Try it

Validate the sample doc (staleness math is pinned to a fixed "today" so the
example is deterministic):

```
cd ceo-todo/references
CEO_TODO_TODAY=2026-07-06 node validate.mjs sample-todo.md
```

Run the golden evals:

```
node evals/ceo-todo/run-evals.mjs
```

Every good fixture exits 0, every bad fixture exits non-zero, and the run
asserts idempotency.

## Usage

Add `SKILL.md` to your Claude project context or system prompt and point it at
your to-do file. For the automated daily version, enable Claude's Google
Workspace (Gmail) and Slack connectors and use the `ceo-todo-daily` agent — see
its runbook on the [catalog page](https://skillsandagents.co/agents/ceo-todo-daily/).
