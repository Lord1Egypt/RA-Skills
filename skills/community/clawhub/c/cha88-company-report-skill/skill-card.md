## Description:

Generates company background reports using business registration, legal, intellectual property, operational, and development data, with strengths, risks, and cooperation suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

Business users and analysts can identify a company and request a background report to inform due diligence and potential cooperation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad company-research triggers may start a full background-report task without clear user intent.

Mitigation: Confirm the selected company and obtain user approval before submitting the report task.

Risk: Saved company reports may contain sensitive business, legal, or reputational information, with no specified retention controls.

Mitigation: Ask before saving, agree on a storage location and retention period, and limit access to the report.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/1688aiinfra/skills/cha88-company-report-skill)

## Skill Output:

**Output Type(s):** [Markdown, Text, Files]

**Output Format:** [Markdown company-selection table and full report in chat, with a locally saved report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Company data comes from the ali1688 connector; unsuccessful tasks return an error rather than an analysis.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
