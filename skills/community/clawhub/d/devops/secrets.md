# Secrets In The Delivery Path

Scope: how credentials reach a build, a deploy, and a running service — and what to do when one leaks. `secrets_backend` in `config.yaml` selects the store; the pointer scheme is identical whatever the store (SKILL.md, Data).

**Before touching credentials**, read `## Delivery Setup` in `~/Clawic/data/devops/memory.md` for the backend in use and the pointers already recorded, and `## Due` for the rotation and access-review cadences — state any overdue one in a line.

**Contents:** [The Hierarchy](#the-hierarchy) · [OIDC Federation](#oidc-federation) · [Pipeline Permissions](#pipeline-permissions) · [Rotation](#rotation) · [Leak Response](#leak-response) · [Where Secrets Escape](#where-secrets-escape) · [Runtime Delivery](#runtime-delivery)

## The Hierarchy

Prefer the highest row that the platform supports.

| Mechanism | Lifetime | Blast radius if stolen | Use |
|---|---|---|---|
| OIDC / workload identity federation | Minutes to ~1 hour, minted per job | One job, one environment, one role | Default for CI → cloud |
| Short-lived tokens from a secrets manager | Hours | The lease window | Services that cannot federate |
| Static credential in the platform's secret store, scoped per environment | Until rotated | Everything that credential can do, forever | Last resort; needs a rotation cadence |
| Credential in a repo, an image, or a config file | Permanent, and copied | Everyone who ever cloned or pulled | Never |

The jump from row 3 to row 1 removes an entire category of incident: there is nothing at rest to steal, and revocation is automatic.

## OIDC Federation

The CI platform mints a signed token describing the job; the cloud trusts that issuer and exchanges it for a short-lived role session.

- **The trust policy is the security boundary.** Constrain the subject claim to the exact repository *and* the exact ref or environment. A trust policy scoped only to the organization lets any repository in it assume your production role — including a new one created by anyone with repo-creation rights.
- Constrain the audience claim too, and pin the issuer URL. A wildcard subject with a correct audience is still wide open.
- One role per environment, each with only the permissions that environment's deploy needs. The production role is not assumable from a pull-request context.
- Verify by trying: run the assume from a branch that should be denied. A trust policy nobody tested negatively has never been tested.

## Pipeline Permissions

- **Default read-only**, elevate per job. A workflow-wide write token means every step — including a compromised third-party plugin — can push code or publish packages.
- Untrusted contributions (fork PRs) run in a context with no secrets and no cache write access. The dangerous pattern is a workflow triggered by a PR that runs with repository-owner privileges *and* checks out the PR's code (`pipelines.md`).
- Pin third-party actions and plugins by commit SHA. Tags move; a compromised popular action is the classic supply-chain vector (`supply-chain.md`).
- Separate the job that can read secrets from the job that runs arbitrary test code. Tests execute code from dependencies — that is precisely where a secret in the environment gets exfiltrated.
- Deploy approvals bind to the environment, not the workflow, so approval cannot be bypassed by a workflow edit in the same PR.

## Rotation

Rotation is a four-step operation, and skipping the third is the most common mistake (SKILL.md Traps):

1. **Issue** the new credential alongside the old — both valid.
2. **Cut over** every consumer; verify each is using the new one.
3. **Revoke** the old credential explicitly.
4. **Verify** the old one now fails. Until that check passes, nothing was rotated.

Cadence, recorded in `## Due` with its last run:

| Credential type | Cadence |
|---|---|
| Federated / short-lived | None — expiry is the rotation |
| Static credential for a machine consumer | On a written schedule, and on every departure of someone who could read it |
| Human access to production | Access review on a fixed cadence; remove on role change, not just on departure |
| Signing keys | Rarely, with a documented ceremony and an overlap window (`supply-chain.md`) |
| Anything that leaked | Immediately, ahead of everything else |

Automate rotation only where the consumers can pick up a new value without a deploy; otherwise scheduled rotation becomes a scheduled outage.

## Leak Response

Order matters — most teams start at step 3 and lose the window.

1. **Revoke or disable first.** A secret in a public repo is scraped in minutes; deleting the commit does nothing while the credential still works.
2. **Assess the blast radius**: what could that credential reach, and what did it do? Pull the access logs for the credential over its whole lifetime, not just since discovery.
3. **Rotate everything it could have exposed** — a leaked deploy key that could read other secrets means those are leaked too.
4. **Purge from history** only after the above, knowing that any clone or fork still has it and cached views may persist.
5. **Fix the path that let it in**: pre-commit secret scanning, CI scanning of the diff, and a review of why the value existed in plaintext at all.
6. **Write it up**: an incident row and a postmortem if it reached a real system (`incidents.md`). Secret leaks recur when the mechanism is never fixed.

## Where Secrets Escape

| Escape route | Why it happens | Prevention |
|---|---|---|
| Build arguments and image layers | Baked into the artifact; deleting the file in a later layer keeps the earlier one | Secret mounts at build time (`docker`) |
| CI logs | `set -x`, env dumps, verbose HTTP clients, failing test output | Masking plus a rule against printing whole environments |
| Artifact contents | `.env` files or config swept into a tarball or a published package | Explicit include lists, never `**` |
| Error tracking and observability | Request bodies, headers, and query strings captured with the error | Scrubbing rules at the SDK, verified with a test event (`observability.md`) |
| State files and plan output | IaC state stores resource attributes including generated passwords | Encrypted state backends, restricted access, never in a PR comment (`iac-workflow.md`) |
| Backups and database dumps | A dump of the config table is a secret store | Same protection class as the source system (`recovery.md`) |
| Pasted into a chat or a document | Convenience during an incident | A pointer, plus a rotation task if a value was ever pasted |

## Runtime Delivery

- Inject at start (environment or mounted file), never bake into the artifact — environment-specific artifacts break Rule 1.
- Prefer a file mount over an environment variable where the platform allows: environment variables leak through crash dumps, child processes, and diagnostic endpoints.
- Give the application a way to reload a rotated secret without a restart if rotation is frequent; otherwise the rotation cadence must fit the deploy cadence.
- Applications log their config on startup more often than anyone expects. Log key names, never values, and test that with a deliberate fake secret.

**Write in the same turn**: the backend in use and the *pointer* for each credential (`vault:secret/ci/deploy`, `env:DEPLOY_TOKEN`) go in `## Delivery Setup` of `~/Clawic/data/devops/memory.md`. Rotation, access review, and scanning cadences go in `## Due` with their last run. A leak becomes a row in `incidents/<year>.md` plus a postmortem in `artifacts/` (`memory-template.md`). No secret value is ever written under `~/Clawic/data/`, including in text the user pastes for safekeeping — replace each value with its pointer before writing, and say in one line that you did.
