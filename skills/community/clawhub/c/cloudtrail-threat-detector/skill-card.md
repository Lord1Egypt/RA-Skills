## Description:

Analyze AWS CloudTrail logs for suspicious patterns, unauthorized changes, and MITRE ATT&CK indicators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anmolnagpal](https://clawhub.ai/user/anmolnagpal)

### License/Terms of Use:


## Use Case:

Security teams and developers use this skill to review user-provided AWS CloudTrail exports for suspicious activity, build an incident timeline, map findings to MITRE ATT&CK Cloud techniques, and identify containment actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented minimum AWS IAM policy is broader than the shown export workflow requires.

Mitigation: Review and narrow the AWS IAM policy before use, grant only the specific read actions and log resources needed for the chosen export method, prefer a temporary role, and do not provide AWS credentials to the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anmolnagpal/skills/cloudtrail-threat-detector)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with tables and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses only user-provided CloudTrail data; does not access AWS accounts directly.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
