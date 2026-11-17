## Description:

Risk-aware support response governance for customer-facing automation that detects legal, sensitive-data, and confidentiality issues, applies hard-block policy checks, and records auditable decision artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaicianflone](https://clawhub.ai/user/kaicianflone)

### License/Terms of Use:

MIT

## Use Case:

Support teams and automation developers use this skill to review proposed customer support replies before sending, returning allow, block, or rewrite decisions with consensus-weighted reasoning and audit records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Support draft text and audit records may be written to the configured local consensus state path.

Mitigation: Use an approved state location, restrict file permissions, and confirm the path is acceptable for support content before production use.

Risk: Dependency hygiene requires review before production deployment.

Mitigation: Pin and review npm dependencies, and update scanner-flagged transitive packages before installing in production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaicianflone/skills/consensus-support-reply-guard)
- [consensus-guard-core npm package](https://www.npmjs.com/package/consensus-guard-core)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [json, text, guidance]

**Output Format:** [JSON decision object with allow, block, or rewrite status and auditable decision metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write decision artifacts under the configured consensus state path.]

## Skill Version(s):

1.1.15 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
