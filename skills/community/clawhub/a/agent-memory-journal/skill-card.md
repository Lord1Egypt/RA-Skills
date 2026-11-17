## Description:

Agent Memory Journal provides a durable three-tier memory system for agents with a Python Journal API, CLI workflows, and inspectable hot, warm, and cold storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[misolith](https://clawhub.ai/user/misolith)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to embed persistent, searchable memory in an agent workspace, record episodic notes and curated facts, and review or rebuild generated hot memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory can carry untrusted or stale instructions into future agent sessions.

Mitigation: Treat stored memory as untrusted, avoid pinning content from untrusted sources, and review .memory/AGENT.md before loading it into an agent startup prompt.

Risk: Hot-memory configuration can write generated memory to workspace files.

Mitigation: Keep hot_path at the default or a known generated file, and review .memory/config.json before maintenance cycles.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/misolith/skills/agent-memory-journal)
- [Agent installation guide](artifact/docs/agent_install.md)
- [README](artifact/README.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown memory files, JSON configuration, Python API calls, and CLI commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists local memory under .memory/ and uses a character budget for generated hot memory.]

## Skill Version(s):

0.2.3 (source: evidence release metadata, pyproject.toml, CHANGELOG, released 2026-04-25)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
