## Description:

Manage the full lifecycle of Alibaba Cloud PAI DSW (Data Science Workshop) instances, including create, update, query, list, start, stop, and ECS spec lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to manage Alibaba Cloud PAI DSW instances through the Aliyun CLI, including provisioning, configuration changes, status checks, and start or stop operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable installers, latest archives, automatic plugin installation, or broad plugin updates can change what code is executed during setup.

Mitigation: Use a trusted package manager or pinned, verified Aliyun CLI release, and avoid automatic plugin installation or unrelated plugin updates unless the user explicitly accepts that broader change.

Risk: Cloud credentials and RAM permissions can expose or modify Alibaba Cloud resources.

Mitigation: Configure credentials outside the agent session, avoid pasting access keys or tokens into commands or chats, and use narrowly scoped RAM permissions.

Risk: Lifecycle commands can create, update, start, or stop billable PAI DSW resources.

Mitigation: Confirm region, workspace, instance, image, ECS spec, dataset, and network parameters before execution, and use the documented check-then-act workflow before creating or updating resources.

## Reference(s):

- [CLI Installation](references/cli-installation-guide.md)
- [RAM Policies](references/ram-policies.md)
- [Related CLI Commands](references/related-commands.md)
- [Verification Method](references/verification-method.md)
- [Acceptance Criteria](references/acceptance-criteria.md)
- [Common Images](references/common-images.md)
- [PAI DSW API Overview](https://help.aliyun.com/zh/pai/developer-reference/api-pai-dsw-2022-01-01-overview)
- [Create and Manage Workspaces](https://help.aliyun.com/zh/pai/user-guide/create-and-manage-workspaces)
- [Create a DSW Instance Image](https://help.aliyun.com/zh/pai/user-guide/create-a-dsw-instance-image)
- [Aliyun CLI Documentation](https://help.aliyun.com/zh/cli/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON response notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation of cloud resource parameters and existing Alibaba Cloud credentials; commands can manage billable PAI DSW resources.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
