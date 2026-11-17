## Description:

AgentLove is a Chinese-first OpenClaw setup wizard that guides users through backup migration, robot configuration, and marriage evolution planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bdodh22](https://clawhub.ai/user/bdodh22)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to plan a new agent setup through a structured conversational checklist. It collects preferences, summarizes configuration choices, and directs users to perform agent creation, skill installation, and credential setup manually in the appropriate consoles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake the generated setup checklist for completed agent creation, backup, platform binding, or skill installation.

Mitigation: Treat the output as planning guidance and verify each required action in OpenClaw or ClawHub before relying on the configuration.

Risk: Users may paste credentials, platform secrets, or personal data into the chat during setup.

Mitigation: Enter secrets only in the official OpenClaw console and avoid sharing sensitive data with the skill.

Risk: Recommended skills may introduce their own permissions, behavior, or operational risks.

Mitigation: Review and approve each separately recommended skill before installation.

## Reference(s):

- [AgentLove ClawHub Page](https://clawhub.ai/bdodh22/skills/agentlove)
- [AGENTS - 5种工作规则类型](references/agents.md)
- [配置参考](references/configs.md)
- [执行说明](references/execution.md)
- [IDENTITY - 6种身份类型](references/identity.md)
- [基础层配置](references/layer1-base.md)
- [渠道增强层配置](references/layer2-channels.md)
- [Skills 推荐配置](references/layer3-skills.md)
- [人格配置](references/personality.md)
- [预设角色库](references/presets.md)
- [SOUL - 16种性格类型](references/soul.md)
- [故障排查](references/troubleshooting.md)
- [USER - 13种协作规则类型](references/user.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with configuration summaries and JSON-style checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill produces planning guidance only; users must complete agent creation, skill installation, platform binding, and credential entry outside the chat.]

## Skill Version(s):

2.9.6 (source: release evidence, frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
