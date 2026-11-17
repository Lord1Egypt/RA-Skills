# From Merged to Released

Merged is not shipped, and shipped is not working. The developer's job ends when the change is verified in production and someone can turn it off (SKILL.md Rule 9). Pipeline construction is `ci-cd` and `deploy`; this is what the author of the change owns.

**Before shipping**, read `releases/<year>.md` for what went out recently — the most common cause of a mystery regression is a change that shipped an hour before yours — and `## Open Threads` in `memory.md` for a pending migration contract step that your deploy must not race.

## Deploy and Release Are Different Decisions

Deploy puts the code on the machine; release exposes the behavior to users. Coupling them means every rollout is all-or-nothing and every rollback is a deploy.

| Mechanism | Use when | Rollback |
|---|---|---|
| Plain deploy | Small, additive, easily reverted change | Revert commit, redeploy — costs one pipeline run |
| Flag, default off | The change is risky, big, or needs staged exposure | Flip the flag: seconds, no build (`feature-flags`) |
| Percentage rollout | Behavior change with measurable effect | Reduce the percentage |
| Dark launch / shadow traffic | New implementation of an existing path | Stop comparing; nothing user-visible changed |
| Expand-contract | Anything touching schema or a public contract | Per step (`migrations.md`) |

Rule of thumb: if a revert takes longer than the incident would last, the change needed a flag.

## Before Merging

- The rollback is named and its cost is known: revert commit, previous artifact, or flag key — plus how long it takes to apply.
- Migration sequencing is decided: data before code, contract step scheduled separately.
- The verification is stated: which metric, log line, or query proves this worked in production, and within what window.
- Anything user-visible has an owner watching after it goes out, and that person knows it is going out.
- Config and environment variables the change needs exist in the target environment *before* the deploy — the most common cause of a deploy that fails only in production (`environments.md`).

## Staged Rollout

1. **Internal or 1%** first, long enough to see real traffic through the path — minutes for high volume, a day for low.
2. **Watch the three signals**: error rate on the changed path, latency p95, and the business metric the change is supposed to move. Two of the three moving in the wrong direction is a rollback, not a debugging session.
3. **10% → 50% → 100%**, with a pause at each step at least as long as the slowest feedback loop (a nightly job means a day).
4. **Delete the flag** once it is at 100% and stable. A flag that outlives its rollout is dead code with a runtime cost and a false sense of control — put the cleanup on `## Due` with a date.

## Verifying in Production

The deploy succeeded is not evidence. Check, in this order: the change is actually live (version endpoint, build id, or a log line you added), the new path is being exercised (a counter, not a hope), the error rate on that path, then the metric it was supposed to move. A change that nobody can prove is live has been "shipped" three times in most teams.

## Rolling Back

- **Roll back first, diagnose after.** The recording of what happened survives; the outage does not need to (`oncall.md`).
- **Revert commits are normal**, not an admission. A clean revert of a small PR is why Rule 2 exists.
- **What is not revertible**: anything that wrote data in the new shape, sent emails, charged cards, or published events. Know which of these your change does before it goes out — that is the list that decides whether it needs a flag.
- **After a rollback**, the branch does not get re-merged until the cause is understood and a test covers it.

## Release Hygiene

- Every release maps to a commit or a tag, and the artifact deployed is the artifact tested — same build, promoted, not rebuilt (`ci-cd`).
- Version according to what consumers rely on: for a library, a breaking change is a major, always (`semantic-versioning`).
- A changelog entry in the user's language, not the commit subject — for anything a user or an integrator can observe.
- Do not ship on Friday afternoon unless someone is watching through the weekend. This is not superstition: it is the mean-time-to-notice, which rises when nobody is looking.

## Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| Merging without naming the rollback | The plan gets invented under pressure | Name it in the PR before merge (Rule 9) |
| Deploy and release coupled for a risky change | Rollback costs a pipeline run and a decision meeting | Flag it |
| Big-bang cutover of a rewritten path | Every failure mode arrives simultaneously | Shadow traffic, then percentage rollout |
| Rebuilding the artifact for production | Not the thing you tested; different dependencies resolve | Promote the tested artifact |
| Watching the deploy dashboard instead of the change | Green pipeline, broken feature | Verify the change is live and exercised |
| Flags that never get removed | Combinatorial states nobody has tested | Cleanup row in `## Due` at the moment the flag is created |
| Config change deployed by hand, once | Reappears on the next instance, missing | Config in the repo and the pipeline, with the code |
| Announcing a release nobody verified | The first report comes from a customer | Verify, then announce |

## Write Down What Shipped

- **Every release** → a row in `~/Clawic/data/developer/releases/<year>.md`: date, what shipped, version/commit, **rollback target filled in before the merge**, flag and its percentage, migration state, and result (`memory-template.md`).
- **Every rollback** → the same file, with what triggered it. This is the file that answers "what changed before it broke" during the next incident.
- **A flag awaiting cleanup, or a migration contract step pending** → `## Open Threads` in `memory.md` plus its row in `## Due` with a date.
- **A release procedure that took discovery to get right** → `artifacts/runbook-release-<service>.md` with its `## Boxes` line.
