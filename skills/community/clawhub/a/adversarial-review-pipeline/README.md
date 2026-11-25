# 🛡️ Adversarial Review Pipeline

[![ClawHub Skill](https://img.shields.io/badge/ClawHub-Skill-blue)](https://clawhub.ai/djc00p/skills/adversarial-review-pipeline) [![Agent Skill](https://img.shields.io/badge/Agent-Skill-blue)](#) [![Language Agnostic](https://img.shields.io/badge/Core-Language_Agnostic-4285F4.svg)](#) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Adversarial review** reads a change the way someone who wants it to fail would. The goal is not to confirm the work is good — it is to find what is wrong with it *before* it ships.

A review that asks *"is this good?"* produces reassurance. A review that asks *"what would break this?"* produces findings. The entire difference is in the framing of the request.

**Three tiers.** Tier 1 runs in any agent session with zero dependencies. Tier 2 adds a three-agent pipeline. Tier 3 adds a fix loop and browser verification.

---

## 🚀 Quick Start

**Tier 1 — single agent, no setup:**

```
Review this branch adversarially before I open the PR. Grade findings
block-merge / high / medium / low, and write the report to review-<slug>.md.
```

**Tier 2 — three agents** (Writer → Breaker → Reviewer):

```
Run the adversarial review pipeline on this change: a Writer implements,
a Breaker attacks the result without seeing the Writer's reasoning, and a
Reviewer reconciles artifact and findings into a verdict.
```

**Tier 3 — five agents** (adds Fixer, Spec Writer, Live Tester) for
user-facing features with forms, redirects, auth flows, or wizards.

---

## 🎯 The Core Idea

Two techniques do most of the work:

**Hand the reviewer only the artifact, never the author's reasoning.** A reviewer that sees the rationale will tend to agree with it. A reviewer that sees only the code has to evaluate the code.

**The artifact is the deliverable, not the completion message.** An agent can report completion confidently and still have written nothing. Verify the file exists and is non-trivial:

```bash
ls -la review-<slug>.md
wc -l review-<slug>.md     # a few bytes = the write failed
```

---

## 🔍 Tier 1 — Single-Agent Review

### 1. Scope the change

Before reviewing anything, list what the change is supposed to reach.

```bash
git diff main...HEAD --stat
git diff main...HEAD --name-only
```

For each changed file, find who depends on it:

```bash
grep -rn "<changed_function_or_constant>" --include="*.<ext>" .
```

> **A file you cannot list the callers of is a file you have not reviewed.** An unreviewed caller is the most common place a "complete" change breaks something.

Also list what the change makes wrong in the docs:

```bash
grep -rn "<the thing you changed>" README.md AGENTS.md docs/ .agents/ 2>/dev/null
```

> **A doc you cannot check is a doc you have not reviewed.** Stale docs make the wrong thing look right to the next person.

### 2. Read the change adversarially

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

Then run the tests. A failing test is the highest-value finding available, and it is also the cheapest to verify.

### 3. Grade every finding

| Severity | Meaning | Action |
|---|---|---|
| `block-merge` | Broken, exploitable, or wrong for real users | Must fix before merge |
| `high` | Correctness or security risk on a reachable path | Fix before merge |
| `medium` | Real issue, but bounded or low-impact | Fix if safe, else defer with a note |
| `low` | Style, naming, taste, or a hypothetical | Defer |

**Do not inflate.** A review where everything is `block-merge` gets ignored. If you are unsure between two severities, take the lower one and say why.

---

## 📋 Output Format

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

### `## Scope & Skipped` is required

A review that silently narrows its own scope reads as full coverage when it is not. Name what you did **not** look at and the risk each omission carries. This section is often more valuable than the findings list — it tells the reader where to look next.

---

## 🤖 Tier 2 — Three-Agent Pipeline

```
Writer  ->  Breaker  ->  Reviewer  ->  Human
 (code)     (findings)   (verdict)    (decide)
```

Each role sees a different slice, and that is the point: the Writer sees only the requirement, the Breaker sees only the artifact, the Reviewer sees both.

> **Why the Breaker must not see the Writer's reasoning:** a reviewer that sees the rationale tends to agree with it. Isolation is the mechanism, not a formality.

### The docs are part of the change

**The Writer owns the project docs the change makes wrong, and the Breaker
checks them.** A branch that changes how the project works and leaves the docs
describing the old behavior is an incomplete branch - and it is the kind of
incompleteness that survives review, because a reader of the diff sees code,
not the doc that contradicts it.

Update these whenever the change affects public interfaces, workflows, or
project state:

- `README.md`
- `AGENTS.md`
- `docs/*`
- `.agents/*`
- the rulebook tracker
- module lists
- architecture notes

The check is the same on both sides:

```bash
grep -rn "<the thing that changed>" README.md AGENTS.md docs/ .agents/ 2>/dev/null
```

Every hit that still describes the **old** behavior is a finding. A doc
describing behavior the change did **not** touch is not a finding - the point
is accuracy, not coverage.

### The verdict decides the next step

| Verdict | What happens next | Interrupts the pipeline? |
|---|---|---|
| `ACCEPT` | the review is done and the report is ready for the human decision | no |
| `ACCEPT WITH FIXES` | apply the listed fixes, then the report is ready for the human decision | no |
| `BROKEN` | a Fixer applies all the fixes, then the branch goes back through the Breaker and Reviewer | no |
| `REJECT` | stop and report why | **yes** |

**No verdict ships anything on its own.** Every one ends in a report a human
reads and acts on - the Reviewer recommends, a human decides. The verdicts
differ only in how much more work happens before that report arrives.

**`BROKEN` is a loop, `REJECT` is a stop.** A branch that comes back `BROKEN`
is normal pipeline traffic - the Fixer addresses it and the branch re-enters
at the Breaker. Those fix-and-recheck rounds happen on their own so the
person reading the final report is looking at the best version of the change
rather than the first draft of it. The shipping decision stays with the
human; the pipeline does not make it. Only `REJECT` interrupts the person
running the pipeline.

Role contract, prompts, and verdict format: `references/three-agent-pipeline.md`

---

## 🔧 Tier 3 — Five-Agent Pipeline

```
Writer -> Breaker -> Fixer -> Spec Writer -> Live Tester
```

The three-agent pipeline plus a fix loop and browser verification — which is what catches the class of bug that unit tests structurally cannot.

> **Why the Breaker and the Fixer are separate agents:** a model in adversarial mode is good at finding problems and bad at writing fixes. An agent that both finds and fixes will rationalize its own findings.

**Open the PR only after `ACCEPT`.** A PR is a claim the work is complete. A branch carrying unresolved Breaker findings, unapplied Fixer work, or a `BROKEN` verdict does not support that claim - and CI would run against code that is about to change. Opening the PR is not the decision to ship; it makes the reviewed work visible for a human to review and merge.

Role definitions, the Fixer prompt, and the ordering rules: `references/five-agent-pipeline.md`

---

## 🧹 The YAGNI & DRY Lens

Every review answers five questions explicitly. They catch a class of problem functional testing never will, because speculative code usually *works*.

1. **YAGNI** — generality the task does not exercise: extra tables, config hooks, extension points, helpers.
2. **DRY** — the same logic, concept, or validation duplicated. Severity by blast radius.
3. **Reinvented house component** — did the change build a new helper when the codebase already has one? Name the existing component.
4. **Unnecessary dependency or indirection** — a package, wrapper, or conversion layer the standard library or a few lines could replace.
5. **Worse-is-better** — a large configurable abstraction over a smaller concrete solution, especially on a money, state, or auth path.

> **Severity escalates by path.** YAGNI and DRY are `medium` in isolation and `high` when the affected code sits in a money, state, or auth path where two copies will drift.

Also covers the **spec-written-to-match-the-implementation** failure mode — when the test passes but only because it was written against the code rather than the requirement.

Full lens and the money/state checklist: `references/review-checklists.md`

---

## 🚨 Common Pitfalls

| Pitfall | Why it hurts |
|---|---|
| Reviewing the diff instead of the change | A diff shows what moved, not what depends on it |
| Accepting the author's reasoning | Pass the artifact, not the rationale |
| Inflating severity | If everything is `block-merge`, the review gets ignored |
| Trusting a completion message over the artifact | The write may have silently failed |
| Spawning agents in parallel | The roles are a dependency chain |
| Letting the same agent find and fix | It will rationalize its own findings |
| Treating `BROKEN` as a stop | `BROKEN` is a loop back through the Breaker, not an escalation |
| Opening a PR before `ACCEPT` | CI runs against a diff that is about to change |
| Fixing the spec instead of the code | When the spec was written to match the implementation |
| Reviewing only the happy path | Defects live in the empty state, boundary, retry, and unauthorized caller |
| Omitting `Scope & Skipped` | A narrow review then reads as a broad one |
| Shipping code with stale docs | The next person reads the wrong thing and trusts it |
| Running the multi-agent pipeline on a trivial change | Coordination cost exceeds the value |

---

## 📚 References

**Pipeline**

* `references/three-agent-pipeline.md` — Writer / Breaker / Reviewer prompts and the role contract
* `references/five-agent-pipeline.md` — the Fixer, Spec Writer, and Live Tester roles

**Review lens**

* `references/review-checklists.md` — YAGNI & DRY, the spec-written-to-match-the-implementation failure, and the money/state checks

**Rails-specific**

* `references/rails-turbo-and-controller-traps.md` — where a Rails framework does something different from what the code looks like it does
* `references/rails-system-spec-review.md` — writing system specs from the user's perspective, and the journeys worth walking
* `references/rails-money-and-state-checks.md` — Rails-specific money and state checks
* `references/rails-review-checks.md` — the commands a Rails review runs

The core is language-agnostic. The Rails material is isolated in Rails-specific references so it can be skipped entirely.

---

## 📦 Install

```bash
clawhub install adversarial-review-pipeline
```

Or clone this repo and add the skill folder to your agent's skills path.

### Repository layout

```
SKILL.md                                  # agent instructions
references/
  three-agent-pipeline.md                 # Tier 2 roles and prompts
  five-agent-pipeline.md                  # Tier 3 roles and prompts
  review-checklists.md                    # YAGNI & DRY, spec failure mode
  rails-turbo-and-controller-traps.md     # Rails: Turbo and controller behavior
  rails-system-spec-review.md             # Rails: system spec review
  rails-money-and-state-checks.md         # Rails: money and state checks
  rails-review-checks.md                  # Rails: review commands
skill-card.md                             # registry skill card
LICENSE                                   # MIT-0 / MIT
README.md                                 # this file
```

### Versions

Releases track the published ClawHub versions.

| Version | ClawHub |
| --- | --- |
| 1.0.4 | [adversarial-review-pipeline v1.0.4](https://clawhub.ai/djc00p/skills/adversarial-review-pipeline) — adds the `BROKEN` verdict; titles match the slug |
| 1.0.3 | [adversarial-review-pipeline v1.0.3](https://clawhub.ai/djc00p/skills/adversarial-review-pipeline) |
| 1.0.1 | [adversarial-review-pipeline v1.0.1](https://clawhub.ai/djc00p/skills/adversarial-review-pipeline) |

---

**Published by [@djc00p](https://github.com/djc00p)**
