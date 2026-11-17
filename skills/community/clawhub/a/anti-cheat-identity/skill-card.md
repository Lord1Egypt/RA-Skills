## Description:

Supports human review of contest submissions by checking submitter and environment consistency and returning structured anti-cheat risk guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Contest organizers and developers use this skill to review submitter identifiers, environment fingerprints, submission counts, and timing for potential anti-cheat concerns. Results support, but do not replace, human decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented identity-review inputs differ from the actual CLI inputs, which can lead to incomplete or incorrect assessments.

Mitigation: Align the CLI inputs with the documented review process and test them before use in a contest.

Risk: Identity-related records and risk scores could be retained or acted on without sufficient privacy or human-review safeguards.

Mitigation: Define privacy and retention controls, limit access, and require human review before consequential decisions.

Risk: The skill declares broader tool access than its local decision-support task appears to require.

Mitigation: Restrict tool permissions to those needed for the actual workflow before installation.

## Reference(s):

- [ClawHub release: anti-cheat-identity](https://clawhub.ai/zhaoxinghua09-cell/skills/anti-cheat-identity)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [JSON with risk level, flags, advice, and status code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI accepts author_id and env_hash, with optional prior fingerprints, submission count, and time gap. Its documented skill-body inputs differ from the actual CLI; confirm inputs before use.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
