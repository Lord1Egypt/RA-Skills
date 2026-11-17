# Working File Templates — Google Cloud

Read this file only when WRITING. `config.yaml` is what the user **declared**; `memory.md` and everything it indexes is what you **observed** or produced. An observation never overwrites a declaration.

## Where each thing goes

| Data | Home | How it grows |
|---|---|---|
| Declared preferences — table keys and preference areas alike | `~/Clawic/data/gcp/config.yaml` | Key by key, read-modify-write |
| Org context, infrastructure, spend, quotas, service accounts, datasets, pain points, due dates, box index | `~/Clawic/data/gcp/memory.md` | Rewritten in place; stays small |
| Compute Engine VMs and GKE node pools | `~/Clawic/data/servers/servers.md` (**shared**) | One row per host, every provider in one inventory |
| DNS zones and registered domains | `~/Clawic/data/domains/domains.md` (**shared**) | One row per domain |
| A client or colleague who owns a project | `~/Clawic/data/contacts/contacts.md` (**shared**) | One row per person, keyed by email or handle; referenced from here by name only |
| Work the user tracks as a project of their own — its decisions and milestones | `~/Clawic/data/projects/<project>.md` (**shared**) | One file per project from the first; the diagram stays in `artifacts/` |
| Agreed RPO and RTO per stateful service | `~/Clawic/data/gcp/artifacts/dr-targets.md` | One artifact, rewritten when a target or a measured restore changes |
| GCP projects, their billing account and owner | `## Org Context` in `memory.md` while there is one; `~/Clawic/data/gcp/projects.md` from the second | One row per project |
| Quota values and increase requests | `## Quotas` in `memory.md`, then `quotas.md` | One row per quota, per project, per region |
| Service accounts and what each one is for | `## Service Accounts` in `memory.md`, then `service-accounts.md` | One row per service account |
| BigQuery datasets, partitioning and scan baselines | `## BigQuery` in `memory.md`, then `datasets.md` | One row per dataset or heavy table |
| Things you produced that get re-read — runbooks, IAM policies that finally worked, architecture decisions, diagrams, expensive-to-derive queries | `~/Clawic/data/gcp/artifacts/<kebab-name>.md` | Born as its own file, from the first one |
| Deploy records, GKE upgrades, timed restore drills | `~/Clawic/data/gcp/deploys/<year>.md` | Append-only, cut by year |
| **Anything durable this table does not name** | `~/Clawic/data/gcp/<plural-noun>.md`, or `artifacts/<kebab-name>.md` if it is a long text read whole | Name the file after what it holds, never after when it was made; add its `## Boxes` line in the same turn |
| Credentials of any kind | Nowhere under `~/Clawic/data/` | Pointer only — see Secrets |

## When to write

No permission needed; every write is announced in one line that names the file. Writes and deletions stay inside the paths declared in this skill's `configPaths`. A deletion is named in that same line, and in a shared box only rows this skill itself wrote are ever updated or removed.

| It happened | Write |
|---|---|
| A VM or node pool was created, resized, discovered or retired | Its row in `servers.md` |
| An Asset Inventory or discovery pass ran (Rule 1) | `## Current Infrastructure` |
| A bill was reviewed, or a saving landed | `## Spend` |
| A resource was left running on purpose after a cleanup sweep | `### Intentionally Idle` |
| A billing export or budget was created | `### Alerts Configured` |
| A project was added, or its billing account or owner named | `## Org Context`, or the projects table |
| A quota was checked, requested, or granted | `## Quotas` |
| A service account was created, or its purpose or bindings changed | `## Service Accounts` |
| A dataset was created, or a query's scan size was measured | `## BigQuery` |
| A DNS zone was created, or a domain pointed at a GCP load balancer | `domains.md` |
| A client, colleague or project owner was named | `contacts.md` |
| A decision was made about work the user tracks as their own project | `~/Clawic/data/projects/<project>.md` |
| An RPO or RTO was agreed, or a measured restore changed one | `artifacts/dr-targets.md` |
| An org-policy exception was granted | `artifacts/org-policies.md` |
| A deploy shipped, a cluster was upgraded, or a restore was timed | `deploys/<year>.md` |
| A runbook, a working IAM policy, an architecture decision, or a query that took real effort to get right came out of the session | `artifacts/` |
| The user declared a preference | Its key in `config.yaml` |
| Recurring work was scheduled or run | `## Due` |

## Start flat, split only when it hurts

Everything except artifacts, deploy records and the shared boxes begins inside `memory.md`. Splitting is a procedure, not a suggestion:

1. Before appending to a section, count its entries.
2. If the append would take it past **~15 entries or ~40 lines of real content** — scaffolding, headings and comments do not count — then, in the same turn: create the new file in `~/Clawic/data/gcp/`, move the whole section into it, **delete the section from `memory.md`**, add its line to `## Boxes`, and append the new entry to the new file.
3. Keep the headings identical on both sides of the move, so the split is a copy-paste and never a rewrite.
4. Never leave a copy behind. If the same data ever appears in both places, the extracted file wins and the `memory.md` copy is deleted.

Artifacts are the exception: a runbook, a decision, or a query that cost a day to get right is born as its own file whatever its size, because it is read whole and only when its subject comes up.

## Secrets

Nothing under `~/Clawic/data/` ever holds a secret value — not the files named here, not files you create, not text the user pastes in and asks you to keep. Store the pointer in its place, in this shape: `<kind>:<locator>`.

`gcp-sm:projects/acme/secrets/db-password` · `env:GOOGLE_APPLICATION_CREDENTIALS` · `keychain:gcp-prod` · `1password:Work/GCP/prod` · `vault:kv/gcp/prod` · `file:~/.config/gcloud/application_default_credentials.json`

When the user pastes something to save, replace each secret value before writing and leave the pointer visible: `password: <gcp-sm:projects/acme/secrets/db-password>`. Say in one line that you did it. Service account JSON key files are the highest-risk paste in this domain: keep the `client_email` and the `project_id`, replace the whole `private_key` block with its pointer, and say so.

In this domain — **not secrets, keep them**: project IDs and numbers, project names, service account emails, role and custom-role names, bucket, dataset, table, VPC, subnet and cluster names, region and zone ids, billing account ids, KMS key resource paths, Secret Manager secret *names*. **Secrets, strip them**: service account private keys, OAuth client secrets, refresh and access tokens, API keys, database passwords and connection strings containing one, SSH private keys, Secret Manager secret *values*, signed-URL signing keys, webhook and pager tokens.

**Contents:** [config.yaml](#configyaml) · [memory.md](#memorymd) · [shared servers inventory](#shared-servers-inventory) · [shared domains inventory](#shared-domains-inventory) · [shared contacts box](#shared-contacts-box) · [shared projects box](#shared-projects-box) · [projects.md](#projectsmd) · [artifacts/](#artifacts) · [deploys/](#deploys) · [split-out files](#split-out-files)

## config.yaml

Keys come from the Configuration table in `SKILL.md`, plus free-form keys nested under a preference area. Write a key only when the user states the preference.

**Writing is read-modify-write**: load the existing file, set or replace only the key just declared, keep every other key byte for byte. Never emit a `config.yaml` from this template — the template shows shape, not content. Create `~/Clawic/data/gcp/` if it does not exist.

```yaml
default_project: acme-prod
default_region: europe-west1
gcloud_configuration: prod
iac_tool: terraform
monthly_budget_usd: 250
org_model: organization
bq_billing_model: on-demand
compliance_regime: gdpr-eu

# Preference areas — free-form keys added as the user reveals them.
# A preference the user states is a declaration and belongs here, never in memory.md.
conventions:
  labels: [env, team, service, cost-center]
  project_ids: "acme-<env>"
  cidr_scheme: "10.<env>.0.0/16, /20 subnets, /14 pods secondary"
platform:
  machine_families: [c4a, n2d]      # Arm-first, N2D fallback
  network_tier: premium
  gke_mode: autopilot
safety_posture:
  destructive_commands: confirm-each
  project_liens: on
```

If you find a preference recorded in `memory.md`, move it here and note the move.

## memory.md

Write only the sections you have content for — a heading with nothing under it is noise, and it inflates the line count that decides a split. Never copy these hints into the user's file. `## Boxes` is the one section that is never dropped when `memory.md` is rewritten: deleting a line there orphans a file forever. This is what a populated file looks like:

```markdown
# GCP Memory

## Status
status: ongoing
last: 2026-07-26

## Boxes
- Projects (4) → `projects.md`; read before any billing, quota or cross-project question
- Spend history (14 months) → `spend-log.md`; read before any cost comparison
- Service accounts (22) → `service-accounts.md`; read before granting a role or debugging a 403
- BigQuery datasets (9) → `datasets.md`; read before estimating or optimizing a query
- Checkout 502 runbook → `artifacts/runbook-checkout.md`; read the moment checkout is the symptom
- Decision: Cloud Run over GKE → `artifacts/decision-serving-platform.md`; read before any change to the request path

## Due
| What | Every | Last run | Next due |
|------|-------|----------|----------|
| Cost review from billing export | month, day 15 | 2026-06-15 | 2026-07-15 |
| Unused service account + key sweep | quarter | 2026-05-04 | 2026-08-04 |
| GKE version support check | quarter | 2026-04-20 | 2026-07-20 |
| Restore drill (Cloud SQL PITR) | quarter | 2026-04-02 | 2026-07-02 |
| Recommender sweep (idle VMs, disks, IPs) | month | 2026-07-01 | 2026-08-01 |
| CUD expiry check | year | 2025-11-30 | 2026-11-30 |

## Org Context
Organization acme.com, one folder per env, billing account 01ABCD-…, two engineers, Terraform-managed, europe-west1.

## Current Infrastructure
One Shared VPC in host project acme-net (10.0.0.0/16, pods 10.64.0.0/14) · Cloud Run `api` behind a global external ALB · Cloud SQL Postgres HA, private IP · GCS assets bucket behind Cloud CDN · GKE Autopilot cluster `batch`.

## Spend
### Monthly
| Month | Actual | As of | Budget | Top services | Notes |
|-------|--------|-------|--------|--------------|-------|
| 2026-06 | 388 USD | 2026-06-30 | 500 USD | Cloud SQL 121 · BigQuery 96 · Cloud Run 44 | closed |
| 2026-07 | 91 USD | 2026-07-08 | 500 USD | Cloud SQL 29 · BigQuery 24 · Cloud Run 11 | month-to-date |

### Alerts Configured
- Billing export to BigQuery: dataset `billing`, enabled 2025-09-01
- Budget 500 USD: alerts at 50%, 90%, 100% actual and 100% forecast

### Optimization Log
| Date | Change | Monthly saving |
|------|--------|----------------|
| 2026-05-11 | Private Google Access on all subnets, NAT egress to Google APIs removed | 17 USD |

### Intentionally Idle
| Resource | Project | Monthly | Why it stays | Recheck |
|----------|---------|---------|--------------|---------|
| disk `pg-restore-scratch` | acme-prod | 8 USD | restore-drill target, rebuilt quarterly | 2026-10-02 |
| static IP `legacy-egress` | acme-prod | 3 USD | allowlisted at a partner, removal needs their change window | 2027-01-15 |

## Quotas
| Project | Region | Quota | Limit | Observed peak | Requested | Granted |
|---------|--------|-------|-------|---------------|-----------|---------|
| acme-prod | europe-west1 | CPUs (N2D) | 200 | 148 | 400 | 2026-06-02 |
| acme-ml | europe-west4 | NVIDIA L4 GPUs | 0 | — | 4 | pending 2026-07-21 |

## Service Accounts
| Email | Project | Purpose | Roles | Keys | Federated from |
|-------|---------|---------|-------|------|----------------|
| api-run@acme-prod | acme-prod | Cloud Run `api` runtime | cloudsql.client, secretmanager.secretAccessor | none | — |
| ci-deploy@acme-prod | acme-prod | GitHub Actions deploys | run.admin, artifactregistry.writer | none | WIF pool `github` |

## BigQuery
| Dataset / table | Location | Partition | Cluster | Size | Typical scan | Notes |
|-----------------|----------|-----------|---------|------|--------------|-------|
| analytics.events | EU | `event_date` | `user_id` | 4.2 TB | 18 GB per dashboard refresh | `require_partition_filter` on |

## Pain Points
March 2026: 900 USD in one week from a dashboard running `SELECT *` against `analytics.events` hourly. Sensitive to scan cost since.

## How They Work
Strong on Kubernetes, new to IAM conditions. Wants the command, not the theory.

---
*Updated: 2026-07-26*
```

Rules that keep this readable next month:

- **`## Boxes`**: one line per file that exists — `<what> (<volume>) → <file>; read when <condition>`. Written in the same turn the file is created. Never delete a line without deleting the file it points to. A box with no index line does not exist.
- **`## Due`**: check it against today's date at the start of a session and state any overdue item in one line — a statement, not a question. Every recurring thing this skill schedules belongs here.
- **`## Spend`**: `As of` is the day the number was read. A row whose `As of` is not the last day of the month is month-to-date and must never be compared against a closed month. Re-checking the current month **overwrites** its row; never a second row for the same month. Amounts always carry their currency. `Top services` is the top three, descending, always the same shape — it is what makes a six-month comparison possible without re-querying the billing export.
- **`### Intentionally Idle`**: anything a cleanup sweep found idle and deliberately kept, with the reason and a recheck date. Without it the monthly Recommender pass (`costs.md`) re-proposes the same deletions every month and someone eventually deletes one that was load-bearing. A row whose recheck date has passed is re-evaluated, not renewed silently; a resource that is finally deleted loses its row and gains an `### Optimization Log` entry.
- With `org_model: organization`, add a `Project` column to `### Monthly`: one row for the billing-account total, plus a row for any project above ~20% of it.
- **`## Quotas`**: a quota row exists to stop the same increase being requested twice and to remember that a default was zero. `Observed peak` is what makes the next request credible — an increase asked for without a usage number gets declined.
- **`## Service Accounts`**: `Keys` records the *count and age* of keys, never a key. A row saying `none` is the whole point of the table.
- **`## BigQuery`**: `Typical scan` is the measured dry-run size of the query that runs most often against that table. It is what turns "BigQuery got expensive" into a number in one read.
- These headings are exactly the ones each split-out file gets, so every split stays a copy-paste.

| Status | Meaning |
|-------|---------|
| `ongoing` | Still learning their setup |
| `complete` | Know their projects and workflow well |

## Shared servers inventory

Lives at `~/Clawic/data/servers/servers.md` and is shared with every other infrastructure skill — the user may not have any of them installed, so the format travels with this skill.

```markdown
# Servers

| Name | Provider | Account / Project | Region | Type | Role | Monthly | Access reference |
|------|----------|-------------------|--------|------|------|---------|------------------|
| api-prod-1 | gcp | acme-prod | europe-west1-b | n2d-standard-2 | API | 58 USD | os-login:api-run@acme-prod |
| batch-pool | gcp | acme-prod | europe-west1 | GKE Autopilot | batch cluster | 140 USD | iap:tunnel |
```

- **Identity is `Name` + `Provider`.** Read the file before adding. If that pair is already there, update the row in place — it is yours. The rule against rewriting protects rows whose `Provider` is not `gcp`; never touch those.
- **Retirement is part of the inventory.** When a VM is deleted or a node pool removed, delete its row and note the date in `memory.md`. An inventory that only grows stops being an inventory.
- **Amounts carry their currency in the value** (`58 USD`), because Hetzner rows next to yours are in EUR and someone will add the column up.
- **`Monthly` is a planning estimate, not a bill.** The billing export is the source of truth; after a cost review, refresh any GCP row whose real cost moved more than ~20%. Note in the row when a price already assumes sustained-use or committed-use discount, since an undiscounted N-series estimate reads ~30% high.
- **Scale cut**: one row per host while there are ≤15. Past that, one file per host at `~/Clawic/data/servers/<name>.md` with the same fields, and `servers.md` becomes the index (`Name | Provider | Role | → file`). If you arrive and the folder already looks like that, follow it — do not start a parallel `servers.md`.
- **Foreign columns win.** If `servers.md` already exists with a different column set, match its columns and add anything missing as a trailing note. Never rewrite its header.
- Access reference is a pointer only. Never a key, token, or password. For GCP the useful pointers are `os-login:<service-account-or-user>`, `iap:tunnel`, or `profile:<gcloud configuration>`.
- A managed group (a GKE node pool, a MIG) is one row named after the group, not one row per ephemeral node.

## Shared domains inventory

Lives at `~/Clawic/data/domains/domains.md`, shared with the DNS, hosting and registrar skills. Written whenever a Cloud DNS zone is created or a domain is pointed at a GCP load balancer.

```markdown
# Domains

| Domain | Registrar | Expires | DNS hosted at | Points to | Notes |
|--------|-----------|---------|---------------|-----------|-------|
| acme.com | cloud-domains | 2027-03-14 | Cloud DNS (acme-net) | global ALB 34.x.x.x, managed cert | apex + www |
```

- **Identity is the domain name.** Read before adding; if the domain is there, update the row in place and leave columns another skill filled alone.
- **Never move a domain's registrar row** because GCP happens to host its DNS — `DNS hosted at` and `Registrar` are different columns for exactly this reason.
- Record the managed-certificate dependency in `Notes`: a Google-managed certificate stops renewing the moment the record stops resolving to the load balancer, and the failure surfaces weeks later as an expired cert.
- **Retirement is part of the inventory.** When a domain is let go, transferred away, or its zone deleted, delete the row and note the date in `memory.md`. A row for a domain that expired eight months ago is worse than no row, because the managed-certificate note beside it reads as live.
- **Scale cut**: one table in `domains.md` while it stays under ~40 hostnames. Past that, group **by apex**: one file per apex domain at `~/Clawic/data/domains/<apex>.md` holding every hostname under it, with `domains.md` left as the index (`Domain | Registrar | Expires | → file`). Split by apex, never by hostname — subdomains of one apex share a registrar, an expiry and usually a certificate. If you arrive and the folder already looks like that, follow it — do not start a parallel `domains.md`.
- **Foreign columns win**: match the header you find, never rewrite it.

## Shared contacts box

Lives at `~/Clawic/data/contacts/contacts.md` and is shared with every skill that knows people — the user may not have any of them installed, so the format travels with this skill. Written whenever a project, a billing account or an escalation path has a named human behind it.

```markdown
# Contacts

| Name | Role | Preferred channel | Context |
|------|------|-------------------|---------|
| Marta Ruiz | Platform lead, Beta Ltd | email marta@beta.example | owns beta-delivery; approves quota and budget increases |
```

- **Identity is the email, lowercased** — or the handle when the person has no email on file. Read the file before adding and match on that key. If the person is already there, **update the row in place and extend `Context` rather than replacing it**; another skill wrote what is there. Only the absence of the key justifies a new row.
- **This box holds the person, not the GCP object.** Role, channel and one line of context. Which project they own, their billing account and their folder stay in `projects.md` and reference them **by name only**. Duplicating the person is the fastest way to make two skills disagree about who the contact is.
- **Retirement**: when a person is no longer a contact at all — engagement over and the project handed back, or they left the company — delete the row and note the date in `memory.md`. Ending one engagement while other work continues is not a retirement; update `Context` instead.
- **Scale cut**: one row per person while there are ≤15. Past that, one file per person at `~/Clawic/data/contacts/<name-kebab>.md` with the same fields, and `contacts.md` becomes the index (`Name | Role | → file`). If you arrive and the folder already looks like that, follow it — do not start a parallel `contacts.md`.
- **Foreign columns win.** If `contacts.md` already exists with a different column set, match its columns and add anything missing as a trailing note. Never rewrite its header.
- Channel is how to reach them, never a portal login, an SSH key, a support-case PIN, or a private judgement about them.

## Shared projects box

Lives at `~/Clawic/data/projects/<project>.md`, one file per project from the first, shared with the planning, client and delivery skills. This is the user's **work** project, not a GCP project — the two are different boxes and neither indexes the other (`projects.md` below holds GCP projects).

```markdown
# Beta — data platform migration

status: active            # active | paused | closed | cancelled
client: Beta Ltd          # name only — the person lives in contacts/

## Decisions
| Date | Decision | Who decided | Written back |
|---|---|---|---|
| 2026-07-26 | Serving on Cloud Run, not GKE; ~190 USD/month europe-west1 | Marta Ruiz | diagram in gcp/artifacts/decision-serving-platform.md |
```

- **Identity is the project name, which names the file** (kebab-case). Read it before writing; append a decision row, never a second file for the same project.
- **What GCP writes here is the one-line decision summary and its date.** The diagram, the rejected alternatives and the cost model stay in `~/Clawic/data/gcp/artifacts/<kebab-name>.md` and are referenced from the row by file name — a decision copied in full into two boxes drifts within a quarter.
- **Foreign structure wins.** If the file already exists with different headings, add rows under the closest existing heading rather than imposing this shape. Never rewrite headings another skill created.
- **Closing is a status, not a deletion.** A finished project keeps its file with `status: closed` and the close date; it is the evidence behind the next estimate. Note the close date in `memory.md` too when GCP resources were handed over or torn down.
- Only write here when the user actually tracks the work as a project. If they do not, the decision lives in `artifacts/` alone and nothing goes in this box.

## projects.md

One GCP project lives in `## Org Context`. From the second, this file:

```markdown
# GCP Projects

| Project ID | Number | Purpose | Folder | Owner / client | Billing account | Default region |
|------------|--------|---------|--------|----------------|-----------------|----------------|
| acme-prod | 123456789012 | production API and data | prod | us | 01ABCD-… | europe-west1 |
| acme-net | 210987654321 | Shared VPC host | platform | us | 01ABCD-… | europe-west1 |
| beta-delivery | 345678901234 | Beta Ltd delivery work | clients | Beta Ltd (see contacts) | 02EFGH-… | europe-west4 |
```

When a project belongs to a client, the client goes in the shared box `~/Clawic/data/contacts/contacts.md` under the protocol above — keyed by email or handle, updated in place if already present — and the `Owner / client` cell here holds their name only. Never duplicate the client record inside the GCP box.

Record the project **number** as well as the ID: several IAM bindings, Workload Identity Federation principals and log filters use the number, and looking it up needs an API call the next session should not have to make.

## artifacts/

One file per thing, at `~/Clawic/data/gcp/artifacts/<kebab-name>.md`, created the first time it exists. Canonical types here, with the file name each one takes: **runbook** (`runbook-<symptom>.md`), **IAM policy or custom role that finally worked** (`role-<name>.md`), **a conditional or federated grant and its CEL** (`iam-conditions.md`), **architecture decision** (`decision-<topic>.md`), **org policy set and every exception granted against it** (`org-policies.md`), **agreed RPO and RTO per stateful service** (`dr-targets.md`), **a query whose cost took real work to bring down** (`query-<name>.md`). Every artifact opens with when to read it, and gets its `## Boxes` line in the same turn.

```markdown
# Runbook — checkout 502s
*Read when: checkout returns 502/504. Written 2026-07-26.*

...steps, with every secret replaced by its pointer...
```

```markdown
# Architecture decision — serving on Cloud Run, not GKE
*Read before any change to the request path, and before sizing anything. 2026-07-26.*

Decision: ...one sentence...
Diagram: ...mermaid or ASCII...
Rejected: GKE Autopilot — no Kubernetes API requirement, cluster fee not earned.
Estimated monthly: 190 USD, europe-west1.
First quota: Cloud Run max instances 100. First timeout: backend service 30s.
```

```markdown
# Custom role — deploy-minimal
*Read before granting anything to CI. 2026-07-26.*

Permissions, why each one is present, and what broke without it.
Replaced: roles/editor on ci-deploy@acme-prod.
```

```markdown
# DR targets
*Read before any backup, retention or failover change, and before every restore drill. 2026-07-26.*

| Service | RPO agreed | RTO agreed | Configuration that delivers it | Last measured RTO |
|---------|-----------|-----------|--------------------------------|-------------------|
| Cloud SQL `main` | 5 min | 1 h | PITR on, 7-day window, cross-project export nightly | 41 min (2026-04-02) |
| GCS `assets` | 0 | 15 min | versioning + 30-day noncurrent lifecycle, dual-region | not drilled |

Agreed with: Marta Ruiz, 2026-07-26. A target with no measured restore beside it is an aspiration.
```

If the user tracks this work as a project of their own, the decision summary also belongs in the shared `~/Clawic/data/projects/<project>.md` under the protocol above, with the diagram staying here and referenced by file name. Note the direction: `~/Clawic/data/projects/` holds the user's *work* projects; `~/Clawic/data/gcp/projects.md` holds *GCP* projects. They are different boxes and neither one is the other's index.

## deploys/

```markdown
# Deploys — 2026

| Date | Service | Image digest / commit | Revision or template | Rollback target | Notes |
|------|---------|-----------------------|----------------------|-----------------|-------|
| 2026-07-24 | api | sha256:9f2c… / a41b7e | api-00042-xyz | api-00041-abc | 10% canary for 1h |

## Cluster Upgrades
| Date | Cluster | From → To | Channel | Surge settings | Incidents |
|------|---------|-----------|---------|----------------|-----------|
| 2026-06-18 | batch | 1.31 → 1.32 | regular | max-surge 1, max-unavailable 0 | none |

## Restore Drills
| Date | What was restored | Measured RTO | What was missing |
|------|-------------------|--------------|------------------|
| 2026-04-02 | Cloud SQL PITR → scratch instance | 41 min | CMEK grant, private-IP peering range |
```

Cloud Run revision names are the rollback artifact: a deploy row without the previous revision name is a deploy with no rollback plan written down.

## Split-out files

Created only by the split procedure above, never on day one. Each keeps the exact headings it had inside `memory.md`.

`spend-log.md` — `## Monthly`, `## Alerts Configured`, `## Optimization Log`, `## Intentionally Idle`. The optimization log is the reason this file exists: without it the same idle disks get rediscovered every quarter and nobody can say what the last cleanup was worth.

`resources.md` — the GCP-shaped inventory (`## Compute`, `## Databases`, `## Storage`, `## Networking`, `## Known Gaps`), one `## <project-id>` heading per project when there is more than one.

`quotas.md` — the `## Quotas` table, one `## <project-id>` heading per project once the table covers more than one.

`service-accounts.md` — the `## Service Accounts` table. Once extracted, add a `Last used` column from IAM's usage data: the file's real job becomes finding the accounts nobody has authenticated as in 90 days.

`datasets.md` — the `## BigQuery` table plus a `## Scan Baselines` section: query name, dry-run bytes, when measured. A scan number with no date is not a baseline.
