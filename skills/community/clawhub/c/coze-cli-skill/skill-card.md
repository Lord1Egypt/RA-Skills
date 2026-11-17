## Description:

Interact with Coze CLI (@coze/cli) to create and deploy Coze projects, manage spaces and organizations, send messages, generate media, upload files, and automate Coze workflows from the terminal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cengsin](https://clawhub.ai/user/cengsin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to operate Coze CLI workflows, including project creation, deployment, messaging, media generation, file upload, and workspace configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent through remote messaging, file upload, production deployment, environment variable changes, project deletion, and commands that may expose logs, source code, credentials, or personal data.

Mitigation: Require explicit user approval before uploads, file- or pipe-based message sends, production deploys, environment variable changes, project deletion, and commands that disclose sensitive outputs.

Risk: Security evidence marks the release suspicious because the skill grants broad Coze CLI operational capability without enough built-in safety scoping.

Mitigation: Review before installing and restrict use to sessions where the user intends the agent to operate Coze CLI.

## Reference(s):

- [Coze CLI command reference](references/commands.md)
- [Coze CLI Official Docs](https://docs.coze.cn/developer_guides/coze_cli)
- [Coze CLI Quickstart](https://docs.coze.cn/developer_guides/coze_cli_quickstart)
- [Coze CLI repository](https://github.com/copilot66/coze-cli)
- [ClawHub skill page](https://clawhub.ai/cengsin/skills/coze-cli-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/cengsin)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Coze CLI text or JSON output format guidance when scripting is requested.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
