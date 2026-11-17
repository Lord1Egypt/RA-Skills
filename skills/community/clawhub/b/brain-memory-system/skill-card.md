## Description:

Brain Memory System provides a local CLI-backed memory system for agents with episodic memories, semantic facts, procedure evolution, attention filtering, consolidation, working memory, and health checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mwmdeadpool](https://clawhub.ai/user/mwmdeadpool)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to store, recall, and manage local agent memory, including experiences, facts, procedures, working context, consolidation, and memory health checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persists broad agent memory in a local database.

Mitigation: Review what will be stored, avoid saving secrets or sensitive operational details, and protect the database according to the deployment environment.

Risk: Procedure evolution can send procedure history to a configured LLM endpoint.

Mitigation: Use a local or trusted endpoint, set API credentials explicitly, and keep secrets out of procedure steps, failure notes, and fixes.

Risk: Model-rewritten procedures can be applied without a built-in approval gate.

Mitigation: Use dry-run mode first and review proposed procedure changes before applying them.

Risk: Multi-agent scoping is organizational rather than a security boundary.

Mitigation: Do not rely on agent scoping for isolation between users, tenants, or high-sensitivity contexts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mwmdeadpool/skills/brain-memory-system)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [CLI text, JSON reports, Markdown working-memory updates, and local SQLite-backed files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use a local or trusted OpenAI-compatible LLM endpoint for procedure evolution when explicitly configured.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
