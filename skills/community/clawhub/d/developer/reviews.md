# Giving and Receiving Code Review

Review is where a change stops being yours. The formal risk-first analysis of a diff — severity scoring, evidence, patch-ready findings — is `review-code`; this is the developer's side of the loop: making a diff reviewable, reviewing without burning the relationship, and unblocking a stalled review.

**Before opening or reviewing a PR**, read `## Conventions` in `~/Clawic/data/developer/repos/<repo>.md`: what this team blocks on, squash or merge commits, required approvals, and who owns which area. Reviewers and code owners are in `~/Clawic/data/contacts/contacts.md`.

## Making a Diff Reviewable

The author controls review quality more than the reviewer does.

- **Size**: under `max_pr_lines` changed lines excluding generated files and lockfiles (default 400). Defect yield collapses past roughly 400 lines in one sitting; effective review runs at ~300-500 LOC per hour (Cisco/SmartBear). A 900-line PR does not get a worse review — it gets approved.
- **Commits tell the story**: refactor, then behavior, then cleanup (`changes.md`). A reviewer who can read commit by commit reviews three times faster than one facing a merged blob.
- **The description answers four questions**: what changes, why now, how it was verified, and what the risk is. Link the ticket; do not make the reviewer reconstruct intent from the diff.
- **Pre-review your own diff.** Read every line as if someone else wrote it. Half of all review comments are things the author would have caught by looking once — debug logs, a commented-out block, a renamed variable half-applied.
- **Annotate the surprising parts yourself.** A self-comment on the one weird line prevents the same question from three reviewers.
- **Flag what you are unsure about.** "I'm not sure this lock is needed" gets you the answer; silence gets you an approval you did not want.
- Generated code, formatting-only changes and mechanical renames go in **separate PRs**, marked as such, reviewed by sampling.

## Reviewing: Order of Attention

Attention is finite and spent in the order you look. Look in this order, and stop commenting on later categories if an earlier one is unresolved.

| Priority | Question | Example of what belongs here |
|---|---|---|
| 1. Correctness | Does it do what the description claims, including at the boundaries? | Off-by-one, unhandled null, wrong branch, missing case |
| 2. Safety | What happens when it fails, or when input is hostile? | Unvalidated input, missing authorization check, secret in code, no rollback (`security.md`) |
| 3. Data and reversibility | Can this be undone? Does it touch schema or a public contract? | Destructive migration, breaking API change (`migrations.md`) |
| 4. Tests | Would the tests fail if the behavior were wrong? | Assertion-free test, mocked-out subject, no test for the bug being fixed |
| 5. Design | Will the next change to this be easy? | Wrong seam, leaked abstraction, a second source of truth |
| 6. Readability | Will someone understand this in six months without the author? | Naming, structure, a comment that records *why* |
| 7. Style | Anything a formatter or linter should own | Never a human comment — automate it or drop it |

If style comments outnumber correctness comments, the review added noise and delay, not safety.

## How To Say It

- **Label every comment** so the author knows what blocks: `blocking:` (must change before merge), `question:` (I need to understand), `suggestion:` (take it or leave it), `nit:` (cosmetic, non-blocking). Unlabeled comments all read as blocking, which is how a 3-comment review costs a day.
- **Ask instead of assert** when you might be missing context: "what happens if this is called twice?" surfaces the bug faster than "this isn't idempotent", and does not require the author to concede anything.
- **Say why it matters**, with the failure: "this throws when the list is empty, which happens on a new account" beats "handle the empty case".
- **Approve with comments** when nothing is blocking. Holding an approval for nits is the most common cause of a stalled review.
- **Praise the thing you would have gotten wrong.** It is the cheapest way to make review feel like collaboration, and it teaches.

## Receiving Review

- Every comment gets a response: changed, or a reason. Silent resolution reads as dismissal.
- Disagreement is fine, once: state the tradeoff and the evidence. If it survives, escalate to the decision, not the person — a synchronous 10-minute conversation resolves what six round trips will not (`collaboration.md`).
- "It works" is not a rebuttal to "this will be hard to change".
- When the review reveals the design is wrong, close the PR and reopen it small. Patching a wrong shape across 20 comments produces a change nobody understands.
- A review that finds nothing on a large diff means the diff was too large, not that the code was perfect.

## Unblocking a Stalled Review

| Symptom | Cause | Move |
|---|---|---|
| No reviewer picked it up in a day | Too big, or no owner named | Split it, and request a named person rather than a team |
| Long thread going in circles | Two people arguing about different problems | Restate both positions in one comment, name the decision to make, take it to a call |
| Reviewer wants a rewrite | Design disagreement discovered late | Stop the PR; agree the design first, in writing (`artifacts/adr-<topic>.md`) |
| Approved but not merged | CI red, or waiting on a dependency | Say what it waits on in the PR and put it in `## Open Threads` |
| Comments are all nits | Reviewer avoided the hard part | Ask directly: "does the concurrency here look right to you?" |

## Reviewing AI-Written Code

Generated diffs compile, run, and pass the tests they were shown — the failure mode is silent and specific:

- **Invented APIs and options** that do not exist in the installed version; check the signature against the lockfile version, not the docs (`dependencies.md`).
- **Plausible-but-wrong defaults**: a retry with no cap, a cache with no invalidation, a permissive CORS or auth check.
- **Silent scope creep**: unrelated files reformatted or "improved" alongside the change.
- **Duplicated logic** that already exists in the repo under a different name.
- **Tests that assert the implementation** it just wrote, so they pass by construction.

Review it as an unfamiliar contributor's patch and go for the hardest path first. The author is accountable for every line, whoever typed it.

## Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| Rubber-stamping a big PR | The size is the reason it needed review most | Ask for a split; review what you can actually read |
| Reviewing more than ~400 lines in one sitting | Detection collapses; later files get skimmed | Review in sessions of ≤60 minutes, or send it back |
| Bike-shedding naming while the transaction boundary is wrong | Attention spent before reaching the risk | Follow the priority order above |
| "LGTM" without running or reading the tests | The test is where the claim is verified | Read the test diff first; it summarizes the behavior |
| Requesting changes without saying which are blocking | The author guesses, usually wrong | Label every comment |
| Author merging their own PR after a nit-only review | Skips the second look where the real comment often lands | Wait for an explicit approval, unless the repo says otherwise |
| Design feedback on a finished PR | The cost of change is highest exactly when the work is done | Agree the approach before implementation on anything over a day |

## Write Down What Came Out Of It

- What this team blocks on, its approval rules and merge style → `## Conventions` in `repos/<repo>.md` (`memory-template.md`).
- A reviewer or code owner who matters, and what they care about → `~/Clawic/data/contacts/contacts.md`, one row per person, updated in place.
- A recurring review finding worth a checklist — the N+1 check, the authorization check on new endpoints → `artifacts/review-checklist-<repo>.md` with its `## Boxes` line.
- A PR left waiting on review or on a decision → `## Open Threads` in `memory.md`.
