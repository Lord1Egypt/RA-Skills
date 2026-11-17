## Description:

Persistent memory for AI agents to store facts, learn from actions, recall information, and track entities across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dennis-da-menace](https://clawhub.ai/user/dennis-da-menace)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to give AI agents local cross-session memory for durable facts, lessons learned, and entity context. It supports recall, cleanup, entity tracking, and JSON export through a Python library and CLI helpers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to keep local cross-session memory, so stored facts, entities, SQLite database files, and JSON exports may contain private or sensitive information.

Mitigation: Do not store secrets, credentials, regulated data, or sensitive personal information unless the storage path and local filesystem protections have been reviewed.

Risk: JSON exports and the SQLite database can expose accumulated agent memory if shared or checked into another location.

Mitigation: Treat exports and database files as private data and restrict access to the configured memory path.

Risk: Forget and cleanup operations permanently delete memory records.

Mitigation: Review deletion commands and cleanup settings before use, especially when operating on a shared or long-lived memory database.

## Reference(s):

- [ClawHub Agent Memory skill page](https://clawhub.ai/dennis-da-menace/skills/agent-memory)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Clawdbot](https://github.com/clawdbot/clawdbot)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, Python code examples, CLI commands, and JSON export data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores local SQLite data by default at ~/.agent-memory/memory.db and can export memory records as JSON.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/src/__init__.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
