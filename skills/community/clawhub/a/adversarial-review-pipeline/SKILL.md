---
name: adversarial-review-pipeline
description: "Adversarially review a code change before it ships - a single-agent severity-graded review that works anywhere, an optional three-agent Writer/Breaker/Reviewer pipeline, and an optional five-agent pipeline with a fix loop and browser verification. Use when: reviewing a diff, branch, or PR before merge; checking a feature for bugs, security issues, or unnecessary complexity; asking whether a change is over-engineered or missing edge cases; or setting up a review workflow for a team. Triggers: adversarial review, review this PR, break this change, find problems with this diff, code review, YAGNI check, over-engineering review."
metadata: {"clawdbot":{"emoji":"🛡️","requires":{"bins":[]},"os":["linux","darwin","win32"],"version":"1.0.1"}}
---

# Adversarial Review Pipeline

Review a change the way someone who wants it to fail would. The goal is not to
confirm the work is good - it is to find what is wrong with it before it ships.

Three tiers. **Tier 1 is the default and needs nothing but the agent you
are already talking to.** Tier 2 adds a three-agent pipeline. Tier 3 adds a
fix loop and browser verification.

---

## The core idea

A review that asks "is this good?" produces reassurance. A review that asks
"what would break this?" produces findings. The difference is entirely in the
framing of the request.

**The strongest single technique: hand the reviewer only the artifact, never
the author's reasoning.** A reviewer that sees the author's rationale will
tend to agree with it. A reviewer that sees only the code has to evaluate the
code.

The second strongest: **the artifact is the deliverable, not the completion
message.** See "The artifact rule" below.

---

## Tier 1 — Single-agent review (no dependencies)

This works in any agent session, with no subagents, no second model, no setup.

### 1. Scope the change

Before reviewing anything, list what the change is supposed to reach. If the
change is a diff:

```bash
git diff main...HEAD --stat
git diff main...HEAD --name-only
```

For each changed file, find who depends on it:

```bash
grep -rn "<changed_function_or_constant>" --include="*.<ext>" .
```

**A file you cannot list the callers of is a file you have not reviewed.** An
unreviewed caller is the most common place a "complete" change breaks
something.

Also list what the change makes wrong in the docs:

```bash
grep -rn "<the thing you changed>" README.md AGENTS.md docs/ .agents/ 2>/dev/null
```

**A doc you cannot check is a doc you have not reviewed.** Stale docs make the
wrong thing look right to the next person.

### 2. Read the change adversarially

Read the diff once as if you were trying to break it. For each hunk, ask:

| Question | What it catches |
|---|---|
| What input makes this wrong? | Off-by-one, empty set, nil, zero, negative, huge |
| Who calls this, and with what? | Changed contract, wrong caller assumption |
| What happens if this raises? | Missing error handling, partial state |
| What happens if it runs twice? | Missing idempotency, double charge, duplicate row |
| What happens if two requests race? | Race condition, lost update, double spend |
| What happens when the data is absent? | Nil dereference, missing record |
| Who can reach this, and who should not? | Authorization, IDOR, missing scope |
| What is logged, returned, or rendered? | Sensitive data leaking to logs or UI |
| Is this the smallest thing that does the job? | Scope creep, speculative generality |
| Is there already a helper for this? | Reinvention, two implementations drifting |
| Does any doc still describe the old behavior? | Stale setup, interface, or workflow instructions |

Then run the tests. A failing test is the highest-value finding available to
you, and it is also the cheapest to verify.

### 3. Grade every finding

Use four severities. The grade decides what happens next, so be honest about
the difference between "this is broken" and "I would have written it
differently."

| Severity | Meaning | Action |
|---|---|---|
| `block-merge` | Broken, exploitable, or wrong for real users | Must fix before merge |
| `high` | Correctness or security risk on a reachable path | Fix before merge |
| `medium` | Real issue, but bounded or low-impact | Fix if safe, else defer with a note |
| `low` | Style, naming, taste, or a hypothetical | Defer |

**Do not inflate.** A review where everything is `block-merge` gets ignored.
If a reviewer is unsure between two severities, take the lower one and say why
you are unsure.

### 4. Write the report

The report is the deliverable. Put it in a file:

```markdown
# Review: <short change description>

## Findings

### [block-merge] <one-line title>
**Where:** path/to/file.rb:42
**What:** <the concrete problem>
**Why it matters:** <the user-visible or security consequence>
**Fix:** <the specific change>

## Scope & Skipped

**Verified:**
- <path/behavior you actually checked>

**Not checked:**
- <thing you did not check> — <risk this carries>

## Verdict

ACCEPT / ACCEPT WITH FIXES / BROKEN / REJECT
```

`ACCEPT` means the review is done and the report is ready for the human
decision. `ACCEPT WITH FIXES` applies the listed fixes and then the report is
ready for that decision. `BROKEN` means it needs more work - a Fixer applies
the fixes and the branch goes back through the Breaker and Reviewer. `REJECT`
means it will not be accepted as written; stop and escalate.

No verdict ships anything on its own. Every one ends in a report a human reads
and acts on.

### 5. The Scope & Skipped section is required

A review that silently narrows its own scope reads as full coverage when it
is not. Name what you did **not** look at and what risk each omission
carries.

```markdown
## Scope & Skipped

**Verified:**
- Payment capture path, including the retry branch
- Authorization check on both entry points

**Not checked:**
- Webhook signature verification — the handler is new and unexercised.
  Risk: forged webhooks accepted.
- Concurrent submission behavior — no test exercises two simultaneous
  requests. Risk: duplicate rows under load.
```

This section is often more valuable than the findings list, because it tells
the reader where to look next.

---

## The artifact rule

**The file on disk is the deliverable. The completion message is a pointer.**

An agent can report completion, summarize its findings confidently, and still
have written nothing. This happens most often with subagents, and it can
happen with the agent you are talking to directly.

```bash
ls -la review-<slug>.md    # confirm it exists and is non-trivial
wc -l review-<slug>.md     # a few bytes = the write failed
```

If the file is missing or nearly empty, do not treat the completion message as
proof the work landed. Recover the content from the session transcript before
redoing the work, so you do not lose findings that were already produced.

---

## Tier 2 — Three-agent pipeline (Writer → Breaker → Reviewer)

The classic shape: a Writer implements, a Breaker attacks the result without
ever seeing the Writer's reasoning, and a Reviewer reconciles the artifact
with the findings into a verdict.

```
Writer  ->  Breaker  ->  Reviewer  ->  Human
 (code)     (findings)   (verdict)    (decide)
```

Each role sees a different slice, and that is the point: the Writer sees only
the requirement, the Breaker sees only the artifact, and the Reviewer sees
both. The role contract, the three prompts, and the verdict format are in
`references/three-agent-pipeline.md`.

**The docs are part of the change.** The Writer updates the project docs the
change makes wrong - README.md, AGENTS.md, docs/*, .agents/*, the rulebook
tracker, module lists, architecture notes - whenever the change affects public
interfaces, workflows, or project state. The Breaker checks that they were.
Both sides use the same grep:

```bash
grep -rn "<the thing that changed>" README.md AGENTS.md docs/ .agents/ 2>/dev/null
```

Every hit that still describes the **old** behavior is a finding. A doc
describing behavior the change did **not** touch is not a finding - the point
is accuracy, not coverage.

## Tier 3 — Five-agent pipeline (Writer → Breaker → Fixer → Spec Writer → Live Tester)

The three-agent pipeline plus a fix loop and browser verification - which is
what catches the class of bug that unit tests structurally cannot.

```
Writer -> Breaker -> Fixer -> Spec Writer -> Live Tester
```

Use it for user-facing features with forms, redirects, auth flows, or
multi-step wizards. The Breaker and the Fixer are deliberately separate
agents: a model in adversarial mode is good at finding problems and bad at
writing fixes, and an agent that both finds and fixes will rationalize its
own findings.

**The PR opens only after the docs match the change.** Before creating the PR,
run the same grep. If any hit still describes the old behavior, the docs are
missing - route back to the Fixer to update them, or update them in the main
session if the fix is small and obvious enough that spawning a Fixer would
cost more. Either way the PR does not open until the stale hits are gone.
Do not open a PR with a known-stale doc and note it for later. The role definitions, the Fixer prompt, and the ordering rules
are in `references/five-agent-pipeline.md`.

## The YAGNI & DRY review

Every review - single-agent or not - answers five questions explicitly. They
catch a class of problem functional testing never will, because speculative
code usually *works*.

1. **YAGNI.** Does the change add generality the task does not exercise - extra
   tables, config hooks, extension points, helpers? If the feature does not
   need it today, flag it. Severity `high` when it touches money, state, or
   auth; otherwise `medium`.
2. **DRY.** Is the same logic, concept, or validation duplicated? Severity by
   blast radius: `medium` for isolated duplication, `high` when the duplicated
   logic sits in a money, state, or auth path where the two copies will drift.
3. **Reinvented house component.** Did the change build a new helper when the
   codebase already has one? Name the existing component to use.
4. **Unnecessary dependency or indirection.** Did the change add a package,
   wrapper, or conversion layer that the standard library or a few lines could
   replace? Severity `medium`; name the simpler option.
5. **Worse-is-better.** Did the change prefer a large configurable abstraction
   over a smaller concrete solution? If the abstraction makes the money,
   state, or auth path harder to trace or test, flag `high`.

The full lens, the spec-written-to-match-the-implementation failure mode, and
the money/state checklist are in `references/review-checklists.md`.

## Reporting back

Close the review with what changes the reader's next action - not a narration
of the steps:

1. **What was found** - finding count by severity, and what was fixed.
2. **What was skipped** - and why.
3. **The risk they must know about** - anything deferred that could bite in
   production, and anything still needing a product decision.

Do not restate the review checklist or narrate the agents.

---

## Common pitfalls

- **Reviewing the diff instead of the change.** A diff shows what moved, not
  what depends on it. Grep for callers.
- **Accepting the author's reasoning.** Pass the artifact, not the rationale.
- **Inflating severity.** If everything is `block-merge`, the review gets
  ignored. Grade honestly.
- **Trusting a completion message over the artifact.** Check the file exists.
- **Spawning agents in parallel.** The roles are a dependency chain.
- **Letting the same agent find and fix.** It will rationalize its own
  findings.
- **Fixing the spec instead of the code** when the spec was written to match
  the implementation rather than the requirement.
- **Reviewing only the happy path.** The defects live in the empty state, the
  boundary, the retry, and the unauthorized caller.
- **Omitting Scope & Skipped.** Then a narrow review reads as a broad one.
- **Running the multi-agent pipeline on a trivial change.** The coordination
  cost exceeds the value.

## Completion check

- [ ] The change's scope and its callers were listed before reviewing.
- [ ] Every finding has a severity, a location, and a concrete consequence.
- [ ] The YAGNI & DRY questions were answered explicitly.
- [ ] The report exists on disk and is non-trivial.
- [ ] A `## Scope & Skipped` section names what was not checked and the risk.
- [ ] Any test that passed by working around a constraint was probed against
      the real request shape.
- [ ] Money/state checks were run if the change touches money, state, or
      webhooks.
- [ ] A verdict was given: ACCEPT, ACCEPT WITH FIXES, BROKEN, or REJECT.
- [ ] A `BROKEN` verdict went back through the Breaker and Reviewer rather
      than being escalated or abandoned.
- [ ] The project docs were updated to match the change - no doc still
      describes the old behavior.

## Related

- `references/rails-turbo-and-controller-traps.md` - the places a Rails
  framework does something different from what the code looks like it does
- `references/rails-system-spec-review.md` - writing Rails system specs from
  the user's perspective, and the journeys worth walking
- `references/rails-money-and-state-checks.md` - Rails-specific money and state
  checks
- `references/rails-review-checks.md` - the commands a Rails review runs
- `references/three-agent-pipeline.md` - Writer / Breaker / Reviewer prompts
  and the role contract
- `references/five-agent-pipeline.md` - the Fixer, Spec Writer, and Live
  Tester roles
- `references/review-checklists.md` - YAGNI & DRY, the spec-written-to-match-
  the-implementation failure, and the money/state checks
- `rails-tdd-standards` - RSpec standards this review depends on
- `rails-ci-fixer` - CI-only failure patterns for a Rails change
