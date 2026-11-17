# Working File Templates — Developer

Read this file only when WRITING. `config.yaml` is what the user **declared**; `memory.md` and everything it indexes is what you **observed** or produced. An observation never overwrites a declaration.

## Where each thing goes

| Data | Home | How it grows |
|---|---|---|
| Declared preferences — table keys and preference areas alike | `~/Clawic/data/developer/config.yaml` | Key by key, read-modify-write |
| Status, box index, cadences, repo index, work in flight, recurring causes, estimate calibration, how the user works | `~/Clawic/data/developer/memory.md` | Rewritten in place; stays small |
| Everything learned about one codebase — how to run it, how to test it, its conventions, its traps, its flaky tests, its baselines | `~/Clawic/data/developer/repos/<repo>.md` | One file per repo, born with the first repo; `## Repos` in `memory.md` is its index |
| Things you produced that get re-read whole — architecture decisions, postmortems, runbooks, the setup recipe that finally worked, a review checklist, a migration plan | `~/Clawic/data/developer/artifacts/<kebab-name>.md` | Born as its own file, from the first one |
| Releases, migrations run, rollbacks | `~/Clawic/data/developer/releases/<year>.md` | Append-only, cut by year |
| Incidents: what broke, how long, what fixed it | `~/Clawic/data/developer/incidents/<year>.md` | Append-only, cut by year |
| People — reviewers, code owners, the PM, a library maintainer you dealt with | `~/Clawic/data/contacts/contacts.md` (**shared**) | One row per person, every skill writing into the same file |
| The work itself — objective, status, milestones, decisions taken | `~/Clawic/data/projects/<project>.md` (**shared**) | One file per project, from the first |
| **Anything durable this table does not name** | `~/Clawic/data/developer/<plural-noun>.md`, or `artifacts/<kebab-name>.md` if it is a long text read whole | Name the file after what it holds, never after when it was made; add its `## Boxes` line in the same turn |
| Credentials of any kind, and customer data pasted into a bug report | Nowhere under `~/Clawic/data/` | Pointer or redaction only — see Secrets |

Deciding where something unnamed goes, in this order: (1) would another skill want to read it — a person, a project, a server, a domain entity? Then it belongs in the shared box, not here. (2) Is it a text read whole when its subject comes up — a runbook, a postmortem, a decision with its reasoning, a setup recipe? Then `artifacts/`, its own file from the first one. (3) Is it one more row of something that accumulates? Then a section of `memory.md` until the split threshold.

## When to write

No permission needed; every write is announced in one line that names the file. Writes and deletions stay inside the paths declared in this skill's `configPaths`. A deletion is named in that same line, and in a shared box only rows this skill itself wrote are ever updated or removed.

| It happened | Write |
|---|---|
| You oriented in a repo, or found its run/test/lint command | Its `repos/<repo>.md`, and its row in `## Repos` |
| A convention, a gotcha, or a build quirk of that repo cost you time | `## Conventions` or `## Gotchas` in that repo's profile |
| A root cause took real effort to find | One line in `## Pain Points`; the second occurrence becomes `artifacts/runbook-<symptom>.md` |
| A decision was made and an alternative rejected | `artifacts/adr-<topic>.md`, plus its one-line summary in the project file if there is one |
| An estimate was given | A row in `## Estimates` — date, work, the optimistic sum `S`, the quoted range |
| That work finished | The same row's `Actual` and `Ratio` (`actual ÷ S`), then the recomputed factor line (Rule 5) |
| A test was found flaky, quarantined, or fixed | `## Flaky Tests` in that repo's profile |
| A performance number was measured | `## Baselines` in that repo's profile — value, how it was measured, date |
| A dependency was added, pinned, refused, or upgraded painfully | `## Dependencies` in that repo's profile; the reasoning behind a refusal goes to `artifacts/` |
| Something shipped, or was rolled back | `releases/<year>.md` |
| A schema or data migration ran | `releases/<year>.md`, with the contract step still pending if it is |
| Production broke | `incidents/<year>.md`; the write-up goes to `artifacts/postmortem-<name>.md` |
| Work was left half-done, blocked, or waiting on review | `## Open Threads` — deleted the moment it lands |
| You met a reviewer, code owner, or maintainer who matters | `~/Clawic/data/contacts/contacts.md` |
| The work has an objective and a status someone else would ask about | `~/Clawic/data/projects/<project>.md` |
| The user declared a preference | Its key in `config.yaml` |
| Recurring work was scheduled or run | `## Due` |

## Start flat, split only when it hurts

Everything except repo profiles, artifacts, releases, incidents and the shared boxes begins inside `memory.md`. Splitting is a procedure, not a suggestion:

1. Before appending to a section, count its entries.
2. If the append would take it past **~15 entries or ~40 lines of real content** — scaffolding, headings and comments do not count — then, in the same turn: create the new file in `~/Clawic/data/developer/`, move the whole section into it, **delete the section from `memory.md`**, add its line to `## Boxes`, and append the new entry to the new file.
3. Keep the headings identical on both sides of the move, so the split is a copy-paste and never a rewrite.
4. Never leave a copy behind. If the same data ever appears in both places, the extracted file wins and the `memory.md` copy is deleted.

Known split targets: `## Estimates` → `estimates.md`, `## Pain Points` → `pain-points.md`. Both keep their headings exactly.

Repo profiles, artifacts, releases and incidents are the exception: each is born as its own file whatever its size, because each is read whole and only when its subject comes up.

## Secrets

Nothing under `~/Clawic/data/` ever holds a secret value — not the files named here, not files you create, not text the user pastes in and asks you to keep. Store the pointer in its place, in this shape: `<kind>:<locator>`.

`env:DATABASE_URL` · `keychain:npm-publish` · `1password:Work/CI/deploy-token` · `vault:kv/app/prod` · `ssm:/prod/api/key` · `profile:staging` · `file:~/.ssh/id_ed25519`

When the user pastes something to save — a `.env`, a config file, a stack trace, a command history, a curl that reproduces the bug — replace each secret value before writing and leave the pointer visible: `DATABASE_URL=<env:DATABASE_URL>`, `Authorization: Bearer <keychain:api-staging>`. Say in one line that you did it.

In this domain — **not secrets, keep them**: repository names and URLs without credentials, branch names, commit SHAs, ticket ids, package names and versions, service and environment names, table and column names, endpoint paths, port numbers, config variable *names*, error messages and stack frames, CI job names, feature-flag keys. **Secrets, strip them**: API keys and tokens, connection strings carrying a password, personal access tokens embedded in a remote URL, session cookies and JWTs copied out of a debug log, private keys and passphrases, webhook URLs with a token in the path, CI and registry credentials, basic-auth in a URL. **Also strip, though not a credential**: real customer data pasted inside a bug report or a failing payload — replace with a shape-preserving placeholder (`email: <redacted-email>`), because a reproduction case does not need the person.

**Contents:** [config.yaml](#configyaml) · [memory.md](#memorymd) · [repos/](#repos) · [artifacts/](#artifacts) · [releases/](#releases) · [incidents/](#incidents) · [shared contacts](#shared-contacts) · [shared projects](#shared-projects) · [split-out files](#split-out-files)

## config.yaml

Keys come from the Configuration table in `SKILL.md`, plus free-form keys nested under a preference area. Write a key only when the user states the preference.

**Writing is read-modify-write**: load the existing file, set or replace only the key just declared, keep every other key byte for byte. Never emit a `config.yaml` from this template — the template shows shape, not content. Create `~/Clawic/data/developer/` if it does not exist.

```yaml
primary_language: typescript
workflow: test-after
max_pr_lines: 400
commit_style: conventional
tracker: linear
estimate_units: days
coverage_policy: changed-lines
risk_confirm: true
explanation_depth: code-first

# Preference areas — free-form keys added as the user reveals them.
# A preference the user states is a declaration and belongs here, never in memory.md.
conventions:
  branch: "<initials>/<ticket>-<slug>"
  tests_location: alongside-source
platform:
  layout: monorepo
  node: ">=20"
constraints:
  banned_deps: [moment]
  licenses: "no AGPL"
```

If you find a preference recorded in `memory.md`, move it here and note the move.

## memory.md

Write only the sections you have content for — a heading with nothing under it is noise, and it inflates the line count that decides a split. Never copy these hints into the user's file. `## Boxes` is the one section that is never dropped when `memory.md` is rewritten: deleting a line there orphans a file forever. This is what a populated file looks like:

```markdown
# Developer Memory

## Status
status: ongoing
last: 2026-07-26

## Boxes
- Repo profiles (3) → `repos/<repo>.md`; read the profile of the repo before touching its code
- Checkout timeout postmortem → `artifacts/postmortem-checkout-timeouts.md`; read when checkout is slow or timing out
- Queue-vs-cron decision → `artifacts/adr-async-jobs.md`; read before adding any background job
- Releases 2026 (22) → `releases/2026.md`; read before shipping, and to find a rollback target
- Incidents 2026 (4) → `incidents/2026.md`; read when production breaks, to check for a repeat

## Due
| What | Every | Last run | Next due |
|------|-------|----------|----------|
| Dependency + CVE review | month | 2026-06-30 | 2026-07-30 |
| Flaky-test sweep | 2 weeks | 2026-07-13 | 2026-07-27 |
| Estimate calibration review | quarter | 2026-04-10 | 2026-07-10 |
| Postmortem action items still open | month | 2026-07-01 | 2026-08-01 |

## Repos
| Repo | Path | Stack | Run | Test | Profile |
|------|------|-------|-----|------|---------|
| checkout-api | ~/code/checkout-api | TS, Fastify, Postgres | `pnpm dev` | `pnpm test` | `repos/checkout-api.md` |
| billing-worker | ~/code/billing-worker | Python, Celery | `make run` | `pytest -q` | `repos/billing-worker.md` |

## Open Threads
- checkout-api: expand step of the `orders.status` migration merged 2026-07-24; contract step NOT done — old column still written
- billing-worker: PR #418 waiting on review since 2026-07-22, blocked on the retry semantics question

## Pain Points
| Date | Symptom | Actual cause | What changed |
|------|---------|--------------|--------------|
| 2026-05-03 | Totals off by cents on invoices | Float arithmetic in the discount path | Moved to integer minor units |
| 2026-06-19 | CI-only failure in the export suite | Test ordering leaked a stubbed clock | Reset in teardown; seed fixed in CI |

## Estimates
| Date | Work | Optimistic (S) | Quoted | Actual | Ratio |
|------|------|------|--------|--------|-------|
| 2026-05-12 | Coupon rules engine | 3 d | 5-9 d | 6 d | 2.0 |
| 2026-06-02 | Webhook retry backoff | 2 d | 3-6 d | 3 d | 1.5 |
Current factor: 1.8 (median ratio of the last 12 closed rows)

## How They Work
Strong on TypeScript, avoids the debugger and reaches for logs. Wants the diff first, reasoning after.
Reviews everything themselves before opening a PR; treats "I'll refactor it later" as a broken promise.

---
*Updated: 2026-07-26*
```

Rules that keep this readable next month:

- **`## Boxes`**: one line per file that exists — `<what> (<volume>) → <file>; read when <condition>`. Written in the same turn the file is created. Never delete a line without deleting the file it points to. A box with no index line does not exist.
- **`## Due`**: check it against today's date at the start of a session and state any overdue item in one line — a statement, not a question. Every recurring thing this skill schedules belongs here.
- **`## Repos`**: the index, one row per codebase, so "what am I working on" answers without opening anything. `Run` and `Test` are the exact commands that work on this machine. Detail belongs in the profile, never in this row.
- **`## Open Threads`**: the most perishable section and the most valuable. Anything half-done, blocked, or waiting on someone else — including the unfinished half of an expand-contract migration. A thread is deleted the turn it lands; a list of stale threads gets ignored wholesale.
- **`## Estimates`**: `Ratio = actual ÷ S`, where `S` is the `Optimistic` column — the pre-factor number, never the quoted range, which already contains the factor. `Current factor` is the median `Ratio` of the closed rows, and stays `2.0` until there are ~10 of them; the `Quoted` column is `S × factor` to `S × factor × 1.5`, rounded outward. Keep the factor line current — it is the input to Rule 5, and an estimate log nobody closes is just a list of old guesses. These headings are exactly what `estimates.md` gets when this section splits.
- **`## Pain Points`**: cross-repo causes only. A cause that belongs to one codebase goes in that repo's `## Gotchas` instead, where the next session will actually be looking.

| Status | Meaning |
|-------|---------|
| `ongoing` | Still learning their repos and how they work |
| `complete` | Know the stack, the conventions, and the traps |

## repos/

One file per codebase at `~/Clawic/data/developer/repos/<repo>.md`, created the first time you work in it, indexed by its row in `## Repos`. Read whole before touching that repo's code — it is the file that stops the next session from rediscovering the build.

```markdown
# checkout-api
*Read before changing anything in this repo. Updated 2026-07-26.*

## Map
Entry: `src/server.ts` → routes in `src/routes/` → services in `src/domain/` → Postgres via `src/db/`.
The money path is `domain/pricing.ts`; everything else is plumbing around it.

## Commands
run `pnpm dev` · test `pnpm test` · one test `pnpm test -- pricing` · lint `pnpm lint --fix` · migrate `pnpm db:migrate`
Local DB: docker compose service `db`, seeded by `pnpm db:seed` (idempotent).

## Conventions
Errors: domain throws typed errors, the route layer maps them — never `res.status()` inside `domain/`.
Tests live next to source as `*.test.ts`. Commits are conventional. PRs squash-merge.

## Gotchas
- `pnpm test` needs the DB up; a bare failure with `ECONNREFUSED` means the compose stack is down, not a bug.
- Node 22 breaks the `bcrypt` build here; the repo is pinned to 20 (`.nvmrc`).
- Env var `PRICING_MODE` must be `strict` locally or half the tests silently skip.

## Dependencies
| Package | Pin | Why |
|---------|-----|-----|
| zod | 3.x, exact | Validation contract shared with the SDK; a minor bump changed error shapes once |
| moment | banned | Replaced by date-fns 2026-03; do not reintroduce |

## Flaky Tests
| Test | Symptom | Suspected cause | Owner | Deadline |
|------|---------|-----------------|-------|----------|
| `webhook retry backoff` | Fails ~1 in 30 in CI | Real timer vs fake clock | Ana (see contacts) | 2026-08-05 |

## Baselines
| What | Number | Measured how | Date |
|------|--------|--------------|------|
| POST /checkout p95 | 240 ms | k6, 50 rps, staging data volume | 2026-07-11 |
| Test suite, cold | 3 min 40 s | `pnpm test` on this machine | 2026-07-11 |

## Owners
Reviews: Ana (pricing), Marc (infra) — both in `~/Clawic/data/contacts/contacts.md`.
```

Sections with nothing in them are omitted, not left empty. When a section here passes ~40 lines — usually `## Gotchas` or `## Flaky Tests` — it moves to `repos/<repo>-<section>.md` with the same heading and gets its own `## Boxes` line.

## artifacts/

One file per thing, at `~/Clawic/data/developer/artifacts/<kebab-name>.md`, created the first time it exists. Canonical types here: **architecture decision (ADR)**, **postmortem**, **runbook**, **setup recipe that finally worked**, **review checklist**, **migration plan**. Every artifact opens with when to read it, and gets its `## Boxes` line in the same turn.

```markdown
# ADR — background jobs on the queue, not cron
*Read before adding any background job. 2026-07-26.*

Decision: all recurring work goes through the existing queue with an idempotency key.
Why: cron jobs on one box have no retry, no visibility, and die with the box.
Rejected: node-cron in-process (lost on deploy), a second scheduler service (nobody would operate it).
Cost: every job must be idempotent by key — that is the price, and it is not optional.
Revisit if: the queue itself becomes the bottleneck, or a job needs sub-second scheduling.
```

```markdown
# Postmortem — checkout timeouts, 2026-06-19
*Read when checkout is slow or timing out. Written 2026-06-20.*

Impact: 41 min, ~1,200 failed checkouts.
Trigger: the coupon lookup went N+1 after a relation was made lazy.
Detection: customer report, 14 min before the alert — the alert threshold was above the SLO.
Mitigation: reverted the deploy (4 min once decided).
Root cause: no query-count assertion on the hot path; the ORM change was invisible in review.
Action items: query-count test on the checkout path (done), alert threshold lowered (done),
  N+1 check added to the review checklist (open, see `## Due`).
```

If the user tracks this work as a project, the decision's one-line summary also belongs in `~/Clawic/data/projects/<project>.md`, with the full text staying here and referenced by filename.

## releases/

```markdown
# Releases — 2026

| Date | What shipped | Version / commit | Rollback target | Flag | Migration | Result |
|------|--------------|------------------|-----------------|------|-----------|--------|
| 2026-07-24 | Coupon rules engine | v2.14.0 / a41b7e | v2.13.3 / 71ad0c | `coupon_rules_v2`, 10% | expand only | fine |
| 2026-07-25 | orders.status expand | — / 9f2c31 | drop new column | — | expand of 3 | contract pending |
```

- `Rollback target` is filled in **before** the merge, not after the incident (SKILL.md Rule 9).
- A migration row stays until its **contract** step ships; while it is pending, it also lives in `## Open Threads`. Half-finished expand-contract is the most common way a schema ends up permanently doubled.

## incidents/

```markdown
# Incidents — 2026

| Date | Symptom | Duration | Mitigation | Root cause | Write-up |
|------|---------|----------|------------|------------|----------|
| 2026-06-19 | Checkout timing out | 41 min | Reverted v2.11.1 | N+1 after a lazy relation | `artifacts/postmortem-checkout-timeouts.md` |
```

The row is written the day it happens, even when the cause is still unknown — `Root cause: unknown` with a date beats a perfect entry that never gets written. The write-up is a separate artifact because it is read whole, and only when that symptom returns.

## Shared contacts

Lives at `~/Clawic/data/contacts/contacts.md` and is shared with every other skill — the user may not have any of them installed, so the format travels with this skill.

```markdown
# Contacts

| Name | Key | Role | Preferred channel | Context | Last contact | File |
|------|-----|------|-------------------|---------|--------------|------|
| Ana Ruiz | ana@example.com | Reviewer, pricing owner | slack | Blocks on missing tests; fastest reviewer on the team | 2026-07-22 | — |
```

- **Identity is `Key`**: the email in lowercase, else the handle, else `<kebab-name>` plus a stable disambiguator. It is a column of the row, never implicit. Read the file before adding; if the key is already there, update that row in place — never append a second one.
- **`Preferred channel` is the kind of channel** (slack, email, phone), not the address.
- Only write people this work actually involves: reviewers, code owners, the PM or designer you agreed something with, a library maintainer who answered an issue. Not everyone who appears in a `git log`.
- **Retirement**: when someone leaves the project, delete the row and note the date in `memory.md`. A contact list that only grows stops being useful.
- **Scale cut**: one row per person while there are ≤15. Past that, one file per person at `~/Clawic/data/contacts/<name>.md` with the same fields, and `contacts.md` becomes the index with the `File` pointer. If you arrive and the folder already looks like that, follow it.
- **Foreign columns win.** If `contacts.md` already exists with a different column set, match its columns and add anything missing as a trailing note. Never rewrite its header.
- Never a phone number, address, or anything private beyond what the work needs — and never a credential.

## Shared projects

Lives at `~/Clawic/data/projects/<project>.md`, one file per project from the first, shared with every other skill.

```markdown
# checkout-v2

status: active
objective: coupons and multi-currency at checkout, without a pricing rewrite
owner: Ana (see contacts)
repos: checkout-api, billing-worker

## Milestones
- [x] Coupon rules engine — shipped 2026-07-24 behind `coupon_rules_v2`
- [ ] Multi-currency totals — estimate 7-11 d, opened 2026-07-26

## Decisions
- 2026-07-26 Background jobs go on the queue, not cron — `developer/artifacts/adr-async-jobs.md`
```

- **Identity is the filename**, the project slug. Read it before writing; update in place.
- **Closure is a status, not a deletion**: `status: done | cancelled — <date>`. The file is the record of what was delivered. Past ~20 closed projects, move them to `projects/archive/<project>.md` without renaming.
- Keep it to what someone outside this skill would ask: objective, status, milestones, decisions. Code-level detail stays in the repo profile; the full decision text stays in `artifacts/` and is referenced by filename.
- **Foreign structure wins.** If the file already exists with different headings, add to what is there and never restructure it.

## Split-out files

Created only by the split procedure above, never on day one. Each keeps the exact headings it had inside `memory.md`.

`estimates.md` — `## Estimates`, plus the current factor line. The reason this file exists is that Rule 5 is worthless without history: ten closed rows turn "how long will this take" from a feeling into a multiplier.

`pain-points.md` — `## Pain Points`, the cross-repo causes. When one line in it turns into a repeat, it graduates to `artifacts/runbook-<symptom>.md` and the row keeps a pointer to it.
