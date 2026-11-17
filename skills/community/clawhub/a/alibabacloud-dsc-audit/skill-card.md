## Description:

Query and handle security risk events from Alibaba Cloud Data Security Center, including unprocessed-risk listing and manual handling workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud security operators use this skill to inspect Alibaba Cloud Data Security Center risk events, page through processed or unprocessed findings, and manually record handling decisions for a confirmed RiskId.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup guidance includes a curl-to-bash installer and automatic Aliyun CLI plugin changes.

Mitigation: Install the Aliyun CLI and plugins through reviewed, trusted, and pinned methods before using the skill.

Risk: Handling a risk event can change Alibaba Cloud Data Security Center risk-event state.

Mitigation: Use a least-privilege RAM role and grant PreHandleAuditRisk only to users approved to change risk-event status.

Risk: Cloud operations require credentials and can expose sensitive account access if run in an overprivileged profile.

Mitigation: Confirm credential status without printing secrets and prefer scoped temporary or role-based credentials for agent sessions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-dsc-audit)
- [Data Security Center API Reference](artifact/references/related-apis.md)
- [Data Security Center RAM Permission Configuration](artifact/references/ram-policies.md)
- [Aliyun CLI Installation and Configuration Guide](artifact/references/cli-installation-guide.md)
- [Acceptance Criteria](artifact/references/acceptance-criteria.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and script output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires confirmed Alibaba Cloud parameters, a valid session-scoped user agent identifier, and explicit RiskId and HandleDetail values before handling risk events.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
