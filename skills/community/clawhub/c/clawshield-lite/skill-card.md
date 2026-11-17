## Description:

Scans AI skills for potential security risks and unsafe commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thenox21](https://clawhub.ai/user/thenox21)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run lightweight static checks over AI skill source code and produce a structured security risk report before installation or review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A SAFE result can miss obfuscated or semantically equivalent risky code because the scanner is a lightweight local heuristic checker.

Mitigation: Supplement results with manual review or stronger static analysis before trusting or deploying a scanned skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thenox21/skills/clawshield-lite)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Guidance]

**Output Format:** [JSON report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports matched patterns, severity, explanations, and an overall SAFE, MEDIUM RISK, or HIGH RISK classification.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
