## Description:

Bagua Memory is a file-based AI agent memory framework that stores workspace memory across eight categories with lifecycle decay and associative retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuanyizhi](https://clawhub.ai/user/xuanyizhi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to initialize and maintain structured long-term memory for an agent workspace, including memory writing, retrieval, archival, compression, and deletion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Activation can modify agent-governing files such as AGENTS.md, SOUL.md, HEARTBEAT.md, MEMORY.md, and memory/bagua files.

Mitigation: Review the exact workspace changes before activation and keep activation under explicit user control.

Risk: The skill persists conversation-derived memory and may store sensitive, stale, or unintended personal information.

Mitigation: Avoid storing secrets or sensitive personal information unless clear review, deletion, retention, and backup controls are in place.

## Reference(s):

- [Architecture Reference](references/architecture.md)
- [Agent Memory Rules Injection](references/soul-inject.md)
- [Heartbeat Memory Maintenance](references/heartbeat-inject.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and workspace file changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local memory and agent-governance files when activated.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
