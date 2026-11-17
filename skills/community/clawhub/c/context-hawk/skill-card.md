## Description:

Context Hawk is a pure Python memory manager for preserving, compressing, and retrieving AI agent memories across sessions, topics, and time without requiring external services by default.

This skill is ready for commercial/non-commercial use.

## Publisher:

[relunctance](https://clawhub.ai/user/relunctance)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use Context Hawk to add persistent memory, task-state recall, context compression, and retrieval behavior to Python-based AI agents. It is suited to agents that need continuity across sessions while controlling memory noise and context size.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persists and reuses conversation-derived memory, which can retain sensitive user or project information across sessions.

Mitigation: Keep memory stores isolated per user and project, periodically inspect or delete ~/.hawk data, and avoid storing secrets or confidential content.

Risk: One-line shell installation and bundled automation paths can make review harder before code runs.

Mitigation: Review the artifact first, install in a virtual environment with pinned dependencies, and avoid running the cron health-check script.

Risk: Optional remote embedding or LLM providers can receive conversation and stored memory text when enabled.

Mitigation: Use local or keyword-only modes for sensitive data, and enable remote providers only after confirming data-sharing requirements are acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/relunctance/skills/context-hawk)
- [README](artifact/README.md)
- [Four-Tier Memory Architecture](artifact/references/memory-system.md)
- [Structured Memory Format](artifact/references/structured-memory.md)
- [Task State Memory](artifact/references/task-state.md)
- [Context Injection Strategies](artifact/references/injection-strategies.md)
- [Compression Strategies](artifact/references/compression-strategies.md)
- [CLI Reference](artifact/references/cli.md)
- [LanceDB Integration](artifact/references/lancedb-integration.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; runtime components produce text recall snippets and JSON-compatible memory records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist conversation-derived memory locally and may use optional remote embedding or LLM providers when configured.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact pyproject.toml reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
