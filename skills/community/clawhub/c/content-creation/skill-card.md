## Description:

部署内容创作 Agent 团队（墨白主编、探风选题、锦书文案），通过交互式引导收集品牌信息并自动配置 OpenClaw 工作区。

This skill is ready for commercial/non-commercial use.

## Publisher:

[little-ke](https://clawhub.ai/user/little-ke)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, operators, and developers use this skill to deploy a three-agent OpenClaw content team for topic planning, editorial review, and article drafting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup script has a local command-injection risk around shell interpretation, especially when OPENCLAW_HOME is controlled or malformed.

Mitigation: Fix command execution before installation and review generated commands before running the skill.

Risk: The skill makes persistent OpenClaw workspace and agent registration changes without strong consent or rollback guidance.

Mitigation: Tell users exactly which files and agents will be created, request explicit confirmation before deployment, and provide removal steps for workspaces and registered agents.

Risk: The skill stores brand and content strategy information in local workspace Markdown files.

Mitigation: Disclose what information is stored and avoid entering sensitive brand or credential data unless the workspace is appropriately protected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/little-ke/skills/content-creation)
- [Publisher profile](https://clawhub.ai/user/little-ke)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with shell commands and generated OpenClaw workspace files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates persistent OpenClaw agent workspaces and stores user-provided brand and content preferences in workspace Markdown files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
