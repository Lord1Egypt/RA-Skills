## Description:

OpenClaw Agent 自进化记忆系统 provides persistent OpenClaw agent memory by syncing Obsidian vault content, compressing session observations, indexing to Qdrant, and monitoring memory health.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yxyujian98-png](https://clawhub.ai/user/yxyujian98-png)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and advanced OpenClaw users use this skill to give agents searchable long-term memory from Obsidian vault content, session observations, and vector-indexed records. It is suited for local knowledge workflows that need automated memory sync, compression, retrieval, and health monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can have ongoing access to OpenClaw sessions and Obsidian vault content.

Mitigation: Use a test copy of the vault first, limit configured sync directories, and review generated memories before relying on routine indexing.

Risk: Embedding or LLM endpoints may receive note or session content during memory processing.

Mitigation: Keep embedding and LLM endpoints local unless remote processing is explicitly acceptable, and protect any configured API keys.

Risk: Automatic self-healing and antibody auto_fix commands may make unintended changes.

Mitigation: Disable automatic repair commands until reviewed, and run maintenance tasks manually before enabling scheduled operation.

Risk: Unpinned Python dependencies or container images can change behavior over time.

Mitigation: Pin Python package versions and container image tags before routine use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yxyujian98-png/skills/agent-openclaw-memory)
- [Publisher Profile](https://clawhub.ai/user/yxyujian98-png)
- [Artifact Skill Definition](artifact/SKILL.md)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bundled scripts can write or update local memory files, vault files, health reports, and Qdrant vector records when installed and executed.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
