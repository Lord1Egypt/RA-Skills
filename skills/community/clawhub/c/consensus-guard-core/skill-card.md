## Description:

Shared deterministic guard primitives for the Consensus.Tools skill family: hard-block taxonomy, weighted vote aggregation, reputation updates, idempotency keys, strict schema enforcement, and indexed board artifact access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaicianflone](https://clawhub.ai/user/kaicianflone)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to keep consensus guard workflows consistent, replayable, and auditable through shared deterministic policy, reputation, idempotency, validation, and board-artifact primitives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Core approval logic and policy thresholds may be relied on as security infrastructure.

Mitigation: Validate vote objects and policy thresholds before calling aggregateVotes, and review behavior in an isolated environment before promotion.

Risk: Board write helpers can create or update local consensus state artifacts.

Mitigation: Use a dedicated non-privileged consensus state directory, run as a non-root user, and do not pass user-controlled state paths directly to write helpers.

Risk: Runtime dependencies form part of the trust boundary for consensus decisions.

Mitigation: Pin dependencies with the lockfile and audit direct and transitive packages before deployment.

Risk: The server security verdict is suspicious because the package has approval logic and local-write boundaries.

Mitigation: Treat installation as a security-infrastructure review, not as a simple helper-library install.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kaicianflone/skills/consensus-guard-core)
- [Source Repository](https://github.com/kaicianflone/consensus-guard-core)
- [Consensus Tools Upstream](https://github.com/kaicianflone/consensus-tools)
- [README](README.md)
- [Security Assurance Note](SECURITY-ASSURANCE.md)
- [AI Self-Improvement Note](AI-SELF-IMPROVEMENT.md)

## Skill Output:

**Output Type(s):** [JSON, Code, Files, Guidance]

**Output Format:** [JavaScript module exports and structured JSON objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deterministic local behavior; board write helpers can create local state artifacts under the configured consensus state path.]

## Skill Version(s):

1.1.13 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
