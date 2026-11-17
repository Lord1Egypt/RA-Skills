## Description:

Creates new OpenClaw agents and binds them to Feishu group chats by collecting requirements, confirming an agent card, generating configuration files, and providing setup commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuanyizhi](https://clawhub.ai/user/xuanyizhi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw administrators use this skill to create a new agent, define its behavior and permissions, and bind it to a Feishu group chat. It supports requirement gathering, agent card confirmation, configuration file generation, group allowlist checks, binding, testing, and operational notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives high-impact OpenClaw and Feishu configuration instructions without enough validation or containment.

Mitigation: Use it only in a trusted administrator context, strictly validate agent names and group IDs, and review exact OpenClaw and Feishu configuration changes before execution.

Risk: Generated behavior text or free-form prompts may be written into shared operational memory.

Mitigation: Avoid writing free-form user prompts or generated behavior text into shared MEMORY.md unless an administrator has reviewed and approved the content.

## Reference(s):

- [Agent Card Template](references/AGENT-CARD-TEMPLATE.md)
- [OpenClaw Agent Creation Guide](references/AGENT-CREATION-GUIDE.md)
- [ClawHub Skill Page](https://clawhub.ai/xuanyizhi/skills/agent-creator-feishu)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands, JSON snippets, and configuration file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce OpenClaw workspace files, Feishu group binding instructions, allowlist checks, and testing guidance for administrator review.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
