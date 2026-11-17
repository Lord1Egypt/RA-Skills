## Description:

Alibaba Cloud Resource Center - Global Resource Inventory, Search & Statistics Skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to search, inventory, inspect, and count Alibaba Cloud Resource Center resources across regions, products, and accounts. It also guides service activation, tag discovery, and Resource Center troubleshooting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may direct users toward unverified installer execution for the Aliyun CLI.

Mitigation: Use a preinstalled, audited Aliyun CLI and do not run `curl | bash` installer commands from an agent session.

Risk: The skill may make broad, persistent Aliyun CLI plugin or configuration changes.

Mitigation: Review plugin and CLI configuration changes before installation, and avoid enabling global auto-plugin installation unless explicitly approved.

Risk: Resource inventory and cross-account operations can expose broad cloud asset visibility.

Mitigation: Use read-only Resource Center permissions for inventory workflows and restrict cross-account scope to the narrowest appropriate account, folder, or directory target.

Risk: Cloud credential handling can create account access risk.

Mitigation: Configure credentials outside the agent session and prefer short-lived or role-based credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-resourcecenter-search)
- [Related APIs - Resource Center](references/related-apis.md)
- [RAM Policies - Resource Center](references/ram-policies.md)
- [Verification Method - Resource Center](references/verification-method.md)
- [Resource Center API error codes](references/error-codes.md)
- [Aliyun CLI Installation & Configuration Guide](references/cli-installation-guide.md)
- [Acceptance Criteria: alibabacloud-resourcecenter-search](references/acceptance-criteria.md)
- [Official Aliyun CLI documentation](https://help.aliyun.com/zh/cli/)
- [Aliyun CLI plugin repository](https://github.com/aliyun/aliyun-cli)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Code, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON-producing helper script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper script prints compact JSON on stdout for resource type discovery; cloud command output depends on the Aliyun CLI and Resource Center APIs.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
