## Description:

Creates AI-agent boarding-pass records with identity labels, evidence hashes, permission lists, and expiry times, and checks their checksum and expiry.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use the skill to issue and check time-limited agent boarding-pass records for coordination and review; the records do not establish issuer identity or authorize sensitive access on their own.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A checksum can be recomputed by anyone and cannot prove who issued a pass or granted its permissions.

Mitigation: Do not use boarding passes as authorization for sensitive data or actions without a trusted issuer mechanism such as digital signatures.

Risk: The skill reads and can write local files despite declaring no filesystem access.

Mitigation: Review file inputs and output destinations and limit the agent's filesystem access before use.

## Reference(s):

- [ClawHub release: agent-boarding-pass](https://clawhub.ai/zhaoxinghua09-cell/skills/agent-boarding-pass)
- [Agent Boarding Pass documentation](artifact/README.md)

## Skill Output:

**Output Type(s):** [JSON, Text, Files]

**Output Format:** [JSON boarding pass or verification result; optional local JSON file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes evidence hashes, permission list, expiry, and SHA-256 checksum; verification reports checks and an exit status.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata; artifact frontmatter says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
