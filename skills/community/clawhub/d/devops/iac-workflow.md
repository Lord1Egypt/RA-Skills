# Infrastructure As A Delivery Process

Scope: the workflow around infrastructure code — review, apply, drift, state layout, policy. The language itself belongs to its own skill (`terraform` for HCL mechanics). `iac_tool` in `config.yaml` selects the dialect; while unset, say which one you are assuming.

**Before proposing a change**, read `## Environments` and `## Services` in `~/Clawic/data/devops/memory.md` and `~/Clawic/data/servers/servers.md` — what exists, in which environment, and who owns it. **Check `## Due`** for the drift-detection cadence and state whether it is overdue in one line.

**Contents:** [The Pipeline For Infrastructure](#the-pipeline-for-infrastructure) · [Splitting State By Blast Radius](#splitting-state-by-blast-radius) · [Drift](#drift) · [Policy As Code](#policy-as-code) · [Applying Safely](#applying-safely) · [Module Releases](#module-releases) · [Importing What Already Exists](#importing-what-already-exists)

## The Pipeline For Infrastructure

Same discipline as application delivery, different artifact: the plan is the artifact.

| Stage | On a pull request | On merge |
|---|---|---|
| Format + validate | Blocking | — |
| Lint + policy check | Blocking, with the failing rule named | Re-run |
| Plan | Posted to the PR, per environment | Re-planned; **apply the saved plan file**, not a fresh one |
| Cost estimate | Advisory comment; blocking above a threshold if the team wants one | — |
| Apply | Never from a PR | Gated by `approval_gate`, then applied to the environment in order |

- **Apply the plan you reviewed.** A fresh plan at apply time can differ from the one approved (someone else applied in between, a data source moved). Save the plan artifact in the PR job and consume it in the apply job.
- Plan output in a PR comment is the review surface: a diff nobody can read is a review that did not happen. Keep the noisy providers' spurious diffs out with lifecycle rules so the signal survives.
- Promote environment by environment along `environment_chain`. Same code, different variable set — never a separate branch per environment, which guarantees drift between them.
- The pipeline's credentials are per-environment and short-lived (`secrets.md`); the production apply role is not usable from a PR job.

## Splitting State By Blast Radius

One state file for everything means every change waits behind every other change, and one bad apply can destroy unrelated resources.

Split by lifecycle and ownership, roughly:

| Layer | Changes | Contains |
|---|---|---|
| Foundation | Rarely | Accounts, networks, DNS zones, identity |
| Data | Occasionally, carefully | Databases, buckets, queues with retained data |
| Platform | Regularly | Clusters, load balancers, shared services |
| Application | Constantly | Services, deployments, per-app resources |

- Cross-layer references go one way: application reads foundation outputs, never the reverse. A cycle between states cannot be created or destroyed in any order.
- Anything holding data gets deletion protection and a lifecycle rule preventing accidental destroy. The apply that says "1 to destroy" on the data layer stops the pipeline until a human explains it.
- Small teams start with two states (foundation+data, everything else) and split further when an apply takes long enough to block someone.

## Drift

Drift is the difference between the declared state and reality (`environments.md` covers the environment-level view).

- **Detect on a schedule**: a plan run against every environment, reporting non-empty diffs to a channel a human reads. Weekly by default; daily where console access is routine. The cadence is a row in `## Due`.
- Classify every diff: (a) someone's console fix → codify it or revert it this week; (b) provider-side churn (fields the cloud rewrites) → suppress with a lifecycle rule and a comment saying why; (c) real unmanaged resource → import it or delete it.
- A drift report nobody triages trains the team to ignore the plan output — which is the mechanism by which a real destroy gets approved.
- After every incident that involved a manual production change, the follow-up action is "reconciled in code", with a date (`incidents.md`).

## Policy As Code

Checks that run in the pipeline and fail the PR, with the rule named in the failure. Worth encoding, in order of return:

1. No resource holding data without deletion protection and a backup configuration.
2. No storage or database reachable from the public internet unless explicitly annotated with a reason.
3. No permissions granting a wildcard action on a wildcard resource.
4. No unencrypted storage, and encryption keys are not created ad hoc per resource.
5. Required tags present (owner, environment, service) — untagged spend is unattributable forever, because most cost-allocation systems only report from activation forward.
6. Instance types and regions within the allowed set (cost and data-residency control).

Each rule needs an escape hatch with an owner and a comment, or engineers route around the whole system. A policy with no documented exception path becomes a policy people disable.

## Applying Safely

- **Never apply from a laptop** to a shared environment. Local applies produce state nobody else can reproduce and lock files nobody else can clear.
- **Target flags are an incident tool, not a workflow.** A targeted apply leaves the rest of the configuration unapplied and the next full apply surprising.
- Locking must be real (a backend that supports it). Two concurrent applies against one state corrupt it, and recovery costs hours.
- Refresh behavior matters: a plan that skips refresh is fast and can be wrong; one that refreshes is slow and true. Pick deliberately per layer, and refresh before anything destructive.
- Destroy is a separate, manually invoked job with a typed confirmation of the environment name. It never lives in the same job as apply.
- Keep state backends versioned so a corrupt state can be rolled back to the previous revision — this is the only real recovery for state loss.

## Module Releases

- A shared module is a product with consumers: version it, tag it, and let consumers pin. Consumers referencing a branch get changes they did not ask for at the worst time.
- Breaking changes get a major version and a migration note; the note is what makes the upgrade cheap enough to happen.
- Test a module against a scratch environment before tagging: `plan` alone does not prove the resources can actually be created together.
- Keep module count low enough that the team can read them. A wrapper module that adds no defaults and no policy is indirection with a maintenance cost.

## Importing What Already Exists

- Write the resource block first, then import, then plan until the diff is empty. A non-empty diff after import means the code does not describe reality — applying it will change or replace the live resource.
- Import one resource at a time for anything with data. Bulk import plus a hasty apply is the fastest known way to replace a production database.
- Record what was imported and why in `## Pain Points`; the inherited-account archaeology is exactly the work nobody wants to repeat (`recovery.md` for what happens if it goes wrong).

**Write in the same turn**: the drift cadence and its last run go in `## Due` of `~/Clawic/data/devops/memory.md`; a state layout or policy decision, with what it rejected, becomes `artifacts/<kebab-name>.md` with its `## Boxes` line; resources that are machines go to `~/Clawic/data/servers/servers.md` and DNS records to `~/Clawic/data/domains/domains.md`; a manual production change and its reconciliation date go in `## Pain Points` (`memory-template.md`). Backend credentials and state-encryption keys are pointers (`env:TF_TOKEN`, `vault:secret/ci/state`), never values.
