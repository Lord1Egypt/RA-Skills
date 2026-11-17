## Description:

Implements a file-based agent memory architecture for durable continuity using core workspace files, typed memory entries, WAL protocol, L1 summaries, memory compression, and contradiction detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to set up, restructure, or audit persistent file-based memory systems for agents that need continuity across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Durable plaintext memory can expose personal, client, or strategic context if files are shared, synced, committed, or loaded in the wrong session.

Mitigation: Create memory directories with private permissions, keep memory files out of git and unencrypted cloud sync, and load personal memory only in approved one-to-one sessions.

Risk: Long-lived memory may accumulate sensitive secrets or outdated facts over time.

Mitigation: Do not store passwords or tokens, define deletion rules, review stale facts during maintenance, and preserve contradiction-detection steps.

Risk: Recurring heartbeat checks can touch private integrations too broadly.

Mitigation: Enable heartbeat checks only for explicitly approved accounts or repositories and use the narrowest read-only scopes available.

## Reference(s):

- [Agent Memory Architecture on ClawHub](https://clawhub.ai/samledger67-dotcom/skills/agent-memory-architecture)
- [Memory File Templates](references/memory-templates.md)
- [Memory Type Taxonomy](references/typing-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with templates, examples, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces file-architecture guidance for local agent memory; does not call external services itself.]

## Skill Version(s):

98.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
