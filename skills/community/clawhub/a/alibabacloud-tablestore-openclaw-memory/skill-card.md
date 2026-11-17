## Description:

This skill installs and configures the Tablestore Mem0 plugin for OpenClaw, using Alibaba Cloud Tablestore as a persistent vector backend for agent long-term memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect OpenClaw memory workflows to Alibaba Cloud Tablestore through the Tablestore Mem0 plugin. It guides credential collection, plugin installation, OpenClaw configuration, restart, and verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for powerful Alibaba Cloud credentials and may provision cloud resources.

Mitigation: Use an ECS RAM role or short-lived, least-privilege credentials, and require explicit approval before provisioning resources.

Risk: The skill installs external npm package code.

Mitigation: Verify the package source, version, and integrity before installation, and install only after user consent.

Risk: The skill may expand Tablestore public internet access when VPC access is unavailable.

Mitigation: Do not allow public access changes unless the user accepts the cost and exposure tradeoffs.

Risk: Credential handling during setup can expose AccessKey or DashScope secrets.

Mitigation: Prefer environment variables, avoid pasting secrets into chat, and never commit credentials to version control.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-tablestore-openclaw-memory)
- [RAM Permissions Declaration](references/ram-policies.md)
- [Attach an ECS RAM Role](https://help.aliyun.com/zh/ecs/user-guide/attach-an-instance-ram-role-to-an-ecs-instance)
- [Access Tablestore by RAM User](https://help.aliyun.com/zh/tablestore/developer-reference/access-tablestore-by-ram-user)
- [Tablestore OpenClaw Mem0 npm Package](https://registry.npmjs.org/@tablestore%2fopenclaw-mem0)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before external package installation and cloud resource provisioning.]

## Skill Version(s):

0.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
