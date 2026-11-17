# Infrastructure as Code — Terraform, Config Connector, Cloud Build, Cloud Deploy

The google provider is mature and the failure modes are specific: identity confusion, resources that force replacement, and state holding secrets. Terraform *language* mechanics — HCL syntax, module design, state surgery — are `terraform`; this file is what is different because the target is GCP.

**Contents:** [Which Tool](#which-tool) · [Provider and Identity](#provider-and-identity) · [State](#state) · [Project Bootstrap Chicken-and-Egg](#project-bootstrap-chicken-and-egg) · [Resources That Force Replacement](#resources-that-force-replacement) · [google vs google-beta](#google-vs-google-beta) · [Importing an Existing Estate](#importing-an-existing-estate) · [Drift](#drift) · [Config Connector](#config-connector) · [Cloud Build](#cloud-build) · [Cloud Deploy](#cloud-deploy) · [Pipeline Safety](#pipeline-safety)

## Which Tool

| Tool | Right when | Cost of owning it |
|---|---|---|
| Terraform (google provider) | Default. Multi-cloud, module reuse, the largest ecosystem | State to manage, and a plan discipline to enforce |
| Config Connector | The team's primary interface is Kubernetes and reconciliation-loop semantics are wanted for cloud resources too | A cluster becomes a dependency of your infrastructure |
| `gcloud` scripts | Never for durable resources. Fine for exploration and one-off operations | Imperative, unversioned, and forgotten |
| Click-ops | Exploration only | Every console change is drift someone else will find |

`iac_tool` decides which dialect every generated artifact uses. Whatever the choice, the rule from SKILL.md Rule 5 holds: the plan comes back clean before any change, or you are about to codify someone's console hotfix as an accident.

## Provider and Identity

- **Terraform authenticates as something other than you.** Locally it uses Application Default Credentials; in CI it uses Workload Identity Federation or an attached service account. A 403 from `terraform apply` is almost always the *automation's* missing role, not yours — check the identity before touching IAM (`iam.md`).
- **Impersonation is the right local pattern**: authenticate as yourself, impersonate the Terraform service account, and get the same permissions as CI without holding a key. Configure it on the provider rather than in shell environment variables, so the configuration travels with the code.
- **`project` is required almost everywhere.** Set it on the provider and let resources inherit; never hardcode a project id in a resource block, because that is what makes a module unusable in a second environment. Use a variable or a `google_project` data source.
- **Provider version pinning is not optional.** The google provider ships frequently and majors change defaults. Pin the major and minor, upgrade deliberately, and read the upgrade guide — a silent default change can produce a destructive plan.
- **APIs must be enabled before their resources exist.** Enabling a service and immediately creating a resource of that type frequently races; add an explicit dependency, and expect the first apply in a new project to need a retry.
- The provider needs `user_project_override` in some cross-project and quota-attribution configurations. When an API call bills or checks quota against the wrong project, that setting is why.

## State

- **Remote state in a Cloud Storage bucket**, with **versioning on** and access restricted to the automation identity. GCS-backed state uses object generation numbers for locking, so there is no separate lock table to operate.
- **The state bucket lives in the platform project**, never in the project it manages. Otherwise deleting the environment deletes the record of the environment.
- **State contains secrets in plain text** — generated passwords, some resource attributes, and anything a provider returns. Treat the bucket exactly like a secret store: private, encrypted, audited, and never copied to a laptop (`security.md`).
- **Split state by lifecycle**, not by team: network, data, application. A single state for everything means one bad change blocks every unrelated deploy and every plan takes minutes.
- Never edit state by hand when a `terraform state` subcommand or an import will do it. If a hand edit is unavoidable, snapshot the bucket object first.

## Project Bootstrap Chicken-and-Egg

Creating projects with Terraform requires solving the ordering problem once:

1. A **bootstrap** configuration, applied by a human with organization-level permissions, creates the seed project, the state bucket, and the Terraform service account with the org-level roles it needs.
2. Bootstrap state can live locally at first and is then migrated into the bucket it just created.
3. Everything after that runs as the Terraform service account, from CI, with no human holding org-level permissions day to day.
4. The Terraform service account needs `roles/resourcemanager.projectCreator` and `roles/billing.user` on the billing account to create and attach projects. Granting billing rights to automation is a real decision — it is also the only way project creation can be code.

Record the bootstrap layout in `~/Clawic/data/gcp/artifacts/` — which project holds state, which identity applies, what was granted at the org node. It is the piece nobody can reconstruct from the code alone (`memory-template.md`).

## Resources That Force Replacement

A plan showing `# forces replacement` on any of these is a data-loss event unless it is intended:

| Change | Effect |
|---|---|
| Project id | New project; the old id is burned forever (`organization.md`) |
| Bucket location or name | New bucket; data must be copied |
| BigQuery dataset location | New dataset; tables must be copied |
| Cloud SQL instance name, region, or private network | New instance; a restore is required |
| Subnet primary range **shrinking** (expanding is in place) | Replacement, and every attached resource with it |
| GKE cluster networking mode, secondary ranges, or Dataplane version | New cluster |
| Disk type in some transitions | New disk |
| CMEK on an existing resource | Usually a new resource |

Put `lifecycle { prevent_destroy = true }` on stateful resources. It converts an accidental destroy into a plan-time error, which is the whole point. Read every plan for replacement markers before applying — a plan skimmed for the resource count is not a plan that was read.

## google vs google-beta

- Beta-only features require the `google-beta` provider, and a resource created with one provider cannot simply be moved to the other by editing the block.
- Mixing both in one configuration is normal and supported. Be explicit about which provider each resource uses rather than relying on a default alias.
- When a feature graduates to GA, migrating the resource is a state operation, not a text edit. Plan it as work.
- A beta resource can change shape between provider releases. Pin harder on anything using `google-beta`.

## Importing an Existing Estate

The common case: a console-built project that now needs to be code.

1. **Inventory first.** Asset Inventory lists everything, including resources whose API nobody remembers enabling (SKILL.md Rule 1). Import against a real list, not against memory.
2. **Import in dependency order**: project and APIs, then network, then IAM, then workloads. Importing a workload before its network produces a plan that wants to recreate the network.
3. **Write the configuration to match reality, then plan.** The plan must come back empty. A non-empty plan after import means the code does not describe what exists, and applying it will change production.
4. **Watch the defaults.** The provider sets defaults for fields the console left implicit; those show as diffs. Set them explicitly to match what exists rather than accepting the provider's opinion.
5. **`import` blocks in configuration** are preferable to the CLI command for anything more than a couple of resources: they are reviewable, and they can generate the configuration.
6. IAM is the hardest part, because the provider offers additive (`_member`), per-role (`_binding`) and authoritative (`_policy`) resources. **Authoritative resources delete every binding they do not manage** — using `google_project_iam_policy` on a project with bindings you have not imported removes them all, instantly. Default to `_member` unless full authority is genuinely wanted.

## Drift

- Drift is any change made outside the code: a console hotfix, a manual quota bump, an autoscaler's decision, or a Google-side default change after a provider upgrade.
- **Run a scheduled plan** (nightly or per-pull-request) and alert on a non-empty result. Finding drift on a Tuesday afternoon is a conversation; finding it mid-incident is an outage.
- **Not all drift is wrong.** Autoscaled node counts and some managed fields change by design — use `ignore_changes` narrowly for those, and never as a way to silence a diff you do not understand.
- The remedy for a console hotfix is to bring it into code the same week, not to revert it during the incident that caused it.

## Cloud Build

- **The build's identity has to be granted first.** Cloud Build runs as a service account whose roles must exist before the first run, or the first deploy fails with a permission error that reads like a bug. Grant what the build deploys, scoped to the target resources (`iam.md`).
- **Private pools** are what let a build reach private resources — a private GKE control plane, a Cloud SQL private IP, an internal registry. The default pool has no VPC access.
- **Build results belong in Artifact Registry**, with images pinned by digest downstream. `gcr.io` addresses now resolve to Artifact Registry, so old references keep working while new work should use the current naming.
- Provenance and attestations from the build feed Binary Authorization, which can require that only images built by your pipeline may be deployed. That is the control that makes "nobody can deploy a laptop-built image" true rather than aspirational.
- Free build minutes per day cover small projects; larger builds bill per minute and a bigger worker is often cheaper than a slow build (`costs.md`).

## Cloud Deploy

- A delivery pipeline with ordered targets (dev → staging → prod), per-target approvals, and canary phases. It renders and applies manifests or Cloud Run configurations rather than executing arbitrary scripts, which is what makes promotion auditable.
- **The release is the artifact.** A release is rendered once and promoted unchanged through targets, so staging and production receive identical configuration. That property is the reason to use it over a hand-built pipeline.
- Rollback is a first-class operation against the previous release, which is exactly the rollback artifact `production.md` insists on naming.
- Verification and post-deploy hooks run as jobs; use them to gate promotion on an SLI rather than on the deploy succeeding.
- Overkill for a single service with one environment. Correct as soon as there is a promotion path that people currently execute by hand.

## Pipeline Safety

- **Plan on pull request, apply on merge**, with the plan output visible in the review. A plan nobody read is not a review.
- **Separate identities for plan and apply**: plan needs read, apply needs write. It is a small amount of setup that removes the largest CI-compromise blast radius.
- **Policy gates** — Terraform policy tooling, Binary Authorization for images, or org policies as the backstop. Org policies are the only one that cannot be bypassed by editing the pipeline, which is why they remain the primary control (`organization.md`).
- **Never let CI hold a service account key.** Workload Identity Federation with an attribute condition on the repository and the ref (`iam.md`).
- **Concurrency control** on the apply job. Two applies against one state produce a lock error at best and a corrupted state at worst.
- Record the pipeline's shape and its identity mapping in `~/Clawic/data/gcp/artifacts/decision-delivery-pipeline.md` with its `## Boxes` line, and every deploy in `deploys/<year>.md` with the rollback target (`memory-template.md`).
