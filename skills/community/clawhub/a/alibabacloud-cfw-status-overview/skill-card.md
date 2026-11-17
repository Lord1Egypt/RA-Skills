## Description:

Alibaba Cloud Firewall Status Overview provides one-click querying of overall cloud firewall status, including asset management, border firewall switch status, and traffic overview.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud security operators use this skill to collect an Alibaba Cloud Firewall status overview from Aliyun CLI commands and produce a concise report covering assets, Internet/VPC/NAT firewall status, and recent traffic. It is intended for read-only operational visibility into configured Alibaba Cloud accounts.

### Deployment Geography for Use:

Global; operational queries are limited by the skill to Alibaba Cloud Firewall regions cn-hangzhou and ap-southeast-1.

## Known Risks and Mitigations:

Risk: The workflow can modify the local Aliyun CLI installation or plugin state before collecting status data.

Mitigation: Review and remove automatic installer and plugin-update steps; use a preinstalled, verified Aliyun CLI.

Risk: Authenticated cloud commands can access account and regional firewall data beyond the intended review scope.

Mitigation: Confirm the exact Alibaba Cloud account and region before execution and grant only read-only Cloud Firewall RAM permissions.

Risk: Access keys or STS tokens may be exposed if they are placed in command-line arguments, prompts, or transcripts.

Mitigation: Use preconfigured credential profiles or external credential setup and do not include any secret values in commands or conversation output.

## Reference(s):

- [Related APIs](references/related-apis.md)
- [RAM Policies](references/ram-policies.md)
- [Verification Method](references/verification-method.md)
- [Acceptance Criteria](references/acceptance-criteria.md)
- [Aliyun CLI Installation Guide](references/cli-installation-guide.md)
- [API Analysis](references/api-analysis.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown summary report with inline shell commands and CLI result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports partial results when individual CLI calls fail; traffic trend outputs are summarized to control response size.]

## Skill Version(s):

0.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
