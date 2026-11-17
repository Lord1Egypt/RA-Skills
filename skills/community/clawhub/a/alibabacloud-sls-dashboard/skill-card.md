## Description:

Design and manage Alibaba Cloud SLS dashboards and visualizations, including charts, troubleshooting, and scheduled reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to create, validate, publish, and troubleshoot Alibaba Cloud SLS dashboards and manage scheduled reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTTP endpoint overrides can expose cloud credentials.

Mitigation: Use HTTPS-only endpoints, avoid HTTP overrides, and use a least-privilege Alibaba Cloud profile.

Risk: Publishing, deleting, or scheduling reports can change cloud resources or send reports to unintended recipients.

Mitigation: Confirm the project, dashboard, recipients, and schedule before running commands with --execute.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sdk-team/skills/alibabacloud-sls-dashboard)
- [Dashboard knowledge index](artifact/references/index.md)
- [Environment and CLI setup](artifact/references/cli-installation-guide.md)
- [Dashboard validation checks](artifact/references/validation/checks.md)
- [Alibaba Cloud SLS API documentation](https://help.aliyun.com/zh/sls/developer-reference/api-sls-2020-12-30-createdashboard)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Code]

**Output Format:** [Markdown with shell commands and dashboard JSON configurations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline validation is available; cloud changes require explicit execution.]

## Skill Version(s):

0.0.1 (source: ClawHub release and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
