## Description:

Query and analyze security events and alerts detected by Alibaba Cloud Firewall IPS to help locate threats and provide remediation recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security operators use this skill to collect read-only Alibaba Cloud Firewall IPS alert data through Aliyun CLI and turn it into a concise incident analysis and remediation report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions can execute remote installer code.

Mitigation: Review setup steps before installation and prefer a trusted package manager or verified pinned download for Aliyun CLI.

Risk: Automatic plugin installation and AI-mode settings can persistently change local CLI behavior.

Mitigation: Enable these settings only when needed for the workflow, verify plugin updates, and disable AI-mode at every workflow exit point.

Risk: Cloud credentials may be exposed if access keys are pasted into agent-visible commands or transcripts.

Mitigation: Use a dedicated read-only RAM profile for Cloud Firewall queries and never paste real access keys into command lines or conversation text.

## Reference(s):

- [API Analysis](references/api-analysis.md)
- [Related APIs](references/related-apis.md)
- [RAM Policies](references/ram-policies.md)
- [Verification Method](references/verification-method.md)
- [Acceptance Criteria](references/acceptance-criteria.md)
- [Aliyun CLI Installation & Configuration Guide](references/cli-installation-guide.md)
- [Skill release page](https://clawhub.ai/sdk-team/skills/alibabacloud-cfw-ips-event)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, API Calls, Guidance]

**Output Format:** [Markdown report with inline Aliyun CLI commands and tabular security analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Alibaba Cloud Firewall IPS queries; results depend on configured Aliyun CLI credentials, RAM permissions, selected region, and time range.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
