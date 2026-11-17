## Description:

Persistent memory system for AI agents to remember facts, learn from experiences, recall memories, and track entities across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sieyer](https://clawhub.ai/user/sieyer)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use Agent Memory to add local, persistent recall to AI agents, including stored facts, lessons from prior actions, and tracked entities across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently stores potentially sensitive conversation facts in plaintext.

Mitigation: Use a custom database path with restrictive filesystem permissions, avoid storing secrets or regulated data, and periodically inspect, export, or purge stored memory.

Risk: Deletion guarantees are weak because the current forget() behavior may not fully clean full-text search data.

Mitigation: Do not rely on forget() for complete removal until the FTS cleanup issue is fixed; purge or replace the database when complete removal is required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sieyer/skills/agent-memory-1-0-0)
- [Artifact README](artifact/README.md)
- [Skill Instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell snippets; runtime APIs return Python objects, dictionaries, and text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores memory in a local SQLite database by default, with a configurable database path.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/src/__init__.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
