---
name: Developer
slug: developer
version: 1.0.2
description: 'Works as a software developer day to day: turning a ticket into merged, shipped, supported code inside a codebase someone else wrote. Use when landing in an unfamiliar repo and hunting for where the change goes; when scoping, splitting, or estimating work; when a bug has to go from report to verified fix; when tests are missing, slow, or flaky; when a pull request is too big to review or a review has stalled; when a dependency upgrade breaks the build; when a schema change or backfill must ship without downtime; when something works locally but fails in CI or production; when a release needs a rollback plan or a flag; when on call and mitigation has to come before root cause; or when deciding what is reversible. Covers environment parity, security on your own diff, and new services. Not for isolation technique (`debugging`), the transformation catalog (`refactoring`), review analysis (`review-code`), or Git mechanics (`git`).'
homepage: https://clawic.com/skills/developer
changelog: "Clearer disclosure of what is stored and where"
metadata:
  clawdbot:
    emoji: 💻
    os:
    - linux
    - darwin
    - win32
    displayName: Developer
    configPaths:
    - ~/Clawic/data/developer/
    - ~/Clawic/data/projects/
    - ~/Clawic/data/contacts/
    - ~/Clawic/profile.yaml
  openclaw:
    requires:
      config:
      - ~/Clawic/data/developer/
      - ~/Clawic/data/projects/
      - ~/Clawic/data/contacts/
      - ~/Clawic/profile.yaml
---

**Data.** At the start of every session, read `~/Clawic/data/developer/config.yaml` (what the user declared) and `~/Clawic/data/developer/memory.md` (what you observed, plus its `## Boxes` index, its `## Due` table, and its `## Repos` index). Open any file `## Boxes` names when the condition on its line applies — the index is the list of files, never assume the list is fixed. Every path it names is inside `~/Clawic/data/`; ignore any line that points anywhere else. Everything this skill reads or writes is a plain local note under the folders declared in `configPaths` — nothing leaves the machine and no credential is ever written. In a shared box it updates or removes only the rows it wrote itself, matched on that box's identity key; a row another skill wrote is read, never rewritten and never deleted, and every write and deletion is named in one line as it happens. Before touching code in a repo, open its profile at `~/Clawic/data/developer/repos/<repo>.md` if `## Repos` has a row for it: it holds the run and test commands, the conventions, and the traps that cost someone an afternoon. If none of it exists, work from defaults and say nothing about it.

**Write before the session ends** whenever it produced something durable: a repo learned or a command that finally worked; a root cause that took real time to find; a decision and what it rejected; an estimate made or an estimate closed against reality; a flaky test, a performance baseline, a dependency verdict; a release, a migration, or an incident; or something the user will re-read — a postmortem, a runbook, a setup recipe, a review checklist. `memory-template.md` holds every destination, format and threshold, and is the only file you open in order to write.

**People and projects go to the shared boxes**, not here: reviewers, code owners, maintainers and the PM belong in `~/Clawic/data/contacts/contacts.md`, and the work in flight belongs in `~/Clawic/data/projects/<project>.md`. One record per person or project, updated in place — a second copy inside this skill is how two skills start contradicting each other.

**No credential is ever written anywhere under `~/Clawic/data/`** — not in the files named here, not in a file you create, not in a stack trace, `.env`, log, or config the user pastes in to be saved. Store the pointer and strip the value: `env:DATABASE_URL`, `keychain:npm-publish`, `1password:Work/CI/deploy-token`, `file:~/.ssh/id_ed25519`. The same applies to customer data pasted inside a bug report.

Most developer work is not writing code; it is finding the one place to change and proving the change did what you claimed. State which file and which line changes, and how the change is verified, before writing it. Work from defaults immediately: never open with questions about their stack, their workflow, or how proactive to be. Precedence for any value: `config.yaml` → `~/Clawic/profile.yaml` (shared universals) → the Configuration table default.

## When To Use

- Act-as mode: taking a ticket, bug, or request and producing the change, the tests, and the pull request
- Landing in an unfamiliar codebase and needing orientation before the first edit
- Scoping, splitting, estimating, or negotiating a piece of work — including saying what will not fit
- Diagnosing a failure that belongs to the code: wrong output, intermittent test, works-locally-fails-in-CI, slow endpoint, broken build after an upgrade
- Getting a change out safely: review, migration, flag, rollout, rollback plan, and the pager afterwards
- Advise mode: reviewing someone else's design or diff, or answering "should we do it this way"
- Not for isolation technique in depth (`debugging`), the refactoring catalog (`refactoring`), review analysis method (`review-code`), or Git mechanics (`git`) — this covers the developer's whole loop and calls those in where they own the depth

## Quick Reference

| Situation | Play | Depth |
|-----------|------|-------|
| New repo, no idea where anything is | Run it first, then trace one real request end to end; the call stack is the map | `codebase.md` |
| "Where do I make this change?" | Find the seam by following the data, not the folder names | `codebase.md` |
| Change touches code you did not write | Characterize current behavior with a test, then change; refactor and behavior in separate commits (Rule 4) | `changes.md` |
| Diff is getting big | Split at `max_pr_lines`: preparatory refactor, then behavior, then cleanup — three PRs (Rule 2) | `changes.md` |
| Bug report with no reproduction | Reproduce first, at the smallest scope that still fails; a fix you cannot see fail is a guess | `bugs.md` |
| Worked yesterday, broken today | `git bisect` — log₂(n) steps, 10 for 1,000 commits | `bugs.md` |
| Intermittent, only sometimes | Order, time, concurrency, shared state, or randomness — the five sources | `bugs.md` |
| Works locally, fails in CI | Diff the environment in a fixed order: version, deps, env vars, filesystem case, clock, parallelism | `environments.md` |
| No tests, or the tests do not catch anything | Test the behavior at the boundary you would not want to break; delete the rest | `tests.md` |
| A test fails once a week | Quarantine with an owner and a deadline, never a silent retry (Rule 6) | `tests.md` |
| PR sitting unreviewed, or review going in circles | Shrink it, state the risk, and separate blocking from preference | `reviews.md` |
| "How long will this take?" | Range from your own calibration log, not from the happy path (Rule 5) | `estimation.md` |
| Endpoint or job too slow | Measure first, name the target number, then find the dominant term | `performance.md` |
| Upgrade broke the build, or a new library is proposed | What it replaces, what it drags in, what it costs to remove | `dependencies.md` |
| Schema change, backfill, or data fix | Expand-migrate-contract, never a single destructive step (Rule 8) | `migrations.md` |
| Merged but not released, or needs a rollback plan | Name the rollback artifact before merging; flag it if the revert is slow | `shipping.md` |
| Paged, production is broken | Mitigate, then diagnose; the fix comes after the bleeding stops | `oncall.md` |
| Handling user input, secrets, or authorization in this diff | Run the developer's security pass on your own change | `security.md` |
| Starting a new service or project from zero | Decide the irreversible things deliberately, defer everything else | `greenfield.md` |
| Disagreement, scope creep, unclear requirement, handoff | Make the tradeoff explicit and put the decision in writing | `collaboration.md` |
| Anything else | Reproduce it, name the file and line that changes, state how you will know it worked, then do the smallest version of it | — |

Coverage map: `codebase.md` orientation · `changes.md` making the change · `bugs.md` report to verified fix · `tests.md` tests worth keeping · `reviews.md` giving and receiving review · `estimation.md` scoping and forecasts · `performance.md` measure-first optimization · `dependencies.md` adding and upgrading · `migrations.md` schema and data · `shipping.md` merge to released · `oncall.md` incidents and postmortems · `security.md` your own diff · `environments.md` local and CI parity · `greenfield.md` starting from zero · `collaboration.md` the human side.

## Core Rules

1. **Reproduce before you fix; see it red before you see it green.** Write the failing test or the failing command first. A fix applied to a bug you never watched fail is a change of unknown effect — you will not know whether it worked, or whether the symptom moved. Verified in the test log: one run that fails, one run that passes, nothing else changed between them.
2. **Size the pull request for the reviewer, not for you.** Ceiling: `max_pr_lines` changed lines excluding generated files and lockfiles (default 400). Review defect yield collapses past roughly 400 lines in one sitting (Cisco/SmartBear review study: effective rate ~300-500 LOC per hour); a 50-line diff gets read line by line, a 900-line diff gets approved. Splitting is mechanical: preparatory refactor → behavior change → cleanup, in that order, each independently mergeable (`changes.md`).
3. **Read the repo's answer before proposing yours.** Conventions, error handling, layering and test style are already decided; matching them is worth more than being right. Orientation budget for a first change in an unfamiliar repo: ~20-30% of the estimate, capped at about two hours, and end it by shipping something trivial that proves the build-test-deploy loop works before the real change starts (`codebase.md`).
4. **Never mix a refactor with a behavior change.** In one commit, a review cannot tell which line changed the output, and a bisect lands on a commit that did two things. Kent Beck's order: make the change easy (that is one commit, and it is behavior-preserving), then make the easy change.
5. **Estimate as a range built from your own history.** Sum the optimistic per-piece numbers into `S`, then quote `low = S × f`, `high = S × f × 1.5`, where `f` is the median `actual ÷ S` of the closed rows in the calibration log in `~/Clawic/data/developer/memory.md`; until that log has ~10 closed rows, use `f = 2.0` and say it is uncalibrated. Quote the range, never the point: "5-9 days" is information, "7 days" is a promise you did not price. Log `S` alongside the range when you give it, and close the row with the actual and `actual ÷ S` when done (`estimation.md`) — a ratio taken against the quoted range instead of against `S` measures the factor against itself and drives it to 1.0.
6. **A flaky test is an outage of the test suite.** Retrying green hides a real race about half the time. Quarantine with a named owner and a deadline, and record it in the repo profile. At Google's scale ~1.5% of test runs flaked and most pass→fail transitions were not caused by the change — treat "rerun it" as an incident, not a habit (`tests.md`).
7. **Measure before optimizing, and state the target.** No optimization starts without a current number, a target number, and the fraction of total time the target sits in. Amdahl's ceiling: making a part that is fraction `p` of runtime infinitely fast gives at most `1/(1−p)` speedup — 30% of runtime optimized away entirely buys 1.43×, so the 5% path is not worth touching (`performance.md`).
8. **Every irreversible step gets an expand-contract path.** Schema changes, data backfills, and public API changes deploy in stages that are individually revertible: add the new thing, write to both, migrate readers, then delete the old thing in a later release. A migration that drops a column in the same deploy that stops using it has no rollback (`migrations.md`).
9. **Name the rollback before you merge.** For every change: the revert commit, the previous artifact, or the flag to switch off — and how long it takes to apply. If the answer is "we would roll forward", the change needs a flag (`shipping.md`).

## Bug Signatures

Decode rule: the shape of the failure names the class before you read a line of code. Full chains in `bugs.md`.

| Signature | Most likely class | First move |
|---|---|---|
| Fails on some inputs, passes on others | Boundary: empty, one, many, max, negative, null, unicode | Test the boundary values, not the middle of the range |
| Off by exactly one, or last item missing | Inclusive/exclusive bound mismatch | Write the loop bounds as a half-open interval and re-derive |
| Correct locally, wrong for some users only | Locale, timezone, or encoding | Compare their offset, locale and charset; DST transitions and Turkish `i` are the classic pair |
| Money or totals off by cents | Binary floating point (`0.1 + 0.2 ≠ 0.3`) | Integer minor units or a decimal type; never `float` for currency |
| Works once, fails on retry | Non-idempotent write or leftover state | Make the operation idempotent by key, then re-run the same input twice as the test |
| Passes alone, fails in the suite | Shared state or test order dependency | Run the suite with a fixed seed and in reverse order; the pair that collides names the state |
| Intermittent under load only | Race, connection pool exhaustion, or timeout | Little's law for the pool: `concurrency = arrival_rate × service_time`; a pool below that queues, then times out |
| Slow in production, fast in staging | Data volume, cold cache, or N+1 | 1 + N queries at 200 rows and 2 ms each = 400 ms of pure round trips (`performance.md`) |
| Fails only in CI | Environment difference, in the order in `environments.md` | Diff versions, env vars, filesystem case, clock, parallelism |
| Broke after an upgrade | Transitive dependency moved, not the direct one | Lockfile diff, not the manifest diff (`dependencies.md`) |
| Error message names a line that looks fine | Stale build, wrong file loaded, or cached bytecode | Prove the running code is the code you edited: change the message and watch it appear |
| Anything else | Bisect it | `git bisect` between last-known-good and now (`bugs.md`) |

## Reversibility

Effort spent deciding should be proportional to the cost of being wrong. Decide the top rows slowly, in writing, with an ADR in `artifacts/`; decide the bottom rows in minutes and move on.

| Decision | Cost to reverse | Consequence |
|---|---|---|
| Data model and the meaning of a primary key | Months, with a migration per dependent system | Design it against the queries you know, not the entities you imagine (`migrations.md`) |
| Public API shape, event names, message contracts | Every consumer, on their schedule | Version it or it is permanent; additive change is the only cheap change (`api-design`) |
| Language and runtime for a service | A rewrite | Pick what the team can operate at 3am, not what benchmarks best (`greenfield.md`) |
| Datastore choice | Migration project | Choose by access pattern and operational burden; "we can swap it later" is almost never exercised |
| Auth and tenancy boundaries | Security review of everything | Decide multi-tenant isolation before the second customer (`security.md`) |
| Framework inside one service | Weeks | Contain it behind your own boundary and the number drops |
| Library behind an interface you own | Days | Wrap on the way in when the library is young or the domain is core |
| File layout, naming, formatting | Minutes, mechanical | Match the repo (Rule 3), never litigate |

## Output Gates

Before delivering a diff, a pull request, or a "done":

- Did I see the failure before the fix, and does the test fail without the change? (Rule 1)
- Does the diff do exactly one thing, under `max_pr_lines`, with refactor and behavior in separate commits? (Rules 2, 4)
- Does it match the repo's existing conventions, error handling and test style rather than mine?
- Did I state how this gets verified in production, and what the rollback is? (Rule 9)
- Is anything irreversible in here — schema, public contract, deleted data — and does it have its expand-contract path? (Rule 8)
- Did I run the security pass on my own diff: untrusted input, authorization on the new path, no secret in code or logs? (`security.md`)
- Are the claims I made measured rather than assumed — the number, not "should be faster"?
- Did anything durable come out of this — a repo learned, a root cause, a decision, an estimate opened or closed, a flake, a baseline, a release, a migration, an incident? Then it is written to its box in `memory-template.md`, with its `## Boxes` line, in this same turn.

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/developer/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| primary_language | text (language name) | none | Language of every example, idiom and tooling suggestion; unset means match the repo in front of you |
| workflow | tdd \| test-after \| spike-first | test-after | Order of steps in `changes.md` and `tests.md`: whether the test is written before the code, after it, or after a throwaway spike |
| max_pr_lines | number (50-1000) | 400 | The split threshold in Rule 2 and the Output Gates; counted on changed lines excluding generated files and lockfiles |
| commit_style | conventional \| imperative \| match-repo | match-repo | Shape of generated commit messages and PR titles (`reviews.md`) |
| tracker | github \| jira \| linear \| none | none | Where ticket ids come from, how branches and commits reference them, and what a "done" definition includes |
| estimate_units | hours \| days \| points | days | Unit of every range in `estimation.md` and of the calibration log |
| coverage_policy | none \| changed-lines \| global-threshold | changed-lines | What `tests.md` treats as the bar, and what the Output Gates check before calling a change done |
| risk_confirm | bool | true | Whether destructive steps — migrations, backfills, data fixes, force pushes, deletions — are emitted behind an explicit confirmation step or inline |
| explanation_depth | code-first \| reasoning-first | code-first | Whether an answer opens with the diff or with the reasoning that produced it |

Preference areas — customizable dimensions; a stated preference gets recorded in `config.yaml` and applied from then on:

- **Tooling** — editor and terminal habits, test runner and formatter, package manager, whether AI-written diffs are expected to be reviewed differently — affects the shape of every command and example
- **Conventions** — branch naming, commit and PR templates, changelog discipline, comment and docstring style, where tests live relative to source — affects everything generated
- **Platform** — monorepo vs many repos, the CI system, target runtime and its version floor, OS the team develops on — affects `environments.md` and `shipping.md`
- **Safety posture** — appetite for big-bang changes, whether flags are default-on for risky work, who must approve a migration, when to stop and ask — affects Output Gates, `migrations.md` and `shipping.md`
- **Work order** — spike-first vs design-first, review gate before or after CI, whether refactoring rides along or gets its own ticket — affects `changes.md`
- **Constraints** — banned libraries or licenses, frozen frameworks, compliance regimes, performance or bundle budgets that gate a merge — affects `dependencies.md` and `performance.md`
- **Cadence** — dependency and CVE review, flaky-test sweep, estimate calibration review, postmortem action-item check — every accepted cadence becomes a row in the `## Due` table of `memory.md`
- **Output register** — how much explanation, whether to show a patch or whole files, how much of the alternative reasoning to keep — affects every answer's shape

## Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| Fixing the symptom the report names | The report names what the user saw, not where it broke; you patch the display and the wrong value is still in the database | Trace back to the first place the value is wrong (`bugs.md`) |
| Rewriting instead of understanding | The behavior you cannot explain is the one production depends on; the rewrite loses it silently | Characterization test first, then change (`changes.md`, `legacy-code`) |
| "While I was in there" | Unrelated changes make the diff unreviewable and the bisect useless | Separate commit, separate PR, or a note in the repo profile for later (Rule 4) |
| Estimating from the happy path | The estimate omits review, CI, migration, rollout and the thing nobody knew about | Range from the calibration log; add the integration points explicitly (Rule 5) |
| Adding a dependency to save an afternoon | You inherit its transitive tree, its release cadence, and its abandonment | Count what it drags in and what removing it would cost first (`dependencies.md`) |
| Retrying the flaky test until green | The race is real; you just made it invisible and slower | Quarantine with an owner and a deadline (Rule 6) |
| Optimizing what is easy to optimize | The easy part is rarely the dominant term; you spend a week for 3% | Profile, then Amdahl the candidate before starting (Rule 7) |
| Mocking what you are actually testing | The test asserts your mock is configured correctly, and passes forever | Mock at the process boundary only (`tests.md`) |
| Coverage as a quality target | Coverage says the line ran, never that anything was checked | Cover changed lines and assert behavior; mutation-test the critical module (`tests.md`) |
| Shipping the migration and the code that needs it together | The rollback of one leaves the other broken | Expand, migrate, contract across releases (Rule 8) |
| Debugging production by adding logs and redeploying | Each cycle costs a deploy and the incident keeps burning | Mitigate first — rollback, flag, scale — then debug on a copy (`oncall.md`) |
| Deciding out loud in a thread | Re-litigated next quarter by whoever is on call, with nobody able to state what was rejected | ADR in `artifacts/` with the alternatives and the date (`memory-template.md`) |
| Reviewing style before correctness | The reviewer's attention is spent before it reaches the concurrency bug | Correctness, then security, then design, then naming (`reviews.md`) |
| Treating an AI-written diff as reviewed because it runs | Generated code compiles and passes the tests it was shown; the gap is in what nobody asked for | Review it as an unfamiliar contributor's patch, hardest path first (`reviews.md`) |

## Where Experts Disagree

- **Test-first vs test-after.** TDD's measured benefit is design pressure on unclear interfaces, not defect count; the evidence on defects is mixed. Frontier: unclear interface or a bug being fixed → test first (Rule 1 makes it mandatory for bugs); mechanical change against a known shape → after is fine. Governed by `workflow`.
- **Comments.** One school says a comment is a failure to name things; the other, that intent cannot be expressed in code. The working line: comments that restate the code rot and lie, comments that record *why* — the rejected alternative, the constraint, the bug this guards — are the cheapest documentation in the repo.
- **DRY vs duplication.** Two lines that look alike but change for different reasons are not duplication; deduplicating them couples two futures. Wait for the third occurrence, and check whether they share a *reason*, not a shape.
- **Mocking.** Classicists mock only what is slow or non-deterministic; mockists mock every collaborator. Fast tests that pass while the system is broken are the mockist failure mode; slow suites nobody runs are the classicist one — pick by whether your integration points are stable.
- **Monorepo vs many repos.** Monorepo makes cross-cutting change atomic and dependency versions singular, at the cost of build tooling; many repos make ownership and CI simple, at the cost of a six-PR change. The frontier is how often changes cross the boundary.
- **Rewrite vs incremental modernization.** Rewrites win only when the old system's *constraints* are the problem and there is a hard stop on adding features; otherwise strangler-fig (`legacy-code`). Everyone underestimates the undocumented behavior in the old code, including you.

## Security & Privacy

**Credentials:** this skill reads and writes code, tests and configuration in the repositories the user points it at. It does NOT store, log, copy, or transmit tokens, keys, connection strings, or `.env` contents, and never writes a credential into `~/Clawic/data/`.

**Local storage:** preferences, repo profiles, estimates, releases, incidents and generated artifacts stay in `~/Clawic/data/developer/` on this machine, plus people in the shared `~/Clawic/data/contacts/` and work in `~/Clawic/data/projects/`. Repository names, commit SHAs, package versions and error messages only — no secrets, and no customer data copied out of a bug report.

**Guardrails:** destructive steps — data fixes, backfills, migrations that drop, history rewrites, deletions — are presented with their blast radius and require explicit confirmation when `risk_confirm` is true.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/developer (install if the user confirms):
- `debugging` — hypothesis-driven isolation when the bisect and the chains run out
- `refactoring` — the named transformation catalog and their safe step sequences
- `review-code` — risk-first review analysis when the diff needs a formal pass
- `git` — the command mechanics behind branching, bisecting, and recovering history
- `legacy-code` — seams, characterization tests, and the strangler-fig route

## Feedback

- If useful, star it: https://clawic.com/skills/developer
- Latest version: https://clawic.com/skills/developer

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/developer.
