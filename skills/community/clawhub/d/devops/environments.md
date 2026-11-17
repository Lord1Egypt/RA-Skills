# Environments — How Many, What Differs, And How Config Gets In

`environment_chain` in `config.yaml` is the promotion path (default `dev → staging → prod`). Every environment added is a gate, a config set, a data policy, and a monthly bill — add one only when it answers a question the others cannot.

**Before answering anything environment-shaped**, read `## Environments` and `## Preview Policy` in `~/Clawic/data/devops/memory.md` (or `envs.md` if `## Boxes` points there) and `~/Clawic/data/servers/servers.md` for the machines behind them. **Read `## Services`** to know which services exist in which environment before proposing a promotion path.

**Contents:** [What Each Environment Is For](#what-each-environment-is-for) · [Parity: What Must Match](#parity-what-must-match) · [Config Injection](#config-injection) · [Preview Environments](#preview-environments) · [Test Data](#test-data) · [Environment Drift](#environment-drift) · [Access And Blast Radius](#access-and-blast-radius)

## What Each Environment Is For

| Environment | The question it answers | Fails at |
|---|---|---|
| Local / dev | "Does my change work at all?" | Anything about scale, real data, or real network paths |
| CI ephemeral | "Does it work from a clean state, reproducibly?" | Long-lived state, integration with third parties |
| Preview (per PR) | "What does this change look and behave like?" | Load, data volume, cross-service versions |
| Staging | "Does the release work against production-shaped wiring?" | Real traffic patterns, real cardinality, real users |
| Production | Everything, at the price of exposure | Nothing — which is why flags and canaries exist |

If two environments answer the same question, one is a bill nobody defends. The common redundancy is a permanent "dev" server that is neither reproducible nor trusted; ephemeral preview environments usually replace it.

## Parity: What Must Match

Parity is expensive; buy it where mismatch has actually bitten. Ranked by how often the mismatch causes a production-only failure:

1. **Data shape and order of magnitude.** A query plan flips when the table is 1000× larger; pagination, timeouts, and N+1 queries only appear at real cardinality. Match the order of magnitude, not the byte count.
2. **Config source and precedence.** Same mechanism everywhere (env vars or a config service), only the values differ. Environments that read config differently produce failures no test can predict.
3. **Identity and permissions.** Staging running with broader IAM than production hides every permission bug until launch day.
4. **Network path.** Same proxy, TLS termination, and egress rules. "Works in staging" where staging talks directly to the database and production goes through a connection pooler is not a test.
5. **Versions of managed dependencies.** Database minor version, runtime version, message broker version. A staging Postgres one major behind is a live trap.
6. **Traffic shape.** Cannot be matched, only approximated — which is why canaries exist (`deploys.md`).

What is fine to differ: replica counts, instance sizes, backup retention, alert routing, log retention. Write each intentional difference into that environment's last column in `## Environments` of `~/Clawic/data/devops/memory.md`; an undocumented difference becomes an assumed bug.

## Config Injection

- **One artifact, config from outside** (SKILL.md Rule 1). Config baked into the artifact means an environment-specific build, which means the tested artifact is not the shipped one.
- **Environment variables for scalars, mounted files for structured or long config**; secrets by reference through `secrets_backend`, never inline (`secrets.md`).
- **Fail fast on missing config at startup**, with the variable name in the error. A service that starts with a missing value and fails on the first request turns a config error into an incident with a confusing signature.
- **Validate the whole config set at deploy time**, before traffic: type, range, and required-ness. Most "bad deploy" incidents are a config typo, not code.
- **Defaults in code must be the safe ones.** A missing feature flag should mean off; a missing timeout should not mean infinite.
- Keep a config diff between environments in review: the diff, not the file, is what people can actually check.

## Preview Environments

One environment per pull request, created on open and destroyed on merge or close.

- **TTL is mandatory** — a common shape is destroy on close plus a hard 72-hour expiry sweep. Without the sweep, abandoned PR environments become the largest untracked line on the bill.
- **Seed data from a fixture set**, never a production copy. A per-PR clone of production data multiplies both cost and exposure.
- **Share expensive dependencies** (one managed database with a schema per preview) unless the change touches the dependency itself.
- **URL and credentials go in the PR**, so review is a click; the environment identity (branch, artifact, URL) belongs in the PR body, not in someone's memory.
- Cost control: previews are the classic runaway. Keep the TTL, the seeding rule, the destroy job, the live count, and the monthly figure with its currency in `## Preview Policy` of `~/Clawic/data/devops/memory.md`; if the destroy job can fail silently, it will.

## Test Data

| Source | Fidelity | Risk | Use when |
|---|---|---|---|
| Hand-written fixtures | Low | None | Unit and integration tests |
| Synthetic generator at production scale | Medium-high on shape, low on weirdness | None | Load tests, query-plan realism (`capacity.md`) |
| Anonymized production copy | High | Real: re-identification, and the copy is now a second production dataset | Only with a documented process and a retention limit |
| Raw production copy | Highest | Unacceptable in most regimes; `compliance_regime` usually forbids it | Never as a default |

Anonymization that preserves distributions is what makes the copy useful; masking every field to `xxx` gives you production volume with fixture-grade realism. Whatever the choice, it is a written decision with an owner — record it as an artifact, because it will be re-litigated.

## Environment Drift

Drift is any difference between what the repo says an environment is and what it actually is.

- Detect on a cadence (`iac-workflow.md`): a scheduled plan that reports a non-empty diff is the alarm. Weekly is a reasonable default; daily if manual console access is common.
- The most common sources: a console hotfix during an incident, a manual scale-up that was never reverted, a secret rotated by hand, and a resource created by a colleague outside the repo.
- Every accepted drift becomes either code or a deletion, in the same week. "We'll reconcile later" is how the plan output becomes 400 lines that nobody reads.
- Config drift is the invisible sibling: compare the *effective* config of each environment periodically, not just the infrastructure.

## Access And Blast Radius

- Production credentials do not exist in dev or staging, and vice versa. Cross-environment credentials turn a staging compromise into a production one.
- Separate accounts/projects/namespaces per environment when the platform allows it — a boundary the platform enforces beats a naming convention people respect.
- Read access to production for debugging is a different grant from write access; most on-call work needs only the first, and issuing only the first removes a whole class of accidents.
- Every human production action goes through an audited path (`compliance_regime` may require the evidence): who, what, when, why, and the record of the change being reproduced in code (SKILL.md Rule 9).

**Write in the same turn**: a new or retired environment, a changed promotion path, or a deliberate parity exception updates `## Environments` in `~/Clawic/data/devops/memory.md`; a preview TTL, seeding rule, destroy job, live count, or monthly figure updates `## Preview Policy` in the same file (both become `envs.md` at the split threshold). Machines behind an environment go to `~/Clawic/data/servers/servers.md`, hostnames and certificate expiry to `~/Clawic/data/domains/domains.md`, and a test-data or environment-topology decision worth re-reading to `artifacts/<kebab-name>.md` with its `## Boxes` line (`memory-template.md`).
