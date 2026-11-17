## Description:

Agent Long-Term Memory provides three-tier persistent memory for AI agents, covering short-term conversation state, structured entity facts, and episodic semantic recall.

This skill is ready for commercial/non-commercial use.

## Publisher:

[exp007](https://clawhub.ai/user/exp007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add persistent memory to AI agents, including structured fact recall, recent conversation state, episodic search, and assembled prompt context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist and reuse sensitive conversations, source code, client data, or secrets across projects through its default shared memory store.

Mitigation: Configure a project-specific data_dir, avoid archiving full conversations by default, and review stored memory before use in sensitive environments.

Risk: When OPENAI_API_KEY is set, entity extraction can send conversation content to OpenAI.

Mitigation: Unset OPENAI_API_KEY or modify the extraction path if strictly local processing is required.

Risk: Long-lived memories can become stale, overbroad, or inappropriate for later prompts.

Mitigation: Inspect and delete stored memories regularly, and use cleanup or forget workflows for low-confidence or outdated records.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/exp007/skills/agent-long-term-memory)
- [Publisher Profile](https://clawhub.ai/user/exp007)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)
- [Python Project Metadata](artifact/pyproject.toml)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python examples, shell commands, configuration notes, and memory-context text strings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can persist memory in SQLite and ChromaDB under a shared default data directory unless a project-specific data_dir is configured.]

## Skill Version(s):

1.0.0 (source: server release metadata and pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
