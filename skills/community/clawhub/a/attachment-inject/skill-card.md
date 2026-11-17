## Description:

Dynamic attachment injection adds changing agent and skill context as attachments instead of embedding it directly in the system prompt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxiaofei860208-source](https://clawhub.ai/user/wangxiaofei860208-source)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to manage dynamic agent, skill, and memory context through lightweight registries and on-demand reads without repeatedly changing the system prompt.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can influence how agents and skills are discovered, summarized, and injected into context.

Mitigation: Review workspace paths before use, prefer allowlists or explicit approval for registry generation, and scan the skill before deployment.

Risk: Broad read/write behavior can modify context files such as registries or AGENTS.md placeholders.

Mitigation: Review generated file changes before accepting them and limit writes to the intended agent, skill, or memory registry locations.

## Reference(s):

- [ClawHub release: Attachment Inject](https://clawhub.ai/wangxiaofei860208-source/skills/attachment-inject)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to create lightweight registry files and dynamic injection placeholders.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
