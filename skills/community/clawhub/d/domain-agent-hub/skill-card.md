## Description:

领域专家枢纽 - 智能判断任务领域，优先推荐成熟方案，无成熟方案时扩展创建

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangdaowan](https://clawhub.ai/user/yangdaowan)

### License/Terms of Use:

MIT

## Use Case:

External users and agent operators use this skill to classify a user request by domain, recommend mature tools when available, and route or shape follow-up work for a specialized agent when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill under-discloses effective delegation and local gateway behavior while recommending broad agent routing.

Mitigation: Review the skill before installation and confirm local gateway use, delegation targets, inherited permissions, and any external services before routing tasks.

Risk: Suggested global npm install commands may introduce package provenance or version risk.

Mitigation: Verify package provenance and versions before running global install commands.

## Reference(s):

- [README](artifact/README.md)
- [ClawHub Skill Page](https://clawhub.ai/yangdaowan/skills/domain-agent-hub)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown text with occasional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend external tools or delegate work to specialized agents depending on the task domain.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
