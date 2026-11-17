## Description:

飞书端读取USER.md任务清单，当用户说"查看任务"、"我的任务"时触发，实时解析并返回格式化的分类任务列表，让用户快速了解当前所有可用任务和技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[349840432m-dev](https://clawhub.ai/user/349840432m-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Feishu and OpenClaw users use this skill to read a local USER.md task list and receive a categorized list of tasks, scheduled automations, and trigger phrases for current workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local task-list disclosure through broad Feishu triggers could expose USER.md contents in chat contexts.

Mitigation: Install only where showing ~/.openclaw/workspace/USER.md in Feishu is acceptable, and narrow or remove generic 帮助 and ? triggers if accidental disclosure would matter.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/349840432m-dev/skills/feishu-user-md)
- [ClawHub publisher profile](https://clawhub.ai/user/349840432m-dev)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, json]

**Output Format:** [Plain text formatted for Feishu, or JSON when invoked with the json command.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads ~/.openclaw/workspace/USER.md at execution time and does not cache results.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and claw.json state 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
