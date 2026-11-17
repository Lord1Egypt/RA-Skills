## Description:

Map AWS environment against CIS, SOC 2, HIPAA, or PCI-DSS controls with prioritized remediation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anmolnagpal](https://clawhub.ai/user/anmolnagpal)

### License/Terms of Use:


## Use Case:

Developers, cloud security teams, and compliance practitioners use this skill to analyze exported AWS Config and Security Hub data against CIS, SOC 2, HIPAA, or PCI-DSS controls and prepare prioritized remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented minimum IAM policy is broader than the shown export workflow requires and could expose sensitive AWS security posture data.

Mitigation: Review the IAM policy before use, prefer a short-lived read-only role with only the exact AWS Config and Security Hub actions needed for exports, and avoid unused IAM policy-listing permissions unless separately required.

Risk: User-provided exports or pasted cloud data may include credentials or other sensitive account details.

Mitigation: Confirm that submitted data contains no credentials, access keys, or secret keys before analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anmolnagpal/skills/compliance-analyzer)
- [Publisher profile](https://clawhub.ai/user/anmolnagpal)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables, narratives, and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include compliance scores, control status tables, gap priority matrices, remediation runbooks, evidence narratives, and AWS Config rule suggestions based on user-provided exports.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
