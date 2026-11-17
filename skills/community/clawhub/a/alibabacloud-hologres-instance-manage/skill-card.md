## Description:

Alibaba Cloud Hologres Instance Management Skill for listing and querying Hologres instances.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to inspect Alibaba Cloud Hologres estate state by listing instances and retrieving read-only instance details through Aliyun CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup guidance may ask users to run mutable remote installers for Aliyun CLI.

Mitigation: Review installation steps before use and prefer a verified, already installed Aliyun CLI.

Risk: Plugin setup may change persistent CLI behavior through automatic plugin installation or blanket plugin updates.

Mitigation: Avoid persistent automatic plugin installation and review plugin updates before applying them.

Risk: Cloud credentials can be exposed if long-lived access keys are pasted into agent-visible commands or logs.

Mitigation: Use least-privilege RAM roles or short-lived credentials scoped to Hologres read-only access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-hologres-instance-manage)
- [Aliyun CLI installation guide](references/cli-installation-guide.md)
- [RAM permissions required](references/ram-policies.md)
- [Related CLI commands](references/related-commands.md)
- [Success verification method](references/verification-method.md)
- [Acceptance criteria](references/acceptance-criteria.md)
- [Hologres ListInstances API documentation](https://api.aliyun.com/api/Hologram/2022-06-01/ListInstances)
- [Hologres error center](https://api.aliyun.com/document/Hologram/2022-06-01/errorCode)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and command explanations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are read-only operational guidance for Aliyun CLI Hologres instance queries.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
