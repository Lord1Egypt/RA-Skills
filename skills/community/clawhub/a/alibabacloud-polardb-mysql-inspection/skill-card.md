## Description:

Inspects Alibaba Cloud PolarDB MySQL instances and generates health reports for individual clusters, multiple clusters, or an account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Database administrators and engineers use this skill to inspect PolarDB MySQL performance, storage, slow queries, sessions, and alerts across selected instances or an account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup and plugin installation or updates can persistently change the local environment.

Mitigation: Review CLI and plugin changes before running; prefer manually verified installation and updates over curl-to-shell or automatic updates.

Risk: Storage analysis uses a backend task permission that is not strictly read-only.

Mitigation: Review the required RAM permissions and grant only the access needed for the inspection.

Risk: Full-account inspection can expose information about every accessible PolarDB MySQL instance.

Mitigation: Confirm the inspection scope and use a least-privilege RAM profile.

Risk: Reports can contain sensitive slow SQL, alert, storage, and live session information.

Mitigation: Store reports in an access-controlled location and limit their distribution.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sdk-team/skills/alibabacloud-polardb-mysql-inspection)
- [RAM permissions](references/ram-policies.md)
- [Report formats](references/report-format.md)
- [Aliyun CLI installation and configuration](references/cli-installation-guide.md)
- [Alibaba Cloud CLI OAuth authentication](https://www.alibabacloud.com/help/en/doc-detail/2995960.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML reports, Guidance]

**Output Format:** [HTML by default; optional Markdown or plain text reports, with the report location returned to the user]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-instance report or a multi-instance report directory with a summary page]

## Skill Version(s):

0.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
