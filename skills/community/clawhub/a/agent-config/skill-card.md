## Description:

Intelligently modify agent core context files (AGENTS.md, SOUL.md, IDENTITY.md, USER.md, TOOLS.md, MEMORY.md, HEARTBEAT.md).

This skill is ready for commercial/non-commercial use.

## Publisher:

[thatguysizemore](https://clawhub.ai/user/thatguysizemore)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to make structured, low-duplication updates to OpenClaw agent context files. It helps route changes to the right file, check for size and duplication issues, and verify configuration edits before reporting them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change persistent agent behavior and memory files, including private user context.

Mitigation: Use it only when persistent OpenClaw configuration changes are intended, and require explicit confirmation before changes to AGENTS.md, USER.md, MEMORY.md, HEARTBEAT.md, or startup behavior.

Risk: Silent logging and first-run BOOTSTRAP deletion behavior can reduce user visibility into what changed.

Mitigation: Review those behaviors before installation and keep an auditable change note for significant configuration updates.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/thatguysizemore/skills/agent-config)
- [OpenClaw Workspace File Map](artifact/references/file-map.md)
- [Change Protocol](artifact/references/change-protocol.md)
- [Claude Instruction Patterns](artifact/references/claude-patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline code blocks, shell commands, and configuration edit proposals]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide edits to persistent OpenClaw context and memory files.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
