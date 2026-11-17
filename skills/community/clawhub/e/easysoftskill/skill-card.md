## Description:

易软（EasySoft）数据查询 Skill。当用户询问易软系统内的数据报表时触发。触发关键词：易软、报表、数据查询、收缴率、预收率、清欠率、欠费、应收、实收、月报。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xjwang2002](https://clawhub.ai/user/xjwang2002)

### License/Terms of Use:

MIT-0

## Use Case:

Property management finance, operations, and management users use this skill to query EasySoft business reports through a conversational agent. It guides credential setup, report selection, report parameters, and tabular display for arrears and related property-management reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests reusable EasySoft business credentials and stores them locally.

Mitigation: Use a dedicated low-privilege EasySoft account, confirm credential storage and deletion behavior before use, and rotate credentials if exposure is suspected.

Risk: Report queries may expose sensitive financial or tenant-related property-management data.

Mitigation: Limit installation and use to authorized users and verify that report access matches the user's business role.

Risk: Entering real passwords through ordinary chat may expose secrets if the host does not provide protected input.

Mitigation: Enter passwords only through a masked secret-entry or verified credential-vault flow provided by the host.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xjwang2002/skills/easysoftskill)
- [Publisher profile](https://clawhub.ai/user/xjwang2002)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Conversational guidance and Markdown tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request EasySoft company key, account, password, report type, project, fee subject, and date range before returning report results.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
