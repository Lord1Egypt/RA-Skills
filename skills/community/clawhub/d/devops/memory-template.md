# Working File Templates — DevOps

Read this file only when WRITING. `config.yaml` is what the user **declared**; `memory.md` and everything it indexes is what you **observed** or produced. An observation never overwrites a declaration.

## Where each thing goes

| Data | Home | How it grows |
|---|---|---|
| Declared preferences — Configuration table keys and preference areas alike | `~/Clawic/data/devops/config.yaml` | Key by key, read-modify-write |
| Delivery setup, services, environments, preview policy, pipeline health, objectives, pain points, due dates, box index | `~/Clawic/data/devops/memory.md` | Rewritten in place; stays small |
| Estate-level facts, true across services rather than per service: CI platform, IaC tool, deploy model, branch model, artifact registry and identity scheme, secrets backend and the pointer for each shared credential, observability stack, paging provider, GitOps controller and the path it reconciles from, managed dependency engines and versions, golden-path template | `## Delivery Setup` in `memory.md` | Free text, a few lines; replaced in place |
| Services: owner, repo, deploy target, strategy, RTO/RPO, backup method, last restore, first ceiling, boot-to-healthy, peak-to-mean, runbook pointer | `## Services` in `memory.md`; `~/Clawic/data/devops/services.md` once it outgrows the section | One row per service |
| Environments: purpose, target, promotion source, config source, data policy, deliberate parity exceptions | `## Environments` in `memory.md`; `~/Clawic/data/devops/envs.md` once it outgrows the section | One row per environment |
| Preview environments as a policy: TTL, seeding, destroy job, live count, monthly figure with currency | `## Preview Policy` in `memory.md`; travels into `envs.md` at the split | Replaced in place; the count and the figure carry the date they were read |
| Pipelines: platform, stages, measured PR duration, cache backend, runner type, quarantined tests | `## Pipeline Health` in `memory.md`; `~/Clawic/data/devops/pipeline-health.md` once it outgrows the section | One row per pipeline |
| Objectives — the only home for an SLI: its definition, target, window, measurement point, budget consumed, pages per shift | `## SLOs` in `memory.md`; `~/Clawic/data/devops/objectives.md` once it outgrows the section | One row per objective |
| Releases, promotions, rollbacks, and the artifact identity each rolls back to | `~/Clawic/data/devops/releases/<year>.md` | Append-only, cut by year |
| Incidents: severity, detection, the three durations, impact, cause class, postmortem pointer | `~/Clawic/data/devops/incidents/<year>.md` | Append-only, cut by year |
| Things you produced that get re-read — runbooks, postmortems, cutover plans, DR plans, a pipeline or IaC file that finally worked, an error-budget policy, an architecture or standardization decision | `~/Clawic/data/devops/artifacts/<kebab-name>.md` | Born as its own file, from the first one |
| Machines: hosts, runners, build boxes, database servers | `~/Clawic/data/servers/servers.md` (**shared**) | One row per host, every provider in one inventory |
| People: service owners, on-call, approvers, vendor contacts | `~/Clawic/data/contacts/contacts.md` (**shared**) | One row per person |
| Tracked delivery work: a migration, a platform initiative, a compliance programme | `~/Clawic/data/projects/<project>.md` (**shared**) | One file per project |
| Hostnames, DNS records, TTLs, certificate expiry | `~/Clawic/data/domains/domains.md` (**shared**) | One row per hostname |
| Delivery-tool spend: CI minutes, observability, error tracking, paging | `~/Clawic/data/finances/subscriptions.md` (**shared**) | One row per subscription, amount with currency |
| **Anything durable this table does not name** | `~/Clawic/data/devops/<plural-noun>.md`, or `artifacts/<kebab-name>.md` if it is a long text read whole | Name the file after what it holds, never after when it was made; add its `## Boxes` line in the same turn |
| Credentials of any kind | Nowhere under `~/Clawic/data/` | Pointer only — see Secrets |

Deciding where something unnamed goes, in this order: (1) would another skill want to read or write it — a machine, a person, a project, a domain, an amount of money? Then it belongs in the shared box, not here. (2) Is it a text read whole when its subject comes up — a procedure, a policy, a decision with its reasoning, a plan? Then `artifacts/`, its own file from the first one. (3) Is it one more row of something that accumulates? Then a section of `memory.md` until the split threshold.

## When to write

No permission needed; every write is announced in one line that names the file. Writes and deletions stay inside the paths declared in this skill's `configPaths`. A deletion is named in that same line, and in a shared box only rows this skill itself wrote are ever updated or removed.

| It happened | Write |
|---|---|
| The registry, secrets backend, observability stack, paging provider, GitOps controller and its path, branch model, or golden-path template was named or changed | `## Delivery Setup` |
| A service was created, adopted, renamed, or decommissioned; its owner, target, or strategy changed | `## Services` |
| An environment was added, retired, or its promotion path or parity exception changed | `## Environments` |
| A preview-environment TTL, seeding rule, destroy job, live count, or monthly figure was set or measured | `## Preview Policy`, the figure with its currency and the date it was read |
| A pipeline's platform, stages, measured duration, cache backend, or runner type changed | `## Pipeline Health` |
| A test was quarantined, fixed, or deleted | `## Pipeline Health`, with the owner and the expiry date |
| A release, promotion, or rollback happened | A row in `releases/<year>.md` with the artifact identity and the rollback target (SKILL.md Rule 2) |
| An incident was declared, mitigated, and resolved | A row in `incidents/<year>.md`; the postmortem in `artifacts/` |
| A postmortem produced action items | `## Due`, one owner and one date each, until closed |
| An SLO was defined or changed, an SLI was chosen or moved, or a budget was exhausted | `## SLOs` — the SLI lives here and nowhere else, including the exclusions agreed for it |
| A limit, quota, ceiling, boot-to-healthy time, or peak-to-mean ratio was measured | `## Services` — these are the numbers otherwise re-derived every six months |
| A backup method was configured, or a restore was tested and timed | `## Services` (`Backup`, and `Last restore` with its date and duration, or the word `never`) |
| A drill, rotation, review, or scan ran or was scheduled | `## Due` |
| A cause was not obvious, or the same failure appeared twice | `## Pain Points`; the second occurrence earns a runbook in `artifacts/` |
| A runbook, cutover plan, DR plan, error-budget policy, working pipeline file, or a decision came out of the session | `artifacts/`, with what was rejected and why |
| A machine, a person, a project, a hostname, or a subscription was named | Its shared box (protocols below), leaving only the name as a pointer here |
| The user declared a preference | Its key in `config.yaml` |

## Start flat, split only when it hurts

Everything except artifacts, the release and incident logs, and the shared boxes begins inside `memory.md`. Splitting is a procedure, not a suggestion:

1. Before appending to a section, count its entries.
2. If the append would take it past **~15 entries or ~40 lines of real content** — scaffolding, headings, and comments do not count — then, in the same turn: create the new file in `~/Clawic/data/devops/`, move the whole section into it, **delete the section from `memory.md`**, add its line to `## Boxes`, and append the new entry to the new file.
3. Keep the headings identical on both sides of the move, so the split is a copy-paste and never a rewrite.
4. Never leave a copy behind. If the same data ever appears in both places, the extracted file wins and the `memory.md` copy is deleted.

Artifacts are the exception: a runbook, a postmortem, or a decision is born as its own file whatever its size, because it is read whole and only when its subject comes up.

## Secrets

Nothing under `~/Clawic/data/` ever holds a secret value — not the files named here, not files you create, not text the user pastes in and asks you to keep. A pasted pipeline file, `.env`, terraform output, kubeconfig, or incident log is the densest source of secrets there is: strip each value **before** writing and leave its pointer in place, in this shape: `<kind>:<locator>`.

`env:DEPLOY_TOKEN` · `vault:secret/ci/deploy` · `ssm:/prod/db/password` · `secretsmanager:prod/api/key` · `gcp-sm:projects/acme/secrets/deploy` · `azure-kv:prod-vault/deploy` · `keychain:ci-runner` · `1password:Work/CI/prod` · `bitwarden:CI/registry` · `profile:prod` · `file:~/.ssh/id_ed25519`

In a text, the pointer goes where the value was: `DATABASE_URL: postgres://app:<ssm:/prod/db/password>@db.internal/app`. Say in one line that you did it.

In this domain — **not secrets, keep them**: service and repository names, environment names, hostnames and URLs, artifact digests and version tags, registry namespaces, pipeline and job names, role and policy names, account and project ids, region ids, ticket and incident ids, CVE ids, metric and alert names, environment *variable names*, cost figures, dates and durations.

**Secrets, strip them**: registry and package-manager tokens, cloud access keys and session tokens, CI/CD tokens and webhook URLs containing a token, database passwords and connection strings that carry one, TLS and SSH private keys and their passphrases, signing keys, kubeconfig client certificates and tokens, paging and chat integration keys, OIDC client secrets, anything in a `.env` the user pastes, and any value labelled secret in a pipeline file.

**Contents:** [config.yaml](#configyaml) · [memory.md](#memorymd) · [releases/](#releases) · [incidents/](#incidents) · [artifacts/](#artifacts) · [shared boxes](#shared-boxes) · [split-out files](#split-out-files)

## config.yaml

Keys come from the Configuration table in `SKILL.md`, plus free-form keys nested under a preference area. Write a key only when the user states the preference.

**Writing is read-modify-write**: load the existing file, set or replace only the key just declared, keep every other key byte for byte. Never emit a `config.yaml` from this template — the template shows shape, not content. Create `~/Clawic/data/devops/` if it does not exist.

```yaml
ci_platform: github-actions
iac_tool: terraform
deploy_model: push
environment_chain: [dev, staging, prod]
deploy_strategy_default: canary
version_scheme: git-sha
pipeline_time_budget_min: 12
slo_target_pct: 99.9
secrets_backend: vault
observability_stack: prometheus-grafana
oncall_model: business-hours
approval_gate: prod-only
compliance_regime: soc2

# Preference areas — free-form keys added as the user reveals them.
# A preference the user states is a declaration and belongs here, never in memory.md.
tooling:
  registry: ghcr.io
  feature_flags: unleash
  paging: pagerduty
  load_testing: k6
conventions:
  branch_model: trunk-based
  release_tag: "v<calver>"
  runbook_location: artifacts/
safety_posture:
  auto_rollback: on-slo-breach
  destructive_confirm: true
cadence:
  restore_drill: quarter
  secret_rotation: quarter
  access_review: quarter
  slo_review: month
compliance:
  cve_sla: {critical_reachable: 7d, high: 30d, rest: dependency-cadence}
  audit_evidence_retention: 12 months
  log_retention_floor: 90 days hot, 1 year cold
  vetoed: [raw production data outside prod]
```

If you find a preference recorded in `memory.md`, move it here and note the move.

## memory.md

Write only the sections you have content for — a heading with nothing under it is noise, and it inflates the line count that decides a split. Never copy these hints into the user's file. `## Boxes` is the one section that is never dropped when `memory.md` is rewritten: deleting a line there orphans a file forever. This is what a populated file looks like:

```markdown
# DevOps Memory

## Status
status: ongoing
last: 2026-07-26

## Boxes
- Releases and rollback targets (2026) → `releases/2026.md`; read before any deploy, promotion or rollback
- Incidents and postmortem pointers (2026) → `incidents/2026.md`; read when a symptom looks familiar, and before any postmortem
- Checkout 5xx runbook → `artifacts/runbook-checkout-5xx.md`; read the moment checkout errors rise
- Error budget policy, agreed with product → `artifacts/error-budget-policy.md`; read before pausing or resuming feature deploys
- Postgres 15 upgrade cutover plan → `artifacts/cutover-postgres-15.md`; read before or during that migration
- DR plan and last drill findings → `artifacts/dr-plan.md`; read before any restore or failover

## Due
| What | Every | Last run | Next due |
|------|-------|----------|----------|
| Restore drill (timed, scratch env) | quarter | 2026-05-14 | 2026-08-14 |
| Secret rotation — static registry token | quarter | 2026-06-01 | 2026-09-01 |
| Access review (prod human access) | quarter | 2026-04-10 | 2026-07-10 |
| Drift detection review | week | 2026-07-20 | 2026-07-27 |
| Base image rebuild and rescan | month | 2026-07-01 | 2026-08-01 |
| SLO and alert hygiene review | month | 2026-07-05 | 2026-08-05 |
| Postmortem action sweep | 2 weeks | 2026-07-15 | 2026-07-29 |
| Action item: idempotency key on payment retry (owner: Marta) | once | — | 2026-08-07 |

## Delivery Setup
GitHub Actions, Terraform, push deploys to ECS. Trunk-based, deploy on merge to main, prod behind one approval.
Artifacts: ghcr.io, tagged by git sha, promoted by digest. Metrics in Grafana Cloud; paging via PagerDuty, business hours only.
Secrets in Vault: CI deploy `vault:secret/ci/deploy`, registry push `env:GHCR_TOKEN`. No GitOps controller — push model. Postgres 14, Redis 7.
Golden path: `acme/service-template` (pipeline, dashboard, alerts, runbook skeleton), last refreshed 2026-06.

## Services
| Service | Owner | Repo | Deploy target | Strategy | RTO / RPO | Backup | Last restore | First ceiling | Boot→healthy | Peak / mean | Runbook |
|---|---|---|---|---|---|---|---|---|---|---|---|
| checkout-api | Marta (contacts) | acme/checkout | ecs prod | canary 10% / 15 min | 1 h / 5 min | PITR, 7 d | 2026-05-14, 41 min | db connections, 200 | 95 s incl. image pull | 3.4× | artifacts/runbook-checkout-5xx.md |
| web | Team Front | acme/web | cdn + ecs | rolling | 4 h / 24 h | nightly snapshot | never | CDN origin egress | 40 s | 2.1× | — |
| billing-worker | Marta (contacts) | acme/billing | ecs prod | recreate | 4 h / 1 h | nightly snapshot + WAL | 2026-05-14, 12 min | provider rate limit 100/s | 60 s | 9× (nightly batch) | artifacts/runbook-billing-lag.md |

## Environments
| Environment | Purpose | Target | Promoted from | Config source | Data | Deliberate differences |
|---|---|---|---|---|---|---|
| dev | integration of merged work | ecs dev | — | SSM /dev | synthetic, 1% volume | single instance, no multi-AZ |
| staging | release validation | ecs staging | dev | SSM /staging | anonymized copy, monthly refresh | 2 instances vs 6 in prod |
| prod | users | ecs prod | staging | SSM /prod | real | — |
| preview | per-PR review | ecs ephemeral | — | SSM /dev | fixtures | 72 h TTL, shared database |

## Preview Policy
Created on PR open, destroyed on merge or close, plus a 72 h expiry sweep at 03:00 UTC. Seeded from the `smoke` fixture set; one shared Postgres, schema per preview. URL and credentials posted to the PR.
Live: 6 previews on 2026-07-26. Monthly: 90 USD as of 2026-07-01, down from 340 USD before the sweep job.

## Pipeline Health
| Pipeline | Platform | PR feedback (p50) | Cache | Runner | Quarantined |
|---|---|---|---|---|---|
| checkout CI | github-actions | 8 min | registry-backed | hosted 4-core | 2 tests, expire 2026-08-05 (owner: Marta) |
| web CI | github-actions | 21 min | gha, thrashing above 10 GB | hosted 2-core | none |

## SLOs
| Service | SLI | Target | Window | Measured at | Budget used | Pages / shift | Actioned |
|---|---|---|---|---|---|---|---|
| checkout-api | successful checkouts < 300 ms, excluding 4xx | 99.9% | rolling 30 d | ALB access logs | 38% as of 2026-07-26 | 1.2 | 70% (2026-07) |
| billing-worker | jobs finished within 15 min of enqueue | 99.5% | rolling 30 d | consumer metrics | 12% as of 2026-07-26 | 0.3 | 100% (2026-07) |

## Pain Points
2026-03: rollback failed because the migration had already contracted; 90 minutes of manual repair. Expand/contract enforced since.
2026-06: preview environments were never destroyed for closed PRs; the bill is in `## Preview Policy`, the sweep job was the fix.

## How They Work
Two teams, no dedicated platform team. Wants the plan and the command, not the theory. Will not approve anything destructive without seeing exactly what it deletes.

---
*Updated: 2026-07-26*
```

Rules that keep this readable next month:

- **`## Boxes`**: one line per file that exists — `<what> (<volume>) → <file>; read when <condition>`. Written in the same turn the file is created. Never delete a line without deleting the file it points to. A box with no index line does not exist.
- **`## Due`**: check it against today's date at the start of a session and state any overdue item in one line — a statement, not a question. Cadences come from `cadence` in `config.yaml` when declared; postmortem action items live here too, with their owner, until they close.
- **`## Delivery Setup`**: the facts that are true across the estate rather than per service — CI platform, IaC tool, deploy model, branch model, registry and artifact identity scheme, secrets backend with the pointer for each shared credential, observability stack, paging provider, GitOps controller and the path it reconciles from, managed dependency engines and versions, golden-path template. If a fact varies service by service it is a `## Services` column instead, and if a column does not exist for it, this section is where it goes rather than a new column invented on the spot.
- **`## Services`**: one row per service, no estate-level facts. `Backup` is the method and its retention (`PITR, 7 d`), not a vendor name alone. `Last restore` is a date and a measured duration, or the word `never` — that word is what makes an untested backup visible. `First ceiling` is the measured limit that saturates first, `Boot→healthy` and `Peak / mean` are measured, never estimated (`capacity.md`). `Owner` is a name that also exists in the shared contacts box. The objective itself is **not** here: it lives in `## SLOs`.
- **`## Environments`**: the last column is for *deliberate* differences. An undocumented difference becomes an assumed bug at 3am.
- **`## Preview Policy`**: written only once per-PR environments exist. The live count and the monthly figure each carry the date they were read, and the figure carries its currency — an untracked preview fleet is the most common runaway line on the bill (`environments.md`).
- **`## Pipeline Health`**: durations are measured, not estimated, with the date they were measured if they are older than a month. Every quarantined test carries an owner and an expiry date, or the list only grows.
- **`## SLOs`**: the single home of every SLI — its definition, its agreed exclusions, where it is measured, and its budget. No other section restates an objective. Budget used, pages per shift, and the actioned fraction each carry the date they were read; a figure with no date cannot be compared against anything.
- These headings are exactly the ones `services.md`, `envs.md`, `pipeline-health.md`, and `objectives.md` get when their sections outgrow this file, so each split stays a copy-paste.

| Status | Meaning |
|-------|---------|
| `ongoing` | Still learning their delivery setup |
| `complete` | Know their services, environments, and process well |

## releases/

Append-only, one file per year, never rewritten. This file is the rollback record (SKILL.md Rule 2) and the source of deploy frequency and lead time (`platform.md`).

```markdown
# Releases — 2026

| Date | Service | Environment | Artifact identity | Strategy | Rollback target | Merged | Deployed | Result |
|------|---------|-------------|-------------------|----------|-----------------|--------|----------|--------|
| 2026-07-24 | checkout-api | prod | sha256:9f2c… (a41b7e) | canary 10% / 15 min | sha256:71ad… | 14:02 | 14:41 | ok |
| 2026-07-25 | web | prod | sha256:3d10… (8c99f2) | rolling | sha256:9f2c… | 09:10 | 09:26 | rolled back 10:06, CDN cache served stale bundle |

## Migrations shipped
| Date | Service | Step | Reversible until | Verified |
|------|---------|------|------------------|----------|
| 2026-07-20 | checkout-api | expand: orders.currency added nullable | contract | backfill 100%, 0 nulls |
| 2026-08-03 | checkout-api | contract: orders.currency NOT NULL | **point of no return** | pending |
```

- The artifact identity is the point of the row. A row without one is a diary entry, not a rollback record.
- `Merged` and `Deployed` timestamps exist so change lead time can be computed later without archaeology.
- `Result` names what happened, including rollbacks — a log that only records successes cannot answer "when did this last break".

## incidents/

```markdown
# Incidents — 2026

| Date | Sev | Service | Detected by | Detect | Mitigate | Resolve | Impact | Cause class | Postmortem |
|------|-----|---------|-------------|--------|----------|---------|--------|-------------|------------|
| 2026-06-11 | 1 | checkout-api | burn-rate page | 4 min | 22 min | 1 h 40 | ~30% of checkouts failing, 18 min of budget | bad config in release | artifacts/postmortem-2026-06-11-checkout.md |
| 2026-07-02 | 2 | billing-worker | customer report | 3 h | 3 h 20 | 5 h | 400 invoices late | provider rate limit | artifacts/postmortem-2026-07-02-billing.md |
```

- Three durations, not one: detect, mitigate, resolve. They point at three different investments (alerting, runbooks, architecture).
- `Detected by` matters: "customer report" is itself a finding, and counting them is how alerting gets prioritized.
- `Cause class` is a small closed vocabulary the user's estate actually produces (bad config, bad code, capacity, dependency, expiry, human action, data) — the value is in seeing which class repeats.
- A repeat of an earlier incident references that row and says whether its action items had closed.

## artifacts/

One file per thing, at `~/Clawic/data/devops/artifacts/<kebab-name>.md`, created the first time it exists. Canonical types here: **runbook**, **postmortem**, **cutover plan**, **DR plan**, **error-budget policy**, **a pipeline or IaC file that finally worked**, **an architecture or standardization decision**. Every artifact opens with when to read it, and gets its `## Boxes` line in the same turn. Every secret inside is already a pointer.

```markdown
# Runbook — checkout 5xx
*Read when checkout error rate rises or the burn-rate page fires. Written 2026-06-11, last exercised 2026-07-24.*

Symptom → verify → mitigate → diagnose → escalate. Ends with the rollback command and where the
artifact identity is recorded (`releases/2026.md`). Every credential is a pointer.
```

```markdown
# Postmortem — 2026-06-11 checkout outage
*Read before changing checkout config handling, or when a similar symptom appears. Blameless.*

Impact · Timeline with timestamps · Detection · Contributing factors (plural) · What went well ·
Action items with owner and date (each one also a row in `## Due` until closed).
```

```markdown
# Decision — canary over blue-green for checkout
*Read before changing the deploy strategy of a user-facing service. 2026-07-26.*

Decision: ...one sentence...
Rejected: blue-green — 2× capacity for the switch window at 380 USD/mo, and the flip could not be
validated per cohort.
Canary sizing: 10% for 15 min ≈ 9,000 requests, bounds a regression above ~0.03% (rule of three).
Revisit when: traffic drops below 10 req/s, or the cost of doubled capacity stops mattering.
```

If the user tracks this work as a project, the one-line decision summary also belongs in the shared `~/Clawic/data/projects/<project>.md`, with the full artifact staying here and referenced by name.

## Shared boxes

These files are shared with every other skill. The user may not have the owning skill installed, so the format and the protocol travel with this one. In all of them: **read the file before adding, find the identity key, update your own row in place, never rewrite a header you did not write, and never touch a row another source owns.**

### `~/Clawic/data/servers/servers.md` — machines

```markdown
# Servers

| Name | Provider | Account / Project | Region | Type | Role | Monthly | Access reference |
|------|----------|-------------------|--------|------|------|---------|------------------|
| build-1 | hetzner | acme | fsn1 | CPX41 | CI runner (self-hosted) | 28 EUR | file:~/.ssh/id_ed25519 |
| db-prod-1 | aws | 111122223333 | eu-west-1 | db.r6g.large | primary postgres | 210 USD | ssm:/prod/db/password |
```

- **Identity is `Name` + `Provider`.** If that pair exists, update the row; only its absence justifies a new one.
- **Retirement is part of the inventory**: when a machine is decommissioned, delete its row and note the date in `## Pain Points` or the relevant service row. An inventory that only grows stops being an inventory.
- **Amounts carry their currency inside the value** (`28 EUR`), because rows from other providers are in other currencies and someone will add the column up. An estimate carries the date it was estimated.
- **Scale cut**: one row per host while there are ≤15. Past that, one file per host at `~/Clawic/data/servers/<name>.md` with the same fields, and `servers.md` becomes the index (`Name | Provider | Role | → file`). If the folder already looks like that, follow it — never start a parallel `servers.md`.
- **Foreign columns win.** If the file exists with a different column set, match its columns and add anything missing as a trailing note.
- Access reference is a pointer only. Never a key, token, or password.

### `~/Clawic/data/contacts/contacts.md` — people

```markdown
# Contacts

| Name | Key | Role | Preferred channel | Context | Last contact | File |
|------|-----|------|-------------------|---------|--------------|------|
| Marta Ruiz | marta@acme.com | owner, checkout-api; primary on-call | email | approves prod deploys | 2026-07-24 | — |
```

- **Identity is `Key`**: lowercase email, else a handle, else `<kebab-name>` plus a stable disambiguator. The key is a column of the row, never implicit.
- `Preferred channel` is the *type* of channel, not the address, and never a phone number or a paging URL that carries a token.
- If the person already has a row, update it in place and add the devops context to `Context` — never a second row for the same key.
- **Scale cut**: pass 15 people, or the moment one does not fit a row, give each a `~/Clawic/data/contacts/<name>.md` and leave `contacts.md` as the index with the `File` pointer.
- In devops files, refer to a person by name only. Duplicating the person here is how two skills start contradicting each other.

### `~/Clawic/data/projects/<project>.md` — tracked work

One file per project from the first one: objective, status, milestones, decisions taken. A delivery migration, a platform initiative, or a compliance programme belongs here; the technical artifact stays in `artifacts/` and is referenced by name. Closing is `status: done | cancelled — <date>` inside the file, never deleting it — the record of what was delivered is the point. Past roughly 20 closed projects, move them to `projects/archive/<project>.md` without renaming.

### `~/Clawic/data/domains/domains.md` — hostnames

```markdown
# Domains

| Hostname | Registrar / DNS | Record | Target | TTL | Expires | Certificate expires | Notes |
|----------|-----------------|--------|--------|-----|---------|---------------------|-------|
| api.acme.com | cloudflare | CNAME | alb-prod-1234.eu-west-1.elb.amazonaws.com | 60 | 2027-03-01 | 2026-09-14 (auto-renew) | TTL lowered 2026-07-20 for the cutover |
```

- **Identity is the hostname.** Update in place; a second row for the same hostname is how a stale target survives a cutover.
- Record the TTL *and* the date it was last changed — the lowering has to precede the cutover by a full old-TTL (`migrations.md`).
- Certificate and domain expiry dates each get a row in `## Due` so renewal is scheduled, not discovered.
- **Scale cut**: past ~40 hostnames, group by apex in `<apex>.md` and leave `domains.md` as the index.

### `~/Clawic/data/finances/subscriptions.md` — delivery-tool spend

```markdown
# Subscriptions

| Service | What it is for | Monthly | Billing | Owner | Notes |
|---------|----------------|---------|---------|-------|-------|
| Grafana Cloud | metrics, logs, SLO dashboards | 180 USD | card, monthly | Marta | log volume is the driver |
```

- **Identity is the subscription name.** Update the row when the amount changes; do not add a second row.
- Amounts carry their currency in the value, and an estimate carries the date it was estimated.
- Cancelling means deleting the row and noting the date in `## Pain Points` — a subscription list that only grows is a bill nobody can audit.
- This file is not partitioned: it stays small because cancellation removes rows.

## Split-out files

Created only by the split procedure above, never on day one. Each keeps the exact headings and columns it had inside `memory.md`, so the move is a copy-paste. The extra headings listed below are **added after the move**, holding content that did not exist before — never a rename of what was copied.

`services.md` — `## Services`. The file that answers "what do we run, who owns it, and what is its promise" without opening a repository. Add a `## Decommissioned` heading with the date when a service is retired, rather than deleting the row: the question "what happened to that service" is asked long after.

`envs.md` — `## Environments` and `## Preview Policy`, both moved verbatim (the second only exists if per-PR environments do).

`pipeline-health.md` — `## Pipeline Health`, plus `## Quarantine` (test, owner, quarantined on, expiry) once the quarantine list needs more than a cell.

`objectives.md` — `## SLOs`, plus `## Budget History` (window, budget used at close, what consumed it). The history is the reason this file exists: without it nobody can say whether reliability is improving or the target is simply too low.
