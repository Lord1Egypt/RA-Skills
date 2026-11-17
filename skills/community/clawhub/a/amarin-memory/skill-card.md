## Description:

Amarin Memory gives agents a local SQLite-backed memory system for storing, semantically searching, revising, and decaying long-term memories across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flaggdavid-source](https://clawhub.ai/user/flaggdavid-source)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to give agents durable local memory for user preferences, decisions, identity blocks, and cross-session context. It is intended for workflows where agents need to store, search, revise, protect, and prune remembered information over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Durable local memory can retain sensitive user, identity, or operational context longer than intended.

Mitigation: Avoid storing secrets, credentials, regulated personal data, or other sensitive material, and regularly review and prune ~/.amarin/agent.db.

Risk: Stored untrusted instruction-like text may later be retrieved as agent context.

Mitigation: Pipe untrusted content through the documented safer input path, label and review stored memories, and revise or forget entries that should not influence future sessions.

Risk: The skill depends on an installed amarin-memory package and local embedding service behavior.

Mitigation: Use a pinned, reviewed amarin-memory dependency and confirm the configured OLLAMA_URL points to the intended embedding service before sensitive use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/flaggdavid-source/skills/amarin-memory)
- [Publisher Profile](https://clawhub.ai/user/flaggdavid-source)
- [Project Homepage](https://github.com/flaggdavid-source/amarin-memory)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local SQLite database at ~/.amarin/agent.db and an embedding service configured by OLLAMA_URL.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
