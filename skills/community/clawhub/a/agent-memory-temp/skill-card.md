## Description:

Persistent memory system enabling AI agents to remember facts, learn from experiences, and track entities across sessions for improved context awareness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liguang00806](https://clawhub.ai/user/liguang00806)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add local, persistent memory for facts, lessons learned, and tracked entities across agent sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persists conversation-derived facts, lessons, and entity attributes in a local SQLite database, which can include personal or sensitive context if agents store it unfiltered.

Mitigation: Use a dedicated database path with restrictive permissions, avoid storing secrets or sensitive personal information, set expirations where possible, and periodically inspect or delete stored memories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liguang00806/skills/agent-memory-temp)
- [Artifact README](artifact/README.md)
- [Skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local SQLite-backed memory operations and examples; no external runtime dependencies are declared.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
