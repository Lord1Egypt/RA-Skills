## Description:

Pre-execution governance for IAM and permission escalation changes, producing deterministic ALLOW, BLOCK, or REQUIRE_REWRITE decisions with strict schema validation, idempotency, and board-native audit artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaicianflone](https://clawhub.ai/user/kaicianflone)

### License/Terms of Use:

MIT

## Use Case:

Developers and platform engineers use this skill as a pre-execution gate for temporary admin elevation, service-account scope expansion, break-glass access requests, and production IAM permission changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Caller-supplied policy constraints can influence high-impact permission escalation decisions.

Mitigation: Supply policy constraints from trusted deployment configuration rather than from the requester.

Risk: External-agent votes can affect approval outcomes without sufficient trusted scoping.

Mitigation: Accept external votes only after authentication or signature checks, duplicate detection, freshness checks, and inclusion of vote evidence in replay decisions.

Risk: State and decision artifacts are written to configured filesystem paths.

Mitigation: Run with a dedicated non-privileged state directory, constrained filesystem permissions, and a non-root runtime user.

Risk: Runtime behavior depends on npm dependencies including consensus-guard-core.

Mitigation: Pin and audit dependencies before deployment and review consensus-guard-core as part of the trust boundary.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaicianflone/skills/consensus-permission-escalation-guard)
- [Security Assurance Note](artifact/SECURITY-ASSURANCE.md)
- [Input schema](artifact/spec/input.schema.json)
- [consensus-guard-core npm package](https://www.npmjs.com/package/consensus-guard-core)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [JSON, Files, Guidance]

**Output Format:** [JSON decision response with audit artifact references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns ALLOW, BLOCK, or REQUIRE_REWRITE with policy flags, votes, aggregation details, required actions, and board write references.]

## Skill Version(s):

0.1.13 (source: evidence.release.version and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
