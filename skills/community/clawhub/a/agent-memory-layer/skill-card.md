## Description:

Agent Memory Layer provides a three-tier memory system for AI agents with short-term, long-term, and episodic memory for persistence, context management, retrieval, and episodic recall.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evezart](https://clawhub.ai/user/evezart)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add memory persistence, conversation context management, knowledge retrieval, and episodic recall patterns to AI agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist potentially sensitive memories in plaintext.

Mitigation: Keep the memory directory access-controlled, avoid storing secrets or credentials, and add retention and deletion controls before production use.

Risk: Storage paths and agent identifiers may not be safely constrained.

Mitigation: Use only with trusted callers, validate agent_id and storage paths, and review deployments before use in environments that handle private user data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/evezart/skills/agent-memory-layer)
- [Short-Term Memory](references/short-term.md)
- [Long-Term Memory](references/long-term.md)
- [Episodic Memory](references/episodic.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist memory records to local JSON files or external stores when implemented by an agent.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
