## Description:

Pre-deployment governance for release and infrastructure rollout requests that returns deterministic ALLOW, BLOCK, or REQUIRE_REWRITE decisions with strict schema validation, idempotency, and audit artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaicianflone](https://clawhub.ai/user/kaicianflone)

### License/Terms of Use:

MIT

## Use Case:

Developers and release engineers use this skill as a pre-deployment gate for code, configuration, and infrastructure rollout requests. It helps agent-assisted CI/CD workflows check release readiness, rollback coverage, error-budget status, and production rollout safeguards before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unbounded external vote data can be persisted and may exhaust storage or runtime resources in deployment automation.

Mitigation: Require bounded input sizes, maxItems and maxLength limits for external votes and nested strings, artifact-size checks, and rate limits before CI/CD installation.

Risk: State writes can affect sensitive locations if the consensus state path is configured too broadly.

Mitigation: Use a dedicated non-privileged state directory, scoped writable mounts, a non-root execution user, and avoid system, secrets, or shared sensitive directories.

Risk: The skill imports shared consensus dependencies that remain part of the trust boundary.

Mitigation: Pin and periodically audit consensus-guard-core and the lockfile before promotion into deployment automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaicianflone/skills/consensus-deployment-guard)
- [ClawHub publisher profile](https://clawhub.ai/user/kaicianflone)
- [consensus-guard-core npm package](https://www.npmjs.com/package/consensus-guard-core)
- [consensus-guard-core source reference](https://github.com/kaicianflone/consensus-guard-core)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Files]

**Output Format:** [JSON decision object with policy flags, votes, aggregation details, final decision, required actions, and audit write references.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces one of ALLOW, BLOCK, or REQUIRE_REWRITE and writes decision artifacts under the configured consensus state path.]

## Skill Version(s):

0.1.10 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
