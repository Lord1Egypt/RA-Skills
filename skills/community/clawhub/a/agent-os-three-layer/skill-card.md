## Description:

Provides a reusable AI agent OS template with separated identity, operations, and knowledge layers for modular intelligent system design.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huamu668](https://clawhub.ai/user/huamu668)

### License/Terms of Use:


## Use Case:

Agent builders and developers use this template to structure an AI agent around identity, operating procedures, and accumulated knowledge. It provides Markdown-based role, memory, status, startup, and verification materials that an agent can follow or adapt.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to adopt active personas and operating roles.

Mitigation: Install only where host, system, and tool authorization rules clearly override the template's role instructions.

Risk: The skill encourages persistent memory and learning after conversations without clear retention limits.

Mitigation: Use it only in environments where memory writes require explicit approval and sensitive content is excluded.

Risk: The skill may shape communication style, task handling, and self-update behavior across sessions.

Mitigation: Review the identity, operations, and knowledge files before use and adapt them to the intended governance policy.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/huamu668/skills/agent-os-three-layer)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files with bash command snippets and configuration metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The template organizes agent behavior into identity, operations, and knowledge files, with helper shell scripts for startup and structure verification.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
