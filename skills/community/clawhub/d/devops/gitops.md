# GitOps — Deploys That Reconcile From A Repository

Applies when `deploy_model: gitops`. The model: a controller inside the target continuously compares declared state in git against live state and converges. Deploying becomes committing; rolling back becomes reverting; drift becomes a metric instead of a discovery.

**Before changing anything in a GitOps repo**, read `## Delivery Setup` in `~/Clawic/data/devops/memory.md` — which controller reconciles which repository path — plus `## Services` and `## Environments` for what it reconciles into, and `releases/<year>.md` for the last synced revision, which is your rollback target.

**Contents:** [What Changes Versus Push Deploys](#what-changes-versus-push-deploys) · [Repository Layout](#repository-layout) · [Promotion](#promotion) · [Sync Behavior](#sync-behavior) · [Secrets In A Public-Shaped Repo](#secrets-in-a-public-shaped-repo) · [When Reconciliation Lies](#when-reconciliation-lies) · [Rollback](#rollback)

## What Changes Versus Push Deploys

| Concern | Push pipeline | GitOps |
|---|---|---|
| Credentials | CI holds deploy credentials for every target | Controller pulls; CI needs no production access |
| Drift | Discovered by a scheduled plan | Corrected continuously, or reported as out-of-sync |
| Audit | Pipeline logs | Repo history is the audit log, per environment |
| Ordering across resource types | Pipeline steps, explicit | Sync waves and health checks, declarative |
| Non-Kubernetes resources | Natural | Awkward unless a controller covers them |
| Debuggability at 3am | Read the pipeline log | Read controller status, which is one more system to know |
| Deploy latency | Immediate | Poll interval or webhook, typically seconds to minutes |

The honest trade (SKILL.md, Where Experts Disagree): GitOps wins on drift, audit, and many clusters; push wins on simplicity and on heterogeneous targets. Mixed estates usually run GitOps for cluster workloads and a pipeline for everything else — that is a legitimate architecture, not a failure to commit.

## Repository Layout

- **Separate the application repo from the delivery repo.** A CI job that commits a new image identity to the delivery repo keeps application history readable and stops reconciliation loops (a controller commit triggering CI triggering a commit).
- One directory per environment, each pinning its own versions. Branch-per-environment looks tidy and produces permanent merge drift; directory-per-environment with an overlay mechanism makes the diff between environments visible in one view.
- The environment directory is the release record: the artifact identity in `prod/` is what is running, and its git history is the deploy log.
- Keep generated manifests out of review noise: review the overlay/values diff, and render the full output only when the base changes.

## Promotion

Promotion is a commit that copies an artifact identity from one environment directory to the next — never a rebuild (SKILL.md Rule 1).

1. CI builds, tests, and pushes the artifact; it writes the identity into `dev/`.
2. A promotion job (or a PR, per `approval_gate`) copies that exact identity into `staging/`, then `prod/`.
3. Each promotion is one small, reviewable diff: an image digest or chart version. A promotion PR touching twenty files is a refactor pretending to be a release.
4. The merge time and the sync completion time are your change lead time (`platform.md`); record the release row when the controller reports healthy, not when the PR merges.

## Sync Behavior

- **Automated sync with self-heal** is the point of the model: manual sync means drift lives until someone notices. Turn self-heal off only for a debugging window, with an expiry.
- **Prune must be deliberate.** Auto-prune deletes resources removed from git — correct, and also the mechanism by which a bad refactor deletes a production namespace. Enable it with a protected-resource annotation on anything holding data.
- **Sync waves** order dependencies: CRDs and namespaces before the workloads that use them; migrations before the app. A wave that never becomes healthy blocks everything after it, which is the intended behavior, not a bug.
- **Health assessment is the gate.** A sync that reports "synced" only means the manifests were applied; "healthy" means the workload passed its checks. Automation must key on healthy.
- Poll interval sets the floor for both deploy latency and drift-correction latency. Webhooks make it immediate; keep polling as the fallback, because a missed webhook is silent.

## Secrets In A Public-Shaped Repo

The repo holds declarative state, so plaintext secrets in it are permanent — git history keeps them after deletion.

| Approach | How it works | Cost |
|---|---|---|
| External secret operator | The repo holds a reference; the controller fetches from `secrets_backend` at reconcile time | One more controller and its credential; the source of truth stays outside git |
| Encrypted-in-repo (SOPS-style, sealed secrets) | Encrypted values are committed; only the cluster can decrypt | Key management and rotation become yours; rotating means re-encrypting everything |
| Nothing in the repo | Secrets injected out of band | Reconciliation cannot rebuild the environment from scratch |

Whichever is chosen, the rule is unchanged: no secret value in the repo, in a values file, in a comment, or under `~/Clawic/data/` — pointer only (`secrets.md`).

## When Reconciliation Lies

| Symptom | Cause | First move |
|---|---|---|
| Repo says v2, cluster runs v1, status is synced | The controller is watching a different path, branch, or revision than you edited | Check the source revision the controller reports, not the repo's HEAD |
| Perpetually out of sync, diff looks empty | A mutating admission controller or the API server rewrites fields the controller then reverts | Ignore-differences rule for those fields, with a comment naming the mutator |
| Sync succeeds, workload never healthy | Health check waits on a dependency in a later wave, or a probe never passes | Read the wave ordering before the manifests |
| A resource keeps coming back after deletion | Self-heal doing its job — it is still in git | Delete it in git; deleting live is never the fix under GitOps |
| Everything reverted at 2am | Someone made a manual change; the controller corrected it as designed | The manual change is the incident, not the controller (SKILL.md Rule 9) |
| Anything else | Compare declared revision, live revision, and health, in that order | The gap between the first two is the whole diagnosis |

## Rollback

Revert the commit that changed the environment directory. The controller converges back; the rollback record is the revert commit plus the row in `releases/<year>.md`.

- Reverting is only complete when the controller reports healthy on the previous revision — a revert that fails to sync is not a rollback.
- Migrations are outside the model's guarantees: the same expand/contract rules apply, and a revert past a contract step corrupts data (`migrations.md`).
- Keep the previous artifact available in the registry for at least the retention window you promise; a garbage-collected image makes the revert unreconcilable (`supply-chain.md`).

**Write in the same turn**: each promotion to production is a row in `~/Clawic/data/devops/releases/<year>.md` with the synced revision and the previous one as the rollback target. A repo layout, prune policy, or secrets-mechanism decision, with what it rejected, becomes `artifacts/<kebab-name>.md` with its `## Boxes` line. The controller and the repository path it reconciles from belong in `## Delivery Setup` of `memory.md`; which services it reconciles into which environment stays in `## Services` and `## Environments` (`memory-template.md`).
