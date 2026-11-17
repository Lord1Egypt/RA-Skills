## Description:

AI员工协作技能包 - 多AI角色配置、任务自动分配、进度监控、结果汇报。适合想要自动化运营的团队。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gdp6539](https://clawhub.ai/user/gdp6539)

### License/Terms of Use:

MIT

## Use Case:

Independent developers, small teams, content operators, project managers, and automation users can use this skill to organize AI roles, assign and track work, monitor status, and produce recurring work reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local file handling is under-scoped and can escape intended directories through unvalidated inputs.

Mitigation: Use the skill only in a dedicated workspace with non-sensitive data, avoid untrusted role or template inputs, and review path validation before using it with business or private information.

Risk: The skill writes persistent configuration and memory files.

Mitigation: Review generated config and memory directories regularly, define retention controls, and remove data that should not persist.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gdp6539/skills/ai-employee-skill)
- [Publisher Profile](https://clawhub.ai/user/gdp6539)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and JavaScript code behavior]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local configuration and memory files when its employee-management script is executed.]

## Skill Version(s):

1.0.0 (source: frontmatter, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
