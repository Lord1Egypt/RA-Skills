## Description:

Helps agents use Coze CLI (@coze/cli) to create, deploy, message, and manage Coze projects and workflows from the terminal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaoliuzhu](https://clawhub.ai/user/chaoliuzhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to operate Coze workspaces and projects through the Coze CLI, including project creation, deployment, messaging, environment management, multimedia generation, and file upload workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to deploy, delete, configure, authenticate, upgrade, or transmit local data through Coze CLI.

Mitigation: Require explicit user approval before deploy, delete, env set/delete, config, auth, upgrade, completion setup, upload, or message commands that transmit local data.

Risk: The skill installs and uses the external @coze/cli package.

Mitigation: Pin and verify the @coze/cli package where possible before installation or upgrade.

Risk: Message and upload workflows may send secrets, confidential source files, or logs to a Coze project.

Mitigation: Use the skill only for intended Coze workspaces and avoid sending secrets or confidential files through message or upload commands.

## Reference(s):

- [Coze CLI Command Reference](references/commands.md)
- [Coze CLI Official Docs](https://docs.coze.cn/developer_guides/coze_cli)
- [Coze CLI Quickstart](https://docs.coze.cn/developer_guides/coze_cli_quickstart)
- [Coze CLI GitHub Repository](https://github.com/copilot66/coze-cli)
- [ClawHub Skill Page](https://clawhub.ai/chaoliuzhu/skills/delonix-coze-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and command reference tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may emit text or JSON through Coze CLI depending on the selected --format option.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
