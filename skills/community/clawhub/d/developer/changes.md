# Making the Change

Scope: from "I know where it goes" to a diff that is reviewable, revertible, and provably does what it claims.

**Before starting**, read `## Open Threads` in `~/Clawic/data/developer/memory.md` — a half-finished migration or a PR waiting on review in the same area changes what you should touch — and the `## Conventions` section of that repo's profile. Matching the repo beats being right (SKILL.md Rule 3).

## The Loop

1. **State the change in one sentence** including its observable effect: "orders over 1,000 get the volume discount". If the sentence needs an "and", it is two changes.
2. **Name the verification before writing code**: the test that will fail now and pass after, or the exact command whose output changes. `workflow: tdd` writes it first; `test-after` writes it in the same commit; either way it exists before the change is called done.
3. **Make the change easy** — the preparatory refactor, behavior-preserving, its own commit, tests unchanged and still green.
4. **Make the easy change** — the behavior, its own commit, with the test that proves it.
5. **Clean up** — dead code, the flag scaffold, the comment that is now wrong. Third commit.
6. **Re-read your own diff** as a reviewer, before anyone else sees it (`reviews.md`).

Steps 3 and 5 are optional; step 4 alone in a commit never is. Mixing them is Rule 4, and it is the single change to this loop that costs the most later.

## Splitting a Change That Grew

When the diff crosses `max_pr_lines`, split along one of these seams — in this order of preference, because each one keeps the pieces independently mergeable:

| Seam | Looks like | Merge order |
|---|---|---|
| Preparatory refactor | Extract, rename, move — no behavior change, no test change | First, alone, merges any day |
| Interface before implementation | Add the new function/endpoint unused, then switch callers | Additive first; the switch is a small diff |
| Flag | Whole feature behind a default-off flag, merged in pieces | Any order; the flag is the seam (`shipping.md`) |
| Data before code | Expand the schema, then the code that uses it | Always data first (`migrations.md`) |
| Mechanical vs judgment | 900 lines of codemod in one PR, 40 lines of decision in another | Mechanical first, reviewed by sampling |
| Vertical slice | One entity or one endpoint end to end, repeated | Whichever is riskiest first, to learn early |

Never split by layer — "all the backend in PR 1, all the frontend in PR 2" produces two PRs that cannot be reviewed or reverted independently, which is the opposite of the point.

## Change in Code You Did Not Write

1. **Pin the current behavior first.** Write a test that asserts what it does today, bug included. If you cannot get a test around it, you cannot know your change was surgical — that is a characterization test, and the seam-finding technique lives in `legacy-code`.
2. **Change the smallest thing that could work.** The urge to restructure while you are there is the urge that makes the diff unreviewable.
3. **Watch what else calls it.** Grep for every caller before changing a signature or a return shape; static analysis misses dynamic dispatch, reflection, string-keyed lookups, and other services.
4. **Assume the weird thing is load-bearing** until the git log says otherwise (`codebase.md`).

## Commits That Survive Contact With a Bisect

- One logical change per commit; the repo must build and test green at every commit, or `git bisect` returns noise (`bugs.md`).
- Subject line says what changes in the imperative, under ~72 characters; the body says **why** — the diff already says what. Shape governed by `commit_style`.
- The body is where the rejected alternative goes when it is small. When it is not small, it is an ADR in `artifacts/`.
- A commit that says "fix" or "wip" is a commit whose reason is now unrecoverable. Amend or squash before pushing (`git`).

## Deciding Between Two Implementations

Ask, in this order, and stop at the first that separates them:

1. **Which one is reversible?** (SKILL.md Reversibility) A worse decision you can undo in an afternoon beats a better one you cannot.
2. **Which one does the reader understand without you?** Cleverness is a loan against future debugging time, taken at 3am.
3. **Which one matches what this repo already does?** Consistency compounds; local optimality does not.
4. **Which one has fewer states?** Fewer nullable fields, fewer flags, fewer orderings — the count of reachable states is the honest complexity metric.
5. **Which one fails loudly?** A wrong result that throws is a bug report; a wrong result that returns is a data corruption ticket in six months (`error-handling`).

Only then, performance — and only with a measurement (SKILL.md Rule 7).

## Definition of Done

Beyond "it works": tests for the new behavior and for the boundary it touches, the error path handled rather than swallowed, logs at the level someone debugging would want, docs or comments where the *why* is not obvious, the flag or rollback named (SKILL.md Rule 9), and the ticket updated in `tracker`. Anything from that list you skipped, say which and why — a silent skip becomes someone else's surprise.

## Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| "I'll split it before opening the PR" | By then the commits are interleaved and splitting means re-doing the work | Split as you go: refactor commit first, always |
| Adding an abstraction on the second occurrence | Two cases do not reveal the axis of variation; the abstraction fits neither | Wait for the third, and check they change for the same reason |
| Renaming things while fixing behavior | The reviewer cannot see the one line that matters | Rename in a separate commit, ideally a separate PR (Rule 4) |
| Leaving the old path "just in case" | Dead code is read, maintained, and eventually called by accident | Delete it; the history keeps it (`tech-debt`) |
| A TODO with no ticket and no name | Never done, and it makes the next reader think it is tracked | Ticket, or delete it |
| Committing commented-out code | Version control already remembers; the comment just rots | Delete |
| Fixing the same class of bug once | The next instance ships next week | Grep the codebase for the pattern; fix the class or record it in `## Gotchas` of the repo profile |

## Write Down What Came Out Of It

- A decision with a rejected alternative → `~/Clawic/data/developer/artifacts/adr-<topic>.md`, plus its one-line summary in `~/Clawic/data/projects/<project>.md` if the work is tracked as a project, and its `## Boxes` line in the same turn (`memory-template.md`).
- A convention or trap you learned about this codebase → `## Conventions` or `## Gotchas` in `repos/<repo>.md`.
- Anything left half-done, blocked, or waiting on review → `## Open Threads` in `memory.md`, deleted the turn it lands.
