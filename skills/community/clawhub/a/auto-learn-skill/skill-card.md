## Description:

自动学习技能从对话中提取可复用知识模式，并帮助代理创建或更新持久化技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to identify repeated conversation patterns, extract reusable knowledge, and create or update agent skills for future workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically convert conversation content into persistent skills without clear approval, which may save sensitive or incorrect information.

Mitigation: Require explicit approval, visible diff review, sensitive-data filtering, and rollback before any generated or updated skill is saved.

Risk: Conversation-derived patterns may encode wrong or misleading procedures.

Mitigation: Review, test, and scan generated skills before deployment or sharing.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance and skill file content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or create persistent skill files from conversation-derived patterns.]

## Skill Version(s):

1.0.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
