---
name: backlog-planner
description: Turn a feature idea, conversation context, or rough notes into researched, detailed, dependency-ordered checkbox tasks appended to the project's roadmap/backlog file — exactly the format goal-runner consumes, so a fresh unattended session can execute them. Grounds every task in the actual codebase before writing it (grep/read or Explore scouts; think-like-fable rigor if installed), puts what + done-when on the checkbox line with verified files, acceptance criteria, and a verification command in plain sub-bullets, and labels assumptions. Appends to the existing ROADMAP.md/BACKLOG.md/TODO.md; when none exists it asks once and defaults to ROADMAP.md. Use this skill whenever the user says "add this to the backlog", "add it to the roadmap", "plan these tasks", "break this down into tasks", "capture this as roadmap tasks", "turn these notes into a task list", or "/backlog-planner" — even if they don't name the skill. Not for executing tasks (goal-runner, task-executor, autopilot) — this writes the plan only.
---

# Backlog Planner

The intake side of `goal-runner`: take an idea, a conversation, or rough notes, **research them against the real codebase**, and turn them into detailed, self-contained checkbox tasks in the roadmap/backlog file. The quality bar: a fresh session with zero memory of this conversation could execute any task from its text alone.

## When to use this skill

- "add this to the backlog" / "add it to the roadmap"
- "plan these tasks" / "break this down into tasks"
- "capture this as roadmap tasks" / "turn these notes into a task list"
- "/backlog-planner"

Do **not** auto-trigger when the user wants tasks *executed* (`goal-runner`, `task-executor`, `autopilot`) or wants a full interactive feature design session — this skill plans the backlog, then stops.

## The target file

1. Glob the repo root for `ROADMAP.md`, `roadmap.md`, `BACKLOG.md`, `backlog.md`, `TODO.md`, `todo.md`.
2. **Exactly one exists** → append to it, matching its existing heading/section structure.
3. **Multiple exist** → ask once which one is the live backlog.
4. **None exist** → ask once (`AskUserQuestion`): **ROADMAP.md (Recommended)** — `goal-runner`'s auto-discovery finds it without naming it in the goal text — vs. BACKLOG.md vs. TODO.md. Running unattended with no way to ask → create `ROADMAP.md` and log the choice as an assumption in the report.

## Research before writing — this is most of the work

Apply the `think-like-fable` skill if installed; either way these rules hold:

1. **Read the need behind the words.** Restate in one line: "this backlog needs `___` so that `___`". If the second blank won't fill, ask — a backlog built on a guessed goal is detailed garbage.
2. **Every name is a claim.** A task that names a file, module, endpoint, or pattern asserts it exists — grep or open it first, or don't name it. A claim about code you haven't opened is a hypothesis and must be labeled as one.
   - ❌ `- [ ] Add caching to UserService.getProfile()` — written from the conversation; no `UserService` exists in this repo.
   - ✅ Grep first → `- [ ] Add response caching to profile lookup in src/services/profile.ts:42 (getProfile)` — or, if nothing matched, a task that says "locate the profile lookup path" instead of naming one.
3. **Scale the scout to the scope.** Touches ≤2 files you can open inline → read them directly. Spans 3+ areas or an unfamiliar layer → fan out parallel `Explore` sub-agents, one question each, `file:line`-cited findings only. "Looked for and did not find" is a finding.
4. **Front-load the riskiest unknown.** Ask: what discovery would invalidate this whole plan? Resolve it during research if cheap; otherwise make it task #1 as an explicit spike whose done-when is the answer.
5. **Scope check first.** If the source material spans multiple independent subsystems ("chat + billing + analytics"), don't refine details of a thing that needs decomposing — split it into one section per subsystem, each of which produces working, testable software on its own, and plan the first one fully before the rest.
6. **Attack the list before writing it.** Walk each drafted task asking: "a fresh session executes exactly this text — what goes wrong?" Missing context, unstated dependency, unverifiable done-when → fix the task, then append. Then run three specific scans:
   - **Coverage:** every requirement in the source material points to a task; every task points back to a requirement (no invented work).
   - **Placeholders:** none of "TBD", "add appropriate error handling", "handle edge cases", "write tests for the above", "similar to task N" — each is a plan failure; replace with the actual content (the specific error case, the specific test name, the repeated detail).
   - **Name consistency across tasks:** a function called `clearLayers()` in task 3 and `clearFullLayers()` in task 7 is a bug the executor will discover the hard way. Same identifiers, same signatures, same paths everywhere.

## The task contract

- **One `- [ ]` line per task: what + done-when.** Never nest checkboxes — every `- [ ]` line is a separate queue item to `goal-runner`, so a checkbox sub-bullet becomes a phantom task.
- **Detail lives in indented plain bullets** under the line (goal-runner's coder receives the task with its sub-bullets): why/context, verified files or entry points, acceptance criteria, the verification command, and `Assumes:` for anything unconfirmed.
- **Interfaces between tasks are written down, not implied.** Each task's executor sees only that task. When task B consumes something task A produces, both carry it explicitly: A gets `Produces: <exact function/type/endpoint name, params, return>`, B gets `Consumes: <the same, verbatim>`. Exact names and signatures, not "the helper from the previous task".
- **Global constraints go once, at the top of the appended block** when the source material has project-wide requirements (version floors, naming rules, "never call the DB from the controller", platform targets) — one line each, values verbatim. Every task implicitly inherits them; the goal-runner coordinator copies this block into each coder brief.
- **Self-contained.** No "the bug we discussed", no "as agreed above" — the executor never saw this conversation.
- **PR-sized.** One coder, one sitting, one commit. Two unrelated deliverables joined by "and" → split into two tasks. Two halves that can't be verified separately → merge into one.
- **Dependency-ordered, append-only.** goal-runner works top to bottom: order new tasks so no task depends on a later one; append after existing unchecked tasks; never reorder or reword existing lines (a run may be mid-file). Insert earlier only if the user explicitly says the new work takes priority.

❌ Vague line, detail nowhere:

```markdown
- [ ] Improve webhook handling
```

✅ Detailed line + grounded sub-bullets:

```markdown
- [ ] Add HMAC signature validation to POST /api/webhooks — done when an invalid signature returns 401 and a valid payload still enqueues (both covered by integration tests)
  - Entry point: src/routes/webhooks.ts:18 (handler currently trusts the payload)
  - Follow the existing middleware pattern in src/middleware/auth.ts
  - Secret comes from env WEBHOOK_SECRET; add to .env.example
  - Verify: npm test -- webhooks
  - Produces: `verifyWebhookSignature(rawBody: Buffer, header: string): boolean` in src/middleware/webhookAuth.ts
  - Assumes: single shared secret is acceptable (no per-tenant secrets found in schema)
```

## Workflow

1. **Restate the goal** ("this backlog needs `___` so that `___`") and inventory the source material (idea, notes, conversation decisions). If `.claude/design-briefs/` holds an `APPROVED` brief for this feature, it is the primary source: its Interfaces become the tasks' `Produces:`/`Consumes:` lines verbatim and its Constraints become the global-constraints block.
2. **Locate the target file** per [The target file](#the-target-file).
3. **Research** per the rules above — ground every name, chase the riskiest unknown.
4. **Draft the tasks** to the contract; order by dependency.
5. **Self-attack** each task with the fresh-session test; fix what fails it.
6. **Append.** Match the file's existing structure; never rewrite, reorder, or tick existing lines.
7. **Report**: quote the appended block verbatim, list assumptions made, and note the ready next step (`/goal "work on the roadmap tasks til completion..."`).

## Examples

### Example 1: from a conversation

**User:** "Great discussion — add all that to the roadmap."

**Claude:** restates the goal, finds `ROADMAP.md`, greps the three modules the discussion named (one doesn't exist → rewrites that task as a locate-first spike), appends 4 dependency-ordered tasks each with entry points, done-when, verify command, and one `Assumes:` line, then quotes the appended block and the assumption.

### Example 2: no backlog file yet

**User:** "Break this feature idea into tasks for later."

**Claude:** globs and finds no roadmap/backlog file → asks once (ROADMAP.md recommended, BACKLOG.md, TODO.md) → creates the chosen file with a `## Backlog` section, researches the idea against the codebase, appends the tasks.

## Anti-patterns

- ❌ Writing tasks straight from the conversation without opening the code — every unverified name ships a landmine to the executor.
- ❌ Padding: the notes contain two tasks' worth of work, but five look more thorough. Two detailed tasks is a valid outcome; so is one.
- ❌ Inventing requirements the source material never stated — scope creep at planning time is still scope creep.
- ❌ Mega-tasks ("build the whole notification system") or confetti-tasks ("create the file", "add the import") — size to one PR.
- ❌ Nested `- [ ]` sub-bullets under a task — goal-runner will execute them as separate queue items.
- ❌ Reordering or rewording existing tasks while appending — a `/goal` run may be mid-file; append-only.
- ❌ Ticking any box or executing any task — this skill writes the plan and stops.
- ✅ Researched, self-contained, PR-sized tasks with done-when on the line and grounded detail beneath — appended, quoted back, assumptions labeled.

## Notes

- Composes with: `goal-runner` (consumes the file), `think-like-fable` (research rigor), and `task-executor` (when the user wants to execute now instead of banking tasks). An idea that still needs a design conversation goes to `design-brief` first if installed — otherwise hold it here (goal, constraints, boundaries, interfaces) before any task is written.
- `ROADMAP.md` is the default because `goal-runner` auto-discovers `ROADMAP.md`/`TODO.md`; a `BACKLOG.md` works too but must be named explicitly in the `/goal` text.
- The format is deliberately generic — any human or agent that reads GitHub-flavored checkbox lists can work the file; nothing in it is goal-runner-specific.
