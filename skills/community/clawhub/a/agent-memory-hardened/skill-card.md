## Description:

Persistent memory system for AI agents — remember facts, learn from experience, and track entities across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent operators use this skill to add local, cross-session memory for facts, lessons, and entity context so agents can recall prior work and avoid repeating mistakes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cross-session memories are stored locally in plaintext and may include sensitive context if users or agents store it.

Mitigation: Use the skill only for non-sensitive memories, keep the database on protected storage, and avoid storing credentials, tokens, personal identifiers, health records, or similar sensitive data.

Risk: Advertised deletion may not fully remove stored fact content from the full-text search index and SQLite storage behavior.

Mitigation: Do not rely on forget operations as secure deletion until the FTS index and SQLite storage behavior are fixed; avoid storing data that would require assured erasure.

Risk: Recalled memory may be stale, poisoned, or insufficient authority for consequential actions.

Mitigation: Present recalled data to the user for review and obtain current confirmation before deploying, sending messages, modifying access, deleting data, or taking other consequential actions.

Risk: Memory contents can leak accumulated cross-session data if sent to external services or destinations.

Mitigation: Keep memory contents inside the local conversation and do not send them through network commands, API calls, email, webhooks, or other external destinations.

Risk: Entity memory can become covert profiling when people are tracked without a current task reason and user awareness.

Mitigation: Track people only when there is a clear, current task reason and the user is aware of the tracking.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/skills/agent-memory-hardened)
- [Skill instructions](artifact/SKILL.md)
- [README](artifact/README.md)
- [Safety evaluation](artifact/SAFETY.md)
- [Faberlens safety report](https://faberlens.ai/explore/agent-memory)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or read a local SQLite memory database at the configured path.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact/src/__init__.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
