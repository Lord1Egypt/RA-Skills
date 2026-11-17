## Description:

Determine whether today or a given date is a working day in mainland China by querying holiday-cn yearly JSON from jsDelivr and applying holiday and makeup-workday rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sube-py](https://clawhub.ai/user/sube-py)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, employees, and workflow agents use this skill to decide whether a mainland China date is a workday, including public holidays and makeup workdays.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workday decisions depend on a public jsDelivr-hosted holiday dataset referenced through a mutable branch, so upstream changes or incorrect data can affect results.

Mitigation: For important decisions, review the returned source URL and reason against an authoritative holiday calendar or pin and audit the dataset version before automation.

Risk: Network failures or unavailable yearly data can prevent the helper from returning a workday result.

Mitigation: Use timeout and retry settings appropriate for the workflow and handle command failure explicitly.

## Reference(s):

- [holiday-cn yearly data source](https://cdn.jsdelivr.net/gh/NateScarlet/holiday-cn@master/{year}.json)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON with date, is_workday, reason, and source URL.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Asia/Shanghai by default and accepts an optional YYYY-MM-DD date.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
