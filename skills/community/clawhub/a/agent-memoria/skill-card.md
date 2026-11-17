## Description:

MEMORIA gives OpenClaw agents a persistent local Markdown memory layer that tracks user context, projects, decisions, lessons, preferences, and blockers across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[contrario](https://clawhub.ai/user/contrario)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use MEMORIA to give an agent continuity across sessions by loading and updating a local memory file with durable personal, project, and workflow context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently stores and resurfaces broad personal, project, and infrastructure context in local memory files.

Mitigation: Install only when long-lived local memory is acceptable, keep memory files private, and periodically inspect memory.md, memory.md.bak, and archive copies.

Risk: Sensitive details such as secrets, credentials, private URLs, IP addresses, regulated data, or sensitive business information could be added to memory.

Mitigation: Do not store those categories of information, and review memory summaries before sharing terminal output, recordings, or copied responses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/contrario/skills/agent-memoria)
- [Publisher profile](https://clawhub.ai/user/contrario)
- [README](artifact/README.md)
- [Examples](artifact/EXAMPLES.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and local Markdown memory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists user-provided context in local memory.md files and creates backup/archive copies when updating memory.]

## Skill Version(s):

1.0.2 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
