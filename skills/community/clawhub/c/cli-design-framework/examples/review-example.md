# Review Example — `depot`

> A DevOps deployment CLI with subcommands for deploying, rolling back, and promoting services across environments.

## 1. Inferred intent

`depot` appears designed to let DevOps engineers deploy, promote, and roll back services across multiple environments (staging, production) from the terminal. It organizes work around services and environments as durable objects, with deployment operations acting on those objects. Some commands suggest pipeline-style orchestration, but the actual command structure and data model are resource-oriented.

## 2. Classification

- **Primary role:** Capability
- **Primary user type:** Human-Primary
- **Primary interaction form:** Batch CLI
- **Statefulness:** Config-Stateful (deployment state persisted to disk, but no true session identity)
- **Risk profile:** Mixed — reads are safe, but `rollback` and `promote` carry high side-effect risk
- **Secondary surfaces:** Partial `--json` on some commands; `depot status` as a lightweight runtime-observation surface
- **Confidence level:** Medium
- **Hybrid notes:** `deploy`, `rollback`, and `promote` have workflow characteristics (multi-step, stage-dependent). `service list/get` and `env show` are pure Capability CRUD. `status` showing ongoing deployments has a thin runtime-observation quality. The center of gravity is Capability because the durable objects (services, environments, deployment records) are what the CLI primarily controls — workflow steps and runtime observation exist as operations on those objects, not as the core abstraction.
- **Evolution trajectory:** If `depot` adds pipeline definitions, step dependencies, or DAG execution, the center of gravity could shift toward Workflow/Orchestration. Current evidence does not support that classification yet.

### Why Capability, not Workflow

This is the central classification question for `depot`. The help text uses words like "pipeline" and "stages," and commands like `deploy` and `promote` look like workflow steps. However, the actual command structure tells a different story:

- **The nouns are durable resources.** `depot service list`, `depot service get <name>`, `depot env show <env>` — these are CRUD operations on objects that exist at rest. A Workflow CLI's core nouns would be tasks, stages, or pipelines, not services and environments.
- **The verbs operate on resources, not on execution flow.** `depot deploy --service web --env staging` means "act on this resource in this context." A workflow CLI would say `depot run pipeline deploy-web` or `depot trigger staging-pipeline` — the verb targets a *flow*, not an *object*.
- **There is no pipeline definition.** No `depot pipeline create`, no DAG specification, no step-dependency configuration. The "pipeline" language in help text is aspirational framing, not a design reality.
- **State is resource-shaped.** Deployment records are stored as durable artifacts (which service, which version, which environment, when). This is Config-Stateful resource tracking, not sessionful execution state.

A Workflow CLI's center of gravity is the *execution graph* — steps, dependencies, conditions, retries. `depot`'s center of gravity is the *resource graph* — services, environments, deployment records.

### Why not Runtime

`depot status` shows ongoing deployments, which gives it a thin runtime-observation quality. But `depot` does not manage a running process — it fires off deployments and tracks their state. There is no `attach`, no live streaming, no mid-execution steering. `status` is resource-state inspection (like `kubectl get pods`), not runtime-session observation (like `tmux attach`).

## 3. Evidence

**Help output observations:**

- `depot --help` groups commands as: Deploy (`deploy`, `rollback`, `promote`), Services (`service list`, `service get`), Environments (`env show`, `env list`), and Status (`status`). The grouping is resource-oriented: the deployment commands are organized *by what they do to resources*, not *by pipeline stage*.
- `depot deploy --help` says "Deploy a service to an environment" and takes `--service`, `--env`, `--version` flags. This is a resource-mutation signature, not a pipeline-invocation signature.
- `depot rollback --help` says "Roll back a service to the previous deployment." No `--dry-run`, no `--confirm`, no impact preview.
- `depot promote --help` says "Promote a deployment from staging to production." Resource flags, no safety guardrails beyond `--yes`.
**Command structure observations:**

- `depot service list` returns a table of services with columns: NAME, CURRENT_VERSION, LAST_DEPLOY, STATUS. Resource-listing pattern.
- `depot service get <name>` returns detailed service info including deployment history. Resource-detail pattern.
- `depot env show <env>` returns environment configuration. Resource-inspection pattern.
- `depot status` returns currently in-progress deployments. This is the only command with runtime-like behavior.
**Output behavior evidence:**

- `depot service list --json` works. Returns a JSON array of service objects.
- `depot service get <name> --json` works. Returns a JSON service object.
- `depot deploy --json` does **not** work — the flag is silently ignored, and human-readable progress output is emitted regardless.
- `depot rollback` has no `--json` flag at all.
- `depot status --json` works, but the output schema differs from `service list --json` in field naming conventions (`deployedAt` vs `last_deploy`).

**Code path observations:**

- The formatter module has separate table formatters per command with no shared output-contract layer.
- Deploy/rollback/promote call an HTTP API and poll for status; polling output is hardcoded human-readable text.
- No shared confirmation module — `--yes` is implemented ad hoc in `promote` and absent from `rollback`.

## 4. What fits the category well

- **Resource-oriented command structure is clear and learnable.** `depot service list`, `depot service get`, `depot env show` follow a `<noun> <verb>` pattern that a Capability CLI should use.
- **Service and environment as top-level nouns is correct.** The CLI's object model matches what operators actually manage — services are the unit of deployment, environments are the unit of targeting.
- **Human-readable table output for list commands is strong.** Column alignment, status coloring, and sort order are all sensible defaults for a Human-Primary Capability CLI.
- **Help text is well-structured for the basic commands.** `--help` on `service` and `env` subcommands gives clear descriptions with examples.

## 5. Classification mismatches

These are places where `depot` is designed as if it were a *different kind* of CLI than it actually is. These are not execution weaknesses — they are category-level design confusion.

**5a. Pipeline language applied to a resource CLI.**
The help text and README describe `depot` as a "deployment pipeline tool" and use terms like "stages" and "pipeline runs." But nothing in the command structure, state model, or data model implements pipelines. There are no stages, no step dependencies, no conditional execution, no retry policies. This language mismatch creates false expectations: a user reading "pipeline" will look for `depot pipeline run` or `depot stage list` and find nothing. If `depot` is a Capability CLI (which it is), its framing should use resource language: "manage deployments across services and environments," not "orchestrate deployment pipelines."

**5b. `deploy`/`rollback`/`promote` designed as workflow verbs, not resource mutations.**
These three commands are top-level verbs (`depot deploy`, `depot rollback`) rather than actions on a resource (`depot deployment create`, `depot deployment rollback <id>`). This makes them feel like pipeline stages rather than operations on objects. For a Capability CLI, the natural structure organizes mutations under the resource they affect. The current design creates a split personality: half the CLI follows `<noun> <verb>` (correct for Capability) and the other half follows bare verbs (natural for Workflow). This is a classification mismatch, not a style preference.

**5c. `status` designed as a runtime observation command, not a resource query.**
`depot status` shows "ongoing deployments" as a live-feeling status board. But `depot` is not a runtime CLI — it does not manage running processes. The deployment status is a *property of deployment records*, not a *runtime session*. The correct Capability design would be `depot deployment list --status=in-progress`, which treats deployment state as a queryable resource attribute rather than a special runtime view. The current design imports a runtime metaphor into a resource CLI.

## 6. In-category design weaknesses

These are places where `depot` is correctly designed as a Capability CLI but executed poorly *within* that category.

**6a. Inconsistent machine-readable surface.**
`--json` works on `service list`, `service get`, `env show`, and `status`, but not on `deploy`, `rollback`, or `promote`. For a Capability CLI with a machine secondary surface, the contract rule is simple: every command that produces output should support `--json`, and the format should be consistent. The mutation commands are exactly the ones CI pipelines most need structured output from (to capture deployment IDs, track success/failure, feed into downstream automation). Omitting `--json` from mutations while providing it for reads is the worst possible inconsistency — it makes the machine surface useless for the highest-value automation path.

**6b. No field-naming consistency across `--json` outputs.**
`service list --json` uses `last_deploy` (snake_case). `status --json` uses `deployedAt` (camelCase). For a Capability CLI claiming a machine secondary surface, field-name stability and consistency are the baseline contract. Mixed conventions signal that the JSON output was added per-command without a shared schema, which means automation consumers cannot trust field names across commands.

**6c. Destructive operations lack proper risk separation.**
`rollback` has no confirmation, no `--dry-run`, no impact preview. `promote` has only a basic `--yes` bypass with a one-line "are you sure?" prompt that does not describe what will happen. For a Mixed risk profile Capability CLI where `rollback` and `promote` affect production traffic, the risk ladder should be:

- Low-risk (no confirmation): `service list`, `service get`, `env show`, `status`
- Medium-risk (confirm + preview): `deploy` to staging — show what will change, require confirmation
- High-risk (confirm + preview + explicit flag): `promote` to production and `rollback` — show the blast radius (which services, which traffic), require `--confirm` or interactive review, support `--dry-run`

The current design treats all mutations as medium-risk (a basic yes/no prompt) when some are clearly high-risk.

**6d. Silent `--json` flag failure on `deploy`.**
When `depot deploy --service web --env staging --json` is run, the `--json` flag is silently ignored and human-readable output is emitted. Silent flag failure violates a basic hardening rule: unknown or unsupported flags should be rejected with an error. A CI script passing `--json` and receiving human-readable text will break on parse or silently misinterpret the output.

**6e. No deployment ID in mutation output.**
`depot deploy` emits progress text but does not return a deployment identifier for subsequent `status`, `rollback`, or audit queries. For a Capability CLI, mutations should return the identity of the created/modified resource. Without this, correlating a deployment action with its result requires timestamp matching — fragile and error-prone.

## 7. Highest-priority improvements

**1. Unify the command structure under resource-action pattern.**
*Why:* The Capability classification means the command structure should be organized around resources, not bare workflow verbs. Restructure `deploy`/`rollback`/`promote` as actions on a `deployment` resource: `depot deployment create`, `depot deployment rollback <id>`, `depot deployment promote <id>`. This eliminates the split personality (§5b), enables consistent `--json` on all `deployment` subcommands, and makes deployment records first-class queryable objects — which they already are in the data model.

**2. Standardize `--json` across all commands with a shared output contract.**
*Why:* For a Capability CLI with a machine secondary surface, every output-producing command must support `--json` with consistent field naming and stable schema. Implement a shared output layer that enforces snake_case field names, includes a `kind` field for type discrimination, and always returns the affected resource identity on mutations. Reject `--json` with a clear error on commands where it is not yet implemented, rather than silently ignoring it.

**3. Implement a risk ladder for destructive operations.**
*Why:* Mixed risk profile with production-affecting mutations means `rollback` and `promote` need explicit guardrails proportional to their blast radius. Add `--dry-run` (shows what will change without executing) and `--confirm` (interactive impact preview) to all mutation commands. Make `promote --env production` require explicit confirmation with a blast-radius summary by default. This is not generic "add safety" advice — it is a direct consequence of the risk profile classification: production-affecting mutations in a Capability CLI must be separable from staging-safe operations.

**4. Replace pipeline/stage language with resource language in help and docs.**
*Why:* The Capability classification means the mental model should be "manage resources," not "orchestrate pipelines." Rewrite help text and README to describe `depot` as managing services, environments, and deployments — not running pipelines. This eliminates the expectation gap (§5a) and aligns documentation with the actual command structure.

**5. Return resource identity from all mutations.**
*Why:* Capability CLIs must return the identity of created/modified resources so downstream operations can reference them. `depot deploy` should return a deployment ID; `depot rollback` should return the ID of the rollback deployment record; `depot promote` should return the new production deployment ID. This enables `depot deployment get <id>` for audit, `depot deployment rollback <id>` for targeted undo, and reliable CI pipeline chaining.

## 8. Questions to confirm with the user

- **Is pipeline orchestration a future direction?** If `depot` genuinely intends to add pipeline definitions, step dependencies, and DAG execution, the classification should be noted as "Capability evolving toward Workflow/Orchestration," and the command structure recommendations would change. The current review assumes pipeline language is aspirational framing, not a design commitment. If it is a commitment, the review needs revision.
- **Is `promote` always staging→production, or are arbitrary environment promotions planned?** If promotion targets are fixed, the risk model can be simpler (promote always means production, always high-risk). If arbitrary promotion paths are planned (staging→canary→production), the risk model needs to account for variable blast radius per target.
- **Should the machine surface (`--json`) become a strong contract or remain a convenience layer?** If CI/CD pipeline integration is a primary use case, the JSON surface should be versioned, field-stable, and documented as a contract. If it is purely for ad-hoc scripting, a lighter approach is acceptable. The improvements above assume a strong contract is intended — if not, items 2 and 5 can be deprioritized.
