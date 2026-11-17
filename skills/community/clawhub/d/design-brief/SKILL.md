---
name: design-brief
description: Turn a vague feature idea into an approved design brief — a file recording the intent, every decision made (with why and cost-if-wrong), scope boundaries, exact interfaces, and constraints — that task-executor, backlog-planner, and autopilot then consume as the spec. Produces decisions, not code; nothing is implemented. Use this skill whenever the user says "brainstorm this", "let's design this first", "think through this feature with me", "spec this out", "I have an idea for", "how should we build", "before we plan this", or "/design-brief" — even if they don't name the skill. Not for a task that already has a clear spec (task-executor), a bug (diagnose), or turning a decided design into tasks (backlog-planner).
---

# Design Brief

Turn "I have an idea" into a design the team has actually agreed on, written down where the executing skills can read it. The brief records **decisions**, not ideas — a brainstorm that ends without decisions has produced nothing an executor can use. This skill never writes code.

## When to use this skill

- "brainstorm this", "let's design this first", "think through this feature with me"
- "spec this out", "I have an idea for …", "how should we build …", "before we plan this"
- `/design-brief`
- `task-executor` classified a task as **architectural**, or `backlog-planner` found the idea undecided — both route here.

Do **not** auto-trigger when the task already has a clear spec (`task-executor`), something is broken (`diagnose`), the friction is in existing code rather than a new feature (`improve-codebase-architecture`), or the design is decided and only needs splitting into tasks (`backlog-planner`).

## The brief contract

Path: `.claude/design-briefs/<slug>.md` in the project root (create the directory if missing; slug = 2–5 kebab-case words naming the feature). Every brief has these sections, in this order, none omitted — an empty section says `none` and why:

1. **Status** — `DRAFT` or `APPROVED <date>`. Only the user's explicit approval flips it.
2. **Intent** — one line: "this needs `___` so that `___`", plus how we'll know it worked (an observable signal, not "users are happier").
3. **Decisions** — table: question → decision → why → cost if wrong. Every fork the interview resolved is a row. A decision without a *why* is a preference, not a decision.
4. **Scope** — in / out, as two lists. "Out" is where the ideas that didn't make the cut live, so they're not lost and not built.
5. **Interfaces** — exact names, signatures, endpoints, tables, events the new work exposes or consumes. `Produces:` / `Consumes:` lines, verbatim-ready for `backlog-planner`.
6. **Constraints** — project-wide rules that bind every task (version floors, layering rules, platform targets), one line each, values verbatim.
7. **Precedent** — the existing feature this one follows, with `file:line`, or "no precedent found — searched `<paths>` for `<terms>`".
8. **Considered alternative** — present when Design It Twice ran: `<approach B>` — rejected because `<one line>`.
9. **Open questions** — must be empty before `APPROVED`. An approved brief with open questions is a draft wearing a badge.

## Workflow

Before each phase, restate the intent line. If the phase isn't serving it, stop and say so.

### Phase 0 — Anchor

- List `.claude/design-briefs/` and read the Status and Intent line of every file there. One matches this subject → resume it (list its open questions, continue from there); never start a duplicate under a new slug.
- Read `CONTEXT.md` / `CONTEXT-MAP.md` if present — its terms are canonical; a conflict between the user's words and the glossary is the first thing to resolve.
- Write the intent line. Can't fill the "so that" blank from what the user said → that is question #1.

### Phase 1 — Read the code before asking

Find the nearest thing that already exists — a sibling feature, entity, endpoint, or screen — and read it end to end. Every answer the code gives is recorded with a `file:line` citation instead of asked. A claim about code you haven't opened is a hypothesis and is labeled one.

- ❌ "How do you usually handle authorization on endpoints?" — the answer is in `src/middleware/auth.ts`; asking wastes a turn and invites a wrong answer.
- ✅ "Endpoints here check `requireRole()` in the route file (`src/routes/orders.ts:14`). I'll assume the same unless this one is different — is it?"

### Phase 2 — Interview

One question at a time via `AskUserQuestion`, 2–4 concrete options, recommended pick first. Wait for the answer before the next question.

**A question earns its slot only if different answers lead to different designs.** Before asking, name to yourself what changes per answer. Nothing changes → don't ask.

- ❌ "Should this be secure and handle errors gracefully?" — every answer is "yes"; nothing forks.
- ✅ "When an order loses priority, do we keep who set it and when?" — "yes" is an audit table, "no" is two columns. The answer picks the schema.

Rules:

- **Sharpen fuzzy words.** "Account" → customer or user? "Cancel" → soft-delete, hard-delete, or status transition?
- **Probe with scenarios.** "What happens if they submit twice while the first request is in flight?" Edge cases force precision.
- **Surface contradictions with the code.** "Your `OrderService.Cancel` cancels the whole order (`src/services/order.ts:88`); you just described partial cancellation. Which wins?"
- **Record each answer as a Decisions row immediately** — with the *why* the user gave. Ask for the why if they didn't give one.

Topics to cover, skipping any the code or the user already answered: intent · inputs/outputs and error cases · domain entities touched (new vs. extended) · authorization and tenancy · persistence and backfill · side effects (email, queue, audit, cache, webhooks) · concurrency and idempotency · edge cases (empty, max, unicode, timezone, partial failure) · observability.

**Exit gate:** every topic is answered by the user, answered by code with a citation, or explicitly deferred by the user into Open questions. Stop the moment further questions stop changing the design.

### Phase 3 — Design fork gate

Ask: **is there a genuine design choice the codebase precedent doesn't already settle?** Name the axis in one sentence ("new `OrderAuditLog` table vs. two columns on `Orders`"). Can't name it cleanly → no fork → single design, move on. Don't manufacture a fork for ceremony.

**Design It Twice (only when the axis is named):**

1. Send a **single message** with 2 `Agent` calls (`general-purpose`), each carrying the Decisions table, Phase 1 precedent findings, the axis, and **one** side to defend: "Draft the best design for your side: files by layer, interfaces, migration if any, test plan by test name, and why it beats the alternative *on this codebase* — cite `file:line`. ≤700 words. Do not write files." If `Agent` is unavailable, draft both yourself under the same instructions.
2. **Debate inline:** 3 things A does better · 3 things B does better · the recommendation in one paragraph, naming the Phase 1/2 evidence that broke the tie.
3. The winner becomes the brief; the loser becomes the Considered alternative line.

### Phase 4 — Write, present, approve

1. Write the brief as `DRAFT` with every section filled.
2. Present a condensed summary inline (intent, decision count, interfaces, alternative if any, open questions) and ask: approve, change, or drop?
3. **Approve** → set `APPROVED <date>`, report the path, and name the next step: one PR-sized change → `task-executor` with the brief as its spec; several tasks → `backlog-planner` reads the brief and writes the roadmap tasks. **Change** → back to the phase the change belongs to; re-present. **Drop** → keep the file as `DRAFT` with `Dropped: <reason>` under Status — the decisions stay findable. Never edit an `APPROVED` brief silently — a change after approval is a new `DRAFT` revision with the old decision struck through and the new one dated.

**A brief-less outcome is valid.** If Phase 1–2 show the idea is one change to an existing flow with no fork and no new interface, say so and hand straight to `task-executor` — the interview *was* the spec.

## Examples

### Example 1: Undecided feature

**User:** "I have an idea — let users pin orders to the top of their list."

**Claude:** Reads the existing list endpoint and sort logic (`src/routes/orders.ts:31`), finds no priority concept. Asks whether pinning is per-user or per-order, then whether pin history matters (audit table vs. one column). Names the fork, runs Design It Twice, recommends the single column citing the codebase's other per-user flags. Writes `.claude/design-briefs/pin-orders.md`, presents the summary, user approves → suggests `backlog-planner` for the three resulting tasks.

### Example 2: Routed in from task-executor

**User:** "Work on task: move notifications to a queue."

**Claude (in task-executor):** classifies as architectural → hands here. This skill anchors on the intent, interviews on delivery guarantees, retry, and ordering, writes the brief, gets approval, then task-executor resumes with the brief as its spec.

## Anti-patterns

- ❌ Asking the checklist top to bottom regardless of answers — a question whose answer changes nothing is filler.
- ❌ Asking what the code already answers — read the precedent first, cite it, confirm only the deviation.
- ❌ Ending with a list of ideas and no Decisions rows — that's a brainstorm transcript, not a brief; nothing downstream can execute it.
- ❌ Marking `APPROVED` because the user said "sounds good" to the summary while Open questions is non-empty.
- ❌ Writing code, a migration, or "a quick prototype to check feasibility" — feasibility is a `task-executor` spike; this skill ends at the approved file.
- ❌ Running Design It Twice on a choice the codebase already made — one precedent slice beats two sub-agent essays.
- ✅ Code read first, forking questions only, decisions with their why, exact interfaces, one approved file, then hand off.

## Notes

- Composes with: `task-executor` (consumes the brief as its spec; routes architectural tasks here), `backlog-planner` (turns an approved brief into roadmap tasks), `autopilot` (consumes an `APPROVED` brief as its spec; an architectural task without one is a hard stop there — the brief is the route back), `think-like-fable` (interview rigor).
- Briefs are project-scoped and should be git-ignored or committed deliberately — an approved brief committed next to the code is a lightweight ADR.
